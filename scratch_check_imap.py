import os
import imaplib
import email
from dotenv import load_dotenv

load_dotenv()
user = os.getenv('SMTP_USER')
pwd = os.getenv('SMTP_PASSWORD')

try:
    mail = imaplib.IMAP4_SSL('imap.stackmail.com')
    mail.login(user, pwd)
    status, folders = mail.list()
    sent_folder = None
    for f in folders:
        line = f.decode('utf-8', errors='ignore')
        if 'Sent' in line:
            sent_folder = line.split(' "/" ')[-1].strip(' "')
            break
    print('Sent folder:', sent_folder)
    if sent_folder:
        mail.select(f'"{sent_folder}"')
        status, data = mail.search(None, 'ALL')
        ids = data[0].split()
        print('Total emails in Sent:', len(ids))
        if ids:
            latest_id = ids[-1]
            status, msg_data = mail.fetch(latest_id, '(RFC822)')
            msg = email.message_from_bytes(msg_data[0][1])
            print('Subject:', msg.get('Subject'))
            print('DKIM-Signature:', msg.get('DKIM-Signature'))
            print('Message-ID:', msg.get('Message-ID'))
    mail.logout()
except Exception as e:
    print('IMAP check error:', e)

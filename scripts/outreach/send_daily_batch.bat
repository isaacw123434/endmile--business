@echo off
cd /d "%~dp0..\.."
echo ======================================================================
echo  EndMile Automated Outreach Dispatcher
echo  Sending daily batch of 5 high-priority consultancy leads...
echo ======================================================================
python scripts/outreach/send_app_outreach.py --limit 5
echo.
pause

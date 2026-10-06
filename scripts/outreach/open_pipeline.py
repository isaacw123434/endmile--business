#!/usr/bin/env python3
"""
Open EndMile Master Pipeline in Microsoft Excel
-----------------------------------------------
Launches the master workbook located at:
  C:\\Users\\isaac\\Documents\\endmile\\endmile_master_pipeline.xlsx
using the default Windows application (Excel).
"""

import os
import sys
from pathlib import Path

MASTER_PATH = Path(r"C:\Users\isaac\Documents\endmile\endmile_master_pipeline.xlsx")

def open_pipeline():
    if not MASTER_PATH.exists():
        print(f"[ERROR] Master pipeline workbook not found at:\n  {MASTER_PATH}")
        print("Run 'npm run outreach:sync' to generate it first.")
        sys.exit(1)

    print(f"[LAUNCH] Opening EndMile Master Pipeline in Excel:\n  {MASTER_PATH}")
    try:
        os.startfile(str(MASTER_PATH))
        print("[OK] Excel launched successfully.")
    except Exception as e:
        print(f"[ERROR] Could not launch file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    open_pipeline()

@echo off
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
  py -m venv .venv
  .venv\Scripts\python -m pip install -r requirements.txt
)

set PYTHONPATH=src
.venv\Scripts\streamlit run app\main.py

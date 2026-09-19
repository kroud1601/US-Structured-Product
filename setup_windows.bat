@echo off
py -m venv .venv
call .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
echo.
echo Setup complete. Edit config\config.yaml and enter your real email address.
python run_project.py doctor
pause


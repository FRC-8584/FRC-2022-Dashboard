@ECHO OFF
@ping 127.0.0.1 -n 1 -w 1000 > nul
.\.venv\Scripts\activate.bat && python main.py
To run the server:

Linux:
export FLASK_APP=server.py
export FLASK_ENV=development
python -m flask run

Windows:
If you are on Windows, the environment variable syntax depends on command line interpreter. On Command Prompt:
C:\path\to\app>set FLASK_APP=server.py
And on PowerShell:
PS C:\path\to\app> $env:FLASK_APP = "server.py"

python -m flask run

To check go to webpage
http://127.0.0.1:5000/

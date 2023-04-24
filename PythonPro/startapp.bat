rem this is a dos batch file
call .\flaskenv\Scripts\activate.bat
echo starting flask app...
rem set FLASK_APP = tastytable
python -m flask --app tastytable run --debug
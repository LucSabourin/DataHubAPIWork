set PgSQLLogin=*****
set PgSQLPassword=*****
set pgSQLServer=*****
python -m venv env
CALL env\scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
deactivate

set PgSQLLogin=team04
set PgSQLPassword=changeme
set pgSQLServer=pgsql-01
python -m venv env
CALL env\scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
deactivate

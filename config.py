import os

# Login info for pgsql server
_pgSqlLogin = os.getenv('PgSQLLogin')
_pgSqlPword = os.getenv('PgSQLPassword')
_pgSqlServer = os.getenv('PgSQLServer')

clientAPgSqlAlchemy = {
    'login': _pgSqlLogin,
    'pword': _pgSqlPword,
    'server': _pgSqlServer,
    'dbName': 'clientA',
    'port': '5432',
    'sqlDriver': 'postgresql+psycopg2',
}

clientBPgSqlAlchemy = {
    'login': _pgSqlLogin,
    'pword': _pgSqlPword,
    'server': _pgSqlServer,
    'dbName': 'clientBping_newer',
    'port': '5432',
    'sqlDriver': 'postgresql+psycopg2',
}



ROOTDIR = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
cache = '/'.join([ROOTDIR, 'cache'])
staging = '/'.join([cache, 'staging'])

if __name__ == '__main__':
    print(clientAPgSqlAlchemy)
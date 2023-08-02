import os

# Login info for pgsql server
_pgSqlLogin = os.getenv('PgSQLLogin')
_pgSqlPword = os.getenv('PgSQLPassword')
_pgSqlServer = os.getenv('PgSQLServer')

vcdsPgSqlAlchemy = {
    'login': _pgSqlLogin,
    'pword': _pgSqlPword,
    'server': _pgSqlServer,
    'dbName': 'vcds',
    'port': '5432',
    'sqlDriver': 'postgresql+psycopg2',
}

hrmapPgSqlAlchemy = {
    'login': _pgSqlLogin,
    'pword': _pgSqlPword,
    'server': _pgSqlServer,
    'dbName': 'hrmapping_newer',
    'port': '5432',
    'sqlDriver': 'postgresql+psycopg2',
}



ROOTDIR = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
cache = '/'.join([ROOTDIR, 'cache'])
staging = '/'.join([cache, 'staging'])

if __name__ == '__main__':
    print(vcdsPgSqlAlchemy)
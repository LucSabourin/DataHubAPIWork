from config import _pgSqlLogin, _pgSqlPword, _pgSqlServer, ROOTDIR

ctlgPgSqlAlchemy = {
    'login': _pgSqlLogin,
    'pword': _pgSqlPword,
    'server': _pgSqlServer,
    'dbName': 'catalogue',
    'port': '5432',
    'sqlDriver': 'postgresql+psycopg2',
}

tagLimit = 20

cache = '/'.join([ROOTDIR, 'cache', 'catalog'])
from config import _pgSqlLogin, _pgSqlPword, _pgSqlServer, ROOTDIR

# Sql Alchemy ODBC information for Catalog
ctlgPgSqlAlchemy = {
    'login': _pgSqlLogin,
    'pword': _pgSqlPword,
    'server': _pgSqlServer,
    'dbName': 'catalogue',
    'port': '5432',
    'sqlDriver': 'postgresql+psycopg2',
}

# Limit of the number of tags which can be assigned to each datasource
tagLimit = 20

# Location of local cache should something break
cache = '/'.join([ROOTDIR, 'cache', 'catalog'])
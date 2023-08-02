# Imports sqlalchemy dependency
from sqlalchemy import create_engine, engine
from sqlalchemy_utils import database_exists, create_database
from pyodbc import Connection

def connectDb(login : str, pword : str, server : str, dbName : str, port : str, sqlDriver : str) -> Connection:
    """Returns connection to a sql source using sqlalchemy.

    Parameters:
    -----------
    login : str
        login/user name
    pword : str
        password
    server : str
        sql server name/site
    dbName : str
        database name
    port : str
        port number for sql server
    sqlDriver : str
        driver for sqlalchemy to communicate with sql source

    Returns:
    --------
    Connection
        returns a pyodbc Connection managed by sqlalchemy (default plugin for
        pandas)
    """

    # Build Connection String
    conn_str = '{}://{}:{}@{}:{}/{}'.format(
        sqlDriver,
        login,
        pword,
        server,
        port,
        dbName
    )

    # Establish Connection
    alchemyEngine = create_engine(conn_str, pool_recycle=3600)
    verifyDb(alchemyEngine)
    return alchemyEngine.connect()

def verifyDb(eng: engine) -> None:
    """Verifies a database exists in sql source for sqlalchemy. If it does not,
    creates the database.

    Parameters:
    -----------
    eng : engine
        sqlalchemy engine used to manage connection to a database
    """

    if not database_exists(eng.url):
        create_database(eng.url)
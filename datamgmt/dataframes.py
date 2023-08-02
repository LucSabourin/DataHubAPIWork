# Import Pandas dependencies
from sqlite3 import OperationalError
import pandas as pd
from pandas import DataFrame
# Import Json dependency
import json
# Import uuid dependency
import uuid

# Import local dependencies
from datamgmt.sql import connectDb
from config import cache
from datamgmt.filemgmt import deleteFile, fileExists

def storeDfSql(df : DataFrame, tblName : str, kwargs : dict) -> None:
    """Stores DataFrame to a sql source as a table.

    Parameters:
    -----------
    df : DataFrame
        DataFrame to be stored
    tblName : str
        name of table in which to store DataFrame
    kwargs : dict
        keyword arguments for connection to sql source
    """

    conn = connectDb(**kwargs)
    df.to_sql(name=tblName, con=conn, if_exists='replace')
    conn.close()

def getDfSql(tblName : str, kwargs : dict) -> DataFrame:
    """Retrieves table from sql tabular source and converts to a DataFrame
    which is then returned.

    Parameters:
    -----------
    tblName : str
        name of table from sql source
    kwargs : dict
        keyword arguments for connection to sql source

    Returns:
    --------
    DataFrame
        DataFrame converted from sql tabular source
    """

    # Establish Connection
    conn = connectDb(**kwargs)
    
    # Error handling if table does not exist
    retrieved = False
    try:
        df = pd.read_sql_table(table_name=tblName, con=conn, index_col='index')
    except KeyError:
        try:
            df = pd.read_sql_table(table_name=tblName, con=conn)
        except ValueError as e:
            msg = e
        else:
            retrieved = True
    except ValueError as e:
        msg = e
    else:
        retrieved = True
    
    # Close Connection
    conn.close()

    # Raise error if table not retrieved
    if not retrieved:
        raise ValueError(msg)

    # Returns dataframe from table if retrieved
    return df

def jsonifyDf(df : DataFrame, file : str = None) -> str:
    """Jsonifies DataFrame, including encoding data with utf-8. This is done
    by caching data in order to encode with utf-8 as dataframes cannot do this.

    Parameters:
    -----------
    df : DataFrame
        DataFrame to be jsonified

    Returns:
    --------
    str
        json string encoded to utf-8
    """

    data = df.to_json(orient='records', force_ascii=False)
    
    # Generate cached file name
    if file is None:
        fileName = str(uuid.uuid4()) + '.json'
        while fileExists('/'.join([cache, fileName])):
            fileName = str(uuid.uuid4()) + '.json'
        fileName = '/'.join([cache, fileName])
    else:
        fileName = '/'.join([cache, 'catalog', file + '.json'])
    
    # Encodes json string in utf-8 by caching it
    with open(fileName, 'wt', encoding='utf-8') as f:
        json.dump(data, f)
    with open(fileName, 'rt', encoding='utf-8') as f:
        data = json.load(f)

    # Delete cached data and return encoded json string
    if file is None:
        deleteFile(fileName)
    return data

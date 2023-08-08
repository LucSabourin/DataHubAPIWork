from datamgmt.excel import readExcel, DataFrame
from datamgmt.dataframes import getDfSql, jsonifyDf, storeDfSql
import json

from config import clientAPgSqlAlchemy, clientBPgSqlAlchemy ,ROOTDIR
from resources import cacheIncoming

def testDir():
    print(cacheIncoming)

def testPost(key : str, fileName : str):
    fileName = '/'.join([ROOTDIR, 'cache', 'incoming', fileName])
    tableName = key

    dfs = readExcel(path=fileName)
    storeDfSql(df=dfs, tblName=tableName, kwargs=clientAPgSqlAlchemy)

catalogTemp = [
    {'key': 'someCatalogKey', 'cred': clientAPgSqlAlchemy},
    {'key': 'someOtherCatalogKey', 'cred': clientAPgSqlAlchemy},
    {'key': 'FinancialInfo', 'cred': clientAPgSqlAlchemy},
    {'key': 'FinancialActual', 'cred': clientAPgSqlAlchemy},
    {'key': 'FinancialExpected', 'cred': clientAPgSqlAlchemy},
    {'key': 'FinancialStats', 'cred': clientAPgSqlAlchemy},
    {'key': 'posting', 'cred': clientBPgSqlAlchemy},
    {'key': 'position', 'cred': clientBPgSqlAlchemy},
    {'key': 'pay_rate', 'cred': clientBPgSqlAlchemy},
    {'key': 'pay_scale', 'cred': clientBPgSqlAlchemy},
    {'key': 'org_budget', 'cred': clientBPgSqlAlchemy},
    {'key': 'org', 'cred': clientBPgSqlAlchemy},
]

def testGet(key : str) -> str:
    catalogTemp = [
        {'key': 'someCatalogKey', 'cred': clientAPgSqlAlchemy},
        {'key': 'someOtherCatalogKey', 'cred': clientAPgSqlAlchemy},
        {'key': 'FinancialInfo', 'cred': clientAPgSqlAlchemy},
        {'key': 'FinancialActual', 'cred': clientAPgSqlAlchemy},
        {'key': 'FinancialExpected', 'cred': clientAPgSqlAlchemy},
        {'key': 'FinancialStats', 'cred': clientAPgSqlAlchemy},
        {'key': 'posting', 'cred': clientBPgSqlAlchemy},
        {'key': 'position', 'cred': clientBPgSqlAlchemy},
        {'key': 'pay_rate', 'cred': clientBPgSqlAlchemy},
        {'key': 'pay_scale', 'cred': clientBPgSqlAlchemy},
        {'key': 'org_budget', 'cred': clientBPgSqlAlchemy},
        {'key': 'org', 'cred': clientBPgSqlAlchemy},
    ]

    tableName = None
    credentials = None
    for entry in catalogTemp:
        if entry['key'] == key:
            tableName = key
            credentials = entry['cred']
            break

    if tableName is None:
        return None
    else:
        df = getDfSql(tableName, kwargs=credentials)
        return json.loads(jsonifyDf(df))
    

if __name__ == '__main__':
    fileName = '/'.join([ROOTDIR, 'data_in', 'FinancialDummyData_Stats.xlsx'])
    tableName = 'FinancialStats'

    dfs = readExcel(path=fileName)
    if type(dfs) == list:
        strings = []
        for num, df in enumerate(dfs):
            storeDfSql(df=df, tblName='-'.join([tableName, str(num)]), kwargs=clientAPgSqlAlchemy)
            df = getDfSql(tableName, kwargs=clientAPgSqlAlchemy)
            strings.append(jsonifyDf(df))
    elif type(dfs) == DataFrame:
        storeDfSql(df=dfs, tblName=tableName, kwargs=clientAPgSqlAlchemy)
        df = getDfSql(tableName, kwargs=clientAPgSqlAlchemy)
        strings = jsonifyDf(df)
    
    print(strings)
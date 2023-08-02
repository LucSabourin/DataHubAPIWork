from datamgmt.excel import readExcel, DataFrame
from datamgmt.dataframes import getDfSql, jsonifyDf, storeDfSql
import json

from config import vcdsPgSqlAlchemy, hrmapPgSqlAlchemy ,ROOTDIR
from resources import cacheIncoming

def testDir():
    print(cacheIncoming)

def testPost(key : str, fileName : str):
    fileName = '/'.join([ROOTDIR, 'cache', 'incoming', fileName])
    tableName = key

    dfs = readExcel(path=fileName)
    storeDfSql(df=dfs, tblName=tableName, kwargs=vcdsPgSqlAlchemy)

catalogTemp = [
    {'key': 'someCatalogKey', 'cred': vcdsPgSqlAlchemy},
    {'key': 'someOtherCatalogKey', 'cred': vcdsPgSqlAlchemy},
    {'key': 'BIRT', 'cred': vcdsPgSqlAlchemy},
    {'key': 'SWE', 'cred': vcdsPgSqlAlchemy},
    {'key': 'FinancialInfo', 'cred': vcdsPgSqlAlchemy},
    {'key': 'FinancialActual', 'cred': vcdsPgSqlAlchemy},
    {'key': 'FinancialExpected', 'cred': vcdsPgSqlAlchemy},
    {'key': 'FinancialStats', 'cred': vcdsPgSqlAlchemy},
    {'key': 'posting', 'cred': hrmapPgSqlAlchemy},
    {'key': 'position', 'cred': hrmapPgSqlAlchemy},
    {'key': 'pay_rate', 'cred': hrmapPgSqlAlchemy},
    {'key': 'pay_scale', 'cred': hrmapPgSqlAlchemy},
    {'key': 'org_budget', 'cred': hrmapPgSqlAlchemy},
    {'key': 'org', 'cred': hrmapPgSqlAlchemy},
]

def testGet(key : str) -> str:
    catalogTemp = [
        {'key': 'someCatalogKey', 'cred': vcdsPgSqlAlchemy},
        {'key': 'someOtherCatalogKey', 'cred': vcdsPgSqlAlchemy},
        {'key': 'BIRT', 'cred': vcdsPgSqlAlchemy},
        {'key': 'SWE', 'cred': vcdsPgSqlAlchemy},
        {'key': 'FinancialInfo', 'cred': vcdsPgSqlAlchemy},
        {'key': 'FinancialActual', 'cred': vcdsPgSqlAlchemy},
        {'key': 'FinancialExpected', 'cred': vcdsPgSqlAlchemy},
        {'key': 'FinancialStats', 'cred': vcdsPgSqlAlchemy},
        {'key': 'posting', 'cred': hrmapPgSqlAlchemy},
        {'key': 'position', 'cred': hrmapPgSqlAlchemy},
        {'key': 'pay_rate', 'cred': hrmapPgSqlAlchemy},
        {'key': 'pay_scale', 'cred': hrmapPgSqlAlchemy},
        {'key': 'org_budget', 'cred': hrmapPgSqlAlchemy},
        {'key': 'org', 'cred': hrmapPgSqlAlchemy},
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
            storeDfSql(df=df, tblName='-'.join([tableName, str(num)]), kwargs=vcdsPgSqlAlchemy)
            df = getDfSql(tableName, kwargs=vcdsPgSqlAlchemy)
            strings.append(jsonifyDf(df))
    elif type(dfs) == DataFrame:
        storeDfSql(df=dfs, tblName=tableName, kwargs=vcdsPgSqlAlchemy)
        df = getDfSql(tableName, kwargs=vcdsPgSqlAlchemy)
        strings = jsonifyDf(df)
    
    print(strings)
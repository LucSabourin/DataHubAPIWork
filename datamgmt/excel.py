import pandas as pd
from pandas import DataFrame

def readExcel(path : str, sheets : list = None) -> DataFrame:
    """
    """

    if sheets is None:
        sheets = []

    if len(sheets) == 0:
        dfs = pd.read_excel(path)
        if type(dfs) == DataFrame:
            return dfs
        elif type(dfs) == list:
            if len(dfs) == 1:
                return dfs[0]
            else:
                return dfs
    elif len(sheets) == 1:
        df = pd.read_excel(filepath=path, sheet_name=sheets[0])
        return df
    else:
        dfs = []
        for sheet in sheets:
            df = pd.read_excel(filepath=path, sheet_name=sheet)
            dfs.append(df)
        return dfs

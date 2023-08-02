import json
import os
import uuid

from config import staging, cache
from datamgmt.other import dateTimeString

def deleteFile(path : str) -> None:
    """Used to delete a file at the given path.

    Parameters:
    -----------
    path : str
        path of file to be deleted
    """

    try:
        if os.path.isfile(path):
            os.remove(path)
    except Exception as e:
        print(f'Failed to delete {path}. Reason: {e}')

def fileExists(path : str) -> bool:
    """
    """
    
    return os.path.isfile(path)

def stageJsonFile(jsonString : dict, file : str = None) -> str:
    """
    """

    if file is None:
        fileName = str(uuid.uuid4()) + '.json'
        while fileExists('/'.join([staging, fileName])):
            fileName = str(uuid.uuid4()) + '.json'
    else:
        fileName = file + '_' + dateTimeString() + '.json'

    with open('/'.join([staging, fileName]), 'wt', encoding='utf-8') as f:
        json.dump(jsonString, f)

    return staging, fileName
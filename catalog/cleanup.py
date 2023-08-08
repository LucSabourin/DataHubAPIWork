keyChars = {
    ' ': '_',
    '.': ''
}

def cleanUpKey(key : str) -> str:
    """Removes problematic characters from a proposed key.

    Parameters:
    -----------
    key: str
        proposed key

    Returns:
    --------
    str
        cleaned key
    """

    for charOld, charNew in keyChars.items():
        key.replace(charOld, charNew)

    return key.lower()
    
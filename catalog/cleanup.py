keyChars = {
    ' ': '_',
    '.': ''
}

def cleanUpKey(key : str) -> str:
    """
    """

    for charOld, charNew in keyChars.items():
        key.replace(charOld, charNew)

    return key.lower()
    
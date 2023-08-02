from datetime import datetime

def dateTimeString() -> str:
    """
    """

    return datetime.strftime(datetime.now(), '%Y.%m.%d-%H.%M.%S')
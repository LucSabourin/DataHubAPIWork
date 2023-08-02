from configparser import ConfigParser
from config import ROOTDIR

configIni = '/'.join([ROOTDIR, 'pbi', 'config', 'config.ini'])
credentials = '/'.join([ROOTDIR, 'pbi', 'config', 'power_bi_state.jsonc'])
config = ConfigParser()
config.read(configIni)
config_info = {
    'client_id': config.get('power_bi_app', 'client_id'),
    'client_secret': config.get('power_bi_app', 'client_secret'),
    'redirect_uri': config.get('power_bi_app', 'redirect_uri'),
    'group_id': config.get('power_bi_app', 'group_id'),
}
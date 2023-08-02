from configparser import ConfigParser

def buildConfig():
    """
    """

    config = ConfigParser()

    config.add_section('power_bi_app')

    config.set('power_bi_app', 'client_id', 'a0e95b31-39e9-4b0a-9228-78418613c6ec')
    config.set('power_bi_app', 'client_secret', 'BiAIcArg3hYypgenqFf7DyDB1N+rLKDvny/Em57+Mlw=')
    config.set('power_bi_app', 'uri', 'https://localhost')
    config.set('power_bi_app', 'redirect_uri', 'https://localhost/redirect')
    config.set('power_bi_app', 'group_id', '217cf6d6-2cce-4838-9928-396f7a59e931')

    with open(file='config/config.ini', mode='w+', encoding='utf-8') as f:
        config.write(f)

if __name__ == '__main__':
    buildConfig()

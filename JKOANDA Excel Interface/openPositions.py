from configparser import ConfigParser
import oandapyV20
import oandapyV20.endpoints.positions as positions

config = ConfigParser()
config.read('oanda.ini')

accountID = config.get('fxpractice','active_account')
client = oandapyV20.API(access_token=config.get('fxpractice','token'))
r = positions.OpenPositions(accountID=config.get('fxpractice','active_account'))
client.request(r)
print r.response


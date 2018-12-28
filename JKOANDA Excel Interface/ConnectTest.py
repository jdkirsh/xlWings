from configparser import ConfigParser

config = ConfigParser()
config.read('oanda.ini')
hostname = config.get('fxpractice','hostname')
steaming_hostname = config.get('fxpractice','streaming_hostname')
port = config.get('fxpractice','port')
ssl = config.get('fxpractice','ssl')
token = config.get('fxpractice', 'token')
username = config.get('fxpractice','username')
active_account = config.get('fxpractice','active_account')
# domain = config.get('instance', 'prod')
# headers = {'Authorization': 'Bearer {}'.format(token)}

# get a list of trades
from oandapyV20 import API
import oandapyV20.endpoints.trades as trades
import json

print("Running ConnectTest...")

api = API(token)
# accountID = "001-001-2033767-001"
r = trades.TradesList(active_account)
# show the endpoint as it is constructed for this call
print("REQUEST:{}".format(r))
rv = api.request(r)
print("RESPONSE:\n{}".format(json.dumps(rv, indent=2)))


# api = API(access_token="bc05fa130d462a39c9d181f053eb4002-5d129c81a25f312a7528a423e57ce83f")
# accountID = "001-001-2033767-001"
# r = trades.TradesList(accountID)
# # show the endpoint as it is constructed for this call
# print("REQUEST:{}".format(r))
# rv = api.request(r)
# print("RESPONSE:\n{}".format(json.dumps(rv, indent=2)))

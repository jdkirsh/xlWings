# get a list of trades
from oandapyV20 import API
import oandapyV20.endpoints.trades as trades
import json

api = API(access_token="5d03d1486fc0de4994c0927cd49968b9-d943b98ce6e1cdb9dd6ee531cb2544f9")
accountID = "101-001-6636926-001"
r = trades.TradesList(accountID)
# show the endpoint as it is constructed for this call
print("REQUEST:{}".format(r))
rv = api.request(r)
print("RESPONSE:\n{}".format(json.dumps(rv, indent=2)))

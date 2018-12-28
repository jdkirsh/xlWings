import json
from collections import namedtuple

def main():

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

	# jk = json2obj(r.response)
    #
	# print('jk=', jk)


# class Json2obj(object):
# 	def __init__(self, data):
# 		self.__dict__ = json.loads(data)

# test1 = Test(json_data)
# print(test1.a)
#
def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())
def json2obj(data): return json.loads(data, object_hook=_json_object_hook)
#
# x = json2obj(data)

if __name__ == "__main__":
	main()
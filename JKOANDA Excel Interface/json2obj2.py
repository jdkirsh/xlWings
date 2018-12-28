import json
from collections import namedtuple


def json_loads_byteified(json_text):
    return _byteify(
        json.loads(json_text, object_hook=_byteify),
        ignore_dicts=True
    )


def _byteify(data, ignore_dicts=False):
    # if this is a unicode string, return its string representation
    if isinstance(data, unicode):
        return data.encode('utf-8')
    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [_byteify(item, ignore_dicts=True) for item in data]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            for key, value in data.iteritems()
        }
    # if it's anything else, return it in its original form
    return data

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
    print (r.response)

    # jk = json_loads_byteified(r.response)
    # print('jk=', jk)




	# jk = json2obj(r.response)
    #
	# print('jk=', jk)


# class Json2obj(object):
# 	def __init__(self, data):
# 		self.__dict__ = json.loads(data)

# test1 = Test(json_data)
# print(test1.a)
#
# def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())
# def json2obj(data): return json.loads(data, object_hook=_json_object_hook)
# #
# # x = json2obj(data)

if __name__ == "__main__":
	main()

'''import json

def json_load_byteified(file_handle):
    return _byteify(
        json.load(file_handle, object_hook=_byteify),
        ignore_dicts=True
    )

def json_loads_byteified(json_text):
    return _byteify(
        json.loads(json_text, object_hook=_byteify),
        ignore_dicts=True
    )

def _byteify(data, ignore_dicts = False):
    # if this is a unicode string, return its string representation
    if isinstance(data, unicode):
        return data.encode('utf-8')
    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [ _byteify(item, ignore_dicts=True) for item in data ]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            for key, value in data.iteritems()
        }
    # if it's anything else, return it in its original form
    return data
    '''

'''>>> json_loads_byteified('{"Hello": "World"}')
{'Hello': 'World'}
>>> json_loads_byteified('"I am a top-level string"')
'I am a top-level string'
>>> json_loads_byteified('7')
7
>>> json_loads_byteified('["I am inside a list"]')
['I am inside a list']
>>> json_loads_byteified('[[[[[[[["I am inside a big nest of lists"]]]]]]]]')
[[[[[[[['I am inside a big nest of lists']]]]]]]]
>>> json_loads_byteified('{"foo": "bar", "things": [7, {"qux": "baz", "moo": {"cow": ["milk"]}}]}')
{'things': [7, {'qux': 'baz', 'moo': {'cow': ['milk']}}], 'foo': 'bar'}
>>> json_load_byteified(open('somefile.json'))
{'more json': 'from a file'}'''
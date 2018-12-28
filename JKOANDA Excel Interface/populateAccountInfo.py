from configparser import ConfigParser
import oandapyV20
# import oandapyV20.endpoints.positions as positions
import oandapyV20.endpoints.accounts as accounts


'''>>> x = json.loads('{"a":1,"b":2}')
>>> y = json.dumps(x, indent=4)
>>> z = json.pretty(x)'''
# Get account info

'''>>> import oandapyV20 >>> 
import oandapyV20.endpoints.accounts as accounts >>> 
client = oandapyV20.API(access_token=...) >>> 
r = accounts.AccountSummary(accountID) >>> 
client.request(r) >>> 
print r.response
'''

from collections import namedtuple
def convert(obj):
    if isinstance(obj, dict):
        for key, value in obj.iteritems():
            obj[key] = convert(value)
        return namedtuple('GenericDict', obj.keys())(**obj)
    elif isinstance(obj, list):
        return [convert(item) for item in obj]
    else:
        return obj

# class Map(dict):
#     """
#     Example:
#     m = Map({'first_name': 'Eduardo'}, last_name='Pool', age=24, sports=['Soccer'])
#     """
#     def __init__(self, *args, **kwargs):
#         super(Map, self).__init__(*args, **kwargs)
#         for arg in args:
#             if isinstance(arg, dict):
#                 for k, v in arg.iteritems():
#                     self[k] = v
#
#         if kwargs:
#             for k, v in kwargs.iteritems():
#                 self[k] = v
#
#     def __getattr__(self, attr):
#         return self.get(attr)
#
#     def __setattr__(self, key, value):
#         self.__setitem__(key, value)
#
#     def __setitem__(self, key, value):
#         super(Map, self).__setitem__(key, value)
#         self.__dict__.update({key: value})
#
#     def __delattr__(self, item):
#         self.__delitem__(item)
#
#     def __delitem__(self, key):
#         super(Map, self).__delitem__(key)
#         del self.__dict__[key]
#
#
# class dotdict(dict):
#     """dot.notation access to dictionary attributes"""
#     __getattr__ = dict.get
#     __setattr__ = dict.__setitem__
#     __delattr__ = dict.__delitem__
#
# mydict = {'val':'it works'}
# nested_dict = {'val':'nested works too'}
# mydict = dotdict(mydict)
# mydict.val
# # 'it works'
#
# mydict.nested = dotdict(nested_dict)
# mydict.nested.val
# # 'nested works too'

config = ConfigParser()
config.read('oanda.ini')

def getAccountInfo():

    accountID = config.get('fxpractice','active_account')
    client = oandapyV20.API(access_token=config.get('fxpractice','token'))
    # r = positions.OpenPositions(accountID=config.get('fxpractice','active_account'))
    r = accounts.AccountSummary(accountID)
    client.request(r)
    print r.response
    return r.response

print ("pause")







if __name__ == "__main__":
    accountInfo = getAccountInfo()

    print ("accountInfo.account.currency=",accountInfo['account']['currency'] )

from configparser import ConfigParser
import oandapyV20
# import oandapyV20.endpoints.positions as positions
import oandapyV20.endpoints.accounts as accounts

from pyxll import xl_func, xl_version, xlAsyncReturn
import logging
import sys
import threading

config = ConfigParser()
config.read('oanda.ini')
_log = logging.getLogger(__name__)



@xl_func("string, async_handle<string>: void")
def get_account_currency(handle):
    """returns the last price for a symbol from iextrading.com"""

    def thread_func(async_handle):
        try:
            accountID = config.get('fxpractice', 'active_account')
            client = oandapyV20.API(access_token=config.get('fxpractice', 'token'))
            # r = positions.OpenPositions(accountID=config.get('fxpractice','active_account'))
            r = accounts.AccountSummary(accountID)
            client.request(r)
            # print r.response
            # result = r.response['account']['currency']
            result = 'JKblah'

            # get the price using an http request to iextrading.com
            # url = "https://api.iextrading.com/1.0/stock/%s/batch?types=quote" % symbol
            # data = urllib2.urlopen(url).read()
            # if sys.version_info[0] > 2:
            #     data = data.decode()
            #
            # # the returned data is in json format
            # result = json.loads(data)["quote"].get("latestPrice", "#NoLatestPrice")
        except Exception, e:
            result = e

        # return the result to Excel
        xlAsyncReturn(async_handle, result)

    # Do the request in a new thread (for a real application using a ThreadPool
    # would be advisable).
    thread = threading.Thread(target=thread_func, args=(handle))
    thread.start()

    # Done, no need to return a value as it is done by the response handler.
    return


'''
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

    print ("accountInfo.account.currency=",accountInfo['account']['currency'] )'''
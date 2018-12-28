"""
PyXLL Examples: Async function

Starting with Excel 2010 worksheet functions can
be registered as asynchronous.

This can be used for querying results from a server
asynchronously to improve the worksheet calculation
performance.
"""

from pyxll import xl_func, xl_version, xlAsyncReturn
import logging
import sys

_log = logging.getLogger(__name__)

try:
    import json
except ImportError:
    _log.warning("json could not be imported. Async example will not work", exc_info=True)
    json = None

#
# this example uses urllib2 to perform an asynchronous http
# request and return the data to Excel.
#
import urllib2
import threading

#
# Async functions are only supported from Excel 2010
#
if xl_version() >= 14 and json is not None:

    @xl_func("string, async_handle<float>: void")
    def pyxll_stock_price(symbol, handle):
        """returns the last price for a symbol from iextrading.com"""

        def thread_func(symbol, async_handle):
            try:
                # get the price using an http request to iextrading.com
                url = "https://api.iextrading.com/1.0/stock/%s/batch?types=quote" % symbol
                data = urllib2.urlopen(url).read()
                if sys.version_info[0] > 2:
                    data = data.decode()

                # the returned data is in json format
                result = json.loads(data)["quote"].get("latestPrice", "#NoLatestPrice")
            except Exception, e:
                result = e

            # return the result to Excel
            xlAsyncReturn(async_handle, result)
 
        # Do the request in a new thread (for a real application using a ThreadPool
        # would be advisable).
        thread = threading.Thread(target=thread_func, args=(symbol, handle))
        thread.start()

        # Done, no need to return a value as it is done by the response handler.
        return

else:

    @xl_func("string: string")
    def pyxll_stock_price(symbol):
        """not supported in this version of Excel"""
        if json is None:
            return "json module could not be imported"
        return "async functions are not supported in Excel %s" % xl_version()
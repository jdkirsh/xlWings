import xlwings as xw
from xlwings import Book, Range


def hello_xlwings():
    wb = xw.Book.caller()
    wb.sheets[0].range("A1").value = "Hello xlwings!"


@xw.func
def hello(name):
    return "hello {0}".format(name)


@xw.func
def summarize_sales():
    """
    Retrieve the account number and date ranges from the Excel sheet
    """
    # Make a connection to the calling Excel file
    wb = Book.caller()

    # Retrieve the account number and dates
    account = Range('B2').value
    start_date = Range('D2').value
    end_date = Range('F2').value

    # Output the data just to make sure it all works
    Range('A5').value = account
    Range('A6').value = start_date
    Range('A7').value = end_date

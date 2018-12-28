import xlwings as xw

CSV_FILE = 'out-acctInfo.csv'


def hello_xlwings():
    wb = xw.Book.caller()
    wb.sheets[0].range("A1").value = "Hello xlwings!"


@xw.func
def hello(name):
    return "hello {0}".format(name)

def csvToRange():
    wb = xw.Book.caller()
    sht = wb.sheets[0]
    for row, line in enumerate(CSV_FILE):
        myrange = 'A' + row
        mydata = line.split(',')
        sht.range(myrange).value = mydata
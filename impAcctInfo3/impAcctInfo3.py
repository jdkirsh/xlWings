import xlwings as xw

CSV_FILE = 'out-acctInfo.csv'


def hello_xlwings():
    wb = xw.Book.caller()
    wb.sheets[0].range("A1").value = "Hello xlwings!"


@xw.func
def hello(name):
    return "hello {0}".format(name)

def csvToRange():
    # xw.Interactive = False
    wb = xw.Book.caller()
    # sht = wb.sheets[0]
    # sht = wb.sheets['Sheet1']
    for row, line in enumerate(CSV_FILE):
        myrange = 'A' + str(row)
        mydata = line.split(',')
        # sht.range(myrange).value = mydata
        # sht.range(myrange).expand().value = mydata
        xw.Range(myrange).value = mydata

def test_ToRange():
    wb = xw.Book.caller()
    sht = wb.sheets['Sheet1']
    sht.range('A1').value = [['Foo 1', 'Foo 2', 'Foo 3'], [10.0, 20.0, 30.0]]
    sht.range('A1').expand().value


def test_csvToDF():
    import pandas as pd
    infile = pd.read_csv(r'C:\FINANCE\Python\PyCharm\Projects\xlWings\impAcctInfo3\acctInfo.csv')
    wb = xw.Book.caller()
    sht = wb.sheets['Sheet1']
    sht.range('A1').value = infile
    sht.range('A1').options(pd.DataFrame, expand='table').value


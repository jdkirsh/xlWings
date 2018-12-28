import xlwings as xw
import numpy as np

#@xw.func
#def double_sum(x, y):
#	"""Returns twice the sum of the two arguments"""
#	return 2 * (x + y)

@xw.func
def add_one(data):
    return [[cell + 1 for cell in row] for row in data]

@xw.func
@xw.ret(expand='table')
def dynamic_array(r, c):
    return np.random.randn(int(r), int(c))

@xw.func
@xw.arg('x', doc='This is x.')
@xw.arg('y', doc='This is y.')
def double_sum(x, y):
    """Returns twice the sum of the two arguments"""
    return 2 * (x + y)

@xw.sub
def my_macro():
    """Writes the name of the Workbook into Range("A1") of Sheet 1"""
    wb = xw.Book.caller()
    wb.sheets[0].range('A1').value = wb.name

@xw.sub
def my_plot1():
    import matplotlib.pyplot as plt
    fig = plt.figure()
    plt.plot([1,2,3])

    sht = xw.Book().sheets[0]
    sht.pictures.add(fig, name='MyPlot', update=True)

@xw.func
def myplot2(n):
    import matplotlib.pyplot as plt
    sht = xw.Book.caller().sheets.active
    fig = plt.figure()
    plt.plot(range(int(n)))
    sht.pictures.add(fig, name='MyPlot', update=True)
    return 'Plotted with n={}'.format(n)



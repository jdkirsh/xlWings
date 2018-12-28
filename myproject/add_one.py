import xlwings as xw

import mat

@xw.func
def add_one(data):
    return [[cell +1 for cell in row] for row in data]
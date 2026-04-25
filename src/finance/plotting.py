import termplotlib as tpl
import numpy as np
from register import Register

def plotAnnualTotals(register:Register):
    df = register.getAnnualTotals()
    fig = tpl.figure()
    fig.plot(df['year'], df['total'], width=100, height = 40)
    print(fig.get_string())



    

import pandas as pd

def readDefaultCsv(csvfile):
    df = pd.read_csv(csvfile)

def readQuickenCsv(csvfile:str, account:str):
    df = pd.read_csv(csvfile)
    df = df.drop(columns=['Category','Split','Scheduled','Unnamed: 0','Payee','Balance'])
    split_dates = df.apply(lambda row: splitDateString(row['Date']), axis=1)
    df = df.join(split_dates)
    df['tag'] = ''
    df['category'] = ''
    df['account'] = account
    df = df.rename(columns={'Amount':'value'})
    df['value'] = df['value'].str.replace(',', '').astype(float)
    return df

def splitDateString(date:str):
    parts = date.split('/')
    return pd.Series([parts[0],parts[1],parts[2]], index=['month','day','year'])
import pandas as pd

def readDefaultCsv(csvfile) -> pd.DataFrame:
    """read a csv of transactions (required format is in README)"""
    return pd.read_csv(csvfile)

def readQuickenCsv(csvfile:str, account:str) -> pd.DataFrame:
    """read a csv of Quicken exported transactions"""
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

def splitDateString(date:str) -> pd.Series:
    """split a Quicken date string into month,day,year components"""
    parts = date.split('/')
    return pd.Series([parts[0],parts[1],parts[2]], index=['month','day','year'])

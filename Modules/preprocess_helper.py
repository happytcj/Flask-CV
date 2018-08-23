import numpy as np
import pandas as pd

reach_op = lambda x: float(x.replace('"', '').strip())
weight_op = lambda x: float(x.split()[0])
stracc_op = lambda x: float(x[:-1])

def height_op(in_str):
    in_str = str(in_str)
    if type(in_str) is int:
        return in_str
    feet, inches = in_str.split(' ')
    feet_num = int(feet[:-1])
    inches_num = int(inches[:-1])
    return feet_num * 12 + inches_num

def result_op(in_str):
    if 'win' in in_str:
        return 1
    elif 'loss' in in_str:
        return 0
    elif 'n/a' in in_str:
        return 0

def cleanup_df(indf):
    ret = pd.DataFrame()
    indf.dropna(subset=['height', 'reach'], inplace=True)
    ret['reach'] = indf['reach'].apply(reach_op)
    ret['weight'] = indf['weight'].apply(weight_op)
    ret['height'] = indf['height'].apply(height_op)
    ret['w/l'] = indf['w']/(indf['w']+indf['l'])
    ret['SLpM'] = indf['SLpM']
    ret['Str. Acc.'] = indf['Str. Acc.'].apply(stracc_op)
    ret['SApM'] = indf['SApM'].apply(float)
    ret['Str. Def'] = indf['Str. Def'].apply(stracc_op)
    ret['TD Avg'] = indf['TD Avg'].apply(float)
    ret['TD Acc.'] = indf['TD Acc.'].apply(stracc_op)
    ret['TD Def.'] = indf['TD Def.'].apply(stracc_op)
    ret['Sub. Avg.'] = indf['Sub. Avg.'].apply(float)
    ret['result'] = indf['result'].apply(result_op)
    return ret

#create new vector consisting of: height, weight, reach, w/l ratio, and statistics
def generate_delta(primary, contender, mode='absolute'):
    #first cleanup input dataframes
    primary_clean = cleanup_df(primary)
    contender_clean = cleanup_df(contender)
    if mode == 'absolute':
        delta = pd.DataFrame(data = (contender_clean.values-primary_clean.values),
                             columns=contender_clean.columns)
    elif mode == 'percentage':
        delta = pd.DataFrame(100*(contender_clean.values-primary_clean.values)/primary_clean.values,
                             columns=contender_clean.columns)
    return delta
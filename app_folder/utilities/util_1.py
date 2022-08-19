import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import pickle
import logging

logging.basicConfig(level=logging.INFO)

log=logging.getLogger("gunicorn.error")

user=os.environ.get("USER_TR","ubuntu")
folder=os.environ.get("FOLDER_TR","data_tr")

csv_path=f"/home/{user}/{folder}/csv/"
jpg_path=f"/home/{user}/{folder}/jpg/"

columns=['time', 'aqi', 'pm25','pm10', 'co', 'so2']


def get_all_plot():

    log.info(" Inside the get_all_plot ")
    df1 = pd.read_csv(csv_path+'fil.csv')
   
    log.info("======================== Read the dataframe ===========================")
    df1['time'] = df1['time'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))

    plt.figure(figsize=(12, 5))

    df1m = df1[columns]
    log.info("--------------------------subsetting---------------------")

    dfm = df1m.melt('time', var_name='metrics', value_name='metric_vals')
    #log.info(df1m.tail(1))
    
    s1 = sns.lineplot(x='time', y='metric_vals', hue='metrics', data=dfm)
    log.info("-------------------------making plot---------------------")
    
    s1.figure.savefig(jpg_path+'get_all_plot.jpg')

    plt.close(s1.figure)
    log.info("-----------------------closing figure--------------------")

def get_specific_plot(cate: str):
    
    log.info(" Inside the specific category plot ")
    df1 = pd.read_csv(csv_path+'fil.csv')

    df1['time'] = df1['time'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
    
    plt.figure(figsize=(12, 5))

    s2 = sns.lineplot(x='time', y=cate, data=df1)

    s2.figure.savefig(jpg_path+'get_specific_plot.jpg')

    plt.close(s2.figure)
    log.info("Closing figure")

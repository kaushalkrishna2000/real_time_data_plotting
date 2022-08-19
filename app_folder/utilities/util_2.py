import os
import pandas as pd
import pickle
import subprocess as sp
import logging

logging.basicConfig(level=logging.INFO)
log=logging.getLogger("gunicorn.error")

user=os.environ.get("USER_TR","ubuntu")
folder=os.environ.get("FOLDER_TR","data_tr")

csv_path=f"/home/{user}/{folder}/csv/"

columns=None

def filtering():

    log.info("Inside the fitering function ")

    if (os.path.exists(csv_path + 'column.pkl')):
        with open(csv_path + 'column.pkl', 'rb+') as f:
            columns = pickle.load(f)

    log.info("--------------filtering the copy.csv------------------")
    sp.getoutput(f"tail -n 24 {csv_path}copy.csv > {csv_path}fil.csv")

    df=pd.read_csv(csv_path+'copy.csv', names=columns)

    if( list(df.iloc[0,:]) == columns ):
        df.drop(0,axis=0,inplace=True)

    log.info("----------------putting to fil.csv--------------------")
    df.to_csv(csv_path+'fil.csv',index=False)

    log.info(" Exiting the filtering function")

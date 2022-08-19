import time
import requests
import pandas as pd
import logging
import os
import pickle

user=os.environ.get("USER_TR","ubuntu")
folder=os.environ.get("FOLDER_TR","data_tr")

log_path = f"/home/{user}/{folder}/log/"
path = f"/home/{user}/{folder}/csv/"

logging.basicConfig(filename=log_path + "log.txt", level=logging.DEBUG)

logger = logging.getLogger(__name__)

p = {
    'token': 'b932564409dc03de5dafbf24822a2a9a1c155593'
}

resource_id = "3b01bcb8-0b14-4abf-b6f2-c1bfd384ba69"  # Real Time Air Quality Index From Various Locations

req_url = "https://api.waqi.info/feed/@12468"

columns = ['idx', 'place', 'station', 'time', 'aqi', 'pm25', 'pm10', 'co', 'so2']

last_updated=None
count=0

with open(path + 'column.pkl', 'wb+') as f:
    pickle.dump(columns, f)

if(os.path.exists(path+'last.pkl')):
    logger.info("----------------------------------Updating from pickle file-----------------------------------------")
    with open(path+'last.pkl', 'rb+') as f:
        last_updated = pickle.load(f)
    logger.info("----------------------------------------------------------------------------------------------------")


try:

    while True:

        resp = requests.get(req_url, params=p)

        place = resp.json()['data']['city']['name'].split(", ")[1]
        station = resp.json()['data']['city']['name'].split(", ")[0]
        pm25 = resp.json()['data']['iaqi']['pm25']['v']
        co = resp.json()['data']['iaqi']['co']['v']
        so2 = resp.json()['data']['iaqi']['so2']['v']
        pm10 = resp.json()['data']['iaqi']['pm10']['v']
        datetime = resp.json()['data']['time']['s']
        idx = resp.json()['data']['idx']
        aqi = resp.json()['data']['aqi']

        dict1 = dict(idx=idx, place=place, station=station, time=datetime, aqi=aqi, pm25=pm25, pm10=pm10, co=co, so2=so2)

        df = pd.DataFrame([dict1])

        count += 1

        logger.info(f"------------------------------------ Count : {count} ------------------------------------------")

        if not last_updated:
            logger.debug(f" Response got for Entry (FIRST TIME) :  {df.iloc[0, 3]} ")
            logger.info(df.head(1))

            if(os.path.exists(path+'copy.csv')):
                df.to_csv(path + 'copy.csv', index=False,mode='a')  # Creating file
                last_updated = df.iloc[0, 3]  # Updating last_update
            else:
                df.to_csv(path + 'copy.csv', index=False)  # Creating file
                last_updated = df.iloc[0, 3]  # Updating last_update

            with open(path + 'last.pkl', 'wb+') as f: # Dumping into Pickle
                pickle.dump(last_updated,f)

        if not (df.iloc[0, 3] == last_updated):
            logger.info(f"{resp.status_code} ")
            logger.info(f"Response got for Entry (CONTINUOUS/RESTART MODE) : {df.iloc[0, 3]}")

            df.to_csv(path + 'copy.csv', mode='a', header=False, index=False) #Storing in append mode
            last_updated = df.iloc[0, 3]

            with open(path + 'last.pkl', 'wb+') as f:  #Dumping into Pickle
                pickle.dump(last_updated,f)

        time.sleep(300)

        logger.info(f"-----------------------------------------------------------------------------------------------")

except Exception as e:

    logger.exception(e.__context__)
    logger.info(f"------------------------------ Final Count : {count} ----------------------------------------------")
    df.to_csv(log_path + 'error.csv')

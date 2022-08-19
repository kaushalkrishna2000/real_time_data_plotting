import os
import logging
from fastapi import APIRouter
from fastapi.responses import FileResponse


from utilities.util_2 import filtering
from utilities.util_1 import get_all_plot,get_specific_plot

logging.basicConfig(filename="log.txt", level=logging.DEBUG)
log = logging.getLogger("gunicorn.error")

router = APIRouter()

user=os.environ.get("USER_TR","ubuntu")
folder=os.environ.get("FOLDER_TR","data_tr")

jpg_path=f"/home/{user}/{folder}/jpg/"


@router.get("/getall")
def get_all_plot_1():

    log.info("-------------------------------- Filtering ---------------------")
    filtering()
    log.info("------------------------------- Get all plot -------------------")
    get_all_plot()
    log.info("----------------------------Sending Reponse --------------------")
    return FileResponse(jpg_path+'get_all_plot.jpg',media_type='image/jpeg')


@router.get("/specificplot")
def get_specific_plot_1(category:str):

    log.info("----------------------------Filtering --------------------------")
    filtering()
    log.info("---------------------------- Get specific plot -----------------")
    get_specific_plot(category)
    log.info("---------------------------Sending response --------------------")
    return FileResponse(jpg_path+'get_specific_plot.jpg',media_type='image/jpeg')


@router.get("/getallpic")
def get_all_pic1():
    
    filtering()

    get_all_plot()
    log.info("---------------------------Sending the file to client -----------")
    return FileResponse(jpg_path+'get_all_plot.jpg',media_type='image/jpef',filename='allplot.jpg')


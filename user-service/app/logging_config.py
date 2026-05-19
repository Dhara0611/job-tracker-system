import logging
import os

#using os to prepare filesystem for logs

def setup_logging():

#check if folder exists else create one
    if not os.path.exists("logs"):
        os.mkdir("logs")
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s : %(message)s",
        handlers=[
            logging.FileHandler("logs/app.log"),
            logging.StreamHandler()
        ]
    )
    

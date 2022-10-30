import logging, sys 
from pathlib import Path

# create a custom logger 
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# create handlers 
f_handler = logging.FileHandler(Path("storage/logs/app.log"))
c_handler = logging.StreamHandler(sys.stdout)

# create formatter 
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_handler.setFormatter(formatter)
c_handler.setFormatter(formatter)

# add handlers 
logger.addHandler(f_handler)
logger.addHandler(c_handler)


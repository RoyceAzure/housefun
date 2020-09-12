from dotenv import load_dotenv, find_dotenv
import os
import time
load_dotenv(find_dotenv())


# _Dbparams = {
#     'host' : os.environ.get('host'),
#     'port' : int(os.environ.get('port')),
#     'user' : os.environ.get('user'),
#     'password' : os.environ.get('password'),
#     'database' : os.environ.get('database'),
#     'charset' : os.environ.get('charset')
# }
_BaseDir = os.environ.get("workdir")
_SaveDir = os.environ.get("SaveDir")
_driver_path=os.environ.get("driver_path")
csvFileName = os.environ.get("csvFileName")
_saveCsvPath = os.path.join(_BaseDir,_SaveDir,time.strftime('%Y_%m_%d_%H') + "_" + csvFileName)

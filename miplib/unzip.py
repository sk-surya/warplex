

import zipfile
from logger import logger
from path import get_mps_files_dir, get_zip_path


def unzip_if_empty():
    if len(list(get_mps_files_dir().iterdir())) == 0:
        unzip()
    else:
        logger.info(f"MPS files already unzipped at {get_mps_files_dir()}")

    # count the number of files in the directory
    num_files = len(list(get_mps_files_dir().iterdir()))
    logger.info(f"Found {num_files} MPS files in {get_mps_files_dir()}")

def unzip():
    logger.info(f"Unzipping {get_zip_path()} to {get_mps_files_dir()}")
    with zipfile.ZipFile(get_zip_path(), 'r') as zip_ref:
        zip_ref.extractall(get_mps_files_dir())
    logger.info(f"Unzipped to {get_mps_files_dir()}")
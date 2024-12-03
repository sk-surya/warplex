


from logger import logger
from metadata import process_instances_df
from path import get_miplib_benchmark_dir, get_zip_path
from tqdm import tqdm
import requests


def download_zip():
    url = "https://miplib.zib.de/downloads/benchmark.zip"
    logger.info(f"Downloading from {url} to {get_zip_path()}")
    
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(get_zip_path(), 'wb') as file, \
         tqdm(
            desc="Downloading",
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as progress_bar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            progress_bar.update(size)

    logger.info(f"Downloaded to {get_zip_path()}")

def download_if_not_exists():
    if not get_zip_path().exists():
        download_zip()
    else:
        logger.info(f"Zip file already exists at {get_zip_path()}")


def download_miplib_datatable():
    instances_path = get_miplib_benchmark_dir() / "data" / "instances.csv"
    if instances_path.exists():
        logger.info(f"instances.csv already exists at {instances_path}")
        return
    instances_path.parent.mkdir(parents=True, exist_ok=True)

    import requests
    from bs4 import BeautifulSoup
    import pandas as pd

    url = 'https://miplib.zib.de/tag_benchmark.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('table')
    headers = [header.text for header in table.find_all('th')]

    rows = []
    for row in table.find_all('tr'):
        cells = row.find_all('td')
        if cells:
            rows.append([cell.text for cell in cells])

    df = pd.DataFrame(rows, columns=headers)
    df = process_instances_df(df)
    
    df.to_csv(instances_path, index=False)
    logger.info(f"MIPLIB Instance Table has been saved to {instances_path}")
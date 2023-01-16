import os
import osmnx as ox
from networkx import MultiDiGraph
from functools import partial
from multiprocessing import Pool
from logger import get_logger

ROAD_NETWORKS_DIR: str = './road_networks'
CITIES_DIR: str = "./cities"


def process_city(country: str, city: str) -> None:
    city_filename: str = os.path.join(f"{ROAD_NETWORKS_DIR}/{country}", city.replace('/', '_') + ".graphml")
    query: str = f"{city}, {country}"
    logger = get_logger()

    if os.path.exists(city_filename):
        logger.info(f"{query} already processed... skipping")
        return

    try:
        G: MultiDiGraph = ox.graph_from_place(query, network_type="drive")
        ox.save_graphml(G, city_filename)
        logger.info(f"{query} road network saved")
    except Exception as e:
        logger.error(f"{e}")


def download_road_networks() -> None:
    for country in sorted(os.listdir(CITIES_DIR)):
        country = country.rsplit('.', maxsplit=1)[0]

        country_dir: str = f"{ROAD_NETWORKS_DIR}/{country}"
        os.makedirs(country_dir, exist_ok=True)

        filename: str = os.path.join(CITIES_DIR, country + ".txt")

        with open(filename, 'r') as f_country:
            with Pool(8) as pool:
                cities = [city.strip() for city in sorted(f_country.readlines())]
                pool.map(
                    partial(process_city, country),
                    cities
                )

import os

from overpy import Overpass, Result
from overpy.exception import OverpassGatewayTimeout, OverpassTooManyRequests
from time import sleep

from logger import get_logger

DIR: str = "./cities2"
SLEEP: int = 5
MAX_TRIES: int = 10


def download_city_names() -> None:
    api: Overpass = Overpass()
    logger = get_logger()

    os.makedirs(DIR, exist_ok=True)

    with open("countries.txt", 'r') as f_countries:
        for country in f_countries.readlines():
            country: str = country.strip()

            file: str = f"{DIR}/{country}.txt"

            if os.path.exists(file):
                logger.info(f"{country} already processed... skipping")
                continue
            else:
                logger.info(f"Working on {country}")

            result: Result

            tries: int = 0

            while tries < MAX_TRIES:
                try:
                    result = api.query(f"""
                        [out:json];
                        area["name:en"="{country}"];
                        (
                          node["place"~"city|town"]["place"!="city_block"](area);
                        );
                        out;
                        """)
                    break
                except (OverpassGatewayTimeout, OverpassTooManyRequests) as e:
                    logger.error(f"{e}")
                    logger.info(f"Trying again...")
                    sleep(SLEEP)
                    tries += 1

            with open(file, 'w') as f_cities:
                cities: str = '\n'.join(
                    sorted([
                        f'{node.tags["name"]}'
                        for node
                        in result.nodes
                    ])
                )
                f_cities.write(cities)

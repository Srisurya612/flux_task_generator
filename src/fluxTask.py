import requests
from dotenv import load_dotenv
import os 
from retry import retry
import logging

load_dotenv()
logging.basicConfig(level=logging.DEBUG)

class FluxTaskGenerator:
    def __init__(self, host, headers, flux_query, user_name, password) -> None:
        """Formats the flux task as per the requirement and deploys it on kapacitor

        Args:
            host (str): endpoint to connect to kapaccitor
            headers (dict): meta data about the request
            flux_query (str): flux query
            user_name (str): influx username
            password (str): influx password
        """
        self.host = host
        self.header = headers
        self.query = flux_query
        self.user_name = user_name
        self.password = password

    def format_query(self,meta_inf):
        """formats the influx query according to meta information

        Args:
            meta_inf (dict): a dictionary of all the meta data to configure a flux task
        """
        site_id = meta_inf["site_id"]
        bucket = meta_inf["bucket"]
        user_name = os.getenv("USER_NAME")
        password = os.getenv("PASSWORD")
        task_name = meta_inf["alert_type"]
        replaced_task_name = self.query.replace("example_task", task_name)
        replaced_host = replaced_task_name.replace(
            "example_host", os.getenv("INFLUX_HOST")
        )
        replaced_token = replaced_host.replace(
            "example_token", f"{user_name}:{password}"
        )
        replaced_bukcet = replaced_token.replace("example_bucket", f"{bucket}/30_days")
        replaced_site = replaced_bukcet.replace("example_site", site_id)

        return replaced_site

    def deploy_task_on_kapacitor(self, meta_inf):
        """deploys the formatted task on kapacitor

        Args:
            meta_inf (dict): a dictionary of all the meta data to configure a flux task
        """
        alert_type = meta_inf["alert_type"]
        site_id = meta_inf["site_id"]
        formatted_query = self.format_query(meta_inf)
        task_def = {"status": "active", "flux": formatted_query}
        try:
            response = requests.post(self.host, headers=self.header, json=task_def)
            logging.info(f"The flux task for {alert_type} for site {site_id} has been deployed on kapacitor")
        except requests.exceptions.HTTPError as err:
            logging.error(f"The flux has not been deployed dur to {err}")

def query_meta_inf():
    pass

@retry(requests.exceptions.HTTPError,tries=3,delay=10)
def main():
    
    meta_inf = {
        "site_id": "agdcc-kol",
        "bucket": "cpa_logs_30_days",
        "alert_type": "wrong_command",
    }
    with open("fluxQuery.flux", "r") as file:
        query_data = file.read()
    headers = {
        "Content-type": "application/json",
        "Authorization": f'Token {os.getenv("USER_NAME")}:{os.getenv("PASSWORD")}',
    }
    flux_task_object = FluxTaskGenerator(
        os.getenv("HOST"),
        headers,
        query_data,
        os.getenv("USER_NAME"),
        os.getenv("PASSWORD"),
    )
    flux_task_object.deploy_task_on_kapacitor(meta_inf)


main()

import requests
from dotenv import load_dotenv
import os

load_dotenv()


class FluxTaskGenerator:
    def __init__(self, host, headers, flux_query, user_name, password) -> None:
        self.host = host
        self.header = headers
        self.query = flux_query
        self.user_name = user_name
        self.password = password

    def deploy_task_on_kapacitor(self, meta_inf):
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
        task_def = {"status": "active", "flux": replaced_site}
        response = requests.post(self.host, headers=self.header, json=task_def)

def query_meta_inf():
    pass

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

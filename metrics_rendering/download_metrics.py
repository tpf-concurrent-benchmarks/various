import os

import requests
import argparse
import yaml
from typing import Tuple


class GrafanaPanelDownloader:
    def __init__(self, grafana_url: str,
                 dashboard_uid: str,
                 timespan: Tuple[str, str],
                 image_width: int = 1000,
                 image_height: int = 500,
                 theme: str = "light"):
        self._grafana_url = grafana_url
        self._image_width = image_width
        self._image_height = image_height
        self._dashboard_uid = dashboard_uid
        self._theme = theme
        self._timespan = timespan
        self._dashboard_json = self.__get_dashboard_json(dashboard_uid)

    def __get_dashboard_json(self, dashboard_uid: str):
        dashboard_json = requests.get(f"{self._grafana_url}/api/dashboards/uid/{dashboard_uid}").json()
        return dashboard_json

    def __get_panel_id(self, panel_name: str):
        # This function will match the panel even if the name is not exactly the same
        panel_name = panel_name.replace(" ", "")
        panel_name = panel_name.replace("_", "")
        panel_name = panel_name.lower()

        for panel in self._dashboard_json["dashboard"]["panels"]:
            if panel_name in panel["title"].replace(" ", "").replace("_", "").lower():
                return panel["id"]
        return None

    def download_panel(self, panel_name: str, save_path: str):
        panel_id = self.__get_panel_id(panel_name)
        if panel_id is None:
            raise ValueError(f"Panel with name {panel_name} not found")

        panel_png = requests.get(f"{self._grafana_url}/render/d-solo/{self._dashboard_uid}/"
                                 f"{self._dashboard_json['meta']['slug']}?"
                                 f"orgId=1&panelId={panel_id}&width={self._image_width}&height={self._image_height}"
                                 f"&from={self._timespan[0]}&to={self._timespan[1]}"
                                 f"&tz=America%2FArgentina%2FBuenos_Aires&theme={self._theme}").content

        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "wb") as f:
            f.write(panel_png)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--config_path",
                        default="config.yaml",
                        help="Path to the config file. Default is config.yaml",
                        type=str)
    parser.add_argument("-c", "--context",
                        default=".",
                        help="Path that will be appended to the each folder path. Default is the current directory",
                        type=str)

    args = parser.parse_args()
    context = args.context

    with open(args.config_path, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    for folder_name in config["folders"]:
        start_time = config["folders"][folder_name]["from"]
        end_time = config["folders"][folder_name]["to"]
        grafana_panel_downloader = GrafanaPanelDownloader(grafana_url=config["grafana_url"],
                                                          dashboard_uid=config["dashboard_uid"],
                                                          timespan=(start_time, end_time),
                                                          image_width=config["size"]["width"],
                                                          image_height=config["size"]["height"],
                                                          theme=config["theme"])
        for panel_name in config["panels"]:
            save_path = os.path.join(context, folder_name, f"{panel_name}.png")
            grafana_panel_downloader.download_panel(panel_name, save_path)


if __name__ == "__main__":
    main()

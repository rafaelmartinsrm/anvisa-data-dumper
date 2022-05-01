from email.policy import default
from urllib.parse import urlencode
from pathlib import Path
import requests
import time
import os
import json


class API:
    url = None
    # Make use of a fake User-Agent
    # http://www.useragentstring.com/pages/useragentstring.php?name=Chrome
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
        "Authorization": "Guest",
    }
    cache_path = None
    initial_filters = {}
    current_filters = {}
    default_filters = {}
    DEBUG = True

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not hasattr(cls, "url"):
            raise TypeError(f"Subclass must define class attribute 'url'")

        # Set initial filters based on subclass parameters
        cls.initial_filters = cls.default_filters
        cls.initial_filters.update(kwargs.get("initial_filters", {}))

        # Create cache folder
        Path(cls.cache_path).mkdir(parents=True, exist_ok=True)

        # Create initial cache files if not exists
        cls.create_cache_file(cls, "initial_filters")

        # Load cache and check if filters changed, if so, prune.
        initial_cache_content = cls.load_cache_file(cls, extension="initial_filters")
        if str(initial_cache_content) != str(cls.initial_filters):
            cls.prune_cache(cls)
            cls.write_cache_file(
                cls, data=cls.initial_filters, extension="initial_filters"
            )
            cls.current_filters = dict(cls.initial_filters)
        else:
            cls.current_filters = cls.load_cache_file(cls, extension="current_filters")

    def prune_cache(self):
        # NOT IMPLEMENTED YET
        print("Pruning is not implemented yet")

    def create_cache_file(self, extension: str):
        cache_file = f"{self.cache_path}/{extension}.json"
        if self.DEBUG:
            print(f"[DEBUG] Creating {cache_file}.")
        try:
            with open(cache_file, "x") as f:
                f.close()
        except FileExistsError:
            pass

    def load_cache_file(self, extension: str) -> dict:
        cache_content = None
        cache_file = f"{self.cache_path}/{extension}.json"
        if self.DEBUG:
            print(f"[DEBUG] Reading {cache_file}.")
        with open(cache_file, "r", encoding="utf-8") as f:
            if f.read(1):
                f.seek(0)
                cache_content = json.load(f)
            f.close()

        return cache_content

    def write_cache_file(self, data: dict, extension: str):
        cache_file = f"{self.cache_path}/{extension}.json"
        if self.DEBUG:
            print(f"[DEBUG] Writing {cache_file}.")

        with open(cache_file, "w", encoding="utf-8") as f:
            f.write(json.dumps(data, indent=4, sort_keys=False))
            f.close()

    def generate_request_url(
        self,
        filters: dict = {},
    ) -> str:
        """Builds the request url for a dict of filters

        Args:
            filters (dict, optional): A dictionary of filters. Defaults to {}.

        Returns:
            str: the generated url
        """
        default_filters = {
            "count": 50,
            "page": 1,
        }
        default_filters.update(filters)
        if self.DEBUG:
            print(f"[DEBUG] Creating URL for filters: {default_filters}.")
        # Use urllib.parse.urlencode
        encoded_args = urlencode(default_filters)
        return self.url + encoded_args

    def request(self):
        start_time = time.time()
        TIMEOUT = 30

        req = None
        url = self.generate_request_url(filters=self.current_filters)

        if self.DEBUG:
            print(f"[DEBUG] Requesting {url}.")

        while True:
            try:
                # Verify is false since Intermediate are not available on consultas.anvisa.gov.br
                req = requests.get(url, headers=self.headers, verify=False)
                break
            except (
                requests.exceptions.Timeout,
                requests.exceptions.HTTPError,
                requests.exceptions.RequestException,
            ) as err:
                if time.time() > start_time + TIMEOUT:
                    raise Exception(err)
                else:
                    time.sleep(10)

        return req

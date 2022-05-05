import asyncio
import json
import os
import time

from .api import API


class Drugs(API):
    """Drugs"""

    url = "https://consultas.anvisa.gov.br/api/consulta/medicamento/produtos/?"
    drugs = []
    cache_path = f"{os.getcwd()}/cache/drugs"
    current_filters = {}
    mandatory_filters = {
        "count": 50,
        "page": 1,
        "filter[periodoPublicacaoFinal]": "2022-04-30T03:00:00.000Z",
    }

    def __init__(self, filters: dict = {}, cache: bool = True):
        self.cache = cache

    async def _adump(self, threads):
        # Get initial page, if not, 1
        initial_page = self.current_filters["page"]

        is_last = False
        while not is_last:
            self.write_cache_file(
                data=self.current_filters, extension="current_filters"
            )

            tasks = []
            for page_n in range(initial_page, initial_page + threads):
                tasks.append(self._request(filters={"page": page_n}))
            responses = await asyncio.gather(*tasks, return_exceptions=True)

            # Write responses to file
            for response in responses:
                self.write_cache_file(data=response, extension=response["number"])

            # Check if is_last in pages
            is_last = self._last_page_in_list(responses)

            initial_page += threads - 1

            time.sleep(1)

    def dump(self, threads: int = 4):
        asyncio.run(self._adump(threads))


class DrugDetail(API):
    """
    Drug details: contains detailed information about the drug registration.
    """
    url = "https://consultas.anvisa.gov.br/api/consulta/medicamento/produtos/"
    cache_path = f"{os.getcwd()}/cache/drugs/details"
    mandatory_filters = {}
    current_filters = {}

    def _load_page_file(self, file_path: str) -> list:
        if self.DEBUG:
            print(f"[DEBUG] Reading {file_path}.")

        with open(file_path, "r", encoding="utf-8") as f:
            file_content = json.load(f)
            f.close()

        return file_content["content"]

    async def _adump_products_from_file(self, file_path: str, threads: int = 4):
        drugs = self._load_page_file(file_path)
        tasks = []

        for drug in drugs:
            tasks.append(self._request(url_suffix=drug["processo"]["numero"]))

        responses = []
        for i in range(0, len(tasks), threads):
            responses = await asyncio.gather(
                *tasks[i : (i + threads)], return_exceptions=True
            )
            for response in responses:
                self.write_cache_file(response, response["processo"]["numero"])

            time.sleep(1)

    def dump_products_from_file(self, file_path: str, threads: int = 4):
        """
        Fetches the details from drugs listed on the output file of the generated Drug.dump() JSON

        Args:
            file_path (str): input file with the list of drugs
            threads (int, optional): number of simultaneous queries to ANVISAs website. Defaults to 4.
        """        
        asyncio.run(self._adump_products_from_file(file_path, threads))

    def dump(self, product_code: str):
        self.url = self.url + product_code
        response = asyncio.run(self._request())
        print(response)

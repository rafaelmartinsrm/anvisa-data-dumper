from .api import API
import os


class Drugs(API):
    """Drugs"""

    url = "https://consultas.anvisa.gov.br/api/consulta/medicamento/produtos/?"
    drugs = []
    cache_path = f"{os.getcwd()}/cache/drugs"
    default_filters = {
        "page": 1,
        "filter[periodoPublicacaoFinal]": "2022-04-30T03:00:00.000Z",
    }
    initial_filters = {}
    current_filters = {}

    def __init__(self, filters: dict = {}, cache: bool = True):
        """initialization

        Args:
            filters (dict, optional): _description_. Defaults to {}.
            cache (bool, optional): _description_. Defaults to True.
        """
        self.cache = cache

    def dump(self, format: str, output_file: str = "drugs") -> None:
        """dumps data

        Args:
            format (str): _description_
            output_file (str, optional): _description_. Defaults to "drugs".
        """
        if output_file == "drugs":
            output_file += "." + format

        is_last = False
        while not is_last:
            self.write_cache_file(
                data=self.current_filters, extension="current_filters"
            )

            response = self.request().json()

            if self.cache:
                self.write_cache_file(
                    data=response, extension=str(self.current_filters["page"])
                )

            is_last = response["last"]
            self.current_filters["page"] += 1

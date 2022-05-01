from .api import API
import os


class Drugs(API):
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
        self.cache = cache
        self.url = self.generate_request_url(filters=self.current_filters)

    def dump(self, format: str, output_file: str = "drugs") -> None:
        if output_file == "drugs":
            output_file += "." + format

        is_last = False
        while not is_last:
            self.write_cache_file(
                data=self.initial_filters, extension="current_filters"
            )

            response = self.request().json()

            if self.cache:
                self.write_cache_file(
                    data=response, extension=str(self.current_filters["page"])
                )

            is_last = response["last"]
            self.current_filters["page"] += 1

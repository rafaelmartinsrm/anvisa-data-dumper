import asyncio

from anvisa_data_dumper.drugs import DrugDetail, Drugs

# print(Drugs().dump(format="json"))
# asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
# asyncio.run(Drugs()._handle_request())


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
# Drugs().dump(threads=16)
# DrugDetail().dump_products_from_file(file_path="cache/drugs/1.json")
DrugDetail().dump_products_from_file(file_path="cache/drugs/2.json")
DrugDetail().dump_products_from_file(file_path="cache/drugs/3.json")

from anvisa_data_dumper.drugs import Drugs
import asyncio

# print(Drugs().dump(format="json"))
# asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
# asyncio.run(Drugs()._handle_request())


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(Drugs()._adump())

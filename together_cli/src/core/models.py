import requests
from rich.table import Table
from together_cli.src.utility import console
from together_cli.src.constants import MODEL_CONFIG

COMPUTER_ENDPOINT="https://computer.together.xyz"

def get_current_load():
    loads = {}
    current_load = requests.post(COMPUTER_ENDPOINT, json={"method":"together_getDepth", "id": "1"}, headers={"Content-Type": "application/json"}).json()['result']
    for model in MODEL_CONFIG:
        service_name = MODEL_CONFIG[model]['together_name']
        if service_name+"?" in current_load:
            queries = current_load[service_name+"?"]['num_bids']
            providers = current_load[service_name+"?"]['num_asks']
        else:
            queries = 0
            providers = 0
        if service_name+"?academic=" in current_load:
            academic_queries = current_load[service_name+"?academic="]['num_bids']
            academic_providers = current_load[service_name+"?academic="]['num_asks']
        else:
            academic_queries = 0
            academic_providers = 0
        loads[model] = {
            "queries": queries,
            "providers": providers,
            "academic_queries": academic_queries,
            "academic_providers": academic_providers
        }
    return loads


def pprint_models():
    table = Table(show_header=True, header_style="bold", title="Models")
    table.add_column("Name",)
    table.add_column("Queries")
    table.add_column("Providers")
    table.add_column("Academic Queries")
    table.add_column("Academic Providers")
    current_load = requests.post(COMPUTER_ENDPOINT, json={"method":"together_getDepth", "id": "1"}, headers={"Content-Type": "application/json"}).json()['result']
    
    for model in MODEL_CONFIG:
        name = model
        together_name = MODEL_CONFIG[model]['together_name']
        if together_name+"?" in current_load:
            queries = current_load[together_name+"?"]['num_bids']
            providers = current_load[together_name+"?"]['num_asks']
        else:
            queries = 0
            providers = 0
        if together_name+"?academic=" in current_load:
            academic_queries = current_load[together_name+"?academic="]['num_bids']
            academic_providers = current_load[together_name+"?academic="]['num_asks']
        else:
            academic_queries = 0
            academic_providers = 0
        table.add_row(name, str(queries), str(providers), str(academic_queries), str(academic_providers))
    console.print(table)
from colorama import Fore

from transfermarkt_analysis.db import create_tables, initialize_db


try:
    create_tables()
    initialize_db()
    print(Fore.GREEN + "Database Setup Is Done :)")
except Exception as err:
    raise err
from colorama import Fore

from transfermarkt_analysis.db.schema import create_tables


try:
    create_tables()
    print(Fore.GREEN + "Database successfully created :)")
except Exception as err:
    raise err
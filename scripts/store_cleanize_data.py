from colorama import Fore

from transfermarkt_analysis.crawl.cleanizers import store_cleanized_matches_dfs, store_cleanized_transfers_df


store_cleanized_transfers_df()
store_cleanized_matches_dfs()

print(Fore.GREEN + "store cleanized data is done :)")
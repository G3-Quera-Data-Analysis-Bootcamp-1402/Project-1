from time import sleep
from transfermarkt_analysis.crawl.match_crawler import multi_match_players_partion_crawler


multi_match_players_partion_crawler("player_appearances", 0, 2000, 100)
sleep(120)
multi_match_players_partion_crawler("player_appearances", 2000, 4000, 100)
sleep(120)
multi_match_players_partion_crawler("player_appearances", 4000, 6000, 100)
sleep(120)
multi_match_players_partion_crawler("player_appearances", 6000, 8000, 100)
sleep(120)
multi_match_players_partion_crawler("player_appearances", 8000, 10000, 100)
sleep(120)
multi_match_players_partion_crawler("player_appearances", 10000, 12000, 100)
sleep(120)
multi_match_players_partion_crawler("player_appearances", 12000, 12676, 135)
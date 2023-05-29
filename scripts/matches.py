from time import sleep
from transfermarkt_analysis.crawl.crawlers.match_crawler import multi_match_partion_crawler


multi_match_partion_crawler("pt1", 0, 2000, 100)
sleep(120)
multi_match_partion_crawler("pt2", 2000, 4000, 100)
sleep(120)
multi_match_partion_crawler("pt3", 4000, 6000, 100)
sleep(120)
multi_match_partion_crawler("pt4", 6000, 8000, 100)
sleep(120)
multi_match_partion_crawler("pt5", 8000, 10000, 100)
sleep(120)
multi_match_partion_crawler("pt6", 10000, 12000, 100)
sleep(120)
multi_match_partion_crawler("pt7", 12000, 12676, 135)
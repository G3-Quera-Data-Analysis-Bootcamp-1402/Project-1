from time import sleep
from transfermarkt_analysis.crawl.crawlers.appearances_crawler import multi_appearances_partion_crawler


multi_appearances_partion_crawler("appearances", 0, 2000, 50)
sleep(120)
multi_appearances_partion_crawler("appearances", 2000, 4000, 50)
sleep(120)
multi_appearances_partion_crawler("appearances", 4000, 6000, 50)
sleep(120)
multi_appearances_partion_crawler("appearances", 6000, 8000, 50)
sleep(120)
multi_appearances_partion_crawler("appearances", 8000, 10000, 50)
sleep(120)
multi_appearances_partion_crawler("appearances", 10000, 12000, 50)
sleep(120)
multi_appearances_partion_crawler("appearances", 12000, 12676, 135)
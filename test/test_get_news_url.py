from news_crawler import get_news_url_heavy, get_news_url_middle, get_news_url_light

keyword_list = ['삼성전자', '유한양행', '하이브']
keyword = keyword_list[0]
year_start = 2019
year_end = 2022


get_news_url_heavy(keyword, year_start, year_end)
# get_news_url_middle(keyword, year_start, year_end)
# get_news_url_light(keyword, year_start, year_end)

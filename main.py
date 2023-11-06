from news_crawler import get_content_from_url
from news_crawler import get_news_url_heavy, get_news_url_middle, get_news_url_light

keyword_list = ['대한항공', '삼성전자']
keyword = keyword_list[0]

get_content_from_url(keyword)

# for keyword in keyword_list:
#     get_news_content(keyword, year_start, year_end)

# --------------------------------
# folder_path = "하이브"  # 여기에 원하는 폴더 경로를 입력하세요.
# csv_data = read_csv_from_folder(folder_path)
#
#
# # 읽은 데이터 출력 (옵션)
# for key, value in csv_data.items():
#     print(f"File: {key}")
#     print(value.head())  # 상위 5개 데이터만 출력

# ----------------------------



keyword_list = ['삼성전자', '유한양행', '하이브']
keyword = keyword_list[0]
year_start = 2019
year_end = 2022


get_news_url_heavy(keyword, year_start, year_end)
# get_news_url_middle(keyword, year_start, year_end)
# get_news_url_light(keyword, year_start, year_end)

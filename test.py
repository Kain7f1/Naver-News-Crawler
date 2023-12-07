import utility_module as util
import crawling_tool as cr
from bs4 import BeautifulSoup

# search_keyword : 검색어
# created_date : 뉴스 생성 날짜 (YYYY-MM-DD 형식)
# created_time : 뉴스 생성 시간 (HH:MM:SS 형식)
# media : 언론사
# title : 뉴스 제목
# text : 뉴스 본문 text
# url : 뉴스 url

url_1 = "https://n.news.naver.com/mnews/article/087/0000158119?sid=102"
url_2 = "https://n.news.naver.com/mnews/article/215/0000491837?sid=101"
url_3 = "https://n.news.naver.com/mnews/article/032/0003256030?sid=101"

# soup = cr.get_soup(url_3)
# data_date_time = soup.select_one("div.media_end_head_info_datestamp_bunch").find('span')['data-date-time']
# created_date = data_date_time.split(" ")[0]
# created_time = data_date_time.split(" ")[1]
# media = soup.select_one("div.media_end_head_top a").find('img')['alt']
# title = soup.select_one("div.media_end_head_title").get_text(strip=True)
# text = soup.select_one("article#dic_area").get_text(strip=True)
#
# print(created_date)
# print(created_time)
# print(media)
# print(title)
# print(text)

##########
search_keyword = "금리"
cr.merge_text_temp_files(search_keyword)

#######################
# 합치기
# util.merge_csv_files(
#     save_file_name="logs_2",
#     read_folder_path_="./url/temp_logs")



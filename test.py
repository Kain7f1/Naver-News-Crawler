import utility_module as util
import crawling_tool as cr
from bs4 import BeautifulSoup

url_1 = "https://n.news.naver.com/mnews/article/087/0000158119?sid=102"
url_2 = "https://n.news.naver.com/mnews/article/215/0000491837?sid=101"
url_3 = "https://n.news.naver.com/mnews/article/032/0003256030?sid=101"

##########
search_keyword = "금리"
# cr.merge_text_temp_files(search_keyword)

#######################
# 합치기
# util.merge_csv_files(
#     save_file_name="logs_2",
#     read_folder_path_="./url/temp_logs")

##################
# 결손 데이터가 있는지 체크
# 예시 사용법
directory = "./text_1/temp_results"  # 'temp_results' 폴더 경로 지정
different_chunk_size_index = cr.find_different_chunk_size(directory)
print(different_chunk_size_index)


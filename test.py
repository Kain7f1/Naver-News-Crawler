from news_crawler import crawl_url_recursion, crawl_text, crawl_text_specifying_index
import utility_module as util
import crawling_tool as cr

##########
search_keyword = "금리"
cr.merge_text_temp_files(search_keyword)

#######################
# 합치기
# util.merge_csv_files(
#     save_file_name="logs_2",
#     read_folder_path_="./url/temp_logs")

##################
# 결손 데이터가 있는지 체크
# 예시 사용법
# directory = "./text_1/temp_results"  # 'temp_results' 폴더 경로 지정
# different_chunk_size_index = cr.find_different_chunk_size(directory)
# print(different_chunk_size_index)
#
#
# ###########################################
# # 수동 크롤링
# index_list = [61, 364, 551, 585, 658, 680, 793, 796, 804, 851, 852, 864]
# crawl_text_specifying_index(search_keyword, index_list)
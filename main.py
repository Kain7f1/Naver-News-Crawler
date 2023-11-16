from news_crawler import crawl_url, crawl_text
import utility_module as util
####################################################################################################
#                                             << 설정값 >>
keyword = "구리시"
start_date = "2023-11-08"
end_date = "2023-11-10"

####################################################################################################
#                                           << 실행하는 곳 >>
crawl_url(keyword, start_date, end_date)
# crawl_text(keyword)


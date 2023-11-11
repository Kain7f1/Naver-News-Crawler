from news_crawler import get_news_url, get_news_text
import utility_module as util
####################################################################################################
#                                             << 설정값 >>
keyword = "이"
start_date = "2021-01-01"
end_date = "2023-11-10"

####################################################################################################
#                                           << 실행하는 곳 >>
# get_news_url(keyword, start_date, end_date)
# get_news_text(keyword)


##########################################
# test
#######################################
#
# date = start_date
# keyword_unicode = util.convert_to_unicode(keyword)
# date_with_dots = date.replace('-', '.')  # 2023.11.10 형식
# date_no_dots = date.replace('-', '')  # 20231110 형식
# search_url = f"https://search.naver.com/search.naver?where=news&query={keyword_unicode}&sm=tab_opt&sort=2&photo=0&field=0&pd=3&ds={date_with_dots}&de={date_with_dots}&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Ar%2Cp%3Afrom{date_no_dots}to{date_no_dots}&is_sug_officeid=0&office_category=0&service_area=0"
# print(search_url)

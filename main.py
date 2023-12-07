from news_crawler import crawl_url_recursion, crawl_text

####################################################################################################
#                                             << 설정값 >>
search_keyword = "금리"
start_date = "2008-04-10"
end_date = "2023-10-19"

####################################################################################################
#                                           << 실행하는 곳 >>
# crawl_url_recursion(search_keyword, start_date, end_date)   # 뉴스 url을 크롤링
crawl_text(search_keyword)   # 뉴스 text를 크롤링

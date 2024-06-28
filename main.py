from news_crawler import crawl_url_recursion, crawl_text, crawl_text_recursion

####################################################################################################
#                                             << 설정값 >>
search_keyword = "축구"
start_date = "2023-04-10"
end_date = "2023-04-11"

####################################################################################################
#                                           << 실행하는 곳 >>
crawl_url_recursion(search_keyword, start_date, end_date)   # 뉴스 url을 크롤링
crawl_text_recursion(search_keyword)                        # 뉴스 text를 크롤링

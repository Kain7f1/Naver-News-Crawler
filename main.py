from news_crawler import crawl_url, crawl_text

####################################################################################################
#                                             << 설정값 >>
keyword = "금리"
start_date = "2008-07-17"
end_date = "2023-10-19"


def crawl_url_recursion():
    try:
        crawl_url(keyword, start_date, end_date)
    except:
        crawl_url_recursion()


####################################################################################################
#                                           << 실행하는 곳 >>
crawl_url_recursion()

# crawl_text(keyword)

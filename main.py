from news_crawler import get_news_url, get_news_text

keyword = "금리"
start_date = "2021-01-01"
end_date = "2023-11-10"
get_news_url(keyword, start_date, end_date)
get_news_text(keyword)
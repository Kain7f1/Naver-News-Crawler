from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import utility_module as util
import crawling_tool as cr
import pandas as pd
import requests
import os
import time


####################################################
# crawl_url()
# 기능 : keyword로 검색한 결과 뉴스의 url을 저장하는 함수
# 입력값 : search_keyword (검색어, 문자열), start_date (검색 시작 날짜, 문자열), end_date (검색 종료 날짜, 문자열)
def crawl_url(search_keyword, start_date, end_date):
    date_list = util.generate_date_list(start_date, end_date)   # 날짜 목록
    keyword_unicode = util.convert_to_unicode(search_keyword)  # 검색키워드의 유니코드 값
    row_list = []   # 크롤링 결과를 저장할 리스트
    columns = ['search_keyword', 'created_date', 'url']
    # [1. url 크롤링 : 하루 단위로]
    for date in date_list:
        print(f"[크롤링 시작] {date} {search_keyword}")
        # [설정값]
        date_having_dots = date.replace('-', '.')   # 2023.11.10 형식
        date_no_dots = date.replace('-', '')        # 20231110 형식
        maximum_page = 400  # 네이버는 400 * 10 = 4000개의 뉴스만 불러오기 때문에 설정한 값
        for index in range(0, maximum_page):
            page = 1 + (index * 10)
            search_url = f"https://search.naver.com/search.naver?where=news&sm=tab_pge&query={keyword_unicode}&sort=2&photo=0&field=0&pd=3&ds={date_having_dots}&de={date_having_dots}&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:r,p:from{date_no_dots}to{date_no_dots},a:all&start={page}"
            print(f"{search_keyword} / {date} / page {page} ~ {page+9} / {search_url}")

            soup = cr.get_soup(search_url)
            rows = cr.get_url_rows(soup, search_keyword, date)   # 크롤링 결과를 받아온다

            for new_row in rows:
                row_list.append(new_row)    # 크롤링 결과 저장

            if cr.is_not_exist_next_page(search_url):
                break   # 다음페이지가 없으면 다음 날짜로 넘어감

    # 결과 출력
    for index, row in enumerate(row_list):
        print(index, row)



def crawl_text(keyword):
    print(f"[ get_content_from_url({keyword}) ]")
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}
    # 파일 이름을 불러온다
    url_file_names = util.load_file_names(f'./{keyword}/url', endswith='url.csv')

    for url_file_name in url_file_names:
        content_file_name = f"{url_file_name[:-8]}_content.csv"
        print(f"[시작] : {url_file_name} 파일의 url로부터 {content_file_name} 파일을 만들겠습니다")

        # url 파일 불러오기
        df_url = util.read_file(f'./{keyword}/url', file_name=url_file_name)
        print(df_url.head())
        print(f"{url_file_name}의 데이터를 불러왔습니다")
        df_content = pd.DataFrame(columns=['date', 'url', 'content'])

        for index, row in df_url.iterrows():
            url = row['url']
            try:
                if url[:14] == 'https://sports':
                    continue
                # url로부터 content를 받아온다
                res = requests.get(url, headers=header)
                soup = BeautifulSoup(res.text, "html.parser")
                content = soup.select_one('article#dic_area').get_text(strip=True).replace("\n", " ")
                print(f'[{url_file_name} : {index}째 row]')
            except Exception as e:
                # url이 이상하면 건너뜀
                print("[error message] ", e)
                print("url : ", url)
                continue
            content = util.preprocess_content(content)  # 간단한 전처리
            new_row = [row['date'], url, content]
            df_content.loc[len(df_content)] = new_row

        # csv로 만든다
        util.create_folder(f'./{keyword}/content')
        util.save_file(df_content, f'./{keyword}/content', file_name=content_file_name)
        print(f"[종료] : {url_file_name} 파일의 url로부터 {content_file_name} 파일을 만들었습니다")

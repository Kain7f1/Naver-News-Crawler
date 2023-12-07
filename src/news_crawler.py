from bs4 import BeautifulSoup
from datetime import datetime
import utility_module as util
import crawling_tool as cr
import pandas as pd
import requests
import time

####################################################
# crawl_url()
# 기능 : keyword로 검색한 결과 뉴스의 url을 저장하는 함수
# 입력값 : search_keyword (검색어, 문자열), start_date (검색 시작 날짜, 문자열), end_date (검색 종료 날짜, 문자열)
def crawl_url(search_keyword, start_date, end_date):
    # [0-1. 기본 설정값]
    keyword_unicode = util.convert_to_unicode(search_keyword)  # 검색 키워드의 유니코드 값
    # 폴더 만들기
    util.create_folder(f"./url/temp_results")
    util.create_folder(f"./url/temp_logs")
    util.create_folder(f"./url/results")
    util.create_folder(f"./url/logs")

    # [0-2. 임시파일 폴더를 읽고, 파일이 있으면 진행된 부분부터 시작한다]
    if not util.is_folder_empty(f"./url/temp_results"):
        temp_date = util.find_date(folder_path="./url/temp_results", option="max")    # 가장 최근 날짜 (YYYYMMDD)
        latest_date = f"{temp_date[:4]}-{temp_date[4:6]}-{temp_date[6:]}"   # YYYY-MM-DD
        start_date = util.get_next_date(latest_date)    # 크롤링 시작할 날짜 설정 (되어있는 날의 다음 날 부터)
    date_list = util.generate_date_list(start_date, end_date)   # 날짜 목록

    # [1. url 크롤링 : 하루 단위로]
    for date in date_list:
        crawling_start_time = datetime.now().replace(microsecond=0)  # 크롤링 시작 시각
        print(f"[크롤링 시작] {date} {search_keyword}")
        # [1-1. 설정값]
        row_list = []    # 크롤링 결과를 저장할 리스트
        date_having_dots = date.replace('-', '.')   # 2023.11.10 형식
        date_no_dots = date.replace('-', '')        # 20231110 형식
        maximum_page = 400  # 네이버는 400 * 10 = 4000개의 뉴스만 불러오기 때문에 설정한 값
        # [1-2. 하루 단위로 크롤링]
        for index in range(maximum_page):
            # [설정값]
            page = 1 + (index * 10)
            search_url = f"https://search.naver.com/search.naver?where=news&sm=tab_pge&query={keyword_unicode}&sort=2&photo=0&field=0&pd=3&ds={date_having_dots}&de={date_having_dots}&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:r,p:from{date_no_dots}to{date_no_dots},a:all&start={page}"
            print(f"{search_keyword} / {date} / page {page} ~ {page+9} / {search_url}")

            # selenium으로 html을 가져오고, soup으로 파싱한다
            driver = cr.get_driver()
            driver.get(search_url)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            # [검색 결과가 없으면, 다음 날짜로 넘어감]
            if index == 0:
                if cr.is_no_result(soup):
                    break

            # [url 크롤링 및 저장]
            # soup = cr.get_soup(search_url)                       # bs로 html 받아오기
            rows = cr.get_url_rows(soup, search_keyword, date)   # 크롤링 결과를 받아온다
            for new_row in rows:
                row_list.append(new_row)

            # [다음 페이지가 없으면 다음 날짜로 넘어감]
            if cr.is_not_exist_next_page(driver):
                driver.quit()
                break
            else:
                driver.quit()

        crawling_end_time = datetime.now().replace(microsecond=0)  # 크롤링 종료 시각
        crawling_duration = round((crawling_end_time - crawling_start_time).total_seconds())  # 크롤링에 걸린 시간

        # [1-3. 하루 단위로 임시 파일, 로그 생성]
        cr.make_url_temp_results(row_list, date_no_dots, search_keyword)
        cr.make_url_temp_logs(row_list, date_no_dots, crawling_duration, search_keyword)

    # [2. 크롤링 결과 합치기]
    cr.merge_url_temp_results(search_keyword, start_date, end_date)

    # [3. 크롤링 로그 합치기]
    cr.merge_url_temp_logs(search_keyword, start_date, end_date)

    print(f"[크롤링 종료] {search_keyword} / {start_date} ~ {end_date}")


def crawl_url_recursion(search_keyword, start_date, end_date):
    try:
        crawl_url(search_keyword, start_date, end_date)
    except Exception:
        crawl_url_recursion(search_keyword, start_date, end_date)


#################################
# - results 파일 columns
# search_keyword : 검색어
# created_date : 뉴스 생성 날짜 (YYYY-MM-DD 형식)
# created_time : 뉴스 생성 시간 (HH:MM:SS 형식)
# media : 언론사
# title : 뉴스 제목
# text : 뉴스 본문 text
# url : 뉴스 url

# - logs 파일 columns
# crawler_type : 크롤러 타입 (naver_news_text_craler)
# search_keyword : 검색어
# url_count : 입력받은 url 개수
# text_count : 수집된 text 정보 개수
# error_count : 오류 발생한 row 개수
# crawling_duration : 크롤링에 걸린 시간

# - errors 파일 columns
# crawler_type : 크롤러 타입 (naver_news_text_craler)
# created_date : 에러가 발생한 뉴스가 만들어진 날짜. 특정 날짜를 기점으로 html 형식이 바뀐 경우도 있기 때문에 수집한다.
# error_message : 에러 메세지
# url : 에러가 발생한 뉴스 url
def crawl_text(search_keyword):
    # [0. 설정값]
    url_files = util.read_files(folder_path=f"./url/results", keyword=f"_{search_keyword}_")
    if len(url_files) == 0:
        print("키워드에 맞는 파일이 존재하지 않습니다.")
        return -1
    url_file_name = url_files[0]   # 키워드가 포함된 첫번째 파일 이름
    print(f"사용할 파일 명 : {url_file_name}")
    df_url = pd.read_csv(filepath_or_buffer=f"./url/results/{url_file_name}", encoding="utf-8")
    print(f"데이터의 길이 : {len(df_url)}")
    print(f"[네이버 뉴스 text 크롤링을 시작하겠습니다] search_keyword : {search_keyword}")
    time.sleep(5)

    # [1. text 크롤링]
    # for url_file_name in url_file_names:
    #     content_file_name = f"{url_file_name[:-8]}_content.csv"
    #     print(f"[시작] : {url_file_name} 파일의 url로부터 {content_file_name} 파일을 만들겠습니다")
    #
    #     # url 파일 불러오기
    #     df_url = util.read_file(f'./{keyword}/url', file_name=url_file_name)
    #     print(df_url.head())
    #     print(f"{url_file_name}의 데이터를 불러왔습니다")
    #     df_content = pd.DataFrame(columns=['date', 'url', 'content'])
    #
    #     for index, row in df_url.iterrows():
    #         url = row['url']
    #         try:
    #             if url[:14] == 'https://sports':
    #                 continue
    #             # url로부터 content를 받아온다
    #             res = requests.get(url, headers=header)
    #             soup = BeautifulSoup(res.text, "html.parser")
    #             content = soup.select_one('article#dic_area').get_text(strip=True).replace("\n", " ")
    #             print(f'[{url_file_name} : {index}째 row]')
    #         except Exception as e:
    #             # url이 이상하면 건너뜀
    #             print("[error message] ", e)
    #             print("url : ", url)
    #             continue
    #         content = util.preprocess_content(content)  # 간단한 전처리
    #         new_row = [row['date'], url, content]
    #         df_content.loc[len(df_content)] = new_row
    #
    #     # csv로 만든다
    #     util.create_folder(f'./{keyword}/content')
    #     util.save_file(df_content, f'./{keyword}/content', file_name=content_file_name)
    #     print(f"[종료] : {url_file_name} 파일의 url로부터 {content_file_name} 파일을 만들었습니다")

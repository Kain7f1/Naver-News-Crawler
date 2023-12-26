from bs4 import BeautifulSoup
from datetime import datetime
import utility_module as util
import crawling_tool as cr
import pandas as pd
import time
import traceback

# 전역변수 SHUNK_SIZE : crawl_text() 에서 데이터를 끊을 단위
CHUNK_SIZE = 1000


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
    if not util.is_folder_empty(f"./url/temp_logs"):
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
def crawl_text(search_keyword, chunk_size=CHUNK_SIZE):
    # [0-1. 설정값, 폴더 만들기]
    crawler_type = "naver_news_text_crawler"
    cr.create_text_folder()

    # [0-2. url results 파일 체크]
    url_files = util.read_files(folder_path=f"./url/results", keyword=f"_{search_keyword}_")  # 폴더 내 파일 있는지 확인
    if len(url_files) == 0:
        return "입력 키워드에 맞는 파일이 존재하지 않습니다"
    url_file_name = url_files[0]   # 키워드가 포함된 첫번째 파일 이름
    print(f"[사용할 파일 명 : {url_file_name}]")
    df_url = pd.read_csv(filepath_or_buffer=f"./url/results/{url_file_name}", encoding="utf-8")  # 파일을 df로 읽어오기
    url_row_count = len(df_url)
    if url_row_count == 0:
        return "url 파일에 저장된 데이터가 없습니다"
    sub_dfs = util.split_df_into_sub_dfs(df_url, chunk_size=chunk_size)    # df를 chunk_size 단위로 쪼갬
    print(f"[데이터를 sub_df 단위로 쪼갰습니다. sub_df의 수 : {len(sub_dfs)}]")

    # [0-3. text 임시파일 체크]
    # temp_logs 임시파일 기준으로, 진행도를 체크한다.
    done_index = util.get_done_index(keyword=f"{search_keyword}", folder_path="./text/temp_logs")  # 마지막으로 작업한 파일 번호
    print(f"[크롤링 진행도 : {(done_index+1)*chunk_size}/{url_row_count}]")
    print(f"[네이버 뉴스 text 크롤링을 시작하겠습니다] search_keyword : {search_keyword}")
    time.sleep(1)

    # [1. text 크롤링 : sub_dfs 단위로]
    for sub_df_index in range(len(sub_dfs)):
        crawling_start_time = datetime.now().replace(microsecond=0)  # 시작 시각 : 실행 시간을 잴 때 사용

        # [1-1. news text 받아오기]
        if sub_df_index <= done_index:  # 작업했던 파일이 존재하면, 다음 것부터 시작한다
            continue
        sub_df = sub_dfs[sub_df_index]  # 작업할 단위 설정 : sub_df
        sub_df_results = []             # 데이터를 저장할 공간 : sub_df_results
        sub_df_errors = []              # 에러 정보를 저장할 공간 : sub_df_errors
        for index, url_row in sub_df.iterrows():
            # [sub_df에서, url_row 1개씩 읽어온다]
            try:
                print(f"[{sub_df_index * chunk_size + index + 1}/{url_row_count}] 본문 페이지 : {url_row['url']}")
                soup = cr.get_soup(url_row['url'])  # url을 Beatifulsoup를 사용하여 읽어온다
                new_row = cr.get_news_row(url_row, soup)  # 본문 정보 크롤링
                sub_df_results.append(new_row)  # sub_df_results에 크롤링한 정보 저장
                print("- 본문 정보를 추가했습니다 : ", new_row[-2])
            except Exception as e:
                print("[에러 발생 : 1-1. news text 받아오기]", e)
                error_info = traceback.format_exc()
                sub_df_errors.append([crawler_type, url_row['created_date'], error_info, url_row['url']])
        # logs 정보 저장
        crawling_end_time = datetime.now().replace(microsecond=0)  # 종료 시각
        crawling_duration = round((crawling_end_time - crawling_start_time).total_seconds())  # 크롤링에 걸린 시간
        sub_df_logs = [[crawler_type, search_keyword, len(sub_df_results), len(sub_df_errors), crawling_duration]]

        # [1-2. 임시 파일 저장]
        cr.save_text_temp_files(search_keyword, sub_df_index, sub_df_results, sub_df_logs, sub_df_errors)

    # [2. 임시 파일 합치기]
    cr.merge_text_temp_files(search_keyword)

    print(f"[크롤링 종료] {search_keyword}")


###########################################
def crawl_text_recursion(search_keyword):
    try:
        crawl_text(search_keyword)
    except Exception:
        crawl_text_recursion(search_keyword)


#################################################
# sub_df 인덱스를 지정하여, 그 부분한 크롤링한다
# 크롤링 결과 데이터가 불완전활 때, 그 부분만 수동으로 크롤링하는 함수이다
def crawl_text_specifying_index(search_keyword, index_list, chunk_size=CHUNK_SIZE):
    # [0-1. 설정값, 폴더 만들기]
    crawler_type = "naver_news_text_crawler"
    cr.create_text_folder()

    # [0-2. url results 파일 체크]
    url_files = util.read_files(folder_path=f"./url/results", keyword=f"_{search_keyword}_")  # 폴더 내 파일 있는지 확인
    if len(url_files) == 0:
        return "입력 키워드에 맞는 파일이 존재하지 않습니다"
    url_file_name = url_files[0]  # 키워드가 포함된 첫번째 파일 이름
    print(f"[사용할 파일 명 : {url_file_name}]")
    df_url = pd.read_csv(filepath_or_buffer=f"./url/results/{url_file_name}", encoding="utf-8")  # 파일을 df로 읽어오기
    url_row_count = len(df_url)
    if url_row_count == 0:
        return "url 파일에 저장된 데이터가 없습니다"
    sub_dfs = util.split_df_into_sub_dfs(df_url, chunk_size=chunk_size)  # df를 chunk_size 단위로 쪼갬
    print(f"[데이터를 sub_df 단위로 쪼갰습니다. sub_df의 수 : {len(sub_dfs)}]")

    # [0-3. text 임시파일 체크]
    # temp_logs 임시파일 기준으로, 진행도를 체크한다.
    print(f"[네이버 뉴스 text 크롤링을 시작하겠습니다] search_keyword : {search_keyword}")
    time.sleep(1)

    # [1. text 크롤링 : sub_dfs 단위로]
    for sub_df_index in index_list:
        crawling_start_time = datetime.now().replace(microsecond=0)  # 시작 시각 : 실행 시간을 잴 때 사용
        sub_df = sub_dfs[sub_df_index]  # 작업할 단위 설정 : sub_df
        sub_df_results = []  # 데이터를 저장할 공간 : sub_df_results
        sub_df_errors = []  # 에러 정보를 저장할 공간 : sub_df_errors
        for index, url_row in sub_df.iterrows():
            # [sub_df에서, url_row 1개씩 읽어온다]
            try:
                print(f"[{sub_df_index * chunk_size + index + 1}/{url_row_count}] 본문 페이지 : {url_row['url']}")
                soup = cr.get_soup(url_row['url'])  # url을 Beatifulsoup를 사용하여 읽어온다
                new_row = cr.get_news_row(url_row, soup)  # 본문 정보 크롤링
                sub_df_results.append(new_row)  # sub_df_results에 크롤링한 정보 저장
                print("- 본문 정보를 추가했습니다 : ", new_row[-2])
            except Exception as e:
                print("[에러 발생 : 1-1. news text 받아오기]", e)
                error_info = traceback.format_exc()
                sub_df_errors.append([crawler_type, url_row['created_date'], error_info, url_row['url']])
        # logs 정보 저장
        crawling_end_time = datetime.now().replace(microsecond=0)  # 종료 시각
        crawling_duration = round((crawling_end_time - crawling_start_time).total_seconds())  # 크롤링에 걸린 시간
        sub_df_logs = [[crawler_type, search_keyword, len(sub_df_results), len(sub_df_errors), crawling_duration]]

        # [1-2. 임시 파일 저장]
        cr.save_text_temp_files(search_keyword, sub_df_index, sub_df_results, sub_df_logs, sub_df_errors)
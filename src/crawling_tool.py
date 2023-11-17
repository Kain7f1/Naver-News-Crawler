from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import utility_module as util
import pandas as pd
import requests
import time


#############################################################################
#                                 << 설정값 >>
# dcinside 헤더 :  dcinside 봇 차단을 위한 헤더 설정
headers_naver = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "sec-ch-ua-mobile": "?0",
        "DNT": "1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ko-KR,ko;q=0.9"
    }

# 목적에 맞는 헤더를 설정한다
headers = headers_naver


###############################################################################
#                                 << 함수들 >>                                 #
###############################################################################
# get_driver()
# 사용 전제 조건 : Users 폴더에 버전에 맞는 chromedriver.exe를 다운받아주세요
# 기능 : driver를 반환합니다
# 리턴값 : driver
def get_driver():
    CHROME_DRIVER_PATH = "C:/Users/chromedriver.exe"    # (절대경로) Users 폴더에 chromedriver.exe에 설치해주세요
    options = Options()                                 # 옵션 선언
    # [옵션 설정]
    options.page_load_strategy = 'eager'                # 페이지 로드 전략 조정 : 페이지가 완전히 로드되기를 기다리지 않음
    options.headless = True                             # GUI 없이 브라우저를 백그라운드에서 실행
    options.add_argument("--disable-javascript")        # 자바스크립트 비활성화
    options.add_argument("--headless")                  # 창 없이 크롬이 실행
    options.add_argument("disable-infobars")            # 안내바가 없이 열리게 한다.
    options.add_argument("--disable-gpu")                 # GPU 가속 비활성화
    options.add_argument("--disable-dev-shm-usage")     # 공유메모리 사용 억제
    options.add_argument('--log-level=3')               # 웹 소켓을 통한 로그 메시지 비활성화
    options.add_argument('--no-sandbox')                # 브라우저 프로파일링 비활성화
    options.add_argument('--disable-plugins')           # 다양한 플러그인 및 기능 비활성화
    options.add_argument('--disable-extensions')        # 다양한 플러그인 및 기능 비활성화
    options.add_argument('--disable-sync')              # 다양한 플러그인 및 기능 비활성화
    options.add_argument("--blink-settings=imagesEnabled=false")      # 이미지 로딩 비활성화
    options.add_argument('--disk-cache-dir=/path/to/cache-dir')       # 캐시 사용 활성화
    options.add_argument("--disable-background-timer-throttling")     # 백그라운드 프로세스 제한
    prefs = {"profile.managed_default_content_settings.images": 2}    # 설정 정의 : 이미지 로딩 비활성화
    options.add_experimental_option("prefs", prefs)             # 이미지 로딩 비활성화
    driver = webdriver.Chrome(CHROME_DRIVER_PATH, options=options)
    return driver


#############################################################################
# get_soup()
# 기능 : url을 받아 requests를 사용하여 soup를 리턴하는 함수입니다
# 특징 : 오류발생 시 재귀하기 때문에, 성공적으로 soup를 받아올 수 있습니다.
def get_soup(url, time_sleep=0, max_retries=600):
    try:
        if max_retries <= 0:
            print("[최대 재시도 횟수 초과 : get_soup()]")
            return None
        with requests.Session() as session:
            response = session.get(url, headers=headers)
            time.sleep(time_sleep)
        soup = BeautifulSoup(response.text, "html.parser")
        if len(soup) == 0:  # 불러오는데 실패하면
            print(f"[soup 로딩 실패, 반복] [get_soup(time_sleep=1)]")
            soup = get_soup(url, 1)
    except Exception as e:
        print(f"[오류 발생, 반복] [get_soup(time_sleep=1)] ", e)
        soup = get_soup(url, 1, max_retries-1)
    return soup


##################################################################
# get_naver_news_url()
# 기능 : 네이버뉴스이면, url을 받아온다
# [param] 기사 1개의 soup_box
# [return] 네이버뉴스이면 url, 네이버뉴스가 아니면 None
def get_naver_news_url(soup_box):
    try:
        a_list = soup_box.select('div.info_group a')
        if len(a_list) != 2:    # "네이버뉴스" 버튼이 있으면, a_list의 길이가 2이다.
            # print("네이버뉴스가 아닙니다")
            return None
        else:
            url = a_list[1]["href"]
            print(f"url : {url}")
            # print("네이버뉴스 입니다")
            return url
    except Exception as e:
        print("네이버뉴스가 아닙니다", e)
        return None


#############################
# is_no_result()
# 기능 : 검색 결과가 존재하는지 체크한다 (1번째 페이지에서만 사용한다)
# [param] url
# [return] 결과가 없으면 True, 존재하면 False
def is_no_result(soup):
    try:
        # 검색 결과가 없을 때, script_text 는 var nx_cr_area_info = []; 이다
        script_text = soup.select_one("div.main_pack script").get_text(strip=True)
        if script_text[-3:] == "[];":
            print("[검색 결과가 없습니다]")
            return True
        else:
            print("[검색 결과가 존재합니다]")
            return False

    except Exception as e:
        print("[검색 결과 x]", e)
        return True


##################################################################
# 기능 : 다음 페이지가 없으면 True 리턴
def is_not_exist_next_page(driver, time_sleep=0, max_retries=5):
    try:
        if max_retries <= 0:
            return True

        # [다음 페이지가 존재하는지 검사한다]
        next_page_button = driver.find_element(By.XPATH, '//*[@id="main_pack"]/div[2]/div/a[2]')  # 다음 page 버튼
        if next_page_button.get_attribute("aria-disabled") == "true":
            print('[다음 페이지가 존재하지 않습니다, 다음 날짜로 넘어갑니다]')
            return True

        elif next_page_button.get_attribute("aria-disabled") == "false":
            print('[다음 페이지가 존재합니다]')
            return False

    except Exception as e:
        print(f"[오류] is_not_exist_next_page(time_sleep={time_sleep}) ", e)
        is_exist = is_not_exist_next_page(driver, time_sleep+1, max_retries-1)
        return is_exist


##################################################################
# get_url_row()
# 기능 : url크롤러에서 크롤링한 결과를 row로 만들어 반환한다.
# [param 1] 검색결과 soup
# [param 2] 뉴스 검색 날짜 (뉴스가 만들어진 날짜)
# [return 1] row : 크롤링한 결과 row의 리스트
def get_url_rows(soup, keyword, date):
    rows = []
    soup_box_list = soup.select("ul.list_news li.bx")  # 뉴스 box 리스트

    for soup_box in soup_box_list:
        url = get_naver_news_url(soup_box)  # [url 크롤링]
        if url is None:
            continue    # [네이버뉴스가 아니면, 스킵]
        new_row = [keyword, date, url]
        rows.append(new_row)

    return rows


###################################################################
def make_url_temp_results(row_list, date_no_dots, search_keyword):
    columns = ['search_keyword', 'created_date', 'url']     # 결과로 만들 df의 칼럼
    df_temp_results = pd.DataFrame(row_list, columns=columns)
    temp_results_path = (f"./url/temp_results/"
                         f"{date_no_dots}_temp_results_{search_keyword}.csv")  # 임시 파일 경로
    df_temp_results.to_csv(temp_results_path, encoding='utf-8', index=False)   # 임시 파일 저장


###################################################################
def make_url_temp_logs(row_list, date_no_dots, crawling_duration, search_keyword):
    columns = ['crawler_type', 'search_keyword', 'row_count', 'crawling_duration']   # 결과로 만들 df의 칼럼
    crawler_type = "naver_news_url_craler"
    row_count = len(row_list)
    logs = [[crawler_type, search_keyword, row_count, crawling_duration]]
    df_temp_logs = pd.DataFrame(logs, columns=columns)
    temp_logs_path = (f"./url/temp_logs/"
                      f"{date_no_dots}_temp_logs_{search_keyword}.csv")  # 임시 파일 경로
    df_temp_logs.to_csv(temp_logs_path, encoding='utf-8', index=False)   # 임시 파일 저장


###############################################################
# 기능 : url temp_results를 합쳐 하나의 파일로 만들고, 임시 파일을 없앤다
def merge_url_temp_results(search_keyword, start_date, end_date):
    # 설정값
    start_date = start_date.replace("-", "")
    end_date = end_date.replace("-", "")
    results_file_name = f"url_results_{search_keyword}_{start_date}_{end_date}"

    # 데이터를 병합하고, 하나의 파일로 만든다
    util.merge_csv_files(
        save_file_name=results_file_name,
        read_folder_path_="./url/temp_results",
        save_folder_path_="./url/results",
        keyword=f"_{search_keyword}"
    )
    # 임시파일 삭제
    util.delete_files(folder_path="./url/temp_results", keyword=f"_{search_keyword}")


###############################################################
# 기능 : url temp_logs를 합쳐 하나의 파일로 만든다
def merge_url_temp_logs(search_keyword, start_date, end_date):
    # 설정값
    start_date = start_date.replace("-", "")
    end_date = end_date.replace("-", "")
    log_files = util.read_files(
        folder_path="./url/temp_logs",
        keyword=f"_{search_keyword}",
        endswith='.csv'
    )
    # 데이터를 하나로 병합한다
    log_file_paths = []
    for log_file in log_files:
        log_file_paths.append(f"./url/temp_logs/{log_file}")
    merged_df = util.sum_dataframes(log_file_paths, encoding='utf-8')    # int값은 더하여 logs를 합친다.

    # 파일로 저장한다
    logs_file_name = f"url_logs_{search_keyword}_{start_date}_{end_date}"
    save_file_path = f"./url/logs/{logs_file_name}.csv"
    merged_df.to_csv(save_file_path, encoding='ANSI', index=False)   # 합친 df를 csv로 만든다

    # delete_files(folder_path="./url/temp_logs", keyword=f"_{search_keyword}")   # logs 임시파일 삭제

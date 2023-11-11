from datetime import datetime, timedelta
from selenium import webdriver
import utility_module as util
import pandas as pd
import os


###############################################################################
#                                 << 함수들 >>                                 #
###############################################################################
# get_driver()
# 사용 전제 조건 : Users 폴더에 버전에 맞는 chromedriver.exe를 다운받아주세요
# 기능 : driver를 반환합니다
# 리턴값 : driver
def get_driver():
    CHROME_DRIVER_PATH = "C:/Users/chromedriver.exe"    # (절대경로) Users 폴더에 chromedriver.exe를 설치했음
    options = webdriver.ChromeOptions()                 # 옵션 선언
    # [옵션 설정]
    # options.add_argument("--start-maximized")         # 창이 최대화 되도록 열리게 한다.
    options.add_argument("--headless")                  # 창이 없이 크롬이 실행이 되도록 만든다
    options.add_argument("disable-infobars")            # 안내바가 없이 열리게 한다.
    options.add_argument("disable-gpu")                 # 크롤링 실행시 GPU를 사용하지 않게 한다.
    options.add_argument("--disable-dev-shm-usage")     # 공유메모리를 사용하지 않는다
    options.add_argument("--blink-settings=imagesEnabled=false")    # 이미지 로딩 비활성화
    options.add_argument('--disk-cache-dir=/path/to/cache-dir')     # 캐시 사용 활성화
    options.page_load_strategy = 'none'             # 전체 페이지가 완전히 로드되기를 기다리지 않고 다음 작업을 수행 (중요)
    options.add_argument('--log-level=3')           # 웹 소켓을 통한 로그 메시지 비활성화
    options.add_argument('--no-sandbox')            # 브라우저 프로파일링 비활성화
    options.add_argument('--disable-plugins')       # 다양한 플러그인 및 기능 비활성화
    options.add_argument('--disable-extensions')    # 다양한 플러그인 및 기능 비활성화
    options.add_argument('--disable-sync')          # 다양한 플러그인 및 기능 비활성화
    driver = webdriver.Chrome(CHROME_DRIVER_PATH, options=options)
    return driver


#############################################################################
# generate_date_list()
# 기능 : 시작 날짜와 종료 날짜를 포함하여 두 날짜 사이의 모든 날짜를 문자열 리스트로 반환한다
# [param] start_date: 시작 날짜 (YYYY-MM-DD 형식)
# [param] end_date: 종료 날짜 (YYYY-MM-DD 형식)
# [return] 두 날짜 사이의 날짜를 포함한 문자열 리스트
def generate_date_list(start_date, end_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    date_list = []

    while start <= end:
        date_list.append(start.strftime("%Y-%m-%d"))
        start += timedelta(days=1)

    return date_list

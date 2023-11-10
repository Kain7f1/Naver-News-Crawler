from selenium import webdriver
import utility_module as util
import pandas as pd
import os


# 크롤링한 url 데이터를 csv로 만든다
# 입력값 : ['date', 'url'] 형식의 2차원 리스트
def save_url_file(keyword, year, data_list):
    folder_path = f'./{keyword}/url'
    util.create_folder(folder_path)
    # 크롤링 데이터 확인
    print(f'{year}년 data_list의 길이 : ', len(data_list))
    columns = ['date', 'url']  # 열 이름
    df = pd.DataFrame(data_list, columns=columns)  # DataFrame 생성
    print(df.tail())  # 결과 확인
    file_path = os.path.join(folder_path, f"{keyword}_{year}_url.csv")
    df.to_csv(file_path, encoding='utf-8', index=False)


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
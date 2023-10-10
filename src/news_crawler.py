# --------------------------------------
# 파이참에 이거 인스톨 해야됨!
# --------------------------------------
# selenium, bs4, webdriver_manager, pandas
# --------------------------------------
import utility_module as util

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup
import pandas as pd
import requests
import os
import time


# - 목적 : 뉴스 url을 전부 긁어오는 코드
# - 입력값 : keyword, year_start, year_end
# - 출력값 : DataFrame형식 - [’date’, ’url’]
# - 기능 : 뉴스의 url을 모아 csv로 저장, 1년단위, 네이버 keyword 검색결과 뉴스
def get_news_url_light(keyword, year_start, year_end):
    folder_path = f"./{keyword}"
    util.create_folder(folder_path)
    year_list = [str(y) for y in range(year_start, year_end + 1)]
    month_list = [f"{m:02d}" for m in range(1, 12 + 1)]

    for year in year_list:
        data_list = []  # 크롤링 데이터 저장 [’date’, ’url’]
        error_log = []  # 에러 로그 저장 [’date’, ’error’]
        for month in month_list:
            ds = f'{year}.{month}.01'  # date start
            de = util.get_last_date(ds)  # date end
            try:
                print(f'{ds}에서 {de}까지 크롤링 합니다')
                ds_nodot = ds.replace('.', '')  # "." 지운거
                de_nodot = de.replace('.', '')  # "." 지운거
                search_url = f'https://search.naver.com/search.naver?where=news&sm=tab_pge&query={keyword}&sort=2&photo=0&field=0&pd=3&ds={ds}&de={de}&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:dd,p:from{ds_nodot}to{de_nodot}'
                driver = get_driver(search_url)
            except Exception as e:
                print('[driver 오류] ', e)
                error_log.append([ds, e])
                time.sleep(1)
                continue

            # url 크롤링
            for page in range(1, 400+1):
                if page == 400:
                    error_message = f"page 한계치에 도달했습니다 (page : {page})"
                    print(error_message)
                    error_log.append([ds, error_message])
                    break
                print('현재 페이지 : ', page)
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')

                # 페이지의 데이터 받아오기 : data_list 에 추가
                try:
                    soup_list = soup.select("ul.list_news div.info_group")  # 여기 수정
                    for element in soup_list:
                        date = element.select('span.info')[-1].get_text(strip=True)
                        a_tags = element.find_all('a')
                        if len(a_tags) == 2:
                            url = a_tags[1]['href']
                            new_row = [date, url]
                            data_list.append(new_row)
                            print(f'{keyword} {len(data_list)}번째 row : {new_row}')
                        else:
                            continue

                except Exception as e:
                    print('[bs4 데이터 받아오기 오류] ', e)
                    error_log.append([ds, e])
                    break

                # 페이지 이동
                try:
                    next_page_button = driver.find_element(By.XPATH,
                                                           '//*[@id="main_pack"]/div[2]/div/a[2]')  # [>] 모양 버튼, 다음페이지로 이동한다
                    if next_page_button.get_attribute("aria-disabled") == "true":
                        # 다음 페이지가 없으면
                        print(f'{year}.{month} 다음 페이지가 존재하지 않습니다. 크롤링을 종료합니다')
                        break
                    elif next_page_button.get_attribute("aria-disabled") == "false":
                        print('다음 페이지로 이동합니다')
                        next_page_button.click()  # 다음 페이지로 이동
                    else:
                        print('[페이지 이동 에러] else')
                        break
                except Exception as e:
                    print('[페이지 이동 에러] ', e)
                    error_log.append([ds, e])
                    break

        save_url_file(keyword, year, data_list)     # 1년 단위 데이터 csv로 만든다

        # error 발생했는지 확인
        if len(error_log) > 0:
            print("error는 발생 log 입니다")
            for date, error in error_log:
                print(date, error)
            df_error = pd.DataFrame(error_log, columns=['date', 'error'])
            error_file_path = os.path.join(folder_path, f"{keyword}_{year}_error.csv")
            df_error.to_csv(error_file_path, encoding='utf-8', index=False)
            print("error는 발생 log 를 파일로 저장했습니다")
        else:
            print("error는 발생하지 않았습니다")

    print('get_news_url_heavy()를 종료합니다')


def get_news_url_middle(keyword, year_start, year_end):
    folder_path = f"./{keyword}"
    util.create_folder(folder_path)
    year_list = [str(y) for y in range(year_start, year_end + 1)]
    month_list = [f"{m:02d}" for m in range(1, 12 + 1)]
    for year in year_list:
        data_list = []  # 크롤링 데이터 저장 [’date’, ’url’]
        error_log = []  # 에러 로그 저장 [’date’, ’error’]
        for month in month_list:
            date_list = util.make_date_range(year, month)    # 3일 단위로 나눔
            for ds, de in date_list:  # day : 1~last day
                try:
                    print(f'{ds}에서 {de}까지 크롤링 합니다')
                    ds_nodot = ds.replace('.', '')  # "." 지운거
                    de_nodot = de.replace('.', '')  # "." 지운거
                    search_url = f'https://search.naver.com/search.naver?where=news&sm=tab_pge&query={keyword}&sort=2&photo=0&field=0&pd=3&ds={ds}&de={de}&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:dd,p:from{ds_nodot}to{de_nodot}'
                    driver = get_driver(search_url)
                except Exception as e:
                    print('[driver 오류] ', e)
                    error_log.append([ds, e])
                    time.sleep(1)
                    continue
                # url 크롤링
                for page in range(1, 100+1):
                    print('현재 페이지 : ', page)
                    if page == 100:
                        error_message = f"page 한계치에 도달했습니다 (page : {page})"
                        print(error_message)
                        error_log.append([ds, error_message])
                        break
                    html = driver.page_source
                    soup = BeautifulSoup(html, 'html.parser')
                    # 페이지의 데이터 받아오기 : data_list 에 추가
                    try:
                        soup_list = soup.select("ul.list_news div.info_group")  # 여기 수정
                        for element in soup_list:
                            date = element.select('span.info')[-1].get_text(strip=True)
                            a_tags = element.find_all('a')
                            if len(a_tags) == 2:
                                url = a_tags[1]['href']
                                new_row = [date, url]
                                data_list.append(new_row)
                                print(f'{keyword} {len(data_list)}번째 row : {new_row}')
                            else:
                                continue

                    except Exception as e:
                        print('[페이지 데이터 받아오기 오류] ', e)
                        error_log.append([ds, e])
                        break

                    # 페이지 이동
                    try:
                        next_page_button = driver.find_element(By.XPATH,
                                                               '//*[@id="main_pack"]/div[2]/div/a[2]')  # [>] 모양 버튼, 다음페이지로 이동한다
                        if next_page_button.get_attribute("aria-disabled") == "true":
                            # 다음 페이지가 없으면
                            print('다음 페이지가 존재하지 않습니다. 크롤링을 종료합니다')
                            break
                        elif next_page_button.get_attribute("aria-disabled") == "false":
                            print('다음 페이지로 이동합니다')
                            next_page_button.click()  # 다음 페이지로 이동
                        else:
                            print('[페이지 이동 에러] else')
                            break
                    except Exception as e:
                        print('[페이지 이동 에러] ', e)
                        error_log.append([ds, e])
                        break

        save_url_file(keyword, year, data_list)     # 1년 단위 데이터 csv로 만든다

        # error 발생했는지 확인
        if len(error_log) > 0:
            print("error는 발생 log 입니다")
            for date, error in error_log:
                print(date, error)
            df_error = pd.DataFrame(error_log, columns=['date', 'error'])
            error_file_path = os.path.join(folder_path, f"{keyword}_{year}_error.csv")
            df_error.to_csv(error_file_path, encoding='utf-8', index=False)
            print("error는 발생 log 를 파일로 저장했습니다")
        else:
            print("error는 발생하지 않았습니다")

    print('get_news_url_middle()를 종료합니다')


def get_news_url_heavy(keyword, year_start, year_end):
    folder_path = f"./{keyword}"
    util.create_folder(folder_path)
    year_list = [str(y) for y in range(year_start, year_end + 1)]
    month_list = [f"{m:02d}" for m in range(1, 12 + 1)]
    for year in year_list:
        data_list = []  # 크롤링 데이터 저장 [’date’, ’url’]
        error_log = []  # 에러 로그 저장 [’date’, ’error’]
        for month in month_list:
            temp_ds = f'{year}.{month}.01'  # date start
            temp_de = util.get_last_date(temp_ds)  # date end
            last_day = int(temp_de[-2:])
            for day in range(1, last_day + 1):  # day : 1~last day
                date = f'{year}.{month}.{day:02d}'
                print(f'{keyword} : {date}의 크롤링 진행')
                try:
                    date_nodot = date.replace('.', '')  # "." 지운거
                    search_url = f'https://search.naver.com/search.naver?where=news&sm=tab_pge&query={keyword}&sort=2&photo=0&field=0&pd=3&ds={date}&de={date}&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:dd,p:from{date_nodot}to{date_nodot}'
                    driver = get_driver(search_url)
                except Exception as e:
                    print('[driver 오류] ', e)
                    error_log.append([date, e])
                    time.sleep(1)
                    continue
                # url 크롤링
                for page in range(1, 100+1):
                    print('현재 페이지 : ', page)
                    if page == 100:
                        error_message = f"page 한계치에 도달했습니다 (page : {page})"
                        print(error_message)
                        error_log.append([date, error_message])
                        break
                    html = driver.page_source
                    soup = BeautifulSoup(html, 'html.parser')
                    # 페이지의 데이터 받아오기 : data_list 에 추가
                    try:
                        soup_list = soup.select("ul.list_news div.info_group")  # 여기 수정
                        for element in soup_list:
                            date = element.select('span.info')[-1].get_text(strip=True)
                            a_tags = element.find_all('a')
                            if len(a_tags) == 2:
                                url = a_tags[1]['href']
                                new_row = [date, url]
                                data_list.append(new_row)
                                print(f'{keyword} {len(data_list)}번째 row : {new_row}')
                            else:
                                continue

                    except Exception as e:
                        print('[bs4 데이터 받아오기 오류] ', e)
                        error_log.append([date, e])
                        break

                    # 페이지 이동
                    try:
                        next_page_button = driver.find_element(By.XPATH,
                                                               '//*[@id="main_pack"]/div[2]/div/a[2]')  # [>] 모양 버튼, 다음페이지로 이동한다
                        if next_page_button.get_attribute("aria-disabled") == "true":
                            # 다음 페이지가 없으면
                            print(f'{date} : 다음 페이지가 존재하지 않습니다. 크롤링을 종료합니다')
                            break
                        elif next_page_button.get_attribute("aria-disabled") == "false":
                            print('다음 페이지로 이동합니다')
                            next_page_button.click()  # 다음 페이지로 이동
                        else:
                            print('[페이지 이동 에러] else')
                            break
                    except Exception as e:
                        print('[페이지 이동 에러] ', e)
                        error_log.append([date, e])
                        time.sleep(1)
                        break

        save_url_file(keyword, year, data_list)     # 1년 단위 데이터 csv로 만든다

        # error 발생했는지 확인
        if len(error_log) > 0:
            print("error는 발생 log 입니다")
            for date, error in error_log:
                print(date, error)
            df_error = pd.DataFrame(error_log, columns=['date', 'error'])
            error_file_path = os.path.join(folder_path, f"{keyword}_{year}_error.csv")
            df_error.to_csv(error_file_path, encoding='utf-8', index=False)
            print("error는 발생 log 를 파일로 저장했습니다")
        else:
            print("error는 발생하지 않았습니다")

    print('get_news_url_heavy()를 종료합니다')


def get_content_from_url(keyword):
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


def get_driver(url):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')  # 창이 없이 크롬이 실행이 되도록 만든다
    # options.add_argument("--start-maximized")  # 창이 최대화 되도록 열리게 한다.
    options.add_argument("disable-infobars")  # 안내바가 없이 열리게 한다.
    options.add_argument('--disable-dev-shm-usage')  # 공유메모리를 사용하지 않는다
    options.add_argument("disable-gpu")  # 크롤링 실행시 GPU를 사용하지 않게 한다.
    options.add_argument("--disable-extensions")  # 확장팩을 사용하지 않는다.
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # site에 접근하기 위해 get메소드에 이동할 URL을 입력한다.
    driver.get(url)
    return driver

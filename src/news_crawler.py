from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import utility_module as util
import pandas as pd
import requests
import os
import time
import crawling_tool as cr


####################################################
# get_news_url()
# 기능 : keyword로 검색한 결과 뉴스의 url을 저장하는 함수
# 입력값 : keyword (검색어, 문자열), start_date (검색 시작 날짜, 문자열), end_date (검색 종료 날짜, 문자열)
def get_news_url(keyword, start_date, end_date):
    date_list = util.generate_date_list(start_date, end_date)
    keyword_unicode = util.convert_to_unicode(keyword)
    # [1. url 크롤링 : 하루 단위로]
    for date in date_list:
        print(f'{keyword} : {date}의 크롤링 진행')
        try:
            date_having_dots = date.replace('-', '.')  # 2023.11.10 형식
            date_no_dots = date.replace('-', '')     # 20231110 형식
            search_url = f"https://search.naver.com/search.naver?where=news&query={keyword_unicode}&sm=tab_opt&sort=2&photo=0&field=0&pd=3&ds={date_having_dots}&de={date_having_dots}&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Ar%2Cp%3Afrom{date_no_dots}to{date_no_dots}&is_sug_officeid=0&office_category=0&service_area=0"

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


def get_news_text(keyword):
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

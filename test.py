import utility_module as util
import crawling_tool as cr
from bs4 import BeautifulSoup

url_8  = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EA%B5%AC%EB%A6%AC%EC%8B%9C&sort=2&photo=0&field=0&pd=3&ds=2023.11.10&de=2023.11.10&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:r,p:from20231110to20231110,a:all&start=8"
url_12 = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EA%B5%AC%EB%A6%AC%EC%8B%9C&sort=2&photo=0&field=0&pd=3&ds=2023.11.10&de=2023.11.10&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:r,p:from20231110to20231110,a:all&start=12"
url_21 = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EA%B5%AC%EB%A6%AC%EC%8B%9C&sort=2&photo=0&field=0&pd=3&ds=2023.11.10&de=2023.11.10&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:r,p:from20231110to20231110,a:all&start=21"
url_32 = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EA%B5%AC%EB%A6%AC%EC%8B%9C&sort=2&photo=0&field=0&pd=3&ds=2023.11.10&de=2023.11.10&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:r,p:from20231110to20231110,a:all&start=32"
url_33 = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EA%B5%AC%EB%A6%AC%EC%8B%9C&sort=2&photo=0&field=0&pd=3&ds=2023.11.10&de=2023.11.10&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:r,p:from20231110to20231110,a:all&start=33"

no_result_url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EC%82%BC%EC%A0%84&sort=2&photo=0&field=0&pd=3&ds=2008.01.01&de=2008.01.01&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:r,p:from20080101to20080101,a:all&start=1"
no_2 = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EC%82%BC%EC%A0%84&sort=2&photo=0&field=0&pd=3&ds=2008.01.01&de=2008.01.01&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:r,p:from20080101to20080101,a:all&start=1"

# driver = cr.get_driver()
# driver.get(no_2)
# html = driver.page_source
# soup = BeautifulSoup(html, 'html.parser')
# driver.quit()
#
# is_no = cr.is_no_result(soup)
# print(is_no)

# 합치기
util.merge_csv_files(
    save_file_name="logs_2",
    read_folder_path_="./url/temp_logs")



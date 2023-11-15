import utility_module as util
import crawling_tool as cr

url_1 = "https://search.naver.com/search.naver?sm=tab_hty.top&where=news&query=zedarhnaezrd&oquery=zedarhnaezrdth&tqi=iSsMldqVOsossbRBdK0ssssssIo-436895&nso=so%3Ar%2Cp%3Afrom20231110to20231110%2Ca%3Aall&de=2023.11.10&ds=2023.11.10&mynews=0&office_category=0&office_section_code=0&office_type=0&pd=3&photo=0&service_area=0&sort=2"
url_2 = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EA%B8%88%EB%A6%AC&sort=2&photo=0&field=0&pd=3&ds=2023.11.10&de=2023.11.10&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:r,p:from20231110to20231110,a:all&start=81"
url_3 = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EA%B8%88%EB%A6%AC&sort=2&photo=0&field=0&pd=3&ds=2023.11.10&de=2023.11.10&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:r,p:from20231110to20231110,a:all&start=2991"
url_4 = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EA%B8%88%EB%A6%AC&sort=2&photo=0&field=0&pd=3&ds=2023.11.10&de=2023.11.10&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:r,p:from20231110to20231110,a:all&start=91"
url_5 = "https://search.naver.com/search.naver?sm=tab_hty.top&where=news&query=%EC%9D%B4%EC%8A%B9%EB%AF%BC+%EC%9E%90&oquery=%EC%9D%B4%EC%8A%B9%EB%AF%BC&tqi=iSslldqVN8VssBgZkJlssssssoR-506494&nso=so%3Ar%2Cp%%E3%85%81%2Ca%3Aall&de=2023.11.10&ds=2023.11.10&mynews=0&office_category=0&office_section_code=0&office_type=0&pd=3&photo=0&service_area=0&sort=2"

url_8  = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EA%B5%AC%EB%A6%AC%EC%8B%9C&sort=2&photo=0&field=0&pd=3&ds=2023.11.10&de=2023.11.10&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:r,p:from20231110to20231110,a:all&start=8"
url_12 = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EA%B5%AC%EB%A6%AC%EC%8B%9C&sort=2&photo=0&field=0&pd=3&ds=2023.11.10&de=2023.11.10&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:r,p:from20231110to20231110,a:all&start=12"
url_21 = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EA%B5%AC%EB%A6%AC%EC%8B%9C&sort=2&photo=0&field=0&pd=3&ds=2023.11.10&de=2023.11.10&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:r,p:from20231110to20231110,a:all&start=21"
url_32 = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EA%B5%AC%EB%A6%AC%EC%8B%9C&sort=2&photo=0&field=0&pd=3&ds=2023.11.10&de=2023.11.10&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:r,p:from20231110to20231110,a:all&start=32"
url_33 = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EA%B5%AC%EB%A6%AC%EC%8B%9C&sort=2&photo=0&field=0&pd=3&ds=2023.11.10&de=2023.11.10&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:r,p:from20231110to20231110,a:all&start=33"

# 8  : 여성신문 - 구리시민·정치권 "GTX-B노선 갈매역 정차" 촉구 (네이버뉴스)
# 12 : 경기신문 - ‘GTX-B 갈매역 정차를 위한 시민궐기대회’
# 32 : 플리뉴스 - [2023 국회 기후환경 매니페스토]

keyword = "구리시"
start_date = "2023-11-09"
end_date = "2023-11-10"

# is_ex = cr.is_exist_next_page(url_32)
# print(is_ex)
#
# soup = cr.get_soup(url_32)
# rows = (cr.get_url_rows(soup, keyword, start_date))
# print(rows)

folder_path = "./url/temp_files"
util.merge_url_temp_logs(keyword, start_date, end_date)

###################
# soup_box = soup.select_one("ul.list_news li.bx")
#
# result = cr.get_naver_news_url(soup_box)
# print(result)
# if result is None:
#     print("awegalewkng")

# a = soup_box.select('div.info_group a')
# print(len(a))
# print(a[1])
# is_naver = is_naver_news(soup)
# print(is_naver)


# is_exist_next_page = cr.is_exist_next_page(soup)
# print(is_exist_next_page)

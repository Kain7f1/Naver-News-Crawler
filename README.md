# Naver-News-Crawler

네이버 뉴스 text 크롤러

---

* ### 차례
  * 기능
  * 설정값
  * 사용법
  * 성능
  * Contacts
  * License
   
---

## 기능

* 네이버에서 키워드로 검색하고, 검색결과 뉴스들의 text를 수집합니다
* 수집된 text는 .csv 파일로 저장됩니다
* `검색 키워드`, `검색 기간`을 설정할 수 있습니다
* 중간에 크롤링이 정지되더라도, 진행상황이 저장되므로 이어서 진행할 수 있습니다
* `크롤링 로그`와 `오류 로그`는 .csv 파일로 저장되어 확인할 수 있습니다

---

## 설정값
모든 설정은 [main.py](https://github.com/Kain7f1/Naver-News-Crawler/blob/main/main.py) 에서 이루어집니다

### keyword
![image](https://github.com/Kain7f1/Naver-News-Crawler/assets/141689851/189e43d3-07f3-492e-ae54-05ccc7399b5c)
* 검색할 키워드를 설정합니다
* 검색 플랫폼 : 네이버

### start_date, end_date
![image](https://github.com/Kain7f1/Naver-News-Crawler/assets/141689851/236763db-8abd-4cdb-b23a-e8f0f872aa17)
* 검색 기간을 설정할 수 있습니다
* 기간 범위 내의 데이터만 수집합니다

---

## 사용법
![image](https://github.com/Kain7f1/Naver-News-Crawler/assets/141689851/7188b756-d7a2-47e4-bc72-aec3cdd7a0a7)

설정값을 입력한 후, 한번에 실행하면 됩니다

* crawl_url_recursion() : 뉴스 url 수집
* crawl_text_recursion() : 뉴스 text 수집

---

## 성능

### Test : "금리"
- 1개의 뉴스 당 약 1.374초가 소요됨
- 데이터의 양 : 1,607,899개
- url 수집 : 1,094,647초 (약 304 시간)
- text 수집 : 371,687초 (약 103 시간)

### 성능 피드백
- url 수집할 때, selenium 사용 과정에서 많은 시간이 소요된다.
- 개선방안을 탐색해보자
  
---

## Contacts

### 이슈 관련
* https://github.com/Kain7f1/Naver-News-Crawler/issues

### E-mail
* kain7f1@gmail.com

---

## License

`DC-Crawler`는 `MIT License` 라이선스 하에 공개되어 있습니다. 모델 및 코드를 사용할 경우 라이선스 내용을 준수해주세요. 라이선스 전문은 `LICENSE` 파일에서 확인하실 수 있습니다.

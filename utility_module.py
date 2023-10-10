import pandas as pd
import os
import re
import time
from datetime import datetime
from calendar import monthrange


######################################
# 입력 : 2000.01.01 형식을 입력받아서
# return : 그 달의 마지막 날짜를 리턴
def get_last_date(date_string):
    date_format = "%Y.%m.%d"    # 날짜 형식 (예: 2023.01.01)
    date_object = datetime.strptime(date_string, date_format)
    _, last_day = monthrange(date_object.year, date_object.month)
    return f"{date_object.year}.{date_object.month:02d}.{last_day:02d}"


####################################
def make_date_range(year, month):
    last_date = get_last_date(f'{year}.{month}.01')
    date_list = []
    for day in range(1, 30, 3):
        day_to = day + 2
        if day == 28:
            day_to = int(last_date[-2:])
        date_list.append([f'{year}.{month}.{day:02d}', f'{year}.{month}.{day_to:02d}'])
    return date_list


#####################################
# 기능 : 함수의 실행 시간을 재는 데코레이터
# 사용법 : @util.timer_decorator 를 함수 정의할 때 함수명 윗줄에 적는다
def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"{func.__name__} 함수의 실행 시간은 {elapsed_time:.2f} 초 입니다")
        return result
    return wrapper


#####################################
# 기능 : 폴더를 생성한다
# 입력값 : 파일 경로(이름)
def create_folder(folder_path):
    # 폴더가 존재하지 않는 경우, 폴더 생성
    if os.path.exists(folder_path):
        print("[폴더가 이미 존재합니다]")
    else:
        os.makedirs(folder_path)
        print(f"[폴더 : {folder_path}를 만들었습니다]")
    print("[create_folder()를 종료합니다]")
    return folder_path


#####################################
# 입력값 : folder_path, endswith (파일이름의 검색조건 : 파일명의 끝)
# 기능 : file_names 리스트를 가져오는 함수
def load_file_names(folder_path, endswith='url.csv'):
    files = []
    # 폴더 내의 모든 파일을 탐색
    print(f"[{folder_path} 내의 파일을 탐색합니다. 검색조건 : endswith={endswith}]")
    for filename in os.listdir(folder_path):
        if filename.endswith(endswith):
            files.append(filename)

    print("load_files()의 결과는 다음과 같습니다. ")
    for file in files:
        print(file)
    print("load_files()을 종료합니다")
    return files


#####################################
# read_file()
# 기능 : .csv의 내용을 읽어옴
# 리턴값 : df 형식의 데이터
def read_file(folder_path, file_name):
    combined_path = os.path.join(folder_path, file_name)        # os.path.join()을 사용하여 두 경로를 합칩니다.
    return pd.read_csv(combined_path, encoding='utf-8')


#####################################
# save_file()
# 기능 : df의 내용을 파일로 저장한다
def save_file(df, folder_path, file_name):
    combined_path = os.path.join(folder_path, file_name)        # os.path.join()을 사용하여 두 경로를 합칩니다.
    df.to_csv(combined_path, encoding='utf-8', index=False)     # df의 내용을 csv 형식으로 저장합니다


#####################################
# combine_csv_file()
# 기능 : df형식의 데이터가 저장되어있는 .csv 파일들을 하나로 합친다
def combine_csv_file(folder_path, result_file_name):
    csv_file_names = load_file_names(folder_path, endswith='.csv')   # .csv로 끝나는 파일들을 전부 검색한다
    dataframes = []

    # 1. 잘 불러왔는지 확인하기
    print(f'[{len(csv_file_names)}개의 파일을 합치겠습니다]')
    for csv_file_name in csv_file_names:
        print(csv_file_name)

    # 2. df 합치기
    for csv_file_name in csv_file_names:
        df_content = read_file(folder_path, file_name=csv_file_name)
        dataframes.append(df_content)
    merged_df = pd.concat(dataframes)
    # merged_df.drop_duplicates(subset='url', keep='first', inplace=True)  # 중복 제거 옵션
    merged_df = merged_df.reset_index(drop=True)
    print(merged_df.tail())

    # 3. df를 csv로 만든다
    result_folder_path = create_folder(f"{folder_path}/{result_file_name}")
    save_file(merged_df, result_folder_path, file_name=f"{result_file_name}.csv")
    print(f"[{len(csv_file_names)}개의 파일을 {result_file_name}.csv 파일로 합쳤습니다]")
    print(f"총 데이터 개수 : {len(merged_df)}개")


#####################################
# 기능 : 에러 로그를 읽고, 에러가 있으면 csv 파일을 만든다
def error_check(error_log, folder_path, file_name):
    # error 발생 했는지 확인
    if len(error_log) > 0:
        print("[에러 발생 로그 입니다]")
        for error in error_log:
            print(error)      # 에러 로그 출력
        df_error = pd.DataFrame(error_log)   # df 생성
        error_file_path = os.path.join(folder_path, f"{file_name}_error.csv")
        df_error.to_csv(error_file_path, encoding='utf-8', index=False)
        print(f"[총 {len(error_log)}개의 에러 로그가 파일로 저장되었습니다]")
        return len(error_log)
    else:
        return 0


#####################################
# 목적 : title 텍스트를 전처리한다
# 기능 : 끝에붙은 대괄호와 안의 숫자, 콤마 (","), "u\202c" 를 제거한다
def preprocess_title(text):
    # 바꿀 것들 리스트
    replacements = {
        "\u202c": "",
        ',': ' '
    }
    for old, new in replacements.items():
        text = text.replace(old, new)       # replacements의 전자를 후자로 교체함
    result = re.sub(r'\[\d+\]$', '', text).strip()  # 뒤에 붙는 댓글수 [3]같은거 제거한다. + 공백제거
    if len(result) == 0:
        return "_"  # 널값이면 "_"을 리턴한다
    else:
        return result  # 전처리 결과값 리턴


#####################################
# preprocess_content_dc()
# 전처리 함수 : dcinside
def preprocess_content_dc(text):
    # 바꿀 것들 리스트
    replacements = {
        '\n': ' ',
        '\t': ' ',
        ',': ' ',
        '- dc official App': '',
        '- dc App': ''
    }
    for old, new in replacements.items():
        text = text.replace(old, new)   # replacements의 전자를 후자로 교체함
    result = text.strip()               # 공백제거
    if len(result) == 0:
        return "_"      # 널값이면 "_"을 리턴한다
    else:
        return result   # 전처리 결과값 리턴


##################################################
# 기능 : 입력한 문자열에, blacklist의 원소가 포함되어 있으면 True, 아니면 False를 리턴하는 함수
def contains_blacklist(str_, blacklist):
    for item in blacklist:
        if item in str_:
            return True
    return False


##########################################
# 기능 : 한글 문자열을 유니코드 UTF-8로 인코딩하여 반환합니다
# 입력 예시 : '에스엠'
# 리턴값 예시 : '.EC.97.90.EC.8A.A4.EC.97.A0'
def convert_to_unicode(input_str):
    return '.' + '.'.join(['{:02X}'.format(byte) for byte in input_str.encode('utf-8')])


#########################################################################################################
# 한국어인지 검사하는 함수
def is_korean(s):
    return bool(re.fullmatch("[\u3131-\u3163\uAC00-\uD7A3]+", s))


# 불용어를 지운다
def remove_stopword(keyword):
    # 파일 열기
    folder_path = f'./{keyword}'
    file_name = f'{keyword}_content_tokenized.csv'
    with open('stopwords.txt', 'r', encoding='utf-8') as file:
        # 라인별로 읽어 리스트로 저장
        stopwords = file.readlines()
    stopwords = [word.strip() for word in stopwords]
    print('stopwords.txt 를 불러왔습니다')

    df = read_file(folder_path, file_name)
    print(f'{file_name} 를 불러왔습니다')
    for stopword in stopwords:
        df['content'] = df['content'].str.replace(f'\\b{stopword} \\b', '', regex=True)
    print('stopwords를 지웠습니다')

    save_file(df, folder_path, f'{keyword}_content_tokenized_removed_stopwords.csv')
    print(f'{keyword}_removed_stopwords.csv 파일을 저장했습니다')


def dropna_and_save(file_path):
    df = pd.read_csv(file_path, encoding='utf-8')
    df.dropna(inplace=True)
    df.to_csv(file_path, encoding='utf-8', index=False)
    
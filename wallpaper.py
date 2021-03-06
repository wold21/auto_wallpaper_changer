import argparse  # CLI앱으로 앱에 인수를 전달할때 사용
import os  # 시스템 접근 라이브러리
import time  # sleep()메서드 사용
import random  # 임의의 번호 생성해 url에 접목시킴
import requests  # http요청
# 파이썬에서 외부 함수를 호출하는 것 C호환 데이터 유형을 제공하고 DLL 및 공유 라이브러리를 호풀 할 수 있다.
# 바탕 화면을 변경하기 위한 SystemParametersInfoW를 호출할 수 있다.
import ctypes
import platform  # 운영체제 파악용도?


def get_wallpaper():
    # Random Number
    # 1에서 99까지의 정수 난수 생성
    num = random.randint(1, 99)

    # 내 API키
    API_KEY = {
        'Authorization': '563492ad6f91700001000001de682d7dd02b4ccaa050d2ac68e69936'}

    # 검색 단어
    query = 'Ocean'

    # URL for PEXELS
    url = 'https://api.pexels.com/v1/search?per_page=1&page=' + \
        str(num) + '&query=' + query

    # 요청 받아오기
    res = requests.get(url, headers=API_KEY)

    # statuscode가 200이면 내용을 json으로 바꿔 이미지 url을 분석해
    # write를 사용하여 파일을 jpg로 저장한다.
    if res.status_code == 200:
        img_url = res.json().get('photos')[0]['src']['original']
        img = requests.get(img_url)
        with open('temp.jpg', 'wb') as f:
            f.write(img.content)
    else:
        print('요청 에러남')


def set_wallpaper():
    get_wallpaper()
    system_name = platform.system().lower()
    path = ''
    if system_name == 'linux':
        path = os.getcwd()+'/temp.jpg'
        command = "gsettings set org.gnome.desktop.background picture-uri file:" + path
        os.system(command)
    elif system_name == 'windows':
        path = os.getcwd()+'\\temp.jpg'
        ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)
        # BOOL SystemParametersInfoW(
        # UINT  uiAction, # 설정하거나 검색 할 시스템 전체 매개변수
        # UINT  uiParam, # 윈도우의 시스템 매개변수에 의존하는 두번째 매개변수, 대부분 0을 사용한다.
        # PVOID pvParam, # 첫번째 인자에 설정된 조치에 대한 인수를 전송하는데 사용. 우리는 파일 위치를 전송한다.
        # UINT  fWinIni # 윈도우 사용자의 모든 최상위 창에 변경 사항을 브로드캐스트 하는게 사용할 수 있다. 안쓰기 때문에 0
        #  );


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--time", help="Enter time in minutes")

    args = parser.parse_args()
    minute = int(args.time)
    while(1):
        time.sleep(minute*60)
        set_wallpaper()


# 사용법

#### 1분 마다 변환 ####
# C:\Users\jaqsp>wallpaper.py -t 1

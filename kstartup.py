import time
import os
import telegram
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

#텔레그램 봇 설정
my_token = '1032194001:AAF3v9R80ExDqIcO7cct_ZJZpRbP_-IkRB8'
bot = telegram.Bot(my_token)
updates = bot.get_updates()
#chat_id = bot.get_updates()[-1].message.chat.id #최근 채팅한 사람에게 전달.
chat_id = -328584120

options = webdriver.ChromeOptions()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# headless 옵션 설정
options.add_argument('headless')
options.add_argument("no-sandbox")

# 브라우저 윈도우 사이즈
options.add_argument('window-size=1920x1080')

# 사람처럼 보이게 하는 옵션들
options.add_argument("disable-gpu")   # 가속 사용 x
options.add_argument("lang=ko_KR")    # 가짜 플러그인 탑재
options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')  # user-agent 이름 설정

browser = webdriver.Chrome(executable_path="./chromedriver.exe", options=options)
time.sleep(3)

kstartup_url = 'https://www.k-startup.go.kr/common/announcement/announcementList.do?mid=30004&bid=701&searchAppAt=A'
jobaba_url = 'https://www.jobaba.net/fntn/list.do'

while True:
    old_list = []
    with open(os.path.join(BASE_DIR, 'latest_kstartup.txt'), mode='r+', encoding='UTF-8') as f_read:
        for i in f_read.readlines():
            old_list.append(i.splitlines()[0])

    browser.get(kstartup_url)
    browser.find_element_by_xpath('//*[@id="listPlusAdd"]/a').click()

    list = browser.find_elements_by_css_selector('h4 > a')
    list_text = []
    for li in list:
        if(len(li.text) > 0):
            list_text.append(li.text)

    #다름을 찾고 다름을 출력함.
    diff_list = []

    for i in list_text:
        if i not in old_list:
            diff_list.append(i)
            print(i)

    if len(diff_list) > 0:
        bot.send_message(chat_id=chat_id, text='\n'.join(diff_list))

    #파일로 저장
    with open(os.path.join(BASE_DIR, 'latest_kstartup.txt'), mode='w+', encoding='UTF-8') as f_write:
        f_write.write('\n'.join(list_text))
        f_write.close()

    #잡아바
    browser.get(jobaba_url)
    old_list = []
    with open(os.path.join(BASE_DIR, 'latest_jobaba.txt'), mode='r+', encoding='UTF-8') as f_read:
        for i in f_read.readlines():
            old_list.append(i.splitlines()[0])

    list = browser.find_elements_by_css_selector('span.mTitle')
    list_text = []
    for li in list:
        if(len(li.text) > 0):
            list_text.append(li.text)
    #다름을 찾고 다름을 출력함.
    diff_list = []

    for i in list_text:
        if i not in old_list:
            diff_list.append(i)
            print(i)

    if len(diff_list) > 0:
        bot.send_message(chat_id=chat_id, text='\n'.join(diff_list))

    #파일로 저장
    with open(os.path.join(BASE_DIR, 'latest_jobaba.txt'), mode='w+', encoding='UTF-8') as f_write:
        f_write.write('\n'.join(list_text))
        f_write.close()

    print("wait")
    time.sleep(60)
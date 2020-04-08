#-*- coding: UTF-8 -*-
#2018/09/05
#longzhu
import os
from PIL import Image
from selenium import webdriver
import time
import itchat

@itchat.msg_register('Text')
def text_reply(msg):
    global flag
    message = msg['Text']
    fromName = msg['FromUserName']
    toName = msg['ToUserName']

    if toName == "filehelper":
        itchat.send(sendMsg, fromName)
        if message == "打卡":
            global driver
            chromedriver = "D:\Python27\chromedriver"
            os.environ["webdriver.chrome.driver"] = chromedriver
            driver = webdriver.Chrome(chromedriver)  # 打開chrome瀏覽器
            login("longzhu", "123456")#請將此處換成你的賬號密碼，需要手動輸入的話請回復代打卡
            daka()
            try:
                yanzhengma()
                itchat.send("可以獲取驗證碼", "filehelper")
            except:
                driver.find_element_by_name("check").click()
                itchat.send("打卡成功", "filehelper")
                time.sleep(2)
                driver.save_screenshot('D:\yzm\yzm.png')
                send('D:\yzm\yzm.png')
        if message == "驗證碼":
            send('D:\yzm\yzm1.jpeg')
        if message == "再次獲取驗證碼":
            yanzhengma()
            itchat.send("獲取成功", "filehelper")
            send('D:\yzm\yzm1.jpeg')
        if message == "代打卡":
            itchat.send("請輸入賬號密碼如：longzhu,123456,備註理由", "filehelper")
        if len(message) > 10:
            message.split(',')
            bz = message[2]
            login(message[0],message[1])
            daka()
            beizhu(bz)
            if driver.find_element_by_id('image'):
                yanzhengma()
                itchat.send("可以獲取驗證碼", "filehelper")
            else:
                driver.find_element_by_name("check").click()
                itchat.send("打卡成功", "filehelper")
                time.sleep(2)
                driver.save_screenshot('D:\yzm\yzm.png')
                send('D:\yzm\yzm.png')
        if len(message) == 4:
            shuru(message)
            time.sleep(3)
            driver.save_screenshot('D:\yzm\yzm.png')
            send('D:\yzm\yzm.png')
        if message == "結果":
            driver.save_screenshot('D:\yzm\yzm.png')
            send('D:\yzm\yzm.png')

#登錄打卡網址
def login(uname, pwd):
    driver.get("http://om.xxxxx.com/attendances/check_out/6111421")
    time.sleep(1)
    driver.maximize_window()  # 將瀏覽器最大化
    time.sleep(2)
    if driver.find_element_by_id("username"):
        for i in uname:
            driver.find_element_by_id("username").send_keys(i)
            time.sleep(0.2)
    time.sleep(1)
    if driver.find_element_by_id("password_input"):
        for j in pwd:
            driver.find_element_by_id("password_input").send_keys(j)
            time.sleep(0.2)
        time.sleep(1)
    if driver.find_element_by_id("login_button"):
        driver.find_element_by_id("login_button").click()
        time.sleep(3)


def beizhu(bz):
    if bz == None:
        return
    if driver.find_element_by_id("sub_check_out_remark"):
        for j in bz:
            driver.find_element_by_id("sub_check_out_remark").send_keys(j)
            time.sleep(0.2)
        time.sleep(1)

#點擊簽出按鈕
def daka():
    try:
        driver.find_element_by_id("checkout_btn").click() # 網頁中查找簽出按鈕
    except:
        driver.find_element_by_id("checkin_btn").click() # 點擊簽入按鈕
    time.sleep(5)

#獲取驗證碼圖片
def yanzhengma():
    if os.path.exists('D:\yzm\yzm.png'):
        os.remove('D:\yzm\yzm.png')
    if os.path.exists('D:\yzm\yzm1.jpeg'):
        os.remove('D:\yzm\yzm1.jpeg')
    driver.save_screenshot('D:\yzm\yzm.png')  # 截取當前網頁，該網頁有我們需要的驗證碼
    imgelement = driver.find_element_by_id('image')  # 定位驗證碼
    location = imgelement.location  # 獲取驗證碼x,y軸座標
    size = imgelement.size  # 獲取驗證碼的長寬
    rangle = (int(location['x']), int(location['y']), int(location['x'] + size['width']),
              int(location['y'] + size['height']))  # 寫成我們需要截取的位置座標
    i = Image.open("D:\yzm\yzm.png")  # 打開截圖
    frame4 = i.crop(rangle)  # 使用Image的crop函數，從截圖中再次截取我們需要的區域
    frame4.convert('RGB').save('D:\yzm\yzm1.jpeg')#成功獲取到驗證碼圖片

#讀取驗證碼
def get_file_content(file):
    with open(file, 'rb') as fp:
        return fp.read()

#驗證碼識別
def send(image_path):
    try:
        itchat.send_image(image_path, 'filehelper')
        print("send success")
    except:
        print("fail")

#刷新驗證碼
def shuaxinyzm():
    if driver.find_element_by_id("image"):
        driver.find_element_by_id("image").click()

#輸入驗證碼
def shuru(yzm):
    if driver.find_element_by_id("code_input"):
        if len(yzm)==1:
            driver.find_element_by_id("code_input").send_keys(yzm)
        else:
            for i in yzm:
                driver.find_element_by_id("code_input").send_keys(i)
                time.sleep(0.2)
    if driver.find_element_by_name("check"):
        driver.find_element_by_name("check").click()
    print("打卡成功")

if __name__ == '__main__':
    sendMsg = u"{消息助手}：暫時無法回覆"
    usageMsg = u"使用方法：\n1.開啓打卡腳本：打卡\n" \
               u"2.發送驗證碼：驗證碼\n3.重新獲取驗證碼：再次獲取驗證碼\n" \
               u"4.幫同事打卡：代打卡\n5.輸入驗證碼：直接回復四位驗證碼\n" \
               u"6.查看打卡是否成功：結果\n"
    itchat.auto_login()
    itchat.send(usageMsg, "filehelper")
    global_var_list = []
    itchat.run()
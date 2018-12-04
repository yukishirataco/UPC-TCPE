#-*- coding:utf-8 -*-
import time, requests, json, urllib, getpass, os

url_code = 'http://tcpe.upc.edu.cn:8086/Common/GetValiCode/'
url_login = 'http://tcpe.upc.edu.cn:8086/Account/DoLogin'
url_get_result = 'http://tcpe.upc.edu.cn:8086/Student/GetStuExpeDetail'
ua = 'Molella/5.0 (YJSNPinux 114.51,KMR OS 19.1) RingoWebKit/810.0 (KHTML, like Gecko) Chrome/49.0.2623.13 Safari/537.36'
header = {"User-Agent": ua, 'Host': 'tcpe.upc.edu.cn:8086'}

login_session = requests.session()
timestamp = int(time.time())

getcookies = login_session.get(url_code + str(timestamp), headers=header)
# 从验证码获取页面一次性获得验证码和登陆要用的Cookies
with open('验证码.png', 'wb') as file:
    file.write(getcookies.content)
# 保存用户验证码
print('Remake and Open-Source by Yukino Shiratamaco in UPC Linux 2018')
useraccount = input('请输入你的学号(如:1701010101):')
password = getpass.getpass(prompt='请输入你的密码（你的输入有可能没有显示，这是正常的现象）:')
usertype = 'Student'
course_id = input(
    '请输入你的课程编号，\n大学物理实验(2-1)请输入1\n大学物理实验(2-2)请输入2\n大学物理实验(小学期)请输入3 :')
valicode = input('请输入与程序同一目录下的 验证码.png 显示的验证码:')
login_session.get(url_login, headers=header)
post_data = {
    'UserAccount': useraccount,
    'Password': password,
    'UserType': usertype,
    'CourseID': course_id,
    'ValidateCode': valicode
}
data = login_session.post(url_login, data=post_data, headers=header)
# 登录

if data.text != 'Ok':
    print('出错了，你的登录信息可能有误!')
    # 登录信息错误

else:
    result = requests.get(
        url_get_result, headers=header, cookies=getcookies.cookies.get_dict())
    res_text = result.content.decode()
    res = json.loads(res_text)
    for item in res:
        # 没出来的成绩在json里是None
        itemt = item.get('Title')
        score = item.get('ExpeItemScore')
        if score is None:
            print('实验项目' + itemt + '的成绩未出')
        else:
            print('实验项目' + itemt + '的成绩为：' + str(score) + '分')

os.remove('./验证码.png')
input('请按回车键退出。')

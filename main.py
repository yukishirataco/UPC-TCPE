#-*- coding:utf-8 -*-
import time, requests, json, urllib, getpass, os
from prettytable import PrettyTable

url_code = 'http://tcpe.upc.edu.cn:8086/Common/GetValiCode/'
url_login = 'http://tcpe.upc.edu.cn:8086/Account/DoLogin'
url_get_result = 'http://tcpe.upc.edu.cn:8086/Student/GetStuExpeDetail'
url_get_noexpe = 'http://tcpe.upc.edu.cn:8086/Mark/GetNotExpeMark'
url_get_final = 'http://tcpe.upc.edu.cn:8086/Mark/GetFinalMarkForStu'
ua = 'Molella/8.10 (YJSNPinux 114.51,KMR OS 19.1)'
header = {"User-Agent": ua, 'Host': 'tcpe.upc.edu.cn:8086'}

login_session = requests.session()
timestamp = int(time.time())

getcookies = login_session.get(url_code + str(timestamp), headers=header)
# 从验证码获取页面一次性获得验证码和登陆要用的Cookies
with open('验证码.png', 'wb') as file:
    file.write(getcookies.content)
# 保存用户验证码
print('Remake and Open-Source by Yukino Shiratamaco in UPC Linux 2018')
print('为了保证使用体验，请最好新建一个文件夹并放入本程序')
useraccount = input('请输入你的学号(如:1701010101):')
password = getpass.getpass(prompt='请输入你的密码（你的输入有可能没有显示，这是正常的现象）:')
usertype = 'Student'
print('请输入你的课程编号')
print('课程类型\t输入内容\t')
print('大学物理实验(2-1) \t1\t')
print('大学物理实验(2-2) \t2\t')
print('大学物理实验(小学期) \t3\t')
course_id = input('编号是:')
try:
    os.system("start 验证码.png")
except OSError:
    print('啊哦，显然你的操作系统不能直接打开验证码，请到程序目录下手动打开')
# Only avaliable in Windows.
valicode = input('请输入打开的图片中显示的验证码，若图片未打开，请手动到程序目录下打开 验证码.png:')
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
    if data.text == 'ValidateErr':
        print('验证码错误')
    elif data.text == 'EmptyErr':
        print('输入的用户名或者密码为空')
    elif data.text == 'AccPwdErr':
        print('用户名或密码错误')
else:
    os.system('cls') # only in windows
    result = requests.get(
        url_get_result, headers=header, cookies=getcookies.cookies.get_dict())
    res_text = result.content.decode()
    res = json.loads(res_text)
    number = 0
    sum = 0
    exp_scores = PrettyTable(["实验项目","项目成绩"])
    print("你在系统中登记的所有实验项目的成绩如下：")
    for item in res:
        # 没出来的成绩在json里是None
        itemt = item.get('Title')
        score = item.get('ExpeItemScore')
        if score is None:
            exp_scores.add_row([itemt,"未出"])
        else:
            exp_scores.add_row([itemt,str(int(score))])
            sum = sum + score
            number = number + 1
    print(exp_scores)
    print('已出成绩%d项，平均分为%.2f分' % (number, sum / number))
    result_unexpe = requests.get(
        url_get_noexpe, headers=header, cookies=getcookies.cookies.get_dict())
    res_unexpe_json = result_unexpe.content.decode()
    res_unexpe = json.loads(res_unexpe_json)
    try:
        for item in res_unexpe:
            itemt = item.get('Item')
            score = item.get('Score')
            print('非实验项目 ' + itemt + ' 的成绩为：' + str(int(score)) + '分')
    except Exception as e:
        pass
    result_final_raw = requests.get(
        url_get_final, headers=header, cookies=getcookies.cookies.get_dict())
    res_final_json = result_final_raw.content.decode()
    res_final = json.loads(res_final_json)
    try:
        for item in res_final:
            FinalScore = item.get('TotMark')
            print('总评成绩: ' + str(int(FinalScore)) + ' 分')
    except Exception as e:
        pass

os.remove('./验证码.png')
input('请按回车键退出。')

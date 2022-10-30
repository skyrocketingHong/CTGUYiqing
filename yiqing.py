import requests
from bs4 import BeautifulSoup


# ****************登录*******************
# 学号
username = ""
# 密码
password = ""
# 手机号
phone_number = ""

login_url = "http://yiqing.ctgu.edu.cn/wx/index/loginSubmit.do"
header = {
    "Referer": "http://yiqing.ctgu.edu.cn/wx/index/login.do?currSchool=ctgu&CURRENT_YEAR=2019",
    # 使用Edge的UA登录
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
}
yiqing_session = requests.session()
post_data = {
    "username": username,
    "password": password
}
response_resource = yiqing_session.post(login_url, data=post_data, headers=header)

# *******从提交页面获取 表单信息**********
# 构建表单（默认身体健康)
post_data = {
    "ttoken":  "",
    "province": "湖北省",
    "city": "宜昌市",
    "district": "西陵区",
    "adcode": "",
    "longitude": "111.315487",
    "latitude": "30.722622",
    "sfqz": "否",
    "sfys": "否",
    "sfzy": "否",
    "sfgl": "否",
    "status": "1",
    "szdz": "湖北省 宜昌市 西陵区",
    "sjh": phone_number,
    "lxrxm": "",
    "lxrsjh": "",
    "sffr": "否",
    "sffrAm": "否",
    "sffrNoon": "否",
    "sffrPm": "否",
    "sffy": "否",
    "sfgr": "否",
    "qzglsj": "",
    "qzgldd": "",
    "glyy": "",
    "mqzz": "",
    "sffx": "否",
    "qt": "",
}
get_form_url = "http://yiqing.ctgu.edu.cn/wx/health/toApply.do"
response_resource = yiqing_session.get(get_form_url)
# 获取必要信息填入表单
soup = BeautifulSoup(response_resource.text, "html.parser")
get_form_list = soup.find_all("input")[0:15]
for form_data in get_form_list:
    post_data[form_data.attrs["name"]] = form_data.attrs["value"]

# *************提交最终表单***********
post_form_url = "http://yiqing.ctgu.edu.cn/wx/health/saveApply.do"
header["Referer"] = "http://yiqing.ctgu.edu.cn/wx/health/toApply.do"
response_resource = yiqing_session.post(post_form_url, data=post_data, headers=header)
print(response_resource.text)

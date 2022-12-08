import requests
import logging
import sys
from logging import StreamHandler, FileHandler
from bs4 import BeautifulSoup

# 全局信息
# 版本号
version = "v1.2.0"
# 日志级别
log_level = logging.INFO
# 将学号、密码和手机号按照“info.txt中的模板填入，每行一个”
info_list = []

# 日志
# 日志文件
try:
    open("yiqing.log", "a")
except:
    open("yiqing.log", mode='w', encoding='utf-8')
# Handler
sh = StreamHandler(sys.stdout)
fh = FileHandler("yiqing.log")
# 日志配置
logging.basicConfig(handlers=[sh, fh], encoding="utf-8", level=log_level, format='%(asctime)s [%(levelname)s] %(message)s')
logging.info("🔔 " + version + " 开始尝试打卡")
def response_log(session):
    response_soup = BeautifulSoup(session.text, "html.parser")
    str = response_soup.get_text("|", strip=True)
    logging.info(str)
    logging.debug(session.text.replace("\n", "").replace(" ", "").replace("\r", "").replace("   ", ""))

# 登录
def login(username, password, phone_number):
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
    response_resource = yiqing_session.post(login_url, data=post_data, headers=header, timeout=None)
    response_log(response_resource)

    # 从提交页面获取 表单信息
    # 构建表单（默认校内+身体健康)
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
    response_resource = yiqing_session.get(get_form_url, timeout=5, headers=header, verify=False)
    response_log(response_resource)

    # 获取必要信息填入表单
    soup = BeautifulSoup(response_resource.text, "html.parser")
    get_form_list = soup.find_all("input")[0:15]
    for form_data in get_form_list:
        try:
            name = form_data.attrs["name"]
            post_data[name] = form_data.attrs["value"]
        except:
            logging.error("[ERROR] 无\"" + name + "\"字段")

    # 提交最终表单
    post_form_url = "http://yiqing.ctgu.edu.cn/wx/health/saveApply.do"
    header["Referer"] = "http://yiqing.ctgu.edu.cn/wx/health/toApply.do"
    response_resource = yiqing_session.post(post_form_url, data=post_data, headers=header, verify=False, timeout=None)

    # 输出结果
    response_log(response_resource)
    logging.info("🔔 学号 " + username + " 打卡结束，打卡过程请自行查看日志")

def read_txt():
    file = open("info.txt", "r")
    file_readlines = file.readlines()
    for line in file_readlines:
        line = line.strip("\n")
        line_list = list(line.split(","))
        info_list.append(line_list)

read_txt()

for info in info_list:
    login(info[0], info[1], info[2])
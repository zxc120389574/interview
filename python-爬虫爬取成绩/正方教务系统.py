
import re
import requests
import urllib
from lxml import etree
import operator as op
import xlwt

# 获取前端动态码
def get___VIEWSTATE(session):
    index_url = 'http://210.44.159.4'
    index_page = session.get(index_url, headers = headers)
    html = index_page.text

    pattern = r'name="__VIEWSTATE" value="(.*?)"'
    __VIEWSTATE = re.findall(pattern, html)
    return __VIEWSTATE[0]

# 获取前端动态码
def get___VIEWSTATE_by_url(session, index_url):
    index_page = session.get(index_url, headers = headers)
    html = index_page.text
    pattern = r'name="__VIEWSTATE" value="(.*?)"'
    __VIEWSTATE = re.findall(pattern, html)
    return __VIEWSTATE[0]

# 获取前端动态码
def get___VIEWSTATE_by_html(session, html_text):
    html = html_text
    pattern = r'name="__VIEWSTATE" value="(.*?)"'
    __VIEWSTATE = re.findall(pattern, html)
    return __VIEWSTATE[0]

# 获取前端动态码
def get___VIEWSTATEGENERATOR(session):
    index_url = 'http://210.44.159.4'
    index_page = session.get(index_url, headers=headers)
    html = index_page.text

    pattern = r'name="__VIEWSTATEGENERATOR" value="(.*?)"'
    __VIEWSTATEGENERATOR = re.findall(pattern, html)
    return __VIEWSTATEGENERATOR[0]

# 获取前端动态码
def get___VIEWSTATEGENERATOR_by_url(session, index_url):
    index_page = session.get(index_url, headers=headers)
    html = index_page.text

    pattern = r'name="__VIEWSTATEGENERATOR" value="(.*?)"'
    __VIEWSTATEGENERATOR = re.findall(pattern, html)
    return __VIEWSTATEGENERATOR[0]

# 获取前端动态码
def get___VIEWSTATEGENERATOR_by_html(session, html_text):
    html = html_text

    pattern = r'name="__VIEWSTATEGENERATOR" value="(.*?)"'
    __VIEWSTATEGENERATOR = re.findall(pattern, html)
    return __VIEWSTATEGENERATOR[0]

# 获取验证码
def get_CheckCode(session):
    index_url = 'http://210.44.159.4/CheckCode.aspx?'
    '''
    postdata = {
        '__VIEWSTATE': get___VIEWSTATE_by_url(session, index_url),
        '__VIEWSTATEGENERATOR': get___VIEWSTATEGENERATOR_by_url(session, index_url),
    }
    index_page = session.post(index_url, postdata, headers = headers)
'''
    index_page = session.get(index_url, stream=True)
    image = index_page.content

    with open("code.gif", "wb") as jpg:
        jpg.write(image)

    code = input('验证码是：')
    return code

# 提取用户姓名
def getUserName(home_text):
    page = etree.HTML(home_text)
    username = page.xpath('//*[@id="xhxm"]/text()')[0]
    return (username.split('同学')[0])

# 获取成绩单网页源码
def getReportCard(session, home_text, usernumber, username):
    index_url = 'http://210.44.159.4/'
    page = etree.HTML(home_text)
    report_card_url = page.xpath('//*[@onclick="GetMc(\'成绩查询\');"]/@href')
    full_link = index_url+report_card_url[0]
    referer = 'http://210.44.159.4/xscj.aspx?xh='+usernumber+'&xm='+urllib.parse.quote(username.encode("gbk"))+'&gnmkdm=N121605'

    headers['Referer'] = referer
    get_content = session.get(referer, headers=headers).text

    __VIEWSTATE = get___VIEWSTATE_by_html(session,get_content)
    __VIEWSTATEGENERATOR = get___VIEWSTATEGENERATOR_by_html(session,get_content)

    #postdata['__VIEWSTATE'] = __VIEWSTATE #没用
    #postdata['__VIEWSTATEGENERATOR'] = __VIEWSTATEGENERATOR #没用
    #postdata['ddlXN'] = '' #没用
    #postdata['ddlXQ'] = '' #没用
    postdata['txtQSCJ'] = '0'
    postdata['txtZZCJ'] = '100'
    postdata['Button2'] = '在校学习成绩查询'.encode("gb2312")

    post_content = session.post(referer, data=postdata,headers=headers).text

    return (post_content)

# 提取成绩单信息到list
def getReportCardList(html):
    page = etree.HTML(html)
    datalist = page.findall('.//table[@id="DataGrid1"]/tr')

    report_list = []
    index = 0
    for data in datalist:
        row = data.findall('td')
        row_list = []
        for c in row:
            row_list.append(c.text.strip())
        report_list.append(row_list)
        index += 1

    return (report_list)

# 统计输出学分情况
def printCreditsByList(report_list):
    compulsory_credits = 0
    tongxuan_credits = 0
    xuanxiu_credits = 0
    open_experiment = 0
    total_credits = 0
    Failed_list = []
    subject_count = {}

    isFirstRow = True

    for row in report_list:
        if isFirstRow:
            isFirstRow = False
            continue

        try:
            score = float(row[-6])
            score2 = -1
            credits = float(row[-2])

            if (op.eq(row[-4],'') == False):
                score2 = float(row[-4])

            if subject_count.__contains__(row[1]) == True:
                subject_count[row[1]] += 1
            else:
                subject_count[row[1]] = 1

            if (score >= 60) or (score2 >= 60):
                total_credits += credits
                curriculum_nature = row[2]
                if op.eq(curriculum_nature, '必修课') == True:
                    compulsory_credits += credits
                elif op.eq(curriculum_nature, '通选课') == True:
                    tongxuan_credits += credits
                elif op.eq(curriculum_nature, '选修课') == True:
                    xuanxiu_credits += credits
                elif op.eq(curriculum_nature, '开放实验') == True:
                    open_experiment += credits
            else:
                Failed_list.append(row)
        except Exception as e:
            print (e)
            print('未统计：', row)
            continue


    print ('\n不及格科目历史记录：')
    for row in Failed_list:
        print (row)

    print ('\n')
    print ('必修课：',compulsory_credits)
    print ('通选课：',tongxuan_credits)
    print ('选修课：',xuanxiu_credits)
    print ('开放实验：',open_experiment)
    print ('总学分：',total_credits)

# 将成绩列表输出到txt文件中
def writeReportListToFile(filename, report_card_list):
    f = open(filename, 'w')
    for l in report_card_list:
        #print(l)
        f.write(str(l) + '\n')

# 将成绩列表导入到excel文件中
def exportExcelFromReportList(filename, report_card_list):
    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet('sheet 1')

    row_index = 0
    for row in report_card_list:
        col_index = 0
        for c in row:
            sheet.write(row_index, col_index, c)
            col_index += 1
        row_index+=1

    wbk.save(filename)
    print ('成功导出文件：', filename)

###############################################################################################################
#                                                开始运行
###############################################################################################################
################################
#       在这输入用户名和密码
################################

usernumber = ''
password = ''

################################
#    准备头信息以及发送的数据
################################

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
headers = {
    'User-Agent':user_agent,
           }
session = requests.session()

__VIEWSTATE = get___VIEWSTATE(session)
__VIEWSTATEGENERATOR = get___VIEWSTATEGENERATOR(session)

post_url = 'http://210.44.159.4/default2.aspx'

postdata = {
    '__VIEWSTATE':__VIEWSTATE,
    '__VIEWSTATEGENERATOR':__VIEWSTATEGENERATOR,
    'txtUserName':usernumber,
    'TextBox2':password,
    #'RadioButtonList1':'%D1%A7%C9%FA',
    #'RadioButtonList1':u"学生".encode('gb2312','replace'), #没用
    "Button1":"",
    "lbLanguage":"",
    'txtSecretCode':get_CheckCode(session),
    'hidPdrs':'',
    'hidsc':'',
}

################################
#           发送请求
################################

login_page = session.post(post_url, data=postdata, headers=headers)
login_code = login_page.text

################################
#  若登陆成功，可提取学生姓名
################################

username = getUserName(login_code)

print('#######################################################################################')
print('                               用户名：',username,'')
print('#######################################################################################')

##############################################################################
# 获取成绩单列表（'在校学习成绩查询'那个按钮），统计和打印学分，生成excel文件
##############################################################################

report_card_code = getReportCard(session, login_code, usernumber, username) # 获取成绩单html源代码
report_card_list = getReportCardList(report_card_code) # 解析成绩单html源代码

list_len = len(report_card_list)
if list_len > 0:
    writeReportListToFile(username+'.txt',report_card_list) # 将成绩单输出到txt文件
    printCreditsByList(report_card_list) # 统计学分并输出
    exportExcelFromReportList(username+'.xls', report_card_list) # 将成绩单输出到excel文件
else:
    print ('成绩表为空')


session.close()

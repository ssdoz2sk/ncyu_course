from __future__ import absolute_import, unicode_literals
import json
import os

import requests
from bs4 import BeautifulSoup
from celery import shared_task, chord

from administrator.models import CourseTemp

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

task_args = []
data = {}

year, semester = -1, -1

def init(y, s):
    global year
    global semester
    year, semester = y, s

    global data
    with open(os.path.join(BASE_DIR, 'postData.json'), 'r', encoding='UTF-8') as file:
        data = json.load(file)


def get_course_async(year, semester):
    init(year, semester)
    get_pub_clata3(year, semester)
    get_pub_clata4(year, semester)

    return chord((get_data.s(url, postDict) for url, postDict in task_args))(_save_curriculum_to_db.s())


def get_pub_clata3(year, semester):
    url = "https://web085003.adm.ncyu.edu.tw/pub_clata3.aspx"

    WebTPcode1 = data['clata3']['WebTPcode1']
    WebDiviCode1 = data['clata3']['WebDiviCode1']
    WebDomainNo1 = data['clata3']['WebDomainNo1']

    global task_args

    for code1 in WebDiviCode1:  # 學院
        for code2 in code1:  # 學系
            for domain in WebDomainNo1:  # 課程類別
                for grade in range(1, 5 + 1):  # 年級
                    # time.sleep( 5 )
                    postDict = {
                        'WebPid1': '',
                        'Language': 'zh-TW',
                        'WebYear1': str(year).zfill(3),
                        'WebTerm1': str(semester),
                        'WebPDC99': WebTPcode1[0].split(':')[1],
                        'WebDiviCode1': code2,
                        'WebDomainNo1': domain,
                        'WebCrsGrade1': str(grade)
                    }
                    task_args.append((url, postDict,))


def get_pub_clata4(year, semester):
    url = "https://web085003.adm.ncyu.edu.tw/pub_clata4.aspx"

    WebPDC99 = data['clata4']['WebPDC99']
    WebDomainNo1 = data['clata4']['WebDomainNo1']

    global task_args

    for pdc_index in range(len(WebPDC99)):
        for domain in WebDomainNo1[pdc_index]:  # 課程類別
            for grade in range(1, 5 + 1):  # 年級
                # time.sleep( 5 )
                postDict = {
                    'WebPid1': '',
                    'Language': 'zh-TW',
                    'WebYear1': str(year).zfill(3),
                    'WebTerm1': str(semester),
                    'WebPDC99': WebPDC99[pdc_index],
                    'WebDomainNo1': domain,
                    'WebCrsGrade1': str(grade)
                }
                task_args.append((url, postDict,))


@shared_task(retry_kwargs={'max_retries': 5})
def get_data(url, postDict):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
    }

    response = requests.post(url, data=postDict, headers=headers)

    data = response.text
    soup = BeautifulSoup(data, "html5lib")

    table = soup.find('table', border=1)
    trs = table.find_all('tr')

    if trs[1].find('td').get_text() == '\n查無任何開課資料!!\n':
        return

    data = []
    for index in range(1, len(trs)):
        tds = trs[index].find_all('td')
        part = []
        for index2 in range(len(tds)):
            part.append(tds[index2].get_text())
        data.append(part)

    return data

@shared_task
def _save_curriculum_to_db(data_list):

    course_list = []

    for sublist in data_list:
        if sublist:
            for data in sublist:
                name = data[2].strip()
                course_num = data[3].strip()
                department = data[4].strip()

                if len(data) >= 25:
                    college = data[6].strip()
                else:
                    college = data[5].strip()

                grade = data[-16].strip()
                if len(grade) == 0:
                    grade = None

                course_type = data[-14].strip()
                credit = data[-13].strip()
                if len(credit) == 0:
                    credit = 0

                teacher_name = data[-8].strip()
                student_limit = data[-3].strip()
                if len(student_limit) == 0:
                    student_limit = 0
                student_select = data[-2].strip()
                if len(student_select) == 0:
                    student_select = 0

                weeks = data[-7].strip().split()
                dayparts = data[-6].strip().split()
                schooltime = []

                if len(weeks) == len(dayparts):
                    for index, w in enumerate(weeks):
                        schooltime.append({'week': w, 'daypart': dayparts[index]})

                course = CourseTemp(
                    name=name,
                    year=year,
                    semester=semester,
                    credit=credit,
                    course_num=course_num,
                    course_type=course_type,
                    grade=grade,
                    department=department,
                    college=college,
                    schooltime=schooltime,
                    teacher_name=teacher_name,
                    student_limit=student_limit,
                    student_select=student_select
                )

                course_list.append(course)

    CourseTemp.objects.bulk_create(course_list)

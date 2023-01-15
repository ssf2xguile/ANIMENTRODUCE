from datetime import datetime
from math import ceil
import requests, bs4
import json
import pprint

def create_single_text_message(message):
    cool = {1: '冬アニメ', 2: '春アニメ', 3: '夏アニメ', 4: '秋アニメ'}
    msg_array = message.split('-')  # メッセージを分割 例：今期アニメ または 今期アニメ-アニメ名
    first_argument = msg_array[0]  # 今期アニメ 、来期アニメ 、前期アニメ 、ヘルプ
    try:
        second_argument = msg_array[1]  # アニメ名
    except IndexError:
        second_argument = None

    if (first_argument == '今期アニメ'):
        year = datetime.now().year  # 今年の年を取得
        course = ceil(datetime.now().month / 3) # 今クールの値を取得 例：1~3月なら1、4~6月なら2、7~9月なら3、10~12月なら4
        data = callapi(year, course)
        if (second_argument != None):
            for i in range(len(data)):
                if(data[i]['title'] == second_argument):
                    message = data[i]['title'] + '\n' + data[i]['public_url'] + '\n' + str(year) + "年" +cool[course]
        else:
            message = ''
            for i in range(len(data)):
                message += data[i]['title'] + '\n'
    elif (first_argument == '来期アニメ'):
        year, course = checkcourse(datetime.now().year, ceil(datetime.now().month / 3)+1)
        data = callapi(year, course)
        if (second_argument != None):
            for i in range(len(data)):
                if(data[i]['title'] == second_argument):
                    message = data[i]['title'] + '\n' + data[i]['public_url'] + '\n' + str(year) + "年" +cool[course]
        else:
            message = ''
            for i in range(len(data)):
                message += data[i]['title'] + '\n'
    elif (first_argument == '前期アニメ'):
        year, course = checkcourse(datetime.now().year, ceil(datetime.now().month / 3)-1)
        data = callapi(year, course)
        if (second_argument != None):
            for i in range(len(data)):
                if(data[i]['title'] == second_argument):
                    message = data[i]['title'] + '\n' + data[i]['public_url'] + '\n' + str(year) + "年" +cool[course]
        else:
            message = ''
            for i in range(len(data)):
                message += data[i]['title'] + '\n'
    elif (first_argument == 'ヘルプ'):
        message = 'このBotはアニメの情報を提供するよ。ボタンの使い方を説明するね。\n' + '『今期アニメ』\n『来期アニメ』\n『前期アニメ』\nそれぞれの時期に合ったアニメ情報が得られるよ。\n' + '『ヘルプ』\nこのメッセージを表示できるよ。'
    else:
        message = 'なんか君不正操作しようとしてない？'

    test_message = [
                {
                    'type': 'text',
                    'text': message
                },
            ]
    return test_message

def callapi(year, course):
    # 取得先のURLに年とクールを指定して、APIを呼び出す
    API_URL = f'https://api.moemoe.tokyo/anime/v1/master/{year}/{course}'
    res = requests.get(API_URL)
    data = json.loads(res.text)
    #pprint.pprint(data[0:2]) # デバッグ用
    return data

def checkcourse(year, course):
    # courseの値が5になったら、次の年の1期になるので、年を1増やす。一方で、courseの値が0になったら、前の年の4期になるので、年を1減らす。
    if (course == 5):
        year += 1
        course = 1
    elif (course == 0):
        year -= 1
        course = 4
    return year, course

def create_img(url):
    # og:imageのURLを取得する
    result = requests.get(url)
    soup = bs4.BeautifulSoup(result.content, 'html.parser')
    og_image_elems  = soup.select('[property="og:image"]')
    img_url = og_image_elems[0].get("content")
    img_dict = {
        'type': 'image',
        'originalContentUrl': img_url,
        'previewImageUrl': img_url
    }
    return img_dict

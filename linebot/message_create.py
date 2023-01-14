from datetime import datetime
from math import ceil
import requests
import json
import pprint

def create_single_text_message(message):
    msg_array = message.split('-')  # メッセージを分割 例：ANIMENTRODUCE-今期アニメ または ANIMENTRODUCE-今期アニメ-アニメ名
    first_argument = msg_array[0]  # ANIMENTRODUCE、ヘルプ
    try:
        second_argument = msg_array[1]  # 今期アニメ、来期アニメ、前期アニメ
    except IndexError:
        second_argument = None
    try:
        third_argument = msg_array[2]  # アニメ名 この引数は任意
    except IndexError:
        third_argument = None
    if (first_argument == 'ANIMENTRODUCE'):
        if (second_argument == '今期アニメ'):
            year = datetime.now().year  # 今年の年を取得
            course = ceil(datetime.now().month / 3) # 今クールの値を取得 例：1~3月なら1、4~6月なら2、7~9月なら3、10~12月なら4
            data = callapi(year, course)
            if (third_argument != None):
                    if(data[i]['title'] == msg_array[2]):
                        message = data[i]['title'] + '\n' + data[i]['public_url'] + '\n#' + data[i]['twitter_hash_tag']
                    else:
                        message = 'そのアニメは今期に放送されていないよ。'
            else:
                message = ''
                for i in range(len(data)):
                    message += data[i]['title'] + '\n'
        elif (second_argument == '来期アニメ'):
            year, course = checkcourse(datetime.now().year, ceil(datetime.now().month / 3)+1)
            data = callapi(year, course)
            if (third_argument != None):
                for i in range(len(data)):
                    if(data[i]['title'] == msg_array[2]):
                        message = data[i]['title'] + '\n' + data[i]['public_url'] + '\n#' + data[i]['twitter_hash_tag']
                    else :
                        message = 'そのアニメは来期に放送されないよ。'
            else:
                message = ''
                for i in range(len(data)):
                    message += data[i]['title'] + '\n'
        elif (second_argument == '前期アニメ'):
            year, course = checkcourse(datetime.now().year, ceil(datetime.now().month / 3)-1)
            data = callapi(year, course)
            if (third_argument != None):
                for i in range(len(data)):
                    if(data[i]['title'] == msg_array[2]):
                        message = data[i]['title'] + '\n' + data[i]['public_url'] + '\n#' + data[i]['twitter_hash_tag']
                    else:
                        message = 'そのアニメは前期に放送されていないよ。'
            else:
                message = ''
                for i in range(len(data)):
                    message += data[i]['title'] + '\n'
        else:
            message = '不正操作しようとしてない？'
    elif (first_argument == 'ヘルプ'):
        message = 'このBotはアニメの情報を提供するよ。ボタンの使い方を説明するね。\n' + '『今期アニメ』\n『来期アニメ』\n『前期アニメ』\nそれぞれの時期に合ったアニメ情報が得られるよ。\n' + '『ヘルプ』\nこのメッセージを表示できるよ。'
    else:
        message = 'なんか君おかしいよ。'

    test_message = [
                {
                    'type': 'text',
                    'text': message
                }
            ]
    return test_message

def callapi(year, course):
    # 取得先のURLに年とクールを指定して、APIを呼び出す
    API_URL = f'https://api.moemoe.tokyo/anime/v1/master/{year}/{course}'
    res = requests.get(API_URL)
    data = json.loads(res.text)
    # pprint.pprint(data) # デバッグ用
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
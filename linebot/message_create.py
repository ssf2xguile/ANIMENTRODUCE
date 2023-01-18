from datetime import datetime
from math import ceil
import requests, bs4
import json
import pprint
import random

def create_single_text_message(message):
    msg_array = message.split('-')  # メッセージを分割 例：今期アニメ または 今期アニメ-アニメ名
    first_argument = msg_array[0]  # 今期アニメ 、来期アニメ 、前期アニメ 、ヘルプ
    flex_message = None
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
                    img_url = create_img(data[i]['public_url'])
                    flex_message_json = create_anime_info_json(year, course, data[i], img_url)
                    flex_message = json.loads(flex_message_json)
        else:
            flex_message_json = create_anime_list_json(first_argument, data)
            flex_message = json.loads(flex_message_json)
    elif (first_argument == '来期アニメ'):
        message = 'すまん、来期アニメのデータ取れないんだわ'
    elif (first_argument == '前期アニメ'):
        year, course = checkcourse(datetime.now().year, ceil(datetime.now().month / 3)-1)
        data = callapi(year, course)
        if (second_argument != None):
            for i in range(len(data)):
                if(data[i]['title'] == second_argument):
                    img_url = create_img(data[i]['public_url'])
                    flex_message_json = create_anime_info_json(year, course, data[i], img_url)
                    flex_message = json.loads(flex_message_json)
        else:
            flex_message_json = create_anime_list_json(first_argument, data)
            flex_message = json.loads(flex_message_json)
    elif (first_argument == 'ヘルプ'):
        message = 'このBotはアニメの情報を提供するよ。ボタンの使い方を説明するね。\n' + '『今期アニメ』\n『来期アニメ』\n『前期アニメ』\nそれぞれの時期に合ったアニメ情報が得られるよ。\n' + '『ヘルプ』\nこのメッセージを表示できるよ。'
    else:
        message = 'なんか君不正操作しようとしてない？'

    if( flex_message != None):
        test_message = [
                    flex_message
                ]
        return test_message
    else:
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
    return img_url

def create_anime_info_json(year, course, data, img_url):
    # 送信するJSONデータを作成する
    cool = {1: '冬アニメ', 2: '春アニメ', 3: '夏アニメ', 4: '秋アニメ'}
    anime_info_json = '''{
    "type": "flex",
    "altText": "アニメ詳細情報",
    "contents": {
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": "''' + img_url + '''",
                "size": "full",
                "aspectRatio": "2:1",
                "action": {
                "type": "uri",
                "uri": "''' + data['public_url'] + '''"
                },
                "aspectMode": "cover"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": "''' + data['title'] + '''",
                    "weight": "bold",
                    "size": "xl"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "baseline",
                        "spacing": "sm",
                        "contents": [
                        {
                            "type": "text",
                            "text": "タイトル",
                            "color": "#aaaaaa",
                            "size": "sm",
                            "flex": 2,
                            "wrap": true
                        },
                        {
                            "type": "text",
                            "text": "''' + data['title'] + '''",
                            "wrap": true,
                            "color": "#666666",
                            "size": "sm",
                            "flex": 5
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "spacing": "sm",
                        "contents": [
                        {
                            "type": "text",
                            "text": "URL",
                            "color": "#aaaaaa",
                            "size": "sm",
                            "flex": 2,
                            "wrap": true
                        },
                        {
                            "type": "text",
                            "text": "''' + data['public_url'] + '''",
                            "wrap": true,
                            "color": "#666666",
                            "size": "sm",
                            "flex": 5
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "spacing": "sm",
                        "contents": [
                        {
                            "type": "text",
                            "text": "クール",
                            "color": "#aaaaaa",
                            "size": "sm",
                            "flex": 2,
                            "wrap": true
                        },
                        {
                            "type": "text",
                            "text": "''' + str(year) + '''年''' + cool[course] + '''",
                            "wrap": true,
                            "color": "#666666",
                            "size": "sm",
                            "flex": 5
                        }
                        ]
                    }
                    ]
                }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                    "type": "uri",
                    "label": "公式サイト",
                    "uri": "''' + data['public_url'] + '''"
                    }
                }
                ],
                "flex": 0
            }
        }
    }'''
    return anime_info_json

def create_anime_list_json(first_argument, data):
    # 送信するJSONデータを作成する APIの仕様なのか30件までしかデータが作成できない
    random.shuffle(data)
    anime_list_json = '''{
    "type": "flex",
    "altText": "'''+ first_argument +'''リスト",
    "contents": {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "'''+ first_argument +'''リスト",
                    "weight": "bold",
                    "size": "md",
                    "align": "center"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "spacing": "sm",
                    "contents": ['''
    for i in range(30):
        anime_list_json += '''
                        {
                            "type": "button",
                            "action": {
                            "type": "message",
                            "label": "''' +data[i]['title']+'''",
                            "text": "'''+ first_argument +'''-'''+ data[i]['title'] + '''"
                            },
                            "height": "sm"
                        },'''

    anime_list_json += '''
                        {
                            "type": "button",
                            "action": {
                            "type": "message",
                            "label": "''' +data[-1]['title']+'''",
                            "text": "'''+ first_argument +'''-'''+ data[-1]['title'] + '''"
                            },
                            "height": "sm"
                        }
                    ]
                }
            ]
        }
    }
    }'''
    return anime_list_json
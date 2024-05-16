import argparse
import datetime
import json
import os
from zipfile import ZipFile

import imagehash
from PIL import Image
from bs4 import BeautifulSoup

page_data = {}

parser = argparse.ArgumentParser(
    prog='difference_parser',
    description='Show top lines from each file')
parser.add_argument('filenames', nargs='+')
args = parser.parse_args()

chat_id = args.filenames[0]


def has_class_but_no_id(tag):
    return tag.has_attr('div', class_='photo_wrap clearfix pull_left')


html_doc = open("ChatExport_2024-05-15/messages.html")
messages = BeautifulSoup(html_doc, 'html.parser')
messages_list = messages.find_all('a', class_='photo_wrap')
for message in messages_list:
    message_id = ''
    photo_ref = message['href']
    print(photo_ref)
    file = open('ChatExport_2024-05-15/' + photo_ref, 'rb')
    image_hash = imagehash.dhash(Image.open(file))
    hash_key = str(image_hash)
    print(hash_key)
    if message.parent.parent.parent.has_attr('id'):
        message_id = message.parent.parent.parent['id'][7:]
    else:
        message_id = message.parent.parent.parent.parent['id'][7:]
    image_key = str(image_hash) + '^' + chat_id
    print(message_id)
    page_data[image_key] = message_id

page_data = dict(reversed(list(page_data.items())))
if os.path.exists('hash_data.zip'):
    os.rename('hash_data.zip', 'hash_data.zip:' + str(datetime.datetime.now()))

with ZipFile('hash_data.zip', 'x') as myzip:
    ZipFile.writestr(myzip, 'hash_data.json', data=json.dumps(page_data))

with open('hash_data.zip', 'rb') as t:
    with ZipFile(t, 'r') as json_data:
        json_str = json.load(json_data.open('hash_data.json'))
for k, v in json_str.items():
    print(k + "   " + v)
print(len(json_str))

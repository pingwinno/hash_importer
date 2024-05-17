import argparse
import datetime
import json
import os
from zipfile import ZipFile

import imagehash
from PIL import Image
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(
    prog='difference_parser',
    description='Show top lines from each file')
parser.add_argument('--id', type=str)
parser.add_argument('--folder', type=str)
args = parser.parse_args()

chat_id = args.id
args.folder = os.path.join('chat_dump/', args.folder)
counter = 0


def has_class_but_no_id(tag):
    return tag.has_attr('div', class_='photo_wrap clearfix pull_left')


def parse_html(html_file):
    zipfile_template = f'chat_dump/hash_data-{counter}.zip'
    page_data = {}
    html_doc = open(html_file)
    messages = BeautifulSoup(html_doc, 'html.parser')
    messages_list = messages.find_all('a', class_='photo_wrap')
    for message in messages_list:
        photo_ref = message['href']
        print(photo_ref)
        file = open(os.path.join(args.folder, photo_ref), 'rb')
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
    if os.path.exists(zipfile_template):
        os.rename(zipfile_template, zipfile_template + ':' + str(datetime.datetime.now()))

    with ZipFile(zipfile_template, 'x') as myzip:
        ZipFile.writestr(myzip, 'hash_data.json', data=json.dumps(page_data))

    with open(zipfile_template, 'rb') as t:
        with ZipFile(t, 'r') as json_data:
            json_str = json.load(json_data.open('hash_data.json'))

    print(zipfile_template + ' has ' + str(len(json_str)) + ' elements')


for file in os.listdir(args.folder):
    if file.endswith(".html"):
        parse_html(os.path.join(args.folder, file))
        counter += 1

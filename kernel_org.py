#! /usr/bin/python3
import requests as req
import time
import logging
from bs4.element import *
from bs4 import BeautifulSoup

chat_id = "<your channel id>"
bot_id = "<your bot id>"

logging.basicConfig(level=logging.INFO,
                    filename="<path to save logs>",
                    filemode="w",
                    format=
                    "%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s"
                    )

def fetch_once():
    ret = []
    try:
        res = req.get("https://kernel.org")
        bs = BeautifulSoup(res.text,features="html.parser")
        table = bs.find("table", id="releases")
        for row in table.children:
            if type(row) != Tag:
                continue
            ret.append(row.find_all("td")[1].string)
        logging.info(ret)
    except BaseException as e:
        logging.error(e)
        return None
    return ret


def list_cmp(list_old, list_new):
    ret = []
    for element in list_new:
        if list_old.count(element) == 0:
            ret.append(element)
    return ret

def send(what):
    status = 0
    while status != 200:
        logging.info("Try sending "+what)
        status = req.post("https://api.telegram.org/bot" + bot_id + "/sendMessage", 
           {"parse_mode":"Markdown", "text":what, "chat_id":chat_id}).status_code

last_result = fetch_once()
while True:
    time.sleep(300)
    next_result = fetch_once()
    if next_result is None:
        continue
    for item in list_cmp(last_result, next_result):
        send("*New Linux Kernel Release*\n["+item+"](https://www.kernel.org/)")
    last_result = next_result

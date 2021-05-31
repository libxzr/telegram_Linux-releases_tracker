#!/usr/bin/python3

import time
import logging

import requests as req
from bs4 import BeautifulSoup
from bs4.element import Tag


chat_id = "<your channel id>"
bot_id = "<your bot id>"

logging.basicConfig(
    level=logging.INFO,
    filename="<path to save logs>",
    filemode="w",
    format="%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s"
)

def fetch_once():
    ret = []
    try:
        res = req.get("https://kernel.org")
        bs = BeautifulSoup(res.text, features="html.parser")
        table = bs.find("table", id="releases")
        for row in table.children:
            if not isinstance(row, Tag):
                continue
            ret.append(next(row.find_all("td")[1].strings))
        logging.info(ret)
    except Exception as e:
        logging.error(e)
        return
    return ret

def list_cmp(list_old, list_new):
    return list(set(list_new) - set(list_old))

def send(what):
    status = 0
    while status != 200:
        logging.info("Try sending "+what)
        status = req.post(
                "https://api.telegram.org/bot%s/sendMessage" % bot_id,
                {"parse_mode": "Markdown", "text": what, "chat_id": chat_id},
            ).status_code

last_result = fetch_once()
while True:
    time.sleep(300)
    next_result = fetch_once()
    if next_result is None:
        continue
    for item in list_cmp(last_result, next_result):
        send("*New Linux Kernel Release*\n[%s](https://www.kernel.org/)" % item)
    last_result = next_result

#!/usr/bin/python3

import time
import os

import requests as req
from bs4 import BeautifulSoup
from bs4.element import Tag

try:
    chat_id = os.environ["KTRACKER_CHAT_ID"]
    bot_id = os.environ["KTRACKER_BOT_ID"]
except:
    print("You must provide both KTRACKER_CHAT_ID and KTRACKER_BOT_ID. Export them as environment variables.")
    exit(1)

def fetch_once():
    ret = set()
    try:
        res = req.get("https://kernel.org", timeout=10)
        bs = BeautifulSoup(res.text, features="html.parser")
        table = bs.find("table", id="releases")
        for row in table.children:
            if not isinstance(row, Tag):
                continue
            ret.add(next(row.find_all("td")[1].strings))
        print(ret)
    except Exception as e:
        print(e)
        return
    return ret

def send(what):
    status = 0
    while status != 200:
        print("Try sending " + what)
        status = req.post(
                "https://api.telegram.org/bot%s/sendMessage" % bot_id,
                {"parse_mode": "Markdown", "text": what, "chat_id": chat_id},
                timeout=10).status_code

print("Service started with chat_id = %s bot_id = %s" % (chat_id, bot_id))
last_result = fetch_once()
while True:
    time.sleep(300)
    next_result = fetch_once()
    if next_result is None:
        continue
    for item in next_result - last_result:
        send("*New Linux Kernel Release*\n[%s](https://www.kernel.org/)" % item)
    last_result = next_result

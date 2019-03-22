import urllib.request
import urllib.parse
import os
import xml.etree.ElementTree as ET
import datetime
import json
import re
import redis

url = os.getenv("RSS_URL")
webhookurl = os.getenv("SLACK_WEBHOOK_URL")
searchstrings = (os.getenv("SERACH_STRINGS")).split(",")
redishost = os.getenv("REDIS_HOST")
redisport = int(os.getenv("REDIS_PORT"))
expireseconds = int(os.getenv("EXPIRE_SECONDS"))

req = urllib.request.Request(url)
res = urllib.request.urlopen(req)
xml_string = res.read()

root = ET.fromstring(xml_string)
for item in root.iter("item"):
    title = item.find("title").text
    link = item.find("link").text
    is_notify = False
    for string in searchstrings:
        pattern = string
        text = title
        searchOB = re.search(pattern, text, re.IGNORECASE)
        if searchOB:
            is_notify = True

    if not is_notify:
        continue

    conn_pool = redis.ConnectionPool(host=redishost, port=redisport, db=0)
    redis_conn = redis.StrictRedis(connection_pool=conn_pool)

    if not redis_conn.exists(link):
        url = webhookurl
        method = "POST"
        headers = {"Content-Type": "application/json"}
        data = { "text": title + "\n" + link }
        json_data = json.dumps(data).encode("utf-8")
        
        request = urllib.request.Request(url, data=json_data, method=method, headers=headers)
        with urllib.request.urlopen(request) as response:
            response_body = response.read().decode("utf-8")
            print(response_body)

        redis_conn.set(link, title, ex=expireseconds)

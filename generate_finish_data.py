import requests
from bs4 import BeautifulSoup
import lxml
import re
import json
import time
import datetime
import csv
import asyncio
import aiohttp

from config import MAX_SUB_COUNT, PROXY_ADDRESS, PROXY_LOGIN, PROXY_PASS

from work_with_json import json_dump, json_load

finish_data_list = []

exceptions = []

error_count = 0

def check_channel_link(cache, channel_link):
	if channel_link not in cache:
		return False

	return cache[channel_link]


async def return_finish_data(session, one_list, proxy_auth, cache):
	global error_count
	url = one_list[-1]
	try:
		if not any(one_list[0] in video_data for video_data in finish_data_list):
			check_channel = check_channel_link(cache, url) 
			if not check_channel:
				async with session.get(url = url, proxy = f"http://{PROXY_ADDRESS}", proxy_auth = proxy_auth) as response:
					response_text = await response.text()
					soup = BeautifulSoup(response_text, 'lxml')
					search = soup.find_all("script")
					data = str(search[33]).split("var ytInitialData = ")[-1].split(";</script>")[0]
					RESULT = json.loads(data)
					try:
						count = RESULT["header"]["c4TabbedHeaderRenderer"]["subscriberCountText"]["simpleText"].split(' ')[0]
						if 'K' in count:
							count = count[:-1]
							count = float(count) * 1000
						elif 'M' in count:
							count = count[:-1]
							count = float(count) * 1000000
						else:
							count = int(count)
					except:
						count = 0
				try:
					is_monetization = RESULT["responseContext"]["serviceTrackingParams"][0]["params"][3]["value"]
				except Exception as ex:
					if str(ex) not in exceptions:
						exceptions.append(str(ex))
					is_monetization = "unknown"

					
				cache[url] = [count, is_monetization]
				json_dump(cache)
			else:
				is_monetization = check_channel[1]
				count = check_channel[0]

			if count < MAX_SUB_COUNT:
					print(one_list, count)
					one_list.append(int(count))
					one_list.append(is_monetization)
					finish_data_list.append(one_list)

	except Exception as ex:
		error_count+=1
		if str(ex) not in exceptions:
			exceptions.append(str(ex))



async def finish_data(youtube_data):
	channels_data = json_load()
	print('длинна кэша: ', len(channels_data))
	session = aiohttp.ClientSession()
	proxy_auth = aiohttp.BasicAuth(PROXY_LOGIN, PROXY_PASS)
	finish_tasks = []
	for youtube_list in youtube_data:
		last_task = asyncio.create_task(return_finish_data(session, youtube_list, proxy_auth, channels_data))
		finish_tasks.append(last_task)

	await asyncio.gather(*finish_tasks)
	await session.close()
	print(exceptions)
	print('error count: ' + str(error_count))
	return finish_data_list
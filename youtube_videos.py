import requests
from bs4 import BeautifulSoup
import lxml
import json
import csv
import asyncio
import aiohttp

from config import MIN_VIEW_COUNT, SHORTS

youtube_data = []
exceptions = []

all_count = 0
good_count = 0
error_count = 0

shorts_count = 0


async def get_page_data(session, word, mode):
	global all_count, good_count, error_count, shorts_count

	url = f"https://www.youtube.com/results?search_query={word}&sp={mode}"
	async with session.get(url = url) as response:
		response_text = await response.text()

		soup = BeautifulSoup(response_text, 'lxml')
		search = soup.find_all('body')[0]
		res_search = search.find_all('script')
		try:
			data = "".join(res_search[-6].text.split(' = ')[1:])
			RESULT = json.loads(data[:-1])
		except Exception as ex:
			print(ex, data, len(data))
			return []
		CONTENT_RES = RESULT['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']

		SECTION_RES = CONTENT_RES['contents'][0]['itemSectionRenderer']

		for i in range(len(SECTION_RES['contents'])):
			try:
				VIDEO_INFO = SECTION_RES['contents'][i]['videoRenderer']
				video_link_type = VIDEO_INFO['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']
				if 'shorts' in video_link_type:
					shorts_count+=1
					if not SHORTS:
						continue
				VIDEO_LINK = 'https://www.youtube.com'+str(video_link_type)
				try:
					VIDEO_VIEWS = int(VIDEO_INFO['viewCountText']['simpleText'].split(' ')[0].replace(u'\xa0', u'').replace(',',''))
				except Exception as ex:
					VIDEO_VIEWS = 0
				try:
					VIDEO_CHANELL_LINK = 'https://www.youtube.com'+str(VIDEO_INFO['longBylineText']['runs'][0]['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url'])
				except:
					continue
				# print([VIDEO_LINK,VIDEO_VIEWS, VIDEO_CHANELL_LINK])
				all_count+=1
				if VIDEO_VIEWS > MIN_VIEW_COUNT:
					good_count+=1
					youtube_data.append([VIDEO_LINK,VIDEO_VIEWS, VIDEO_CHANELL_LINK])
			except Exception as ex:
				error_count+=1
				if str(ex) not in exceptions:
					exceptions.append(str(ex))
				pass


async def gather_data(word_list, mode):
	"""creating a list of tasks for get pages data"""
	session = aiohttp.ClientSession()
	tasks = []
	try:
		for word in word_list:
			task = asyncio.create_task(get_page_data(session, word, mode))
			tasks.append(task)
		await asyncio.gather(*tasks)
		print('----------------------------')
		print(exceptions)
		print("all count: " + str(all_count))
		print("good count: " + str(good_count))
		print("error count: " + str(error_count))
		print("shorts count: " + str(shorts_count))
		await session.close()
		return youtube_data
	except Exception as ex:
		print(ex)
		await session.close()
		try:
			return youtube_data
		except:
			return []



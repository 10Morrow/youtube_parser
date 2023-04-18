import asyncio
import aiohttp
from functools import partial

from config import PROXY_ADDRESS, PROXY_LOGIN, PROXY_PASS, MAX_SUB_COUNT
from services import parse_data_by_channel_subs, check_channel_link, json_dump, json_load
from logger import get_logger

logger = get_logger("final_parsing")

finish_data_list = []


async def check_list_by_sub_count(session: aiohttp.ClientSession, proxy_auth: aiohttp.BasicAuth,
							cache: dict, one_list: list) -> None:
	"""check subscribers count on video owner's channel
	and return this data if count more than MAX_SUB_COUNT (from config.py)"""

	global finish_data_list

	channel_url, video_url = one_list[-1], one_list[0]
	if not any(video_url in video_data for video_data in finish_data_list):

		channel_in_cache = check_channel_link(cache, channel_url)

		if not channel_in_cache:
			try:
				async with session.get(url=channel_url, proxy=f"http://{PROXY_ADDRESS}",
									proxy_auth=proxy_auth) as response:
					response_text = await response.text()
			except aiohttp.TooManyRedirects:
				logger.info("too many redirects error")
				return None
			filtered_data = parse_data_by_channel_subs(response_text, one_list, cache, channel_url)
			if filtered_data["success"]:
				finish_data_list.append(filtered_data["checked_data"])
		else:
			is_monetization = channel_in_cache[1]
			count = channel_in_cache[0]
			if count < MAX_SUB_COUNT:
				one_list += [count, is_monetization]
				finish_data_list.append(one_list)


def create_task_for_finish_data(session: aiohttp.ClientSession, proxy_auth,
								cache: dict, youtube_list: list) -> asyncio.Task:

	return asyncio.create_task(check_list_by_sub_count(session, proxy_auth, cache, youtube_list))


async def finish_data(youtube_data: list) -> list:
	"""returns the finished parsing result, which has been filtered by channel subscribers"""
	cache = json_load()
	logger.info(f"cache amount is {len(cache)}")
	session = aiohttp.ClientSession()
	proxy_auth = aiohttp.BasicAuth(PROXY_LOGIN, PROXY_PASS)
	partial_function = partial(create_task_for_finish_data, session, proxy_auth, cache)
	finish_tasks = list(map(partial_function, youtube_data))
	await asyncio.gather(*finish_tasks)
	await session.close()
	return finish_data_list

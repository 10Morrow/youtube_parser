import asyncio
import aiohttp
from aiohttp import ClientSession
from functools import partial

from services import parse_web_page_by_our_settings
youtube_data = []


async def get_page_data(session, mode: str, word: str, ) -> None:
	"""parse data and add to youtube_data list"""
	global youtube_data

	url = f"https://www.youtube.com/results?search_query={word}&sp={mode}"
	async with session.get(url=url) as response:
		response_text = await response.text()
		if response_text:
			page_data = parse_web_page_by_our_settings(response_text)
			if page_data["success"]:
				youtube_data += page_data["parsed_videos"]


def create_task_for_asyncio(session: ClientSession, mode: str, word: str) -> asyncio.Task:
	return asyncio.create_task(get_page_data(session, mode, word))


async def gather_data(word_list: list, mode: str) -> list:
	"""creating a list of tasks for get_page_data function"""
	global youtube_data
	session = aiohttp.ClientSession()

	try:
		partial_function = partial(create_task_for_asyncio, session, mode)
		tasks = list(map(partial_function, word_list))
		await asyncio.gather(*tasks)
		await session.close()

		return youtube_data
	except Exception as ex:
		print(ex)
		await session.close()
		try:
			return youtube_data
		except:
			return []

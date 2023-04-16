import sys
import asyncio

from config import PARTS_COUNT, WORDS_FILE, YOUTUBE_FILTERS
from services import create_word_list, write_data

from youtube_videos import gather_data
from generate_finish_data import finish_data


youtube_data = []
finish_data_list = []


def main():
	word_list = create_word_list(WORDS_FILE)
	mode = int(input("""choose a mode for parsing:
1.parse today by views a long videos
2.parse today by views all videos
3.parse week by views a long videos

info:
long video - from 4 to 20 minutes.\n\n:"""))

	mode = list(YOUTUBE_FILTERS.values())[mode-1]
	print('\n[+] Script start working')
	count = 1
	for i in range(PARTS_COUNT, len(word_list), PARTS_COUNT):

		part_of_words = word_list[i-PARTS_COUNT:i]
		print(f"start work with words from {i-PARTS_COUNT} till {i}")

		if sys.platform == 'win32':
			asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
		else:
			asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())

		relevant_video_data = asyncio.run(gather_data(part_of_words, mode))

		if relevant_video_data:
			finished_data_list = asyncio.run(finish_data(relevant_video_data))
		else:
			continue

		if finished_data_list:
			write_data(finish_data_list, count)
		count += 1
		print(f'finish {i} words.')

	print("[+] parsing finished")


if __name__ == "__main__":
	main()

import sys
import asyncio
import time
from config import PARTS_COUNT, WORDS_FILE, YOUTUBE_FILTERS
from services import create_word_list, write_data
from parsing_by_words_and_views import gather_data
from final_parsing_by_sub_count import finish_data
from logger import get_logger

logger = get_logger("run_parser")


def main():
	"""start full process of parsing"""

	word_list = create_word_list(WORDS_FILE)
	mode = int(input("""choose a mode for parsing:
1.parse today by views a long videos
2.parse today by views all videos
3.parse week by views a long videos

info:
long video - from 4 to 20 minutes.\n\n:"""))
	logger.info(f"start in {mode} mode")
	mode = list(YOUTUBE_FILTERS.values())[mode-1]
	count = 1
	for i in range(PARTS_COUNT, len(word_list), PARTS_COUNT):
		t1 = time.time()
		part_of_words = word_list[i-PARTS_COUNT:i]
		logger.info(f"start work with words from {i-PARTS_COUNT} till {i}")

		if sys.platform == 'win32':
			asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
		else:
			asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())

		relevant_video_data = asyncio.run(gather_data(part_of_words, mode))
		if relevant_video_data:
			logger.info(f"was parsed by views {len(relevant_video_data)}")
			finished_data_list = asyncio.run(finish_data(relevant_video_data))
		else:
			logger.info(f"have no relevant videos from {i-PARTS_COUNT} till {i}")
			continue

		if finished_data_list:
			logger.info(f"will be written {len(finished_data_list)} lines")
			write_data(finished_data_list, count)
			t2 = time.time()
			logger.info(f"was parsed for {t2-t1} s.")
			count += 1
		else:
			logger.info(f"have no good from {len(relevant_video_data)} relevant videos.")

	logger.info("[+] parsing finished")


if __name__ == "__main__":
	logger.info("script started")
	main()

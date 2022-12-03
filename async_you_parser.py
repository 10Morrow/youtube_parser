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

from config import PARTS_COUNT, WORDS_FILE, JSON_FILE
from youtube_videos import gather_data
from generate_finish_data import finish_data



modes = {
	"today_four_minuts_plus_by_views_count":"CAMSBggCEAEYAw%253D%253D",
	"today_by_views_count":"CAMSBAgCEAE%253D",
	"week_four_minuts_plus_by_views_count":"CAMSBAgDGAM%253D",
}

youtube_data = []
finish_data_list = []


def write_data(data_list,count):
	cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")
	with open(f"videos_data/videos_{cur_time}_part_{count}.csv", mode="w", encoding='utf-8') as w_file:
		file_writer = csv.writer(w_file, delimiter = ",", lineterminator="\r")
		file_writer.writerow(["Video link", "Views count", "Channel link", "subscribers count", "monetization"])
		file_writer.writerows(data_list)


def create_word_list():
	with open(WORDS_FILE) as file:
		word_list = file.readlines()
	word_list = [line.rstrip() for line in word_list]
	return word_list


def main():
	word_list = create_word_list()
	mode = int(input("""choose a mode for parsing:
1.parse today by views a long videos
2.parse today by views all videos
3.parse week by views a long videos

long video - from 4 to 20 minutes\n\n:"""))
	mode = list(modes.values())[mode-1]
	print('\n[+] Script start working')
	count = 1
	for i in range(0, len(word_list),PARTS_COUNT):
		if i!=0:
			list_of_words = word_list[i-PARTS_COUNT:i]
			print(len(list_of_words))
			asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
			relevant_video_data = asyncio.run(gather_data(list_of_words, mode))
			finish_data_list = asyncio.run(finish_data(relevant_video_data))
			if finish_data_list:
				write_data(finish_data_list, count)
			count+=1
			print(f'finish {i} words.')

if __name__ == "__main__":
	main()
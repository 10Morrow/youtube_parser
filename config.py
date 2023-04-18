from dotenv import load_dotenv
import os

load_dotenv()

# name of file where will be saved channels cache
JSON_FILE = "channels.json"

# nama of folder where your .csv files will be saved
VIDEO_FOLDER_NAME = "videos_data"

# the size of the part of the list of words by which the list of words will be split
PARTS_COUNT = 5000

# name of file with words which you want to use
WORDS_FILE = "50K.txt"

# that's a minimum amount of views on video (if vedeo has less views, it won't be parsed)
MIN_VIEW_COUNT = 50000

# if you don't want to see "shorts" video in parsed data you should set (False),
# otherwise "shorts" videos also will be parsed.
# (False or True)
SHORTS = False

# that's a minimum amount of subscribers on video channel
# (if video channel has fewer subscribers, it won't be parsed)
MAX_SUB_COUNT = 20000

# PROXY_ADDRESS, PROXY_LOGIN and PROXY_PASS will be taken from ".env" file.
PROXY_ADDRESS = os.environ.get("PROXY_ADDRESS")

PROXY_LOGIN = os.environ.get("PROXY_LOGIN")

PROXY_PASS = os.environ.get("PROXY_PASS")

# when you filter videos in YouTube, any filter have they own parameters, w
# which I just copy from url add paste here
# that isn't all parameters, but most important for me
YOUTUBE_FILTERS = {
	"today_four_minuts_plus_by_views_count" : "CAMSBggCEAEYAw%253D%253D",
	"today_by_views_count" : "CAMSBAgCEAE%253D",
	"week_four_minuts_plus_by_views_count" : "CAMSBAgDGAM%253D",
}

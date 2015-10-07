#/usr/bin/python2.7
import json, urllib2

# API Endpoints 
BASE_URL = "http://a.4cdn.org/"
ALL_BOARDS_URL = BASE_URL + "boards.json"
BOARD_URL = BASE_URL + "%s/threads.json"
THREAD_URL = BASE_URL + "%s/thread/%s.json"

class Post:
    def __init__(self, data, b):
        self.board 		= b
        self.id 		= data["no"]
        self.time_created   	= data["now"]
	try:
            self.author 	= data["name"]
	except KeyError:
	    self.author		= None
        self.reply_to       	= data["resto"]
        try:
            self.comment 	= data["com"]
        except KeyError:
            self.comment 	= None
        try:
            self.filename       = data["filename"]
            self.cdn_filename   = data["tim"]
            self.file_width     = data["w"]
            self.file_height    = data["h"]
            self.file_ext       = data["ext"]
            self.md5            = data["md5"]
            self.filesize       = data["fsize"]
            self.file_url       = "http://i.4cdn.org/%s/%s%s" % (self.board, self.cdn_filename, 
self.file_ext)
            self.has_file       = True
        except KeyError:
            self.has_file       = False

class Thread:
    def __init__(self, data, b):
	self.orig_post      = data["posts"][0]
	self.remaining_data = data["posts"][1:]
        self.board          = b
	self.id             = self.orig_post["no"]
        self.short_title    = unicode(self.orig_post["semantic_url"].replace("-"," ")) if "semantic_url" in self.orig_post else None
	self.time_created   = self.orig_post["now"]
	self.created_by	    = self.orig_post["name"]
	self.file_name      = self.orig_post["filename"]
	self.file_ext       = self.orig_post["ext"]
	self.md5            = self.orig_post["md5"]
	self.img_url        = "http://i.4cdn.org/%s/%s%s" % (self.board, self.orig_post["tim"], self.file_ext)
	self.file_dim       = "%s x %s" % (self.orig_post["w"], self.orig_post["h"])
	self.filesize       = self.orig_post["fsize"]
	self.reply_count    = self.orig_post["replies"]
	self.image_count    = self.orig_post["images"]
        self.posts          = []
    
    def get_posts(self):
        self.posts = []
        for post in self.remaining_data:
            self.posts.append(Post(post, self.board))
	return self.posts          

class Board:
    def __init__(self, data):
        self.short_name             = data["board"]
        self.bump_limit             = data["bump_limit"]
        self.cooldowns              = data["cooldowns"]
        self.cooldown_images        = data["cooldowns"]["images"]
        self.cooldown_replies       = data["cooldowns"]["replies"]
        self.cooldown_images_intra  = data["cooldowns"]["images_intra"]
        self.cooldown_replies_intra = data["cooldowns"]["replies_intra"]
        self.image_limit            = data["image_limit"]
        self.max_comment_chars      = data["max_comment_chars"]
        self.max_webm_filesize      = data["max_webm_filesize"]
        self.max_filesize 	    = data["max_filesize"]
        self.description    	    = data["meta_description"]
        self.pages                  = data["pages"]
        self.per_page       	    = data["per_page"]
        self.title          	    = data["title"]
        self.nsfw = True if data["ws_board"] == 0 else False
        self.threads                = []

    def get_all_threads(self):
        self.threads = []
        for page in json.load(urllib2.urlopen(BOARD_URL % self.short_name)):
                for thread in page["threads"]:
                    try:
                        self.threads.append(Thread(json.load(urllib2.urlopen(THREAD_URL % (self.short_name, thread["no"]))), self.short_name))
                    except: 
                        continue
	return self.threads

    def __str__(self):
        return "%s - /%s/" % (self.title.encode("utf-8"), self.short_name.encode("utf-8"))

    # Get thread by specifying only the thread ID
    def get_thread(self, id):
	return Thread(json.load(urllib2.urlopen(THREAD_URL % (self.short_name, id))), 
self.short_name)

class PyChan:
    def __init__(self):
        self.boards = []
        for board in json.load(urllib2.urlopen(ALL_BOARDS_URL))["boards"]:
            self.boards.append(Board(board))

    # Print a formatted list of all boards
    def list_boards(self):
        for board in self.boards:
            print board

    # Select board by either 'short_name' or 'title' (e.g. 'b' or 'Random')
    def select_board(self, b):
        for board in self.boards:
            if board.short_name == b or board.title == b:
                return board
            else:
                continue

    # Get thread by specifying the board and thread ID
    def get_thread(self, b, id):
        return Thread(json.load(urllib2.urlopen(THREAD_URL % (b, id))), b)

from configparser import ConfigParser

config = ConfigParser()
config.read('target.ini')

def cleanlist(l):
    l_ = []
    for i in l:
        l_.append(i.rstrip())
    return l_


class MonitorOptions:

    def __init__(self):

        self.a = 'b'
        self.keywords = []
        self.websites = []
        self.outfile = config['IO']['out_file']
        self.priorityfile = config['IO']['priority_file']

        self.apikey = config['KEYS']['API_KEY']
        self.csekey = config['KEYS']['CSE_KEY']

        keywordFile = config['IO']['keys_file']
        websiteFile = config['IO']['sites_file']

        with open(keywordFile) as f_obj:
            keywordList = f_obj.readlines()

        with open(websiteFile) as f_obj:
            websiteList = f_obj.readlines()

        self.keywords = cleanlist(keywordList)
        self.websites = cleanlist(websiteList)

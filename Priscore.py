from configparser import ConfigParser
# Priority score generation class
# Very simple, adds up the total score for each instance a keyword is found in a list
config = ConfigParser()
config.read('target.ini')

# Read the weights from the ini file
weights = [
    int(config['TARGETS']['weight1']),
    int(config['TARGETS']['weight2']),
    int(config['TARGETS']['weight3'])
    ]


class Score:

    def __init__(self, entities, keys):
        self.entities = entities
        self.keys = keys
        self.score = 0

    def calc(self):

        for entity in self.entities:

            if entity['keywords'][0][0] == self.keys[0]:

                self.score = self.score + weights[0]

            elif entity['keywords'][0][0] == self.keys[1]:

                self.score = self.score + weights[1]

            elif entity['keywords'][0][0] == self.keys[2]:

                self.score = self.score + weights[2]

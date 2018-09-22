from google.cloud import language
from fuzzywuzzy import fuzz
import urllib
from urllib import request

def match(keys, entity):

    # Generate a fuzzy match score from each entity against a list of keys

    matches = []

    for key in keys:

        score = fuzz.partial_ratio(key, entity.name)

        matches.append((key, score))

    return matches


def score_check(matches, threshold):

    # Filter out entities that don't match our keywords

    clean_matches = []

    for i in matches:

        if i[1] >= threshold:

            clean_matches.append(i)

    return clean_matches


class Whomst:

    def __init__(self, url, keys, thresh=None):

        self.url = url
        self.entity_list = []
        self.eval_ents = []
        self.keys = keys

        # Option to modify the matching threshold if passed the argument

        if thresh:

            self.threshold = thresh
        else:

            self.threshold = 90

    def get_entities(self):

        # get all entities
        # throw out the ones that don't match a keyword list
        # return a list of dictionaries

        connection = urllib.request.urlopen(self.url)

        raw = connection.read()

        document = language.types.Document(content=raw, type='HTML')

        client = language.LanguageServiceClient()

        entities = client.analyze_entity_sentiment(document=document, encoding_type='UTF32').entities

        for entity in entities:

            scored_matches = match(self.keys, entity)
            checked_matches = score_check(scored_matches, self.threshold)

            # If any of the keywords matched

            if checked_matches:

                score_dict = {
                    'name': entity.name,
                    'score': entity.sentiment.score,
                    'magnitude': entity.sentiment.magnitude,
                    'keywords': checked_matches
                        }

                self.entity_list.append(score_dict)

# Monitor.py - a program to monitor certain keywords on specific sites
# v2

from googleSearch import google_search
import ents
from Priscore import Score
from xopts import MonitorOptions as Options
from tablib import Dataset

# Get all options
opts = Options()

# Using tablib to create two datasets, one for every entity found
# the other for a list of URLs with composite score

data = Dataset()
data.headers = ['URL','keyword','match','sentiment','magnitude']

scoredset = Dataset()
scoredset.headers = ['URL','Priority']

# creates a list of queries from the primary keyword and websites
queryList = []

for website in opts.websites:
    query = "site:" + website + ' ' + '"' + opts.keywords[0] + '"'
    queryList.append(query)

resultsList = []

print("Searching...")

# makes the queries to the CSE and saves results to list
# TODO fix whatever creates TypeError when run with certain websites/keyword lists

for query in queryList:
    results = google_search(query, opts.apikey, opts.csekey, num=10)
    try:
        for result in results:
            resultsList.append(result['link'])
    except Exception as e:
        print(e)


print("Prioritizing...")

for url in resultsList:
    # Get the entities found in each URL and their sentiment

    entities = ents.Whomst(url, opts.keywords)
    try:
        entities.get_entities()
    except Exception as e:
        print("Exception: %s" % (e))

    # Generate a priority score for each URL
    priority = Score(entities.entity_list, opts.keywords)
    priority.calc()

    # Append relevant output to both datasets
    scoredset.append([url, priority.score])

    for entity in entities.entity_list:

        data.append([
                    url, entity['keywords'][0][0], entity['keywords'][0][1],
                    entity['score'], entity['magnitude']
                    ])

print("Writing...")
# Write output to CSV
with open(opts.outfile, 'w') as f:
    f.write(data.csv)

with open(opts.priorityfile, 'w') as f:
    f.write(scoredset.csv)
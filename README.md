# About
Crawls job sites and collects job postings by searching key words.

Leverages NLTK to summarize the job descriptions.

## How to Use
Entry point is "main.py". In command line, enter "python main.py" to activate the app.

In the pop-up window, type in the job key words to search, i.e. "python developer".

Web crawler graps the data from public resource and dumps at "resources/crawled_jd.json".

The app distills the job descriptions and save the summarized data at "resources/distilled_jd.json"

## Caveat
API of public job posting resources may change.
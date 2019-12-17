# About
A sample ETL application that crawls job posting sites and collects data by searching key words.

It leverages Natural Language Processing model to summarize the job descriptions.

## How to Use
Entry point is "extract.py" and "load.py". 

In command line, enter "python extract.py" to activate the app.

In the command line, type in the job key words to search, e.g. "python developer".

Web crawler graps the data from public resource and dumps at "resources/crawled_jd.json".

After the crawling process is finished, inspect the crawled data, if satisfied, run "python load.py" to distill the job descriptions. 

The summarized information is then saved at "resources/distilled_jd.json".

View data and result in jupyter notebook.

## Use With Docker
docker command:

* docker build -t careerhub .

* docker run -it -p 8888:8888 careerhub bash

* python extract.py

* python load.py

* jupyter lab --ip=0.0.0.0 --allow-root

## Caveat
API of public job posting resources may change.
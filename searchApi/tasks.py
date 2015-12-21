from celery import Celery
from celery.utils.log import get_task_logger
from searchApi import searchSleepTweets as sleep
from searchApi import searchDiagnosticTweets as diagnostic

app = Celery('tasks')

logger = get_task_logger(__name__)
app.config_from_object('celeryconfig')


@app.task
def searchtweet():
    sleep.runTweets.delay()

@app.task
def searchtweet2():
    diagnostic.fetchDiagnosticTweets.delay()

@app.task
def add(x, y):
    print "executing"
    return x + y

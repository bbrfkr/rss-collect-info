# Tool for notifying RSS info to slack
This repository includes python script to notify RSS info to slack.

## usage
* Deploy redis server. It is assumed that hostname and port of redis server are `redis` and `6379`

* Build docker container image.

```
docker build -t rss-collect-info .
```

* Run container image with environment variables.

```
docker run -it \
  -e RSS_URL=<RSS Feed URL> \
  -e SLACK_WEBHOOK_URL=<Slack incomming webhook URL> \
  -e SERACH_STRINGS=<Search strings (comma separated)> \
  -e REDIS_HOST=redis \
  -e REDIS_PORT=6379 \
  -e EXPIRE_SECONDS=<shelf life for the recode of notification> \
  rss-collect-info
```
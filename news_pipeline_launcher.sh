#! /bin/bash

fuser -k 6060/tcp

sudo service redis_6379 start
sudo service mongod start

sudo pip3 install -r requirements.txt

cd ./news_topic_modeling_service/server
python3 server.py &

cd ../../news_pipeline
python3 news_monitor.py &
python3 news_fetcher.py &
python3 news_deduper.py &

echo "=============================================="
read -p "PRESS [ANY KEY] TO TERMINATE PROCESSES." PRESSKEY

fuser -k 6060/tcp

kill $(jobs -p)
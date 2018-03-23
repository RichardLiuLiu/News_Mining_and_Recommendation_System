#! /bin/bash

fuser -k 3000/tcp
fuser -k 4040/tcp
fuser -k 5050/tcp

sudo service redis_6379 start
sudo service mongod start

pip3 install -r requirements.txt

cd ./news_recommendation_service
python3 click_log_processor.py &
python3 recommendation_service.py &

cd ../backend_server
python3 services.py &

# cd ../tap_news/client
# npm run build &

cd ../tap_news/server
npm start &

echo "=============================================="
read -p "PRESS [ANY KEY] TO TERMINATE PROCESSES." PRESSKEY

fuser -k 3000/tcp
fuser -k 4040/tcp
fuser -k 5050/tcp

sudo service redis_6379 stop
sudo service mongod stop

kill $(jobs -p)

# lower austria fire brigade incidents mining

This is a small project to mine data of fire brigade incidents in lower austria.

This project was inspired by the [Youtube Mining](https://github.com/bitnulleins/youtube_mining) project by [BYTEthinks](https://www.bytethinks.de/).

Systems:

* MongoDB (on host or extern)
* Mongo Express (optional)
* Python-Client

# Installation

## Docker

1. Add your API Key and Mongo credentials.
2. Install docker-compose
3. Do command:
```sudo docker-compose up -d```

If you want to shutdown the service only type:
```sudo docker-compose down```

## Local

1. Only put your MongoDB settings to sample.env and rename it to .env.
2. Install dependencies with pip ```pip install -r requirements.txt```
3. Then run ```python src/main.py```

## On Linux

1. Clone this github repository to a folder (e.g. ```~/Programs/```)
2. Add it to crontabs for repeatly update ```crontab -e */1 * * * * python3 ~/Programs/fire_brigade_mining/src/main.py >> ~/Programs/fire_brigade_mining/output.log 2>&1```
3. Check output.log for output

To update the client, go to the root folder and type ```git pull```

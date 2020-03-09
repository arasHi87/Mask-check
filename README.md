# Mask check

Mask is the line bot project to check last mask quantity in Taiwan's pharmacy.

## Installation

```bash
git clone https://github.com/arasHi87/Mask-check && cd Mask-check
pip install -r requirements.txt
mv config.sample.py config.py
```

## Run

Before run remeber set your `CNANNEL_ACCESS_TOKEN` and `CNANNEL_SECRET` in config file.

```bash
python app.py
```

## Features

* send location and get the top ten data

* postback and get the map of data

## Future

* dynamic renew data

* send the name and get data
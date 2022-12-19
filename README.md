# Torob Crawler

Torob Crawler is a Python application for crawling Hard drive items from the Torob website. Also it provides an flask based API for filtering items.

## Installation

Install required packages using [pip](https://pip.pypa.io/en/stable/).

```bash
pip install -r requirements.txt
```

## Usage

For crawling, crawler.py gets two parameter items and url , url is optional its default value is torob hard disks page, and items parameter is required, which refers to the number of items that must be crawled. crawler.py reads other parameters from app.env file.

```python
python3 crawler.py --items 50
```

By this command, flask application will run and read parameters from app.env file.
```python
python3 crawler.py --items 50
```

By this command, flask application will run and read parameters from app.env file.
```python
python3 crawler.py --items 50
```
An example of using api

```python
curl --request POST \
  --url http://127.0.0.1:5000/filter \
  --header 'cache-control: no-cache' \
  --header 'postman-token: 2d6d3a9a-b793-b622-fd4d-ce5c4abe8ea4' \
  --data '{\n    "Capacity":{\n        "less":5000,\n        "more":2000\n    },\n    "Price":{\n        "more":100000,\n        "less":50000\n    },\n    "Seller":["مبیت", "زیکتز"],\n    "Model":["مبیت", "زیکتز"]\n    \n}'
```


## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

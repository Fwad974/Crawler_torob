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
  --header 'content-type: application/json' \
  --data '{\n    \n\n    "Seller":["مبیت", "زیکتز"]}'
```


## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

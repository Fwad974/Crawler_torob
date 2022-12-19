from driver import web_driver
from info_extractor import info_extraction
import pandas as pd
import psycopg2
import argparse
from pathlib import Path
import os
from dotenv import load_dotenv

def schem_validator(data):
    schema={
        "shop": str,
        "model": str,
        "capacity":int,
        "price":int
    }
    for i in data:
        if type(data[i]) is not schema[i]:
            return False
    else:
        return True

def make_db_cur():
    config=load_db_config()
    conn = psycopg2.connect("dbname='{db}' user='{user}' host='{host}' port='{port}' password='{passwd}'".format(
        user=config["user"],
        passwd=config["password"],
        host=config["host"],
        port=config["port"],
        db=config["db"]))

    return conn

def insertIntoTable(df, table,conn):
        """
        Using cursor.executemany() to insert the dataframe
        """
        # Create a list of tupples from the dataframe values
        tuples = list(set([tuple(x) for x in df.to_numpy()]))

        # Comma-separated dataframe columns
        cols = ','.join(list(df.columns))
        # SQL query to execute
        query = "INSERT INTO %s(%s) VALUES(%%s,%%s,%%s,%%s)" % (
            table, cols)

        try:
            cur = conn.cursor()
            cur.executemany(query, tuples)
            conn.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            conn.rollback()
            return 1
def load_db_config():
    dotenv_path = Path('./app.env')
    load_dotenv(dotenv_path=dotenv_path)
    return {
        "user":os.getenv("DB_USER"),
        "password":os.getenv("PASS"),
        "host":os.getenv("HOST"),
        "port":os.getenv("PORT"),
        "db":os.getenv("DB"),
    }

def data_clrawler(url,item_cnt):
    base_url=url.split(".com")[0]+".com/"
    page = web_driver(url, 50)
    R = []
    cnt = 0
    info_extractor = info_extraction(page)
    items = page.get_slector()
    for item in items:
        cnt += 1
        addr = base_url + item.attrib["href"]
        page.go_link(addr)
        vals = info_extractor.get_values(5)
        R += [rec for rec in vals if schem_validator(rec)]
        page.go_back()
        if len(R)>=item_cnt:
            break
    R=R[:item_cnt]
    df=pd.DataFrame(R)
    df.columns = ["Seller", "Price", "Model", "Capacity"]
    return df

def main():
    url = "https://torob.com/browse/243/%D9%87%D8%A7%D8%B1%D8%AF-%D8%A7%DA%A9%D8%B3%D8%AA%D8%B1%D9%86%D8%A7%D9%84-hard/"
    parser = argparse.ArgumentParser(description='Crawler.')
    parser.add_argument('--items', type=int,
                        help='Number of items for crawling',required=True)

    parser.add_argument('--url', type=str,
                        help='Crawling url', required=False, default=url)

    args = parser.parse_args()
    data=data_clrawler(url=args.url, item_cnt=args.items)

    dotenv_path = Path('./app.env')
    load_dotenv(dotenv_path=dotenv_path)
    conn=make_db_cur()
    insertIntoTable(df=data,table=os.getenv("TABLE"),conn=conn)
if __name__ == "__main__":
    main()

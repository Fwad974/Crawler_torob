from flask import Flask, request, jsonify
from pathlib import Path
import os
from dotenv import load_dotenv
import psycopg2
import json
app = Flask(__name__)

class DB:
    def __init__(self):
        self.config,self.table=self.load_db_config()
        self.conn=self.make_db_cur()


    def load_db_config(self):
        dotenv_path = Path('./app.env')
        load_dotenv(dotenv_path=dotenv_path)
        return {
            "user":os.getenv("DB_USER"),
            "password":os.getenv("PASS"),
            "host":os.getenv("HOST"),
            "port":os.getenv("PORT"),
            "db":os.getenv("DB"),
        },os.getenv("TABLE")
    def make_db_cur(self):
        config=self.config
        conn = psycopg2.connect("dbname='{db}' user='{user}' host='{host}' port='{port}' password='{passwd}'".format(
            user=config["user"],
            passwd=config["password"],
            host=config["host"],
            port=config["port"],
            db=config["db"]))

        return conn
    def query_executor(self,query):
        cur = self.conn.cursor()
        cur.execute(query)
        row= cur.fetchall()
        return row


def query_builder(condition_inp):
    condition={}

    for cnd in ["Seller", "Model","Capacity", "Price"]:
        if cnd in ["Capacity", "Price"]:
            r={}
            for i in ["less","more","equal"]:
                if condition_inp.get(cnd,{}).get(i,None) is not None:
                    r[i]=condition_inp[cnd][i]
            if len(r)!=0:
                condition[cnd]=r
        elif cnd in ["Seller", "Model"]:
            if condition_inp.get(cnd,None) is not None and type(condition_inp.get(cnd,None)) is list:
                condition[cnd]=condition_inp[cnd]

    query = "SELECT * FROM Data"
    if len(condition) == 0:
        return query
    query += " WHERE"
    parts = []
    for z, part in enumerate(condition):

        if part in ["Capacity", "Price"]:
            if condition[part].get("less", None) is not None:
                parts.append(" " + part + " < " + str(condition[part]["less"]))
            if condition[part].get("more", None) is not None:
                parts.append(" " + part + " > " + str(condition[part]["more"]))
            if condition[part].get("equal", None) is not None:
                parts.append(" " + part + " = " + str(condition[part]["equal"]))
        if part in ["Seller", "Model"]:
            tmp_part = ''
            for rec in condition[part]:
                tmp_part += part + " = '" + rec + "' OR "
            tmp_part = "( " + tmp_part[:-4] + " )"
            parts.append(tmp_part)
    for part in parts:
        query += part + " AND"
    return query[:-4] + ";"

db=DB()


@app.route('/filter', methods= ['POST',"GET"])
def projects(db=db):
    req_json = request.get_json()
    query=query_builder(req_json)

    rows=db.query_executor(query)
    keys = ["Model", "Seller", "Price", "Capacity"]
    res= [dict(zip(keys,i)) for i in rows]
    return json.dumps(res)

if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)
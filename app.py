from flask import Flask, render_template, jsonify
from sqlalchemy.orm import Session
from sqlalchemy import create_engine,func
import json

#Load From the Database file that I created. It is in this same directory
import pandas as pd
from Database import deaths_vs_vaccination
from Database import new_cases_last_7_days
from Database import country_info

app = Flask(__name__)

#Route to produce your main home page. 
@app.route("/") 
def index(): 
    return render_template("index.html")

#This is the main data route, it will produce JSON for your javascript to use
#You will wind up calling into it using d3.json("/LoadData/1") to get period 1
@app.route("/LoadData")
def LoadData(): 
    userName = "postgres"
    password = "postgres" #use your postgres password if you changed it
    database = "COVID-19 Data" #you can use any db you want, I just happened to use this one

    engine = create_engine(f"postgresql+psycopg2://{userName}:{password}@localhost:5433/{database}")

    conn = engine.connect()
    query = "SELECT * FROM Cases"
    data = pd.read_sql(query, engine)
    json_data = data.to_dict(orient="records")
    return json_data

@app.route("/sample")
def sample():
    return jsonify(deaths_vs_vaccination().to_dict(orient="records"))

@app.route("/sample2")
def sample2():
    return jsonify(new_cases_last_7_days().to_dict(orient="records"))

@app.route("/sample3")
def sample3():
    return country_info()


if __name__ == "__main__":
    app.run(debug=True)


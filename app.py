// JavaScript Document
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

import pandas as pd
import os
import numpy as np
from flask import (
    Flask,
    render_template,
    jsonify,
    request)

from flask_sqlalchemy import SQLAlchemy


engine = create_engine("sqlite:///belly_button_biodiversity.sqlite")


Base = automap_base()


Base.prepare(engine, reflect=True)


print(Base.classes.keys())


samples = Base.classes.samples
otu = Base.classes.otu
samples_metadata = Base.classes.samples_metadata


session = Session(engine)

sample_names = samples.__table__.columns.keys()
sample_names.pop(0)


list_of_sample_names =[]

for row in session.query(samples).all():
    list_of_sample_names.append(row)


list_of_otu_description =[]

for row in session.query(otu.lowest_taxonomic_unit_found).all():
    list_of_otu_description.append(row[0])


filtered_sample = []
for row in session.query(samples_metadata.AGE, samples_metadata.ETHNICITY,samples_metadata.GENDER, samples_metadata.BBTYPE, samples_metadata.LOCATION, samples_metadata.SAMPLEID).filter(samples_metadata.SAMPLEID == 940).all():
    filtered_dictionary = {
        "AGE": row[0],
        "BBTYPE": row[1],
        "ETHNICITY": row[2],
        "GENDER": row[3],
        "LOCATION": row[4],
        "SAMPLEID": row[5],
              
    }
    filtered_sample.append(filtered_dictionary)
print(filtered_sample)

weekly_WFREQ = []
for row in session.query(samples_metadata.WFREQ).filter(samples_metadata.SAMPLEID == 940).all():
    filtered_WFREQ = {
        "WFREQ": row[0],
         
    }
    weekly_WFREQ.append(filtered_WFREQ)

otu_id_and_sample_values = []
otu_id = []
sample_values = []

otu_id_and_sample_values_dic ={
    "otu_id": otu_id,
    "sample_values":sample_values
}

otu_id_and_sample_values.append(otu_id_and_sample_values_dic)
for row in session.query(samples.otu_id,samples.BB_940).filter(samples_metadata.SAMPLEID == 940).order_by(samples.BB_940.desc()).all():
    otu_id.append(row[0])
    sample_values.append(row[1])





app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", sample_names= sample_names)
    
 
@app.route("/names")
def names():
    return jsonify(sample_names)
    

@app.route("/otu")
def otu():
    return jsonify(list_of_otu_description)

@app.route("/metadata")
def metadata():
    return jsonify(filtered_sample)

@app.route('/wfreq')
def wfreq():
    return jsonify(weekly_WFREQ)

@app.route('/samples')
def samples():
    data = [{
        "y": otu_id_and_sample_values[0]["otu_id"][0:10],
        "x": otu_id_and_sample_values[0]["sample_values"][0:10]}]
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
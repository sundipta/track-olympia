from flask import render_template
from flask import request
from track_olympia import app
from corpus import vectorize

from gensim.test.utils import common_corpus, common_dictionary, get_tmpfile
from gensim.models import LsiModel


from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
import psycopg2

user = 'sundipta' #add your username here (same as previous postgreSQL)            
host = 'localhost'
dbname = 'WA_leg'
db = create_engine('postgres://%s%s/%s'%(user,host,dbname))
con = None
con = psycopg2.connect(database = dbname, user = user)

@app.route('/')
def bill_input():
    return render_template("input.html")


@app.route('/#about')
def bill_input():
    return render_template("about.html")

@app.route('/#contact')
def bill_input():
    return render_template("contact.html")


@app.route('/output')
def bill_output():
  input_term = request.args.get('bill_search')
  query = 'SELECT * FROM bill_info_table WHERE "Active" = True ORDER BY "ID" ASC ;'
  query_result=pd.read_sql_query(query,con)
  query_results = query_result.set_index('ID')
  results = vectorize(input_term)
  bills = []
  for result in results:
      get_index = result[0]
      if get_index in query_results.index:
            bills.append(dict(agency=query_results.loc[get_index]['Agency'],
      				    bill_id=query_results.loc[get_index]['Bill_ID'], 
      				    description=query_results.loc[get_index]['LongDescription']))
  print(bills)
  return render_template("output.html",bills = bills)

  


from flask import render_template
from flask import request
from string import Template
from track_olympia import app
from corpus import vectorize
from national_model import return_category

from gensim.test.utils import common_corpus, common_dictionary, get_tmpfile
from gensim.models import LsiModel


from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd


@app.route('/search')
def bill_input():
    return render_template("input.html")

@app.route('/')
def map_input2():
    return render_template("home1.html")

@app.route('/home')
def map_input():
    return render_template("home1.html")

@app.route('/home1')
def map_input1():
    return render_template("home1.html")

@app.route('/map')
def map_input3():
    return render_template("home1.html")

@app.route('/<district_number>')
def district_number_page(district_number):
	legislator_info = pd.read_csv("leg_info.csv")
	all_legs = legislator_info[legislator_info['District']==int(district_number)]
	senator_df = all_legs[legislator_info['Position']=='S']

	sen_data = []
	sen_data.append(dict(name=senator_df['Member Name'].values[0],
      				    photo=senator_df['Image'].values[0][1:-1], 
      				    email=senator_df['Email'].values[0],
      				    phone=senator_df['Phone'].values[0],
      				    party=senator_df['Party'].values[0]))
    
	leg1_df = all_legs[legislator_info['Position']=='1']

	leg1_data = []
	leg1_data.append(dict(name=leg1_df['Member Name'].values[0],
      				    photo=leg1_df['Image'].values[0][1:-1], 
      				    email=leg1_df['Email'].values[0],
      				    phone=leg1_df['Phone'].values[0],
      				    party=leg1_df['Party'].values[0]))

	leg2_df = all_legs[legislator_info['Position']=='2']

	leg2_data = []
	leg2_data.append(dict(name=leg2_df['Member Name'].values[0],
      				    photo=leg2_df['Image'].values[0][1:-1], 
      				    email=leg2_df['Email'].values[0],
      				    phone=leg2_df['Phone'].values[0],
      				    party=leg2_df['Party'].values[0]))
	dist_numb = district_number
      				    
	return render_template('district.html', sen_data=sen_data, leg1_data=leg1_data, leg2_data=leg2_data, dist_numb=[dist_numb])

@app.route('/about')
def about_screen():
    return render_template("about.html")

@app.route('/contact')
def contact_input():
    return render_template("contact.html")

@app.route('/output')
def bill_output():
  input_term = request.args.get('bill_search')
  engine = create_engine('sqlite:///./bill_db.sqlite')
  query = 'SELECT * FROM bill_info_table WHERE Active ORDER BY "index" ASC ;'
  query_result=pd.read_sql_query(query,engine)
  query_results = query_result.set_index('index')
  results = vectorize(input_term)
  bills = []
  for result in results:
      get_index = result[0]
      print(get_index)
      if get_index in query_results.index:
            bills.append(dict(agency=query_results.loc[get_index]['Agency'],
      				    bill_id=query_results.loc[get_index]['Bill_ID'], 
      				    description=query_results.loc[get_index]['LongDescription']))
  if len(bills)> 0:
    return render_template("output.html",bills = bills)
  else:
    return render_template("output_alt.html")

@app.route('/category')
def category_output():
   input = request.args.get('category_search')
   output_category = return_category(input)
   print(output_category)
   return render_template("categories.html",category = output_category.iloc[0]) 


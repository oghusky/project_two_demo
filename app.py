from pymongo import MongoClient
import os
import sys
import subprocess
from flask import Flask,jsonify, render_template

try:
  import pandas as pd
  from flask_cors import CORS
  import sqlalchemy
  from sqlalchemy.ext.automap import automap_base
  from sqlalchemy.orm import Session
  from sqlalchemy import create_engine
  import psycopg2
except ImportError:
  subprocess.check_call([sys.executable, '-m', 'pip','install', 'pandas'])
  subprocess.check_call([sys.executable, '-m', 'pip','install', 'flask_cors'])
  subprocess.check_call([sys.executable, '-m', 'pip','install', 'sqlalchemy'])
  subprocess.check_call([sys.executable, '-m', 'pip','install', 'psycopg2'])
finally:
  import pandas as pd
  from flask_cors import CORS
  import sqlalchemy
  from sqlalchemy.ext.automap import automap_base
  from sqlalchemy.orm import Session
  from sqlalchemy import create_engine
  import psycopg2

pokedex = pd.read_csv('./resources/pokemon.csv').dropna()

pokedex.to_csv('./resources/cleaned_pokemon.csv')

app = Flask(__name__)

app.config["MONGO_CONNECT"] = False
CORS(app)

client = MongoClient(os.getenv('MONGO_URI', 'mongodb://localhost:27017'))
pokemongo = client.pokedex

clean_pokemon = pd.read_csv('./resources/cleaned_pokemon.csv').to_dict('records')

# sql stuff
engine = create_engine('postgresql://postgres:password@localhost/pokedex')
Base = automap_base()
Base.prepare(engine,reflect=True)

# pd.read_csv('./resources/cleaned_pokemon.csv').to_sql('pokedex_two',con=engine)

# for item in clean_pokemon:
#   pokemongo.pokedex.insert_one({
#     'index': item['#'],
#     'name': item['Name'],
#     'type_one': item['Type 1'],
#     'type_two': item['Type 2'],
#     'total': item['Total'],
#     'hp': item['HP'],
#     'attack': item['Attack'],
#     'defense': item['Defense'],
#     'sp_attack': item['Sp. Atk'],
#     'sp_defense': item['Sp. Def'],
#     'speed': item['Speed'],
#     'generation': item['Generation'],
#     'is_legend': item['Legendary'],
#   })

@app.route('/',methods=['GET']) #post, put(grab user by username and update the username), delete(grab by ID and delete)
def home_page():
  return render_template('index.html')

@app.route('/two',methods=['GET']) #post, put(grab user by username and update the username), delete(grab by ID and delete)
def page_two():
  return render_template('page_two.html')

@app.route('/api/mongo_data',methods=['GET'])
def mongo_data():
  print(len(get_mongo_pokedata()))
  return jsonify(data=get_mongo_pokedata())

@app.route('/api/sql_data',methods=['GET'])
def sql_data():
  df = pd.read_sql('''SELECT * FROM pokedex_two''', con=engine)
  sql_pokedata = df.to_dict('records')
  return jsonify(sql_pokedata)


def get_mongo_pokedata():
  pokedata=[]
  for item in list(pokemongo.pokedex.find()):
    pokedata.append({
      'index': item['index'],
      'name': item['name'],
      'type_one': item['type_one'],
      'type_two': item['type_two'],
      'total': item['total'],
      'hp': item['hp'],
      'attack': item['attack'],
      'defense': item['defense'],
      'sp_attack': item['sp_attack'],
      'sp_defense': item['sp_defense'],
      'speed': item['speed'],
      'generation': item['generation'],
      'is_legend': item['is_legend'],
    })
  return pokedata

if __name__ == '__main__':
  app.run(debug=True)

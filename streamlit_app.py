
import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Mom New Healthy Dinner')

streamlit.header('BreakFast Menu')
streamlit.text(' Omega 3 & Blueberry Oatmeal')
streamlit.text(' Kale, Spinanch & Rocket Snoothie')
streamlit.text(' Hard-Boiled Free-Range Egg')
streamlit.text('Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
#fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)
streamlit.header("Fruityvice Fruit Advice!")
def get_fruit_vice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("please set a fruit to get Information.")
  else:
    back_from_function=get_fruit_vice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()
# #import requests

# #fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
# #streamlit.text(fruityvice_response.json())
# #normalize
# fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# streamlit.dataframe(fruityvice_normalized)
#
streamlit.header("The Fruit load list contains:")
#snowflake functions
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * from fruit_load_list")
    return my_cur.fetchall()
#add button to load the fruit
if streamlit.button('Get fruit Load list '):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows=get_fruit_load_list()
  my_cnx.close()
  streamlit.dataframe(my_data_rows)
def insert_row_snow_flake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values('"+new_fruit+"')")
    return "Thanks for adding "+new_fruit
add_my_fruit = streamlit.text_input('what fruit do you like to add?')
if streamlit.button('Add a fruit to list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function=insert_row_snow_flake(add_my_fruit)
  my_cnx.close()
  streamlit.text(back_from_function)
  
# my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
# my_cur = my_cnx.cursor()
# add_my_fruit = streamlit.text_input('what fruit do you like to add?')
# streamlit.write('Thanks for adding', add_my_fruit)
# my_cur.execute("insert into fruit_load_list values('"from streamlit')")
# #my_cur.execute("SELECT * from fruit_load_list")
# my_data_row = my_cur.fetchall()
# streamlit.header("Fruit load list contans:")
# streamlit.dataframe(my_data_row)
streamlit.stop()

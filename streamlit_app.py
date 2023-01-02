
import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

# https://idair-first-streamlit-app-streamlit-app-l8ibwu.streamlit.app/

streamlit.title("My Mom's New Healthy Diner")
streamlit.header('Breakfast Menu')
streamlit.text('🥣Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avacado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Grapes'])

# Display the table on the page.
# streamlit.dataframe(my_fruit_list)

fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the selected fruits table on the page.
streamlit.dataframe(fruits_to_show)

#API Call
#--------------------------------------------------------------

streamlit.header("Fruityvice Fruit Advice!")
try:
  #Allow user to enter fruit name, capture entry and pass to API
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.write('Please select a fruit for information.')
  else:
    streamlit.write('The user entered ', fruit_choice)
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    # Normalize the data  
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    # display data in a table
    streamlit.dataframe(fruityvice_normalized)
except URLError as e:
    streamlit.error() 

#https://docs.google.com/spreadsheets/d/1hLBv0pO1qpeMtUncE8Yv1NSdqaDrY9CqmXoP5b9313s/edit?resourcekey#gid=663712744

#-----------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------Snowflake connection ----------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
#streamlit.text("Hello from Snowflake:")
#streamlit.text(my_data_row)

streamlit.title("View our fruit list - add your Favorites!")
streamlit.header("Fruit Load List Contains:")

def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from fruit_load_list")
    return my_cur.fetchall()  #Fetch all rows not just one

#Add a button to load the fruit 
if streamlit.button('Get fruit list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list() 
  my_cnx.close()
  streamlit.dataframe(my_data_rows)
    
#-----------------------------------------------------------------------------------------------------------------------
#Allow user to enter fruit name, capture entry and pass to API
#-----------------------------------------------------------------------------------------------------------------------
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur: 
    my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('" + new_fruit +"')")  
    return 'Thanks for adding ' + new_fruit 
  
add_fruit_choice = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a fruit to list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  function_return_val = insert_row_snowflake(add_fruit_choice) 
  my_cnx.close()
  streamlit.text(function_return_val)    
  
  
  

import streamlit
import pandas
import requests


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
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")

streamlit.header("Fruityvice Fruit Advice!")
streamlit.text(fruityvice_response.json())  #displays the json data as is 

# Normalize the data  
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# display data in a table
streamlit.dataframe(fruityvice_normalized)

#https://docs.google.com/spreadsheets/d/1hLBv0pO1qpeMtUncE8Yv1NSdqaDrY9CqmXoP5b9313s/edit?resourcekey#gid=663712744

import snowflake
import snowflake.connector
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from streamlit_option_menu import option_menu 
# import streamlit_dynamic_filters # type: ignore
# from streamlit_dynamic_filters import dynamic_filters # type: ignore
# import altair 



st.set_page_config(page_title="Pharma Sales - Analysis and Prediction",layout='wide')
st.title("Pharma Sales Analysis")

st.markdown(
    """
    <style>
    div[data-testid="stApp"]  {
        background-color: rgba(0,0,0, 0.9);
            }
   </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    section[data-testid="stSidebar"] 
    div[class="st-emotion-cache-u5opgr eczjsme11"]{
    background-image: linear-gradient(#8993ab,#8993ab); 
    color: white
    }
    </style>
    
    """,
    unsafe_allow_html=True
)

st.markdown("""
<style>
div[data-testid="column"] {
   background-color: rgba(0,0,0, 0.9);
   border: 3px solid rgba(0,0,0, 0.9);
#    border: 3px solid rgba(64,224,208,0.9);
   padding: 3% 2% 3% 3%;
   border-radius:4px;
   color: rgb((255,0,0));
   overflow-wrap: break-word;
}

/* breakline for metric text         */
div[data-testid="element-container"] > label[data-testid="stMetricLabel"] > div {
   overflow-wrap: break-word;
   white-space: break-spaces;
   color: red;
}
</style>
"""
, unsafe_allow_html=True)

# Define connection parameters securely
connection_parameters = {
    'user': 'Ralf1114',
    'password':'Winter_1996',
    'account':'vabkqah-bz11525',
    'warehouse':'COMPUTE_WH',
    'database':'TESTING',
    'schema':'DATASETS'
}
 
# Create a Snowflake connection
conn = snowflake.connector.connect(
    user=connection_parameters['user'],
    password=connection_parameters['password'],
    account=connection_parameters['account'],
    warehouse=connection_parameters['warehouse'],
    database=connection_parameters['database'],
    schema=connection_parameters['schema']
)
 
# Define a SQL query
query = "SELECT * FROM PHARMA"
 
# Run the query and convert the result to a Pandas dataframe
df = pd.read_sql(query, conn)
 
# Close the connection
conn.close()

#check dataset
df.head()
df.info()
df.isnull().sum()
df.duplicated().sum()

#Change datatypes
df['TIME']=pd.to_datetime(df["TIME"])

#EDA
st.write('EXPLOARATORY DATA ANALYSIS')








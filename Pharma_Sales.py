import snowflake
import snowflake.connector
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import time
import plotly.express as px 
from streamlit_option_menu import option_menu 
# import streamlit_dynamic_filters # type: ignore
# from streamlit_dynamic_filters import dynamic_filters # type: ignore
# import altair 



st.set_page_config(page_title="Pharma Sales - Analysis and Prediction",layout='wide')
st.title("Pharma Sales Analysis")

page_element="""
<style>
div[data-testid="stApp"]{
  # background-image: url("https://cdn.wallpapersafari.com/88/75/cLUQqJ.jpg");
  background-image: url("https://c1.wallpaperflare.com/preview/839/207/808/pill-tablet-pharmacy-medicine.jpg");
  background-size: cover;
}
[data-testid="stHeader"]{
  background-color: rgba(0,0,0,0.9);
}
</style>
"""
st.markdown(page_element, unsafe_allow_html=True)

page_element="""
<style>
    div[data-testid="stSidebar"]{
    # div[class="st-emotion-cache-u5opgr eczjsme11"]{
    background-image: url("https://c1.wallpaperflare.com/preview/839/207/808/pill-tablet-pharmacy-medicine.jpg"); 
    color: white
    }
    </style>
    
    """
st.markdown(page_element, unsafe_allow_html=True)


st.markdown("""
<style>
div[data-testid="column"] {
   # background-color: rgba(204, 204, 255, 0.9);
   background-color: rgba(255,255,255,0.5);
   # border: 1px solid rgba(255,255,255,0.5);
   padding: 3% 2% 3% 3%;
   border-radius:1px;
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
    'user': 'sudharchanan',
    'password':'Sudharcha@123',
    'account':'xboggta-td16226',
    'warehouse':'COMPUTE_WH',
    'database':'PROJECT',
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

df['TIME']=pd.to_datetime(df['TIME'])
df['NEWDATE'] = df['TIME'].dt.date
df.info()

with st.sidebar:
    selected=option_menu(
        menu_title="Menu",
        options=["Analysis","ML Model"],
        icons=["bar-chart","table"],
        menu_icon="house",
        default_index=0,
    )

if selected=="Analysis":

    placeholder = st.empty()

    with placeholder.container():

        
            
            

        d1,d2,d3,d4=st.tabs(["Pharma Sales Analysis","Line plot - Sales Trend","Total Sales","Frequency Distribution of Sales"])

        with d1:
             
            summry="""
            Pharma sales analysis involves examining data related to the sales of pharmaceutical products. This analysis is crucial for pharmaceutical companies to understand market trends, evaluate the performance of their products, and make informed business decisions. Here's a brief overview of pharma sales analysis and its advantages:
            1. :red[Identifying Market Trends:] Analysis helps in understanding market trends, such as which drugs are in high demand, seasonal variations in sales, and emerging market preferences.
            2. :red[Optimizing Inventory:] By analyzing sales data, companies can optimize their inventory management by stocking the right amount of each drug, reducing stockouts, and minimizing excess inventory.
            3. :red[Sales Forecasting:] Analysis allows for accurate sales forecasting, helping companies plan production, marketing campaigns, and budget allocation effectively.
            4. :red[Performance Evaluation:] Sales analysis provides insights into the performance of sales teams, territories, and individual products, facilitating performance evaluation and improvement strategies.
            5. :red[Decision Making:] Data-driven insights from sales analysis support informed decision-making across various aspects of the business, leading to improved overall performance and profitability.
            """
            def stream_data():
                for word in summry.split(" "):
                 yield word + " "
                 time.sleep(0.05)
            
            st.write_stream(stream_data)

        with d2:

                r1,r4=st.columns([20,42.5])

                with r1:

                    year_filter = st.selectbox("Select Year", pd.unique(df['YEAR']))
                    df = df[df['YEAR'] == year_filter]
                    
                # with r2:
                    
                #     month_filter = st.selectbox("Select Month", pd.unique(df['MONTH']))
                #     df = df[df['MONTH'] == month_filter]
                                        
                    
                with r4:
                    selected_drugs = st.multiselect(
                    'Select drug categories to plot',
                    options=['ACETICACIDDERIVATIVES', 'PROPIONICACIDDERIVATIVES', 'SALICYLICACIDDERIVATIVES',
                    'PYRAZOLONESANDANILIDES', 'ANXIOLYTICDRUGS', 'HYPNOTICSSNDSEDATIVESDRUGS',
                    'OBSTRUCTIVEAIRWAYDRUGS', 'ANTIHISTAMINES'],
                    default=['ACETICACIDDERIVATIVES', 'PROPIONICACIDDERIVATIVES']
                    )

                # Plotting
                if selected_drugs:
                    plt.figure(figsize=(14, 7))
                    for drug in selected_drugs:
                        plt.plot(df['NEWDATE'], df[drug], label=drug)
                    plt.xlabel('Year')
                    plt.ylabel('Sales')
                    plt.title('Time Series of Pharma Sales')
                    plt.legend()
                    st.pyplot(plt)
                else:
                    st.write("Please select at least one drug category to display the line plot.")

        with d3:
             
            drug_categories = [
                'ACETICACIDDERIVATIVES', 'PROPIONICACIDDERIVATIVES', 'SALICYLICACIDDERIVATIVES',
                'PYRAZOLONESANDANILIDES', 'ANXIOLYTICDRUGS', 'HYPNOTICSSNDSEDATIVESDRUGS',
                'OBSTRUCTIVEAIRWAYDRUGS', 'ANTIHISTAMINES'
                ]
             
            total_sales = df[drug_categories].sum()

            fig = px.pie(values=total_sales, names=drug_categories, title='Proportion of Total Sales by Drug Category')
            fig.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)',paper_bgcolor='rgba(0, 0, 0, 0)')
            st.plotly_chart(fig)


        with d4:

            Acetid_df = df[df['ACETICACIDDERIVATIVES'] != 0]
            fig = px.histogram(
            Acetid_df,
            x='ACETICACIDDERIVATIVES',
            title='Frequency Distribution of Acetic Acid Derivatives Sales',
            labels={'ACETICACIDDERIVATIVES': 'Acetic Acid Derivatives Sales'},
            nbins=10  # Number of bins
             )
            fig.update_layout(plot_bgcolor='rgba(0, 0, 0, 9)',paper_bgcolor='rgba(0, 0, 0, 9)')

            Sali_df=df[df['SALICYLICACIDDERIVATIVES'] !=0]
            gig=px.histogram(
            Sali_df,
            x='SALICYLICACIDDERIVATIVES',
            title='Frequency Distribution of Salicylic Acid Derivatives',
            labels={'SALICYLICACIDDERIVATIVES': 'Salicylic Acid Derivatives'},
            nbins=10  # Number of bins
             )
            gig.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)',paper_bgcolor='rgba(0, 0, 0, 0)')

            Prop_df=df[df['PROPIONICACIDDERIVATIVES']!=0]
            ag=px.histogram(
            Prop_df,
            x='PROPIONICACIDDERIVATIVES',
            title='Frequency Distribution of Propionic Acid Derivatives Sales',
            labels={'PROPIONICACIDDERIVATIVES': 'Propionic Acid Derivatives Sales'},
            nbins=10  # Number of bins
             )
            ag.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)',paper_bgcolor='rgba(0, 0, 0, 0)')
          
            Pyra_df=df[df['PYRAZOLONESANDANILIDES']!=0]
            cg=px.histogram(
            Pyra_df,
            x='PYRAZOLONESANDANILIDES',
            title='Frequency Distribution of Pyrazolones And Anilides Sales',
            labels={'PYRAZOLONESANDANILIDES': 'Pyrazolones And Anilides Sales'},
            nbins=10  # Number of bins
             )
            cg.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)',paper_bgcolor='rgba(0, 0, 0, 0)')

            Anx_df=df[df['ANXIOLYTICDRUGS']!=0]
            dg=px.histogram(
            Anx_df,
            x='ANXIOLYTICDRUGS',
            title='Frequency Distribution of Anxiolytic Drugs Sales',
            labels={'ANXIOLYTICDRUGS': 'Anxiolytic Drugs Sales'},
            nbins=10  # Number of bins
             )
            dg.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)',paper_bgcolor='rgba(0, 0, 0, 0)')
          
            hyp_df=df[df['HYPNOTICSSNDSEDATIVESDRUGS']!=0]  
            eg=px.histogram(
            hyp_df,
            x='HYPNOTICSSNDSEDATIVESDRUGS',
            title='Frequency Distribution of Hypnotics and Sedatives Drugs Sales',
            labels={'HYPNOTICSSNDSEDATIVESDRUGS': 'Hypnotics and Sedatives Drugs Sales'},
            nbins=10  # Number of bins
             )
            eg.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)',paper_bgcolor='rgba(0, 0, 0, 0)')

            Obs_df=df[df['OBSTRUCTIVEAIRWAYDRUGS']!=0]
            hg=px.histogram(
            Obs_df,
            x='OBSTRUCTIVEAIRWAYDRUGS',
            title='Frequency Distribution of Obstructive Airway Drugs Sales',
            labels={'ObstructiveAirwayDrugs': 'Obstructive Airway Drugs Sales'},
            nbins=10  # Number of bins
             )
            hg.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)',paper_bgcolor='rgba(0, 0, 0, 0)')

            Anti_df=df[df['ANTIHISTAMINES']!=0]
            ig=px.histogram(
            Anti_df,
            x='ANTIHISTAMINES',
            title='Frequency Distribution of Antihistamines Sales',
            labels={'ANTIHISTAMINES': 'Antihistamines'},
            nbins=10  # Number of bins
             )
            ig.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)',paper_bgcolor='rgba(0, 0, 0, 0)')
            
            st.session_state.horizontal = True

            histo=st.radio(
                "Choose drug",
                ['ACETICACIDDERIVATIVES', 'PROPIONICACIDDERIVATIVES', 'SALICYLICACIDDERIVATIVES',
                'PYRAZOLONESANDANILIDES', 'ANXIOLYTICDRUGS', 'HYPNOTICSSNDSEDATIVESDRUGS',
                'OBSTRUCTIVEAIRWAYDRUGS', 'ANTIHISTAMINES'],
                horizontal=st.session_state.horizontal,
            )

            if histo=="ACETICACIDDERIVATIVES":
                st.plotly_chart(fig)

            elif histo=="SALICYLICACIDDERIVATIVES":
                st.plotly_chart(gig)

            elif histo=="PROPIONICACIDDERIVATIVES":
                st.plotly_chart(ag)

            elif histo=="PYRAZOLONESANDANILIDES":
                st.plotly_chart(cg)

            elif histo=="ANXIOLYTICDRUGS":
                st.plotly_chart(dg)

            elif histo=="HYPNOTICSSNDSEDATIVESDRUGS":
                st.plotly_chart(eg)

            elif histo=="OBSTRUCTIVEAIRWAYDRUGS":
                st.plotly_chart(hg)

            elif histo=="ANTIHISTAMINES":
                st.plotly_chart(ig)









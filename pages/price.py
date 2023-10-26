
from urllib.error import URLError
import altair as alt
import pandas as pd
import streamlit as st
from streamlit.hello.utils import show_code
from datetime import datetime
import calculos


def data_frame_demo():
    @st.cache_data
    def calc_price():
        AWS_BUCKET_URL = "https://streamlit-demo-data.s3-us-west-2.amazonaws.com"
    
    try:
        cols = st.columns(5)
        # intial inputs to calculate
        with cols[0]:
            rate = st.number_input("Intereste rate", value=0.0185993143, placeholder="type a rate...", format="%.6f")
        with cols[1]:
            loan = st.number_input("Loan value", value=93868.71, placeholder="Type loan value...")
        with cols[2]:
            term = st.number_input("Term", value=60, placeholder="Type term...", min_value=0)
        with cols[3]:
            grace = st.number_input("Grace Period", value=0, placeholder="Type grace period...")
        with cols[4]:
            start_date = st.date_input("Select a start date", datetime(2023, 6, 1))

    # define the dataframe with the inputs
    
        

        df = calculos.inputs(rate, loan, term, grace, start_date)
        
        if isinstance(df, list):
            for error in df:
                st.warning(error)
        else:
            st.write("### Inputs selected", df)
            df_amort = calculos.amort_by_column(df)
            df_final = calculos.processar_dataframe(df_amort)
            st.dataframe(df_final)

            
            csv_data = df_final.to_csv(index=False)
            st.download_button(
                    label="Clique aqui para baixar o CSV",
                    data=csv_data,
                    file_name="data.csv",
                key="download-csv",
                                )

    except URLError as e:
        st.error(
            """
            **This demo requires internet access.**
            Connection error: %s
        """
            % e.reason
        )








st.set_page_config(page_title="Simulador Price", page_icon="📊")
st.markdown("# Simulador Price")
st.sidebar.header("Simulador Price")

data_frame_demo()

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
            rate = st.number_input("Intereste rate", value=0.0185993143, placeholder="type a rate...")
        with cols[1]:
            loan = st.number_input("loan value", value=93868.71, placeholder="Type a number...")
        with cols[2]:
            term = st.number_input("term", value=60, placeholder="Type a number...", min_value=0)
        with cols[3]:
            carencia = st.number_input("carencia", value=0, placeholder="Type a number...")
        with cols[4]:
            start_date = st.date_input("Select a start date", datetime(2023, 6, 1))

    # define the dataframe with the inputs
    
        

        df = calculos.inputs(rate, loan, term, carencia, start_date)
        
        if isinstance(df, list):
            for error in df:
                st.warning(error)
        else:
            st.write("### Inputs selected", df)
            

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
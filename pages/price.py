
from urllib.error import URLError
import altair as alt
import pandas as pd
import streamlit as st
from streamlit.hello.utils import show_code
from datetime import datetime


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
    
        def inputs(rate, loan, term, carencia, start_date):
            rate_day = (rate + 1) ** (1 / 30) - 1

            if carencia == 0:ajust_loan = loan
            elif carencia < 1: ajust_loan = loan - ((rate_day + 1) ** (30 - carencia * 30) - 1) * loan
            else: ajust_loan = ((rate_day + 1) ** (carencia * 30) - 1) * loan + loan
            pmt = ajust_loan * (rate * (1 + rate) ** (term - carencia)) / ((1 + rate) ** (term - carencia) - 1)

            new_data = {'rate': rate, 'rate_day': rate_day, 'carencia': carencia, 'ajust_loan': ajust_loan, 'loan': loan, 'term': term, 'pmt': pmt, 'startDate': start_date}

            df_loan = pd.DataFrame(new_data, index=[0])

            return df_loan

        df = inputs(rate, loan, term, carencia, start_date);
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
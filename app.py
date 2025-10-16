
import streamlit as st

pg = st.navigation([st.Page("pages\Executive_Summary.py"), st.Page("pages\Customer_Touchpoint_Analysis.py"),st.Page("pages\Marketing_Budget_Analysis.py"), st.Page("pages\Sales.py"), st.Page("pages\In_Store.py") ])
pg.run()


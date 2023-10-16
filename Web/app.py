import streamlit as st
import presentation
import yvelines
import maisons_laffitte
import lyon
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Real Estate Value Analysis",
                   layout="wide")




PAGES = {
    "🏠 Presentation": presentation,
    "🌳 Analyse des DVF in Yvelines": yvelines,
    "🏞️ Analyse des DVF in Maisons-Laffite": maisons_laffitte,
    "🏙️ Analyse des DVF in Lyon": lyon
}

# Styling the sidebar
st.sidebar.title('🧭 Navigation')
st.sidebar.markdown('Choisir une page:')



# Using buttons for consistent full box styling
for page_name in PAGES:
    if st.sidebar.button(page_name, key=page_name, on_click=st.session_state.update, args=({"current_selection": page_name},)):
        pass  # the button has been clicked, the page will be updated due to the session state update

# Display the content of the selected page
page = PAGES.get(st.session_state.get("current_selection", "🏠 Presentation"), presentation)
page.app()

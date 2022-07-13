from libraries import *

def input_data():
    uploaded_file = st.file_uploader("Choose a CSV", type=["csv"])
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file, encoding= 'unicode_escape')
        return data



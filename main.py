from PIL.Image import HAMMING
from numpy.random.mtrand import f
from libraries import *
from home import *
from lib.dataset import *
from lib.processing import *
from lib.EDA import *


st.set_page_config(page_title='Online Retail', layout = 'wide', initial_sidebar_state = 'auto')

# Initialization
dates: Dict[Any, Any] = dict()
report: List[Dict[str, Any]] = []


MESSAGE_LIMIT_SIZE = 200

home()        

@st.cache
def data_process(data):
    data['InvoiceDate'] = invoice_data_process(data,string_to_date)
    data['CustomerID'] = data_processing(data)
    data['Country_new'] = new_country(data)
    return data

st.sidebar.title("Select Data and Model")
# Load data
with st.sidebar.expander("Dataset", expanded=True):
    uploaded_file = st.file_uploader("Choose a CSV", type=["csv"])
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file, encoding= 'unicode_escape')
    
        select_func = st.selectbox("Choose a function",
        ('View EDA & Processing', 'Customer Segmentation'))
        
        



if uploaded_file is not None:   
    with st.sidebar.expander("Customer Segmentation", expanded=True):
        df_CT = st.selectbox('Pick your Country', options=data['Country'].unique())
        
    
        country = country_select(data, df_CT)
        country = country[pd.notnull(country['Country'])]
        country = country[(country['Quantity'] >0)]
        country['TotalSale'] = country['Quantity'] * country['UnitPrice']
        #convert country['InvoiceDate'] to datetime
        country['InvoiceDate'] = pd.to_datetime(country['InvoiceDate']).dt.date
        df_RFM = data_rfm(country)
        df_RFM = create_rfm_col(df_RFM)
        def join_rfm(x): return str(int(x['R'])) + str(int(x['F'])) + str(int(x['M']))
        df_RFM['RFM_Segment'] = df_RFM.apply(join_rfm, axis=1)
        df_RFM['RFM_Score'] = df_RFM[['R','F','M']].sum(axis=1)
        df_RFM['RFM_Level'] = df_RFM.apply(rfm_level, axis=1)
        rfm_agg = rfm_agg_processs(df_RFM)
        df_now = df_RFM[['Recency', 'Frequency', 'Monetary']]
        if select_func == 'Customer Segmentation':
            clusters_number = st.slider('Pick a Cluster Number',min_value=1, max_value=10, value=3)
            rfm_agg2 = get_customerID_by_cluster(df_now,clusters_number)
            rfm_agg3 = get_plot_by_k(df_now)
            
            view_cluster = st.checkbox("View by each Cluster")
            if view_cluster:
                cluster = rfm_agg2[rfm_agg2['Cluster'].isin(rfm_agg2['Cluster'])]
                cluster_to_view = st.selectbox('Please select a cluster to view data', options=cluster['Cluster'].unique())
                cluster_to_show = cluster[cluster['Cluster'] == cluster_to_view]
            if not view_cluster:
                cluster_to_show = rfm_agg3
            
            if view_cluster:
                view_customer = st.checkbox("Select your Customer")
                if view_customer:
                    customer_id = st.selectbox('Select CustomerID',options = cluster_to_show['CustomerID'].unique())
                    df_customer = data[data['CustomerID'] == customer_id]
                if not view_customer:
                    df_customer = data[data['CustomerID'].isin(rfm_agg2['CustomerID'])]
                
            download_data = st.checkbox("Download Data",value=False)
    





if uploaded_file is None:
    st.error('No data was uploaded')

if uploaded_file is not None:
    st.success('Data was successfully uploaded')

    
    if select_func == 'View EDA & Processing':
        data = EDA(data)
        st.write('89% of Customer come from UK, but we can use the dropdown to explore other countries information')
        st.dataframe(country.head())
        st.write(f'### Information about the {df_CT}')
        for i in country.columns:
            count = country[i].nunique()
            st.write(i, ": ", count)
        st.write(f'### Transaction Information of {df_CT}')
        st.write(f"Transaction timeframe from {country['InvoiceDate'].min()} to {country['InvoiceDate'].max()}")
        st.write('{:,} Transaction don\'t have a customer id'.format(country[country['CustomerID'].isnull()].shape[0]))
        st.write('{:,} unique_customer_id'.format(len(country['CustomerID'].unique())))
        st.write('### RFM Segmentation of the dataset')
        st.dataframe(df_RFM.head())
        st.dataframe(df_RFM.tail())
        st.write('Review some information from RFM data')
        for i in range(len(df_RFM.tail(3))):
            st.write(f"- CustomerID {df_RFM.index[i]} has frequency {df_RFM['Frequency'].iloc[i]} with the monetary value: {df_RFM['Monetary'].iloc[i]} and recency {df_RFM['Recency'].iloc[i]} days")
        st.write('### Visualize RFM Segmentation with given RFM')    
        #Create our plot and resize it.
        fig2 = plt.gcf()
        ax = fig2.add_subplot()
        fig2.set_size_inches(14, 10)

        #Define colors array
        #colors_dict = {'ACTIVE':'bluesapphire','FOCUS':'royalblue', 'LIGHT':'cyan','LOST':'red', 'LOYAL':'purple', 'NEW':'green', 'REGULARS':'gold', 'SHARK':'gold', 'WHALE':'gold'}

        squarify.plot(sizes=rfm_agg['Monetary_count'],
                    text_kwargs={'fontsize':12,'weight':'bold', 'fontname':"sans serif"},
                    #color=colors_dict.values(),
                    label=['{} \n{:.0f} days \n{:.0f} orders \n{:.0f} $ \n{:.0f} customers ({}%)'.format(*rfm_agg.iloc[i])
                            for i in range(0, len(rfm_agg))], alpha=0.5 )


        plt.title("Customers Segments",fontsize=26,fontweight="bold")
        plt.axis('off')

        plt.savefig('RFM Segments.png')
        st.pyplot(fig2)
        
        

    if select_func == 'Customer Segmentation':
        string_to_date = lambda x : datetime.strptime(x, "%d-%m-%Y %H:%M").date()

        df_country = country_processing(data)
        # st.write(data.head())
        plt_agg3 = plot_by_k(rfm_agg3)
        plt.savefig('Clustering Segments.png')
        if download_data:    
            with open("Clustering Segments.png", "rb") as file:
                btn = st.download_button(
                    label="Download image",
                    data=file,
                    file_name="Clustering Segments.png",
                    mime="image/png"
                    )
            
        st.write('### View all Cluster Information')
        st.dataframe(rfm_agg3)
        if download_data:
            csv_rfm_agg3 = convert_df(rfm_agg3)
            csv_name = f'AllClusterInformation.csv'
            st.download_button(
                "Download All Cluster Information ",
                csv_rfm_agg3,
                csv_name,
                "text/csv",
                key='download-csv'
                )

        if view_cluster:
            st.write(f"### View {cluster_to_view} Information")
            st.dataframe(cluster_to_show)
            if download_data:
                csv_cluster_to_show = convert_df(cluster_to_show)
                csv_name = f'{cluster_to_view}Information.csv'
                st.download_button(
                    "Download Cluster Information",
                    csv_cluster_to_show,
                    csv_name,
                    "text/csv",
                    key='download-csv'
                    )

            if view_customer:
                st.write('### View all Customer Information In Cluster')
                # df_customer = data[data['CustomerID']]
                st.dataframe(df_customer)
                if download_data:
                    csv_df_customer = convert_df(df_customer)
                    csv_name = f'CustomerFrom{cluster_to_view}.csv'
                    st.download_button(
                        "Download Customer Information",
                        csv_df_customer,
                        csv_name,
                        "text/csv",
                        key='download-csv'
                        )            
                               
                                     
        st.write('### Summary Cluster Information')
        if not view_cluster:
            for i in range(len(cluster_to_show)):
                st.write(f"- {cluster_to_show['Cluster'][i]} has frequency {cluster_to_show['FrequencyMean'].iloc[i]} with the monetary value {cluster_to_show['MonetaryMean'].iloc[i]} and recency {cluster_to_show['RecencyMean'].iloc[i]} days")
        if view_cluster:
            view_by_cluster = rfm_agg3[rfm_agg3['Cluster'] == cluster_to_view].reset_index().drop('index', axis=1)
            for i in range(len(view_by_cluster)):
                st.write(f"- {view_by_cluster['Cluster'][i]} has frequency {view_by_cluster['FrequencyMean'].iloc[i]} with the monetary value {view_by_cluster['MonetaryMean'].iloc[i]} and recency {view_by_cluster['RecencyMean'].iloc[i]} days")
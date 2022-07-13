from libraries import *
from lib.dataset import *


@st.cache 
# df_head = data.head(3)
# df_tail = data.tail(3)
# df_info = data.info()
# df_shape = data.shape
# data.isnull().sum()
# # pp.ProfileReport(data)

# st.dataframe(df_head)
# st.dataframe(df_tail)

# InvoiceDate


# Convert InvoiceDate from object to datetime format
def invoice_data_process(data):
    string_to_date = lambda x : datetime.strptime(x, "%d-%m-%Y %H:%M").date()
    data['InvoiceDate'] = data['InvoiceDate'].apply(string_to_date)
    data['InvoiceDate'] = data['InvoiceDate'].apply(lambda x: x.strftime('%Y-%m-%d'))
    return data['InvoiceDate']


# data['InvoiceDate'] = data['InvoiceDate'].apply(string_to_date)
# data['InvoiceDate'] = data['InvoiceDate'].astype('datetime64[ns]')

# Let’s take a closer look at the data we will need to manipulate.
# print('Transactions timeframe from {} to {}'.format(data['InvoiceDate'].min(), data['InvoiceDate'].max()))
# print('{:,} transactions don\'t have a customer id'.format(data[data.CustomerID.isnull()].shape[0]))
# print('{:,} unique customer_id'.format(len(data.CustomerID.unique())))

def data_processing(data):
    data = data.dropna()
    data = data.drop_duplicates()
    data['CustomerID'] = data['CustomerID'].astype('int64')
    return data['CustomerID']

def new_country(data):
    values = ['UK', 'Others']
    condition = (data['Country'] == 'United Kingdom'), (data['Country'] != 'United Kingdom')
    data['Country_new'] = np.select(condition, values)
    return data['Country_new']

def country_processing(data):
    df_country = data[['Country', 'CustomerID']].groupby(['Country']) \
                .count().sort_values(by='CustomerID', ascending=False) \
                .reset_index()
    df_country['Percent'] = df_country['CustomerID'] / df_country['CustomerID'].sum()*100
    return df_country



# Trong data, số lượng InvoiceNo của Country United Kingdom chiếm phần lớn 88.8%
# Ta chọn Country = 'United Kingdom' làm phân tích

def country_select(data, df_CT):
    country = data.loc[data['Country'] == df_CT]
    return country

#Quantity Information
def quanity_country(country):
    st.write('Quantity Information')
    st.write("Quantity <= 0:")
    st.write("Count : ",country[country['Quantity'] <= 0]['InvoiceNo'].count())
    st.write("Percent: ",country[country['Quantity'] <= 0]['InvoiceNo'].count() / country.shape[0])
    st.write("Quantity > 0:")
    st.write("Count : ",country[country['Quantity'] > 0]['InvoiceNo'].count())
    st.write("Percent: ",country[country['Quantity'] > 0]['InvoiceNo'].count() / country.shape[0])
    
#gross sale calculation -> gross_sale = UnitPricexQuantity

#create RFM analysis for each customer

def data_rfm(country):
    max_date = country['InvoiceDate'].max()
    Recency = lambda x : (max_date - x.max()).days
    Frequency = lambda x : len(x.unique())
    Monetary = lambda x : round(sum(x), 2)
    
    df_RFM = country.groupby('CustomerID').agg({'InvoiceDate': Recency,
                                    'InvoiceNo': Frequency,
                                    'TotalSale': Monetary})

    # Rename the columns of DataFrame
    df_RFM.columns = ['Recency', 'Frequency', 'Monetary']
    df_RFM = df_RFM.sort_values('Monetary', ascending=False)
    df_RFM.index = df_RFM.index.astype(int)

    return df_RFM



def RScore(x,p,d):
    if x <= d[p][0.25]:
        return 4
    elif x <= d[p][0.50]:
        return 3
    elif x <= d[p][0.75]: 
        return 2
    else:
        return 1
    
def FMScore(x,p,d):
    if x <= d[p][0.25]:
        return 1
    elif x <= d[p][0.50]:
        return 2
    elif x <= d[p][0.75]: 
        return 3
    else:
        return 4

#create RFM column
def create_rfm_col(df_RFM):
    quantiles = df_RFM.quantile(q=[0.25,0.5,0.75])
    quantiles = quantiles.to_dict()
    df_RFM['R'] = df_RFM['Recency'].apply(RScore, args=('Recency',quantiles,))
    df_RFM['F'] = df_RFM['Frequency'].apply(FMScore, args=('Frequency',quantiles,))
    df_RFM['M'] = df_RFM['Monetary'].apply(FMScore, args=('Monetary',quantiles,))
    return df_RFM

#manual segmentation
def rfm_level(df):
    if (df['R'] == 4 and df['F'] ==4 and df['M'] == 4)  :
        return 'WHALE'
    
    elif (df['R'] == 4 and df['F'] ==1 and df['M'] == 1):
        return 'NEW'
    
    elif (df['R'] == 4 and df['F'] ==1 and df['M'] == 4):
        return 'FOCUS'
    
    else:     
        if df['M'] == 4:
            return 'SHARK'
        
        elif df['F'] == 4:
            return 'LOYAL'
        
        elif df['R'] == 4:
            return 'ACTIVE'
        
        elif df['R'] == 1:
            return 'LOST'
        
        elif df['M'] == 1:
            return 'LIGHT'
        
        return 'REGULARS'

#rfm_agg process
def rfm_agg_processs(df_RFM):
    rfm_agg = df_RFM.groupby('RFM_Level').agg({'Recency':'mean', 'Frequency':'mean', 'Monetary':['mean','count']}).round(0)
    rfm_agg.columns = rfm_agg.columns.droplevel()
    rfm_agg.columns = ['Recency_mean', 'Frequency_mean', 'Monetary_mean', 'Monetary_count']
    rfm_agg['Percent'] = round((rfm_agg['Monetary_count']/rfm_agg['Monetary_count'].sum())*100,2)
    #reset the index
    rfm_agg = rfm_agg.reset_index()
    return rfm_agg

def rfm_agg_tree_plot(rfm_agg):
    #Create our plot and resize it.
    fig1 = plt.gcf()
    ax = fig1.add_subplot()
    fig1.set_size_inches(14, 10)

    #Define colors array
    #colors_dict = {'ACTIVE':'bluesapphire','FOCUS':'royalblue', 'LIGHT':'cyan','LOST':'red', 'LOYAL':'purple', 'NEW':'green', 'REGULARS':'gold', 'SHARK':'gold', 'WHALE':'gold'}

    squarify.plot(sizes=rfm_agg['Monetary_count'],
                text_kwargs={'fontsize':12,'weight':'bold', 'fontname':"sans serif"},
                #color=colors_dict.values(),
                label=['{} \n{:.0f} days \n{:.0f} orders \n{:.0f} $ \n{:.0f} customers ({}%)'.format(*rfm_agg.iloc[i])
                        for i in range(0, len(rfm_agg))], alpha=0.5 )


    plt.title("Customers Segments",fontsize=26,fontweight="bold")
    plt.axis('off')
    st.pyplot(fig1)




def rfm_agg_plotly(rfm_agg):
    
    fig1 = px.scatter(rfm_agg, x="Recency_mean", y="Monetary_mean", size="Frequency_mean", color="RFM_Level",
            hover_name="RFM_Level", size_max=100)
    st.plotly_chart(fig1, use_container_width=True)
    
    
    
def k_processing(df_RFM):
    df_now = df_RFM[['Recency', 'Frequency', 'Monetary']]
    sse = {}

    for k in range(1, 20):
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(df_now)
        sse[k] = kmeans.inertia_ # SSE to closest cluster centroid
        

def get_customerID_by_cluster(df_now, clusters_number):
    model = KMeans(n_clusters=clusters_number, random_state=42)
    model.fit(df_now)
    model.labels_.shape

    df_now['Cluster'] = model.labels_
    df_now.groupby('Cluster').agg({'Recency':'mean', 'Frequency':'mean', 'Monetary':['mean','count']}).round(2) 

    # Calculate average values for each RFM_Level, and return a size of each segment 
    rfm_agg2 = df_now.groupby(['Cluster','CustomerID']).agg({
    'Recency': 'mean',
    'Frequency': 'mean',
    'Monetary': ['mean', 'count']}).round(0)

    rfm_agg2.columns = rfm_agg2.columns.droplevel()
    rfm_agg2.columns = ['RecencyMean','FrequencyMean','MonetaryMean', 'Count']
    rfm_agg2['Percent'] = round((rfm_agg2['Count']/rfm_agg2.Count.sum())*100, 2)

    # Reset the index
    rfm_agg2 = rfm_agg2.reset_index()

    # Change thr Cluster Columns Datatype into discrete values
    rfm_agg2['Cluster'] = 'Cluster '+ rfm_agg2['Cluster'].astype('str')

    # Print the aggregated dataset
    return rfm_agg2

#for plotting
# Calculate average values for each RFM_Level, and return a size of each segment 
def get_plot_by_k(df_now):
    rfm_agg3 = df_now.groupby('Cluster').agg({
    'Recency': 'mean',
    'Frequency': 'mean',
    'Monetary': ['mean', 'count']}).round(0)

    rfm_agg3.columns = rfm_agg3.columns.droplevel()
    rfm_agg3.columns = ['RecencyMean','FrequencyMean','MonetaryMean', 'Count']
    rfm_agg3['Percent'] = round((rfm_agg3['Count']/rfm_agg3.Count.sum())*100, 2)

    # Reset the index
    rfm_agg3 = rfm_agg3.reset_index()

    # Change thr Cluster Columns Datatype into discrete values
    rfm_agg3['Cluster'] = 'Cluster '+ rfm_agg3['Cluster'].astype('str')
    return rfm_agg3

#Create our plot and resize it.
def plot_by_k(rfm_agg3):
    fig = plt.gcf()
    ax = fig.add_subplot()
    fig.set_size_inches(14, 10)

    # colors_dict2 = {'Cluster0':'yellow','Cluster1':'royalblue', 'Cluster2':'cyan',
    #             'Cluster3':'red', 'Cluster4':'purple', 'Cluster5':'green', 'Cluster6':'gold'}

    squarify.plot(sizes=rfm_agg3['Count'],
                text_kwargs={'fontsize':12,'weight':'bold', 'fontname':"sans serif"},
                label=['{} \n{:.0f} days \n{:.0f} orders \n{:.0f} $ \n{:.0f} customers ({}%)'.format(*rfm_agg3.iloc[i])
                        for i in range(0, len(rfm_agg3))], 
                alpha=0.5 )


    plt.title("Customers Segments",fontsize=26,fontweight="bold")
    plt.axis('off')


    st.pyplot(fig)


def convert_df(df):
   return df.to_csv().encode('utf-8')


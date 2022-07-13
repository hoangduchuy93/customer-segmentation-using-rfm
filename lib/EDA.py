from libraries import *

def EDA(data):
    df_head = data.head(3)
    df_tail = data.tail(3)

    st.write("Some data")
    st.write(df_head)
    st.write(df_tail)

    data['InvoiceDate'] = data['InvoiceDate'].str.split(' ',expand=True)[0]

    string_to_date = lambda x : datetime.strptime(x, '%d-%m-%Y').date()
    # convert invoiceDate from object to datetime format
    data['InvoiceDate'] = data['InvoiceDate'].apply(string_to_date)
    data['InvoiceDate'] = data['InvoiceDate'].astype('datetime64[ns]')

    data = data[pd.notnull(data['CustomerID'])]
    #Let's take a look on the countries of data
    customer_country=data[['Country','CustomerID']].drop_duplicates()
    df_customer_country = customer_country.groupby(['Country'])['CustomerID'].aggregate('count').reset_index().sort_values('CustomerID', ascending=False)
    
    st.write("CustomerID count with every country:")
    st.write(df_customer_country)

    countries = customer_country['Country'].value_counts()

    data_country = dict(type='choropleth',
    locations = countries.index,
    locationmode = 'country names', z = countries,
    text = countries.index, colorbar = {'title':'Order nb.'},
    colorscale=[[0, 'rgb(224,255,255)'],
                [0.01, 'rgb(166,206,227)'], [0.02, 'rgb(31,120,180)'],
                [0.03, 'rgb(178,223,138)'], [0.05, 'rgb(51,160,44)'],
                [0.10, 'rgb(251,154,153)'], [0.20, 'rgb(255,255,0)'],
                [1, 'rgb(227,26,28)']],    
    reversescale = False)

    layout = dict(title='Number of orders per country',
    geo = dict(showframe = True, projection={'type':'mercator'}))
    choromap = go.Figure(data = [data_country], layout = layout)
    choromap.update_layout(title_x=0.5, width=1000, height=700, font_color="#000000", title_font_color="#FF9833")
    # iplot(choromap, validate=False)
    st.plotly_chart(choromap,validate=False,use_container_width=True)
    
    st.write(f'The CustomerID in UK {customer_country[customer_country["Country"]=="United Kingdom"].shape[0]}')
    st.write(f'The CustomerID in Non-UK {customer_country[customer_country["Country"]!="United Kingdom"].shape[0]}')
    st.write(f'The ratio between total CustomerID in UK vs Non-UK {customer_country[customer_country["Country"]!="United Kingdom"].shape[0]/customer_country[customer_country["Country"]=="United Kingdom"].shape[0]:,.2f}')


def get_month(dframe, x) : return dt.datetime(x.year,x.month,1)
def get_month_int (dframe,column):
    year = dframe[column].dt.year
    month = dframe[column].dt.month
    day = dframe[column].dt.day
    return year, month , day 

def Cohort(dframe):
    dframe['InvoiceMonth'] = dframe['InvoiceDate'].apply(get_month)
    grouping = dframe.groupby('CustomerID')['InvoiceMonth']
    dframe['CohortMonth'] = grouping.transform('min')
    # data.tail()
    invoice_year,invoice_month,_ = get_month_int(dframe,'InvoiceMonth')
    cohort_year,cohort_month,_ = get_month_int(dframe,'CohortMonth')

    year_diff = invoice_year - cohort_year 
    month_diff = invoice_month - cohort_month 

    dframe['CohortIndex'] = year_diff * 12 + month_diff + 1 

    #Count monthly active customers from each cohort
    grouping = dframe.groupby(['CohortMonth', 'CohortIndex'])
    cohort_data = grouping['CustomerID'].apply(pd.Series.nunique)
    # Return number of unique elements in the object.
    cohort_data = cohort_data.reset_index()
    cohort_counts = cohort_data.pivot(index='CohortMonth',columns='CohortIndex',values='CustomerID')
    cohort_counts

    # Retention table
    cohort_size = cohort_counts.iloc[:,0]
    retention = cohort_counts.divide(cohort_size,axis=0) #axis=0 to ensure the divide along the row axis 
    retention.round(3) * 100 #to show the number as percentage

    #Build the heatmap
    plt.figure(figsize=(15, 8))
    plt.title('Retention rates')
    sns.heatmap(data=retention,annot = True,fmt = '.0%',vmin = 0.0,vmax = 0.5,cmap="BuPu_r")
    st.pyplot(fig)

    #Average quantity for each cohort
    grouping = dframe.groupby(['CohortMonth', 'CohortIndex'])
    cohort_data = grouping['Quantity'].mean()
    cohort_data = cohort_data.reset_index()
    average_quantity = cohort_data.pivot(index='CohortMonth',columns='CohortIndex',values='Quantity')
    average_quantity.round(1)
    average_quantity.index = average_quantity.index.date

    #Build the heatmap
    plt.figure(figsize=(15, 8))
    plt.title('Average quantity for each cohort')
    sns.heatmap(data=average_quantity,annot = True,vmin = 0.0,vmax =20,cmap="BuGn_r")
    st.pyplot(fig)

def RFM(dframe):
    max_date = dframe['InvoiceDate'].max().date()
    Recency = lambda x: (max_date - x.max().date()).days
    Frequency = lambda x: len(x)
    Monetary = lambda x: x.sum()
    df_RFM = dframe.groupby('CustomerID').agg({'InvoiceDate': Recency, 'InvoiceNo': Frequency, 'TotalSale':Monetary})
    
    #Rename the columns of DataFrame
    df_RFM.columns = ['Recency', 'Frequency', 'Monetary']
    #Desending sorting
    df_RFM = df_RFM.sort_values(by=['Monetary'], ascending=False)

    # Visualization the distribution of R F M
    fig = plt.figure(figsize=(10,10))
    plt.subplot(3,1,1)
    sns.distplot(df_RFM['Recency'])#plot distribution of R
    plt.subplot(3,1,2)
    sns.distplot(df_RFM['Frequency'])#plot distribution of F
    plt.subplot(3,1,3)
    sns.distplot(df_RFM['Monetary'])#plot distribution of M
    st.pyplot(fig)


def hopkins(X):
    d = X.shape[1]
    #d = len(vars) # columns
    n = len(X) # rows
    m = int(0.1 * n) # heuristic from article [1]
    nbrs = NearestNeighbors(n_neighbors=1).fit(X.values)
 
    rand_X = sample(range(0, n, 1), m)
 
    ujd = []
    wjd = []
    for j in range(0, m):
        u_dist, _ = nbrs.kneighbors(uniform(np.amin(X,axis=0),np.amax(X,axis=0),d).reshape(1, -1), 2, return_distance=True)
        ujd.append(u_dist[0][1])
        w_dist, _ = nbrs.kneighbors(X.iloc[rand_X[j]].values.reshape(1, -1), 2, return_distance=True)
        wjd.append(w_dist[0][1])
 
    H = sum(ujd) / (sum(ujd) + sum(wjd))
    if isnan(H):
        print(ujd, wjd)
        H = 0

    return H




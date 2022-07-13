from libraries import *

def home():
    st.title("Online Retail Data Set")
    st.write("### Business Objective/Problem")
    st.write("Build the clustering of customers based on the given information from the company, which divided audience by type for a suitable business plan and customer service in next time.")
    st.write("### Business Understanding")
    st.write("Find the solution to improve the marketing, and based on these data we can do more activities like: increase sales, improve customer experience.")    
    
    st.write("### Data Understanding / Acquire")
    st.write("This is a transactional data set which contains all the transactions occurring between 01/12/2010 and 09/12/2011 for a UK-based and registered non-store online retail.The company mainly sells unique all-occasion gifts. Many customers of the company are wholesalers.")
    st.write("All the data are exported and saved under avocado.csv with 18249 records. With the included information:")
    st.write("- InvoiceNo: Invoice number. Nominal, a 6-digit integral number uniquely assigned to each transaction. If this code starts with letter 'c', it indicates a cancellation.")
    st.write("- StockCode: Product (item) code. Nominal, a 5-digit integral number uniquely assigned to each distinct product.")
    st.write("- Description: Product (item) name. Nominal.")
    st.write("- Quantity: The quantities of each product (item) per transaction. Numeric.")    
    st.write("- InvoiceDate: Invice Date and time. Numeric, the day and time when each transaction was generated.")    
    st.write("- UnitPrice: Unit price. Numeric, Product price per unit in sterling.")    
    st.write("- CustomerID: Customer number. Nominal, a 5-digit integral number uniquely assigned to each customer.")    
    st.write("- Country: Country name. Nominal, the name of the country where each customer resides.") 
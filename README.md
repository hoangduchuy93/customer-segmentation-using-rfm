![image](https://user-images.githubusercontent.com/91864024/178642808-201e7d4e-7c46-499c-a16d-24b32190c179.png)
# Customer Segmentation using RFM
## I. Outline
- This project aims to cluster customers based on their characteristics and consumption history to understand and provide customers with better service.
- The demo app is implemented on Streamlit, available for your experience:
https://hoangduchuy93-customer-segmentation-using-rfm-main-ckkqey.streamlitapp.com/
## II. Business Objective/ Problem
- Company X mainly sells products that are gifts for special occasions. Many of the company's customers are wholesale customers.
- Company X wishes to be able to sell more products as well as introduce products to the right customers, take care and satisfy customers.
- This segmentation project is built on that request
## III. Project implementation
### 1. Business Understanding
Based on the above description => identify the problem:

- Find solutions to improve advertising effectiveness, thereby increasing sales, improving customer satisfaction.
- Objectives/problems: build a customer clustering system based on the information provided by the company, which can help the company identify different customer groups to have improve business and care strategy.
- Applied mothodes/models:
  - RFM score segmentation
  - KMeans clustering
  - Hierarchical clustering
  - GMM clutering

![image](https://user-images.githubusercontent.com/91864024/178650606-5afdf562-5658-4d1e-9543-c2933e2c2661.png)
### 2. Data Understanding/ Acquire
- All data is stored in the file OnlineRetail.csv with 541,909 records containing all transactions that occurred from December 1, 2010 to December 9, 2011 for online retail.
- Data Description: https://archive.ics.uci.edu/ml/datasets/online+retail
- Attribute Information:
  - InvoiceNo: Invoice number. Nominal, a 6-digit integral number uniquely assigned to each transaction. If this code starts with letter 'c', it indicates a cancellation.
  - StockCode: Product (item) code. Nominal, a 5-digit integral number uniquely assigned to each distinct product.
  - Description: Product (item) name. Nominal.
  - Quantity: The quantities of each product (item) per transaction. Numeric.
  - InvoiceDate: Invice Date and time. Numeric, the day and time when each transaction was generated.
  - UnitPrice: Unit price. Numeric, Product price per unit in sterling.
  - CustomerID: Customer number. Nominal, a 5-digit integral number uniquely assigned to each customer.
  - Country: Country name. Nominal, the name of the country where each customer resides.
### 3. Build model
The steps to build model are:
- Read and understand the data
- Clean the data
- Prepare the data for modelling
- Modelling applied RFM segmentation, KMeans clustering, Hierarchical clustering, GMM clustering
- Final analysis and choose option that suitable for company
### 4. User interface
You can connect to the demo app (https://hoangduchuy93-customer-segmentation-using-rfm-main-ckkqey.streamlitapp.com/) for your experience. Below image show welcome screen:
![image](https://user-images.githubusercontent.com/91864024/178672346-1ce4424d-cc84-4da3-8e8b-cf16cdbd14dc.png)

#### 1. EDA and processing
- Upload OnlineRetail.csv from your local path (click on the box "Browse file" on the left).
- By default, you will access to "View EDA & Processing", with country United Kingdom. You can change to another country for your reference. 
- In this part, you can see some information about transaction made by that country (in this case is UK), RFM segmentation for UK and visulization for RFM
- Some photos for this function as below:
![image](https://user-images.githubusercontent.com/91864024/178682454-394c99dd-98e0-47ba-bc34-6f721d9f419d.png)
![image](https://user-images.githubusercontent.com/91864024/178682650-02c9d473-bec2-4e9e-9886-6b075abef1eb.png)

#### 2. Customer Segmentation
- In this function, you can choose your country from drop-box (by default: United Kingdom), number of clusters that you want to make segmentation.
- Besides, you can also click to choose a cluster, a customer_id for review or download (e.g: you can choose cluster 0, user_id = 12747 from drop-box, and tick download data from box). This should enable to download information of cluster 0, information for customer_id = 12747 for further analysis.
![image](https://user-images.githubusercontent.com/91864024/178686233-73aa2f3d-e9cb-461d-b3ad-38f093b42cc7.png)





  

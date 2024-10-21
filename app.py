import streamlit as st
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import datetime
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go

#Setting page layout
st.set_page_config(layout = 'wide')
st.markdown('<style>div.block-container{padding-top:3rem;}</style>', unsafe_allow_html = True)
## The code modifies the appearance of the Streamlit app by adding top padding to the main content container. It also allows custom CSS styling.

#Uploading instacart logo
logo = Image.open('instacart_logo_.jpg')

#Reading the data from csv files
@st.cache_data
def load_data():
    df_products = pd.read_csv('instacart_markey_basket_analysis/products.csv')
    df_aisles = pd.read_csv('instacart_markey_basket_analysis/aisles.csv')
    df_departments = pd.read_csv('instacart_markey_basket_analysis/departments.csv')
    df_orders = pd.read_csv('instacart_markey_basket_analysis/orders.csv') 
    df_ordprior = pd.read_csv('instacart_markey_basket_analysis/order_products__prior.csv') 
    return df_products, df_aisles, df_departments, df_orders, df_ordprior

@st.cache_data
def preprocess_data(df_products, df_aisles, df_departments, df_orders, df_ordprior):
    # Merging product, aisle, and department data
    df_pa = pd.merge(df_products, df_aisles, on='aisle_id', how='inner')
    df_prod_ais_dep = pd.merge(df_pa, df_departments, on='department_id', how='inner')
    df_prod_ais_dep = df_prod_ais_dep.drop(['aisle_id', 'department_id'], axis=1)
    
    # Merging order and product data
    df_orders = pd.merge(df_orders, df_ordprior, on='order_id', how='inner')
    df_orders_product = pd.merge(df_orders, df_prod_ais_dep, on='product_id', how='inner')
    
    # Selecting only Orders with Organic Products
    # Step 1: Filter products that are organic
    df_organic_product = df_orders_product[df_orders_product['product_name'].str.contains('Organic', na=False)]
    # Step 2: Identify unique order_ids for orders containing organic product
    organic_order_ids = df_organic_product['order_id'].unique()
    # Step 3: Filter the df_orders_product dataframe to include only orders with at least one organic product
    df_organic_orders_product = df_orders_product[df_orders_product['order_id'].isin(organic_order_ids)]
    
    # Return both the original filtered DataFrame and the processed DataFrame
    return df_organic_product, df_organic_orders_product
    
# Load data
df_products, df_aisles, df_departments, df_orders, df_ordprior = load_data()

# Preprocess data
df_organic_product, df_organic_orders_product = preprocess_data(df_products, df_aisles, df_departments, df_orders, df_ordprior)

col1, col2 = st.columns([0.1, 0.9])
with col1:
    st.image(logo, width = 100)

html_title = """
    <style>
    .title-test {
        font-weight: bold;
        padding: 3px;
        border-radius: 6px;
    }
    .subtitle-test {
        margin-top: -7px;
    }
    </style>
    <center><h2 class='title-test'>Instacart Organic Product Shopping Behavior</h2></center>
    <center><h4 class='title-test subtitle-test'>- Orders Containing Organic Products -</h4></center>
    """

with col2:
    st.markdown(html_title, unsafe_allow_html = True)

st.markdown(
    """
    <style>
    .block-container .main > div {
        margin-bottom: 8.5rem;
    }
    </style>
    """, unsafe_allow_html=True
    )
   

col8, col9, col10, col11 = st.columns([0.11, 0.29, 0.33, 0.26])

with col8:
    box_date =str(datetime.datetime.now().strftime("%d %B %Y"))
    st.write(f'Instacart Data: 2017 ')

with col9:
    st.metric("Instacart Organic Products", "5035")
    st.markdown(
        """
        <div style="font-size: 0.85em; color: rgba(49, 51, 63, 0.6); margin-top: -18px;">
            2017 Instacart Data
        </div>
        """,
        unsafe_allow_html=True
    )

with col10:
    st.metric("Instacart Organic Products (Same-day delivery)", "4280")
    st.markdown(
        """
        <div style="font-size: 0.85em; color: rgba(49, 51, 63, 0.6); margin-top: -18px;">
            2024 NYC Instacart Data
        </div>
        """,
        unsafe_allow_html=True
    )
    
with col11:
    st.metric("% Orders with Organic Products", "73.6%")
    st.markdown(
        """
        <div style="font-size: 0.85em; color: rgba(49, 51, 63, 0.6); margin-top: -18px;">
            2017 Instacart Data
        </div>
        """,
        unsafe_allow_html=True
    )
    
col18, col19 = st.columns([0.1, 0.9])
with col19:
    st.markdown(
                """
                <div style="padding: 15px 0 3px 0; font-weight: bold; font-size: 20px;">
                Shopping Habits: Hourly, Weekly, and Reorder Trends
                </div>
                """,
                unsafe_allow_html=True
            )

col3,col4,col5 = st.columns([0.1, 0.45, 0.45])

#Preparing Col4 Data

# Preparing Col4 Data
df_organic_orders_hour_freq = df_organic_orders_product['order_hour_of_day'].value_counts().reset_index().sort_values('order_hour_of_day', ascending = True).reset_index(drop = True)
df_organic_orders_hour_freq.columns = ['hour', 'count']

with col4:
    fig = px.bar(df_organic_orders_hour_freq, x='hour', y='count',
                color='count',  # Equivalent to the hue parameter in Seaborn
                color_continuous_scale= 'Matter',
                title='Hourly Trends in Online Shopping')
            
    fig.update_traces(
            hovertemplate='<b>Hour:</b> %{x}<br><b>Orders:</b> %{y:,}<extra></extra>'
        )
        
    fig.update_yaxes(range=[0, 3_000_000], title='Orders')
    fig.update_coloraxes(showscale=False)
    fig.update_xaxes(tickmode='linear', dtick=2)
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width = True)

#Preparing Col5 Data
df_organic_orders_day_freq = df_organic_orders_product['order_dow'].value_counts().reset_index().sort_values('order_dow', ascending = True).reset_index(drop = True)
df_organic_orders_day_freq.columns = ['day', 'count']

# Map the days to abbreviations
day_mapping = {
    0: 'Sun',
    1: 'M',
    2: 'Tue',
    3: 'W',
    4: 'T',
    5: 'F',
    6: 'Sat'
}

# Apply the mapping to the DataFrame
df_organic_orders_day_freq['day'] = df_organic_orders_day_freq['day'].map(day_mapping)

with col5:
    fig1 = px.bar(df_organic_orders_day_freq, x='day', y='count', color='count', 
                 color_continuous_scale= 'Matter', 
                 title ='Weekly Trends in Online Shopping')
    fig1.update_traces(
            hovertemplate='<b>Hour:</b> %{x}<br><b>Orders:</b> %{y:,}<extra></extra>'
        )
        
    fig1.update_coloraxes(showscale=False)
    fig1.update_xaxes(tickmode='linear')
    fig1.update_yaxes(title='Orders')
    fig1.update_layout(height=300)
    st.plotly_chart(fig1, use_container_width = True)

# Reduce vertical space with custom CSS
st.markdown(
    """
    <div style="padding-left: 13.5%; font-size: 0.85em; color: rgba(49, 51, 63, 0.6);margin-top: -40px;">
        Online shopping activity peaks during late morning to early afternoon hours (9 AM - 5 PM) and is most frequent on weekends (Saturday and Sunday).
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    .block-container .main > div {
        margin-top: -45px;
    }
    </style>
    """, unsafe_allow_html=True
)

col6, col7 = st.columns([0.1, 0.9])

#Graph on Monthly Trends
df_organic_orders_day_since_order = df_organic_orders_product['days_since_prior_order'].value_counts().reset_index().sort_values('days_since_prior_order', ascending = True).reset_index(drop = True)
df_organic_orders_day_since_order.columns = ['days_since_prior_order', 'count']

with col7:
    fig2 = px.bar(df_organic_orders_day_since_order, x='days_since_prior_order', y='count', color='count', 
                     color_continuous_scale= 'Matter', 
                     title ='Days Since Last Order')
    fig2.update_traces(
            hovertemplate='<b>Day:</b> %{x}<br><b>Orders:</b> %{y:,}<extra></extra>'
         )
            
    fig2.update_coloraxes(showscale=False)
    fig2.update_xaxes(tickmode='linear', dtick=2)
    fig2.update_layout(height=300)
    fig2.update_xaxes(title='Days since last order')
    fig2.update_yaxes(title='Orders')
    st.plotly_chart(fig2, use_container_width = True)

st.markdown(
    """
    <div style="padding-left: 13.5%; font-size: 0.85em; color: rgba(49, 51, 63, 0.6);margin-top: -30px;">
        Reorder activity peaks one week after purchase, with higher weekly order frequency. Setting reminders at the 1-week mark could encourage consistent reordering, especially for wellness and nutrient products. *Note: Orders with gaps over 30 days are capped at 30 in the dataset.
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    .block-container .main > div {
        margin-top: -30px;
    }
    </style>
    """, unsafe_allow_html=True
)

#Graph on Organic Product Department
col12, col13 = st.columns([0.1, 0.9])

data = df_organic_orders_product.groupby("department")["product_id"].count().sort_values(ascending=False).reset_index()
data.columns = ['department', 'total_purchases']

with col13:
    st.markdown(
            """
            <div style="padding: 15px 0 3px 0; font-weight: bold; font-size: 20px;">
            Exploring Customer Preferences in Organic Product Purchases
            </div>
            """,
            unsafe_allow_html=True
        )
    fig3 = px.bar(data, 
                 x='department', 
                 y='total_purchases', 
                 color='total_purchases', 
                 color_continuous_scale='Matter',
                 title='Popular Departments for Organic Product Purchases')
    fig3.update_traces(
            hovertemplate='<b>Aisle:</b> %{x}<br><b>Orders:</b> %{y:,}<extra></extra>'
         )
            
    fig3.update_layout(
        xaxis_title="Department",
        yaxis_title="Orders",
        xaxis=dict(tickangle=270),
    )
    fig3.update_layout(height=350)
    fig3.update_coloraxes(showscale=False)
    st.plotly_chart(fig3, use_container_width=True)
    
#Graph on Organic Product Aisle
col14, col15 = st.columns([0.1, 0.9])

data = df_organic_orders_product.groupby("aisle")["product_id"].count().sort_values(ascending=False).reset_index().head(30)
data.columns = ['aisle', 'total_purchases']

with col15:
    fig4 = px.bar(data, 
                 x='aisle', 
                 y='total_purchases', 
                 color='total_purchases', 
                 color_continuous_scale='Matter',
                 title='Popular Aisles for Organic Product Purchases (Top30)')
    fig4.update_traces(
            hovertemplate='<b>Aisle:</b> %{x}<br><b>Orders:</b> %{y:,}<extra></extra>'
         )
            
    fig4.update_layout(
        xaxis_title="Aisle",
        yaxis_title="Orders",
        xaxis=dict(tickangle=270),
    )
    fig4.update_layout(height=400)
    fig4.update_coloraxes(showscale=False)
    st.plotly_chart(fig4, use_container_width=True)


#Table on Reorder Products
col16, col17 = st.columns([0.1, 0.9])

df_organic_reorder = df_organic_product.groupby('product_name')['reordered'].agg(['count', 'sum']).reset_index()
df_organic_reorder.columns = ['product_name', 'total_purchase', 'reorders']
df_organic_reorder['% of reorder'] = df_organic_reorder['reorders']/df_organic_reorder['total_purchase'] * 100
df_organic_reorder = df_organic_reorder.sort_values('total_purchase', ascending = False).reset_index(drop = True)

with col17:
    st.markdown(
    """
    <div style="font-size: 16px; font-weight: bold; padding: 10px 0; text-align: left; color: #333;padding-left: 1%;">
        Reorder Analysis of Organic Products (Ranked High to Low)
    </div>
    """,
    unsafe_allow_html=True
    )
    st.dataframe(df_organic_reorder.style.format({"% of reorder": "{:.2f}%"}), height=205, use_container_width=True)















#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import streamlit as st
import plotly.express as px


st.set_page_config(page_title="Sales Dashboard",page_icon=":bar_chart:",layout="wide")

def get_data_from_excel():
    df = pd.read_excel(
        io='supermarkt_sales.xlsx',
        engine="openpyxl",
        sheet_name='Sales',
        skiprows=3,
        usecols='B:R',
        nrows = 1000
    )
    df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df


df = get_data_from_excel()
#st.dataframe(df)

#print(df)

# ---- SIDEBAR ----
st.sidebar.header("Please filter your search here:")
city = st.sidebar.multiselect(
    "Select the City:",
    options=df["City"].unique(),
    default = df["City"].unique()
)


customer_type = st.sidebar.multiselect(
    "Select the Customer:",
    options=df["Customer_type"].unique(),
    default = df["Customer_type"].unique()
)

gender = st.sidebar.multiselect(
    "Select the Gender",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

#see the meaning of these lines
#these lines are used for quering the data and filtering it out
df_selection = df.query(
    "City == @city & Customer_type == @customer_type & Gender == @gender"
)

#st.dataframe(df_selection)

#---- MAINPAGE ----

st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

#TOP KPI'S
total_sales = int(df_selection["Total"].sum())
average_rating = round(df_selection["Rating"].mean(), 1)
star_rating = ":star:" * int(round(average_rating, 0))
average_sale_by_transaction = round(df_selection["Total"].mean(), 2)
total_tax = round(df["Tax 5%"].sum(), 2)
total_income = round(df["gross income"].sum(),2)


left_column,middle_column,right_column = st.columns(3) #read about column method
with left_column:
    st.subheader("Total Sales: ")
    st.subheader(f"US $ {total_sales:,}")
with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("Average Sales Per Transaction:")
    st.header(f"US $ {average_sale_by_transaction}")

left_column,middle_column,right_column = st.columns(3) #read about column method
with left_column:
    st.subheader("Gross Income")
    st.subheader(f"US $ {total_income}")
with middle_column:
    st.subheader("")
    st.subheader(f"")
with right_column:
    st.subheader("")
    st.header("")


st.markdown("---")

#Sales by product line
sales_by_product_line = (
    df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by = "Total")
)
fig_product_sales = px.bar(
    sales_by_product_line,
    x="Total",
    y = sales_by_product_line.index,
    orientation="h",
    title = "<b> SALES BY PRODUCT LNE </b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
    #template = "plotly white",
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)


#Data of sales Quantity
quantity_by_product_line = (
    df_selection.groupby(by=["Product line"]).sum()[["Quantity"]]
)
#st.dataframe(quantity_by_product_line)
fig_quantity_product_sales = px.bar(
    quantity_by_product_line,
    x=quantity_by_product_line.index,
    y = "Quantity",
    title = "<b>QUANTITIES SOLD</b>",
    color_discrete_sequence=["#0083B8"] * len(quantity_by_product_line),
    labels=dict(Quantity = "QUANTITY", Product= "PRODUCT LINE")
    #template = "plotly white",
)
fig_quantity_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
    yaxis=(dict(showgrid=False))
)

# SALES BY HOUR 
sales_by_hour = df_selection.groupby(by=["hour"]).sum()[["Total"]]
fig_hourly_sales = px.line(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
    title="<b>SALES BY HOUR</b>",
    labels=dict(Total = "TOTAL BILL",hour= "HOUR")
    #color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    #template="plotly_white",
)
fig_hourly_sales.update_layout(
    xaxis=dict(showgrid=False),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)
#st.dataframe(sales_by_product_line)

payment_method = (
    df_selection.groupby(by = ["Payment"]).sum()[["Total"]]
)
fig_payment_method = px.pie(
    payment_method,
    values = "Total",
    names = payment_method.index,
    title = "<b> MODE OF PAYMENT </b>",
    color = payment_method.index,
    color_discrete_map={'Cash': 'darkblue','Ewallet': 'royalblue','Cedit Card': 'cyan'},
)

#st.dataframe(payment_method)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_payment_method, use_container_width=True)
right_column.plotly_chart(fig_quantity_product_sales, use_container_width=True)
# st.plotly_chart(fig_product_sales)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            footer:after {
                content: 'MADE WITH ❤️ YASH';
                visibility: visible;
                padding: 5px;
                font-size: 20px;
            }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
import pandas as pd
import numpy as np
import openpyxl
import sqlalchemy
from sqlalchemy import create_engine
import os
import urllib
import pyodbc

df = pd.read_excel("Superstore1.xlsx")

df.drop(["Row ID", "Customer Name"], axis=1, inplace=True)

df["Order ID"] = df["Order ID"].str.replace("-", " ")

df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Order Date"] = df["Order Date"].dt.strftime("%Y/%m/%d")

df["Ship Date"] = pd.to_datetime(df["Ship Date"])
df["Ship Date"] = df["Ship Date"].dt.strftime("%Y/%m/%d")

# calculate different between orderdate date and ship date in new column
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])
df["Days_Delivered"] = df["Ship Date"] - df["Order Date"]

# Separate columns based on data types
 
# String columns

df_str = df.select_dtypes(include=["object", "string"])
 
# Numerical columns (integers and floats)

df_num = df.select_dtypes(include=["number"])
 
# Date and timedelta columns

df_date = df.select_dtypes(include=["datetime", "timedelta"])
 
# Combine all selected columns

combine = pd.concat([df_str, df_num, df_date], axis=1)
 
# Filter orders delivered after 4 days

delayed_orders = df[

    df["Days_Delivered"] > pd.Timedelta(days=4)

]
 

# Created new column for the original product price
df["Original_Price"] = df["Sales"] / (1 - (df["Discount"] / 100))

df["Days_Delivered"] = df["Days_Delivered"].dt.days

canada_states = df[df["Country/Region"]=="Canada"]["State/Province"]
US_states = df[df["Country/Region"] == "United States"]["State/Province"]

df2 = df.groupby(["Segment"]).agg({"Quantity":"sum", "Days_Delivered": "mean"}).round(2)
df3= pd.DataFrame(df2)
# df3.to_csv(r"C:\Users\MohitTarade\Desktop\\Python\df3.csv")

# Send data to SQL for quering
server = "INLT-F194ZC4\PRIMARY1"
database = "New"

params = urllib.parse.quote_plus(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    f"SERVER={server};"
    f"DATABASE={database};"
    "Trusted_Connection=yes;"
)
engine = create_engine(
    f"mssql+pyodbc:///?odbc_connect={params}"
)
dfm = df
dfm.to_sql("Superstore", 
    con=engine,
    if_exists="append",
    index=False)
print("Data sent Successfully")

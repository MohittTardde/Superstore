import pandas as pd
import numpy as np
import openpyxl
import sqlalchemy
from sqlalchemy import create_engine
import os
import urllib

df = pd.read_excel(r"C:\Users\MohitTarade\Desktop\Superstore1.xlsx")

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

df_str = df.select_dtypes("str")
df_int = df.select_dtypes("float64", "int64")
df_date = df.select_dtypes("datetime64", "timedelta64")
combine = pd.concat([df_str, df_int, df_date], axis=1)

delayed_orders = df[df["Days_Delivered"]>pd.Timedelta(days =4)]

# to differenciate data types numerical and string
df_str = df.select_dtypes("str")
df_int = df.select_dtypes("float64", "int64")
df_date = df.select_dtypes("datetime64", "timedelta64")

# Created new column for the original product price
df["Original_Price"] = df["Sales"] / (1 - (df["Discount"] / 100))

df["Days_Delivered"] = df["Days_Delivered"].dt.days

canada_states = df[df["Country/Region"]=="Canada"]["State/Province"]
US_states = df[df["Country/Region"] == "United States"]["State/Province"]

df2 = df.groupby(["Segment"]).agg({"Quantity":"sum", "Days_Delivered": "mean"}).round(2)
df3= pd.DataFrame(df2)
df3.to_csv(r"C:\Users\MohitTarade\Desktop\\Python\df3.csv")

# Send data to SQL for quering
server = "INLT-F194ZC4\PRIMARY1"
database = "New"

params = urllib.parse.quote_plus(
    "DRIVER={ODBC Driver 17 for SQL Server};"
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

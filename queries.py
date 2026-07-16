import sqlite3
import pandas as pd

conn = sqlite3.connect('supply_chain.db')
query = """select `Shipping Mode`, `Order Region`, 
count(*) from orders where `Delivery Status` = 'Late delivery' 
group by `Shipping Mode`, `Order Region`
order by count(*) DESC"""

query = """SELECT `order date (DateOrders)` FROM orders LIMIT 5"""
df = pd.read_sql_query(query, conn)
print(df)

conn.close()
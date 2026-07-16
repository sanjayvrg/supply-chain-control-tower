import sqlite3
import pandas as pd

conn = sqlite3.connect('supply_chain.db')

def late_delivery_overview():
    query =  """select `Delivery Status`, count(*)
    from orders 
    group by `Delivery Status`                    
    order by count(*) desc """

    df = pd.read_sql_query(query, conn)
    print("=== Delivery Status Overview === ")
    print(df)
    print()

def late_by_region():
    query =  """select `Order Region`, count(*)
    from orders 
    where  `Delivery Status` = 'Late delivery'
    group by `Order Region`
    order by count(*) desc """

    df = pd.read_sql_query(query, conn)
    print("=== Late Deliveries by Region === ")
    print(df)
    print()

def late_by_shipping_mode():
    query = """select `Shipping Mode`, count(*)
    from orders 
    where `Delivery Status` = 'Late delivery' 
    group by `Shipping Mode`
    order by count(*) desc"""

    df = pd.read_sql_query(query, conn)
    print("=== Late by Shipping Mode ===")
    print(df)
    print()

def late_rate():
    query = """select `Shipping Mode`, 
    count(*) as total_orders, 
    round(100.0 * sum(case when `Delivery Status` = 'Late delivery' then 1 else 0 end) / count(*), 2) as late_rate
    from orders
    group by `Shipping Mode`
    order by late_rate desc """

    df = pd.read_sql_query(query, conn)
    print("=== Late Rate by Shipping Mode ===")
    print(df)
    print()

def late_rate_first_class():
    query = """select `Order Region`, 
    count(*) as total_orders, 
    round(100.0 * sum(case when `Delivery Status` = 'Late delivery' then 1 else 0 end) / count(*), 2) as late_rate
    from orders
    where `Shipping Mode` = 'First Class'
    group by `Order Region`
    order by late_rate desc"""

    df = pd.read_sql_query(query, conn)
    print("=== Late Rate by First Class ===")
    print(df)
    print()

def late_rate_second_class():
    query = """select `Order Region`, 
    count(*) as total_orders, 
    round(100.0 * sum(case when `Delivery Status` = 'Late delivery' then 1 else 0 end) / count(*), 2) as late_rate
    from orders
    where `Shipping Mode` = 'Second Class'
    group by `Order Region`
    order by late_rate desc"""

    df = pd.read_sql_query(query, conn)
    print("=== Late Rate by Second Class ===")
    print(df)
    print()

def sales():
    query = """ select `Delivery Status`, round(sum(sales), 2) as total_revenue, count(*) as total_orders
    from orders
    group by `Delivery Status`
    order by total_revenue desc"""

    df = pd.read_sql_query(query, conn)
    print("=== Sales ==== ")
    print(df) 
    print()

def profit():
    query = """ select `Delivery Status`, round(sum(`Order Profit Per Order`), 2) as total_profit, count(*) as total_orders
    from orders
    group by `Delivery Status`
    order by total_profit desc"""

    df = pd.read_sql_query(query, conn)
    print("=== Profit ==== ")
    print(df) 
    print()

def trend_over_time(): 
    query = """select `order date (DateOrders)`, `Delivery Status`
    from orders"""

    df = pd.read_sql_query(query, conn)
    df['year'] = pd.to_datetime(df['order date (DateOrders)']).dt.year
    result = df.groupby('year')['Delivery Status'].apply(lambda x: round(100.0 * (x == 'Late delivery').sum() / len(x), 2)).reset_index()
    result.columns = ['year', 'late_rate']
    print("=== Trend Over Time ===")
    print(result)
    print()

# export late by region
df_region = pd.read_sql_query("""
    select `Order Region`, count(*) as late_orders
    from orders
    where `Delivery Status` = 'Late delivery'
    group by `Order Region`
    order by late_orders DESC
""", conn)
df_region.to_csv('late_by_region.csv', index=False)

# export late by shipping mode
df_ship = pd.read_sql_query("""
    select `Shipping Mode`, COUNT(*) as late_orders
    from orders
    where `Delivery Status` = 'Late delivery'
    group by `Shipping Mode`
    order by late_orders DESC
""", conn)

df_ship.to_csv('late_by_shipping.csv', index=False)

# export delivery status overview
df_status = pd.read_sql_query("""
    select `Delivery Status`, count(*) as total
    from orders
    group by `Delivery Status`
    order by total DESC
""", conn)
df_status.to_csv('delivery_status.csv', index=False)


#print("CSVs exported.")

# #late_delivery_overview()
# #late_by_region()
# late_by_shipping_mode()
# late_rate()
# late_rate_first_class()
# late_rate_second_class()
# sales()
# profit()
trend_over_time()

conn.close()
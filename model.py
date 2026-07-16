import pandas as pd
import sqlite3

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

conn = sqlite3.connect('supply_chain.db')

X = None
model = None

def model():
    global X, model
    query =  """select `Shipping Mode`, `Order Region`, `Days for shipment (scheduled)`, `Order Item Quantity`, `Late_delivery_risk` from orders """

    df = pd.read_sql_query(query, conn)
    df = pd.get_dummies(df, columns=['Shipping Mode', 'Order Region'])
    X = df.drop(columns=['Late_delivery_risk'])
    y = df['Late_delivery_risk']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print("==== Model ====")
    print("Accuracy:", accuracy_score(y_test, y_pred))
    importances = pd.Series(model.feature_importances_, index=X.columns)
    print(importances.sort_values(ascending=False).head(10))

def flag_order(shipping_mode, order_region, days_scheduled, quantity):
    input_data = pd.DataFrame(columns=X.columns)
    input_data.loc[0] = 0
    
    if f'Shipping Mode_{shipping_mode}' in input_data.columns:
        input_data[f'Shipping Mode_{shipping_mode}'] = 1
    if f'Order Region_{order_region}' in input_data.columns:
        input_data[f'Order Region_{order_region}'] = 1
    
    input_data['Days for shipment (scheduled)'] = days_scheduled
    input_data['Order Item Quantity'] = quantity
    
    prediction = model.predict(input_data)[0]
    risk = "HIGH RISK" if prediction == 1 else "LOW RISK"
    print(f"Order: {shipping_mode} | {order_region} | {days_scheduled} days | qty {quantity} → {risk}")

shipping_mode = input("Enter shipping mode: ")
order_region = input("Enter order region: ")
days_scheduled = int(input("Enter days scheduled: "))
quantity = int(input("Enter quantity: "))

model()
flag_order(shipping_mode, order_region, days_scheduled, quantity)
conn.close()
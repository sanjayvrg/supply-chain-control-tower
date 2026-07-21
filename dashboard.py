import streamlit as st
import pandas as pd
import sqlite3
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

st.title("Supply Chain Control Tower")
tab1, tab2, tab3 = st.tabs(["Overview", "Explore", "Risk Predictor"])

conn = sqlite3.connect("supply_chain.db")

@st.cache_data
def load_data():
    query = """
            select `Shipping Mode`, `Order Region`, `Days for shipment (scheduled)`, `Order Item Quantity`, `Late_delivery_risk`, `Sales`, `Order Profit Per Order`
            from orders
            """
    return pd.read_sql_query(query, conn)

df = load_data()

@st.cache_resource
def train_model(data):
    model_df = pd.get_dummies(data, columns=["Shipping Mode", "Order Region"])
    X = model_df.drop(columns=["Late_delivery_risk", "Sales", "Order Profit Per Order"])
    y = model_df["Late_delivery_risk"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model, X.columns

model, model_columns = train_model(df)

with tab1:
    late_rate = df["Late_delivery_risk"].mean()
    revenue_at_risk = df[df["Late_delivery_risk"] == 1]["Sales"].sum()
    profit_at_risk = df[df["Late_delivery_risk"] == 1]["Order Profit Per Order"].sum()
    total_orders = len(df)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Late Delivery Rate", f"{late_rate:.0%}")
    col2.metric("Revenue at Risk", f"${revenue_at_risk/1_000_000:.1f}M")
    col3.metric("Profit at Risk", f"${profit_at_risk:,.0f}")
    col4.metric("Total Orders", f"{total_orders:,}")

    st.subheader("Late Rate by Shipping Mode")
    shipping_late = df.groupby("Shipping Mode")["Late_delivery_risk"].mean()
    st.bar_chart(shipping_late)

    st.subheader("Late Rate by Region")
    region_late = df.groupby("Order Region")["Late_delivery_risk"].mean()
    st.bar_chart(region_late)

with tab2:
    st.subheader("Filter the Data")

    regions = st.multiselect("Order Region", options=sorted(df["Order Region"].unique()))
    shipping_modes = st.multiselect("Shipping Mode", options=sorted(df["Shipping Mode"].unique()))

    filtered = df.copy()
    if regions:
        filtered = filtered[filtered["Order Region"].isin(regions)]
    if shipping_modes:
        filtered = filtered[filtered["Shipping Mode"].isin(shipping_modes)]

    st.write(f"{len(filtered):,} orders match this filter")

    if len(filtered) > 0:
        c1, c2 = st.columns(2)
        c1.metric("Late Rate (filtered)", f"{filtered['Late_delivery_risk'].mean():.0%}")
        c2.metric("Revenue at Risk (filtered)", f"${filtered.loc[filtered['Late_delivery_risk'] == 1, 'Sales'].sum():,.0f}")

    st.dataframe(filtered.head(200))

    csv_data = filtered.to_csv(index=False)
    st.download_button("Download filtered data as CSV", data=csv_data, file_name="filtered_orders.csv", mime="text/csv")

with tab3:
    st.subheader("Predict Late-Delivery Risk for a New Order")

    importances = pd.Series(model.feature_importances_, index=model_columns)
    top_features = importances.sort_values(ascending=False).head(5)

    with st.expander("What drives this model's predictions?"):
        st.bar_chart(top_features)

    c1, c2 = st.columns(2)
    with c1:
        shipping_mode = st.selectbox("Shipping Mode", sorted(df["Shipping Mode"].unique()))
        order_region = st.selectbox("Order Region", sorted(df["Order Region"].unique()))
    with c2:
        days_scheduled = st.number_input("Days for Shipment (Scheduled)", min_value=0, value=4)
        quantity = st.number_input("Order Item Quantity", min_value=1, value=1)

    if st.button("Predict Risk"):
        input_data = pd.DataFrame(columns=model_columns)
        input_data.loc[0] = 0

        shipping_col = f"Shipping Mode_{shipping_mode}"
        region_col = f"Order Region_{order_region}"
        if shipping_col in input_data.columns:
            input_data[shipping_col] = 1
        if region_col in input_data.columns:
            input_data[region_col] = 1

        input_data["Days for shipment (scheduled)"] = days_scheduled
        input_data["Order Item Quantity"] = quantity

        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0][1]

        if prediction == 1:
            st.error(f"**HIGH RISK** — predicted late, with {probability:.0%} confidence.")
        else:
            st.success(f"**LOW RISK** — predicted on-time, with {1 - probability:.0%} confidence.")
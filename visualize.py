import pandas as pd
import matplotlib.pyplot as plt

# Load the CSVs
df_status = pd.read_csv('delivery_status.csv')
df_region = pd.read_csv('late_by_region.csv')
df_ship = pd.read_csv('late_by_shipping.csv')

# Chart 1 - Delivery Status Overview
plt.figure(figsize=(10, 5))
plt.barh(df_status['Delivery Status'], df_status['total'])
plt.title('Delivery Status Overview')
plt.xlabel('Total Orders')
plt.tight_layout()
plt.savefig('chart_delivery_status.png')
plt.close()

# Chart 2 - Late by Region
plt.figure(figsize=(10, 7))
plt.barh(df_region['Order Region'], df_region['late_orders'])
plt.title('Late Deliveries by Region')
plt.xlabel('Late Orders')
plt.tight_layout()
plt.savefig('chart_late_by_region.png')
plt.close()

# Chart 3 - Late by Shipping Mode
plt.figure(figsize=(10, 5))
plt.barh(df_ship['Shipping Mode'], df_ship['late_orders'])
plt.title('Late Deliveries by Shipping Mode')
plt.xlabel('Late Orders')
plt.tight_layout()
plt.savefig('chart_late_by_shipping.png')
plt.close()

print("Charts saved.")
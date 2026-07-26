# Supply Chain Control Tower

A supply chain analytics project built on the [DataCo Supply Chain dataset](https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis) (~180K order records), combining SQL analysis, a machine learning model, and an interactive Streamlit dashboard to flag late-delivery risk before it happens.

## Key Findings

- **54% of all orders arrived late** — more than half of shipments missed their scheduled delivery window.
- **First Class shipping fails 95%+ of the time**, consistently, across every region in the dataset — the fastest promised shipping option is also the least reliable.
- **~$20M in revenue and ~$2M in profit** are tied to orders that shipped late, quantifying the real business cost of the delivery problem.
- A **Random Forest classifier reaches 69% accuracy** predicting whether an order will be delivered late, using shipping mode, region, scheduled shipment days, and order quantity as features.

## Dashboard

An interactive Streamlit dashboard (`dashboard.py`) sits on top of the analysis, with three views:

- **Overview** — headline KPIs (late delivery rate, revenue at risk, profit at risk, total orders) plus late-rate breakdowns by shipping mode and region
- **Explore** — filter orders by region and shipping mode, with metrics that update live, a data table, and a CSV export of the filtered results
- **Risk Predictor** — enter a shipping mode, region, scheduled days, and quantity to get a live HIGH RISK / LOW RISK prediction with a confidence score, plus a breakdown of which features drive the model's predictions

## Tech Stack

- **SQLite** — relational database for the raw order data
- **Python / pandas** — data wrangling and SQL query execution
- **scikit-learn** — Random Forest classifier for late-delivery prediction
- **Streamlit** — interactive dashboard
- **matplotlib** — static visualizations of delivery status, late rate by region, and late rate by shipping mode

## Project Structure

```
├── setup.py          # loads scd.csv into a SQLite database (supply_chain.db)
├── queries.py        # SQL queries used for exploratory analysis
├── analysis.py       # runs the queries, computes late-delivery stats
├── visualize.py      # generates matplotlib charts
├── model.py          # trains and evaluates the Random Forest classifier
├── dashboard.py       # interactive Streamlit dashboard
├── chart_delivery_status.png
├── chart_late_by_region.png
└── chart_late_by_shipping.png
```

## How to Run

1. Download the [DataCo Supply Chain dataset](https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis) from Kaggle and save it as `scd.csv` in the project root.
2. Install dependencies:
   ```bash
   pip install pandas scikit-learn matplotlib streamlit
   ```
3. Build the database:
   ```bash
   python setup.py
   ```
4. Run the analysis:
   ```bash
   python analysis.py
   ```
5. Generate the charts:
   ```bash
   python visualize.py
   ```
6. Train and evaluate the model:
   ```bash
   python model.py
   ```
7. Launch the interactive dashboard:
   ```bash
   streamlit run dashboard.py
   ```

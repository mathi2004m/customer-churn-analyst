# Customer Churn Intelligence Dashboard 📊

An interactive data analytics project that explores customer churn patterns, visualizes key findings, and suggests business actions to help improve customer retention.

## 🔗 Live Dashboard

**[View Customer Churn Intelligence Dashboard](https://mathi2004m.github.io/customer-churn-analyst/)**

## 🎯 Project Objective

Customer churn occurs when customers stop using a company's services. High churn can affect revenue, customer relationships, and business growth.

The objective of this project is to analyse customer data, identify groups with higher churn rates, and translate the findings into practical business recommendations.

## 📊 About the Dataset

This project uses the IBM Telco Customer Churn dataset.

| Dataset Detail | Description |
|---|---|
| Total customer records | 7,043 |
| Original columns | 21 |
| Target variable | `Churn` |
| Analysis focus | Contract type, customer tenure, monthly charges |

The `Churn` column indicates whether a customer left the service (`Yes`) or stayed (`No`).

## ✨ Project Features

- **Interactive Visual Dashboard:** Explore customer churn patterns through charts.
- **Customer Insights:** Compare churn rates across contract types, customer tenure groups, and monthly bill ranges.
- **Monthly Charges Distribution:** Compare the distribution of monthly charges for retained and churned customers.
- **Suggested Business Actions:** View practical retention recommendations based on the selected customer-group attributes.
- **About the Data:** Understand the dataset, analysis approach, and project limitations.

## 🔍 Key Findings

- Overall customer churn rate: **26.54%**
- Month-to-month contracts: **42.71% churn rate**
- One-year contracts: **11.27% churn rate**
- Two-year contracts: **2.83% churn rate**

These findings show that month-to-month customers had a substantially higher churn rate than customers with longer-term contracts in this dataset.

**Business implication:** Businesses could investigate whether clearer plan comparisons, proactive customer support, and suitable loyalty offers improve retention. The effectiveness of these actions should be tested using actual business outcomes.

## 🛠️ Tools and Technologies

- **Python** — Data processing and analysis
- **Pandas** — Data cleaning and manipulation
- **Plotly** — Interactive data visualizations
- **HTML, CSS and JavaScript** — Dashboard interface and interactions
- **Git and GitHub** — Version control and project hosting
- **GitHub Pages** — Dashboard deployment

## 🔄 Project Workflow

1. **Data Collection:** Load the customer churn dataset.
2. **Data Cleaning:** Remove duplicate customer IDs, convert numeric fields, and prepare the required columns.
3. **Exploratory Data Analysis:** Examine customer groups and churn rates.
4. **Data Visualization:** Create interactive charts to communicate the findings.
5. **Business Interpretation:** Identify customer groups with higher observed churn.
6. **Recommendations:** Suggest retention actions that businesses can evaluate.
7. **Deployment:** Publish the dashboard using GitHub Pages.

## 📁 Project Structure

```text
customer-churn-analyst/
│
├── index.html
├── generate_chart_data.py
├── chart_data.json
├── 01_data_cleaning.ipynb
├── churn_analysis.py
├── metrics.json
├── model.json
└── README.md
```

The files shown above represent the intended project structure. Include only files that are present in your repository.

## ▶️ How to Run the Project Locally

### Prerequisites

- Python installed
- Pandas installed
- The dataset file `Telco-Customer-Churn.csv`
- Visual Studio Code with the Live Server extension

### Step 1: Install the dependency

```bash
python -m pip install pandas
```

### Step 2: Generate the chart data

Keep `generate_chart_data.py` and `Telco-Customer-Churn.csv` in the same folder, then run:

```bash
python generate_chart_data.py
```

This generates `chart_data.json` for the dashboard.

### Step 3: Open the dashboard

Open `index.html` using the VS Code Live Server extension. The HTML page loads `chart_data.json` and uses Plotly.js for the interactive charts.

An internet connection is required for the Plotly library loaded through its CDN.

## 💼 Business Value

This project demonstrates how data analytics can support business decision-making by:

- Identifying customer groups with higher observed churn.
- Presenting business metrics through interactive visualizations.
- Communicating findings in an understandable format.
- Translating analytical findings into retention strategies to test.

## 📚 What I Learned

Through this project, I strengthened my understanding of:

- Data cleaning and preprocessing with Python and Pandas.
- Exploratory Data Analysis (EDA).
- Comparing business metrics across customer groups.
- Creating interactive visualizations.
- Communicating analytical findings to non-technical audiences.
- Turning data insights into practical business recommendations.
- Deploying a web-based analytics dashboard.

## ⚠️ Limitations

- The dashboard presents descriptive analysis and historical group-level churn rates.
- Group-level statistics are not individual customer churn predictions.
- The recommendations are rule-based suggestions, not outputs from a live AI system.
- The analysis identifies associations, not proof of causation.
- The business recommendations require further testing to measure their impact on retention.

## 👩‍💻 Author

**Valarmathi**

Interested in Data Analytics, Business Intelligence, and using data to solve business problems.

**Feedback and suggestions are welcome!**

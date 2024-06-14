# %%
import time  # to simulate a real time data, time loop

import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import streamlit as st  # 🎈 data web app development
import matplotlib.pyplot as plt
import requests
from io import StringIO


# %%

def df_from_url(url):
    # URL of the CSV file

    # Fetch the CSV data, disabling SSL verification
    response = requests.get(url, verify=False)
    response.raise_for_status()  # Raise an error for bad status codes

    # Convert the CSV data to a pandas DataFrame
    csv_data = StringIO(response.text)
    df = pd.read_csv(csv_data)
    return df

def get_data():
    try:
        df_claim = df_from_url("https://raw.githubusercontent.com/ellahyc/bowtieinternasmpublic/main/claim.csv")
        df_policy = df_from_url("https://raw.githubusercontent.com/ellahyc/bowtieinternasmpublic/main/policy.csv")
        df_invoice = df_from_url("https://raw.githubusercontent.com/ellahyc/bowtieinternasmpublic/main/invoice.csv")

        return df_claim, df_policy, df_invoice
    except Exception as e:
        # print(e)
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# %%
def get_fig_premium(df_invoice):

    #question 3i total amount of invoice

    df_invoice['charge_date'] = pd.to_datetime(df_invoice['charge_date'], format='ISO8601')
    df_invoice['year_month'] = df_invoice['charge_date'].dt.to_period('M')
    total_premium = df_invoice.groupby(df_invoice['year_month'])['total_amount'].sum()
    total_premium.index = total_premium.index.astype(str)

    indices = np.arange(len(total_premium)) * (1 + 0.6)

    fig_premium, ax = plt.subplots(figsize=(20, 6))
    plt.tight_layout()
    plt.bar(total_premium.index, total_premium, width=0.5)

    plt.xlabel('month')
    plt.ylabel('total amount of premium received')
    plt.title('amount of premium received per month')

    plt.xticks(rotation=45, ha='right') 
    plt.gca().tick_params(axis='x', which='major', pad=10) 

    return fig_premium, total_premium

# %%
def get_fig_policy_count(df_policy):
    #question 3ii total policy issued 

    df_policy['issue_date'] = pd.to_datetime(df_policy['issue_date'], format='ISO8601')
    df_policy['year_month'] = df_policy['issue_date'].dt.to_period('M')
    policy_count_per_month = df_policy.groupby('year_month')['policy_number'].count()
    policy_count_per_month.index = policy_count_per_month.index.astype(str)

    fig_policy, ax = plt.subplots(figsize=(20, 6))
    plt.bar(policy_count_per_month.index, policy_count_per_month, width=0.5)
    plt.xlabel('issue date')
    plt.ylabel('total policy issued')
    plt.title('total policy issued per month')

    # Rotate x-axis labels for better readability and adjust alignment
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels by 45 degrees and align them to the right

    return fig_policy

# %%
def get_fig_loss_ratio(df_claim, total_premium):
    #question 3iii loss ratio 
    # Ensure payment_date is a datetime object
    
    df_claim['payment_date'] = pd.to_datetime(df_claim['payment_date'],format='ISO8601')
    df_claim['submit_date'] = pd.to_datetime(df_claim['submit_date'],format='ISO8601')

    df_claim['year_month'] = df_claim['payment_date'].dt.to_period('M')

    claims_sum_per_month = df_claim.groupby('year_month')['total_base_payable_amount'].sum()
    claims_sum_per_month.index = claims_sum_per_month.index.astype(str)

    loss_ratio_per_month = claims_sum_per_month / total_premium
    loss_ratio_per_month = loss_ratio_per_month.fillna(0)
    loss_ratio_per_month.index = loss_ratio_per_month.index.astype(str)

    fig_loss_ratio, ax = plt.subplots(figsize=(20, 6))
    plt.bar(loss_ratio_per_month.index, loss_ratio_per_month, width=0.5)
    plt.xlabel('Month')
    plt.ylabel('Loss Ratio')
    plt.title('Loss Ratio Per Month')

    # Rotate x-axis labels for better readability and adjust alignment
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels by 45 degrees and align them to the right

    return fig_loss_ratio


# streamlit display
st.set_page_config(layout="wide")

# Get the data
df_claim, df_policy, df_invoice = get_data()

fig_premium, total_premium = get_fig_premium(df_invoice)
fig_policy = get_fig_policy_count(df_policy)
fig_loss_ratio = get_fig_loss_ratio(df_claim, total_premium)

st.title("Bowtie Business Performance Dashboard")
col_premium, col_policy_issued, col_loss_ratio = st.columns(3)

with st.container():
    st.header("Premium Received By Month")
    st.pyplot(fig_premium)

with st.container():
    st.header("Total Policy Issued By Month")
    st.pyplot(fig_policy)

with st.container():
    st.header("Loss Ratio By Month")
    st.pyplot(fig_loss_ratio)



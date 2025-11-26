import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from groq import Groq

# --------------------------
# Set your Groq API key manually (for Colab)
# --------------------------
# You can either:
# 1️⃣ Use environment variable:




GROQAPIKEY222 = os.getenv("GROQAPIKEY222")

# --------------------------
# Initialize Groq client
# --------------------------
if not GROQAPIKEY222:
    st.warning("⚠️ Please set your GROQ_API_KEY in Colab before running.")
client = Groq(api_key=GROQAPIKEY222)

# --------------------------
# Streamlit App Config
# --------------------------
st.set_page_config(page_title="AI Expense Analyzer", page_icon="💰", layout="wide")
st.title("💰 AI Expense Analyzer")
st.markdown("Track your expenses, visualize spending patterns, and get smart AI suggestions!")

# --------------------------
# Initialize Session State
# --------------------------
if "expenses" not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])

# --------------------------
# Expense Input Form
# --------------------------
with st.expander("➕ Add New Expense", expanded=True):
    with st.form("expense_form"):
        date = st.date_input("Date")
        category = st.selectbox("Category", ["Food", "Transport", "Shopping", "Entertainment", "Bills", "Other"])
        amount = st.number_input("Amount (in PKR)", min_value=0.0, step=100.0)
        description = st.text_area("Description (optional)")
        submitted = st.form_submit_button("Add Expense")

        if submitted:
            new_data = pd.DataFrame([[date, category, amount, description]],
                                    columns=["Date", "Category", "Amount", "Description"])
            st.session_state.expenses = pd.concat([st.session_state.expenses, new_data], ignore_index=True)
            st.success("✅ Expense added successfully!")

# --------------------------
# Display Expenses
# --------------------------
if not st.session_state.expenses.empty:
    st.subheader("📊 Expense Records")
    st.dataframe(st.session_state.expenses, use_container_width=True)

    # Pie Chart
    st.subheader("🧩 Expense Distribution by Category")
    category_data = st.session_state.expenses.groupby("Category")["Amount"].sum()
    fig1, ax1 = plt.subplots()
    ax1.pie(category_data, labels=category_data.index, autopct="%1.1f%%", startangle=90)
    ax1.axis("equal")
    st.pyplot(fig1)

    # Trend Chart
    st.subheader("📈 Spending Trend Over Time")
    trend_data = st.session_state.expenses.groupby("Date")["Amount"].sum().reset_index()
    fig2, ax2 = plt.subplots()
    ax2.plot(trend_data["Date"], trend_data["Amount"], marker="o")
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Total Spending (PKR)")
    ax2.set_title("Spending Trend")
    st.pyplot(fig2)

    # AI Analysis
    st.subheader("🤖 AI Expense Insights")

    user_expense_summary = st.session_state.expenses.to_string(index=False)

    if st.button("Analyze My Expenses 💬"):
        with st.spinner("Analyzing your expense patterns with Groq Llama 3.3..."):
            try:
                prompt = f"""
                You are a financial advisor. Analyze the following expense data and identify:
                1. Spending patterns
                2. Categories with overspending
                3. Suggested saving strategies
                4. A short summary of financial health.

                Expense Data:
                {user_expense_summary}
                """

                chat_completion = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.3-70b-versatile",
                )

                ai_analysis = chat_completion.choices[0].message.content
                st.success("✅ Analysis Complete!")
                st.markdown(ai_analysis)

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
else:
    st.info("💡 Add some expenses above to get started!")

import pandas as pd
import plotly.express as px
import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Stock Explorer", layout="wide")
st.title("📈 Stock Price Explorer")
st.caption(
    "Prices are indexed to 1.00 at the start, so each line shows growth since Jan 2018."
)

st.info(
    "Did you know? Microsoft was founded in 1975 by Bill Gates and Paul Allen."
)

@st.cache_data
def load_data():

    tickers = [
        "AAPL",
        "MSFT",
        "GOOG",
        "AMZN",
        "NVDA",
        "TSLA",
        "ABBN.SW",
        "AMD"
    ]

    data = yf.download(
        tickers,
        start="2018-01-01",
        auto_adjust=True
    )["Close"]

    data = data / data.iloc[0]
    data.reset_index(inplace=True)
    data.rename(columns={"Date": "date"}, inplace=True)

    return data

df = load_data()
display_names = {
    "AAPL": "Apple",
    "MSFT": "Microsoft",
    "GOOG": "Google",
    "AMZN": "Amazon",
    "NVDA": "NVIDIA",
    "TSLA": "Tesla",
    "ABBN.SW": "ABB",
    "AMD": "AMD"
}
tickers = [c for c in df.columns if c != "date"]

chosen = st.sidebar.multiselect(
    "Choose stocks",
    tickers,
    default=["AAPL", "MSFT", "GOOG"],
    format_func=lambda x: display_names.get(x, x)
)

st.sidebar.header("Stock Selection")

investment = st.sidebar.number_input(
    "Initial investment (€)",
    min_value=100,
    value=1000,
    step=100
)

if not chosen:
    st.warning("Pick at least one stock from the sidebar.")
    st.stop()

growths = {t: (df[t].iloc[-1] - 1) * 100 for t in chosen}
best_stock = max(growths, key=growths.get)

st.success(
    f"🏆 Best Performer: {display_names.get(best_stock, best_stock)} ({growths[best_stock]:.1f}% growth)"
)

st.subheader("💰 Investment Outcome")

investment_cols = st.columns(len(chosen))

for col, t in zip(investment_cols, chosen):
    final_value = investment * df[t].iloc[-1]

    col.metric(
        display_names.get(t, t),
        f"€{final_value:,.0f}"
    )

cols = st.columns(len(chosen))
for col, t in zip(cols, chosen):
    growth = (df[t].iloc[-1] - 1) * 100

    col.metric(
        display_names.get(t, t),
        f"{df[t].iloc[-1]:.2f}x",
        f"{growth:+.1f}%"
    )

fig = px.line(
    df,
    x="date",
    y=chosen,
    title="Normalized price over time"
)

st.plotly_chart(fig, width="stretch")

growth_df = pd.DataFrame(
    {
        "Stock": chosen,
        "Growth (%)": [growths[t] for t in chosen]
    }
)

bar_fig = px.bar(
    growth_df,
    x="Stock",
    y="Growth (%)",
    title="Total Growth Comparison"
)

st.plotly_chart(bar_fig, width="stretch")
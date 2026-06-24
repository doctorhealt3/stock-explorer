import pandas as pd
import plotly.express as px
import streamlit as st

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
    df = px.data.stocks()
    df["date"] = pd.to_datetime(df["date"])
    return df


df = load_data()

display_names = {
    "AAPL": "Apple",
    "MSFT": "Microsoft",
    "GOOG": "Google",
    "AMZN": "Amazon",
    "FB": "Meta",
    "NFLX": "Netflix"
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

growths = {
    t: (df[t].iloc[-1] - 1) * 100
    for t in chosen
}

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
    title="Normalized Price Over Time"
)

st.plotly_chart(fig, width="stretch")

growth_df = pd.DataFrame(
    {
        "Stock": [display_names.get(t, t) for t in chosen],
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
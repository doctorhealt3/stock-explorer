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
tickers = [c for c in df.columns if c != "date"]

chosen = st.sidebar.multiselect(
    "Choose stocks",
    tickers,
    default=["AAPL", "MSFT", "GOOG"]
)

if not chosen:
    st.warning("Pick at least one stock from the sidebar.")
    st.stop()

growths = {t: (df[t].iloc[-1] - 1) * 100 for t in chosen}
best_stock = max(growths, key=growths.get)

st.success(
    f"🏆 Best Performer: {best_stock} ({growths[best_stock]:.1f}% growth)"
)

cols = st.columns(len(chosen))
for col, t in zip(cols, chosen):
    growth = (df[t].iloc[-1] - 1) * 100
    col.metric(t, f"{df[t].iloc[-1]:.2f}x", f"{growth:+.1f}%")

fig = px.line(
    df,
    x="date",
    y=chosen,
    title="Normalized price over time"
)

st.plotly_chart(fig, width="stretch")
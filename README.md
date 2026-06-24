# Stock Explorer

Stock Explorer is a Streamlit web application for comparing major technology stocks with interactive Plotly charts, growth metrics, and investment outcome estimates.

## Deployment Link

Live app: https://stock-explorer-6m66ju7qrohm46bgptc8be.streamlit.app/

## Features

* Compare multiple technology stocks
* Interactive stock selection
* Growth metrics for each stock
* Best performer indicator
* Interactive Plotly chart
* Public deployment using Streamlit Cloud

## Architecture

```mermaid
flowchart LR
    A[Plotly/YFinance Stock Data]
    B[Streamlit App]
    C[GitHub Repository]
    D[Streamlit Cloud]
    E[End User]

    A --> B
    B --> C
    C --> D
    D --> E
```

## Technologies Used

* Python
* Streamlit
* Plotly
* Pandas
* GitHub
* Streamlit Cloud

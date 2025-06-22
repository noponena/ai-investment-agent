# AI Investment Agent

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-WIP-yellow.svg)

A modular, extensible AI-powered investment assistant that fetches, summarizes, and analyzes the latest market trends and news, then recommends investments according to your customizable strategy.  
Integrates with APIs like Alpha Vantage, NewsAPI, and yfinance.  
**Built for automation and transparency.**

---

## 🚀 Features

- **Automatic fetching of market news and price data**
- **Modular data sources:** Easily extend with new APIs
- **AI-powered summarization and portfolio suggestions**
- **Configurable investment buckets and strategy**
- **Secure handling of API keys and settings**
- **Seamless integration with Interactive Brokers (IBKR) planned**

## Installation

This project requires **Python 3.12** or later.
Clone the repository and install dependencies using [requirements.txt](requirements.txt):

```bash
pip install -r requirements.txt
```

## Configuration

Create a `config/.env` file containing your API keys:

```bash
OPENAI_API_KEY=your-openai-key
ALPHA_VANTAGE_API_KEY=your-alpha-vantage-key
NEWS_API_KEY=your-newsapi-key
```

## Running the demo

Run the demo script to fetch data and print recommendations:

```bash
python main.py
```



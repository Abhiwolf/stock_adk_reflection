# Stock ADK Reflection

A sophisticated stock analysis application that leverages LangChain, LangGraph, and OpenAI to provide intelligent portfolio recommendations using an agent-based architecture.

## Overview

This application analyzes stock market data and generates comprehensive portfolio decisions with detailed reasoning, technical analysis, and risk assessments. The system uses a multi-agent architecture to process market data, perform technical analysis, and generate actionable investment recommendations.

## Features

- **Real-time Market Data**: Fetches current stock data using Yahoo Finance API
- **Technical Analysis**: Analyzes RSI, MACD, moving averages, and other technical indicators
- **Risk Assessment**: Calculates volatility, Sharpe ratio, and other risk metrics
- **AI-Powered Decisions**: Uses OpenAI models through LangChain for intelligent analysis
- **Agent-Based Architecture**: Implements LangGraph for coordinated multi-agent processing
- **Comprehensive Reporting**: Generates detailed investment recommendations with confidence scores

## Prerequisites

- Python 3.9 or higher
- OpenAI API key (configured through internal authentication system)
- Internet connection for market data access

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd stock_adk_reflection
   ```

2. **Create and activate virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

1. **Activate the virtual environment** (if not already active):
   ```bash
   source venv/bin/activate
   ```

2. **Run the main application**:
   ```bash
   python main.py
   ```

3. **Enter stock ticker** when prompted:
   ```
   Enter stock ticker: TCS
   ```

### Example Output

The application will provide a comprehensive analysis including:
- **Action Recommendation**: BUY/SELL/HOLD with allocation percentage
- **Confidence Score**: Risk assessment confidence level
- **Technical Analysis**: RSI, MACD, moving averages analysis
- **Risk Metrics**: Volatility, Sharpe ratio, and other risk indicators
- **Market Context**: Economic indicators and market sentiment
- **Action Plan**: Specific steps for monitoring and decision-making

## Project Structure

```
stock_adk_reflection/
├── main.py                 # Main application entry point
├── graph.py               # LangGraph agent workflow definition
├── agents/                # Agent implementations
├── config/                # Configuration files
│   └── hawkeye.py        # OpenAI authentication setup
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
├── .vscode/              # VS Code configuration
└── README.md             # This file
```

## Dependencies

Key packages include:
- `langgraph`: Agent workflow orchestration
- `langchain`: LLM framework and chains
- `langchain-openai`: OpenAI integration
- `yfinance`: Yahoo Finance API for market data
- `pandas`: Data manipulation and analysis
- `numpy`: Numerical computations
- `ta`: Technical analysis library
- `loguru`: Logging framework

## Configuration

The application uses an internal authentication system for OpenAI API access. The configuration is handled automatically through the `config/hawkeye.py` module.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[Add your license information here]

## Support

For issues or questions, please create an issue in the repository or contact the development team.

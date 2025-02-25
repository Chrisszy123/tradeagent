from trading_agent import TradeAgent, MarketData
from datetime import datetime

def main():
    # Configuration
    email_config = {
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 465,
        'username': 'your_email@gmail.com',
        'password': 'your_app_password',
        'from_email': 'your_email@gmail.com',
        'to_email': 'recipient@email.com'
    }
    
    telegram_config = {
        'token': 'your_telegram_bot_token',
        'chat_id': 'your_chat_id'
    }
    
    # Initialize trading agent
    agent = TradeAgent(
        api_key='your_openai_api_key'
    )
    
    # Example market data
    market_data = [
        MarketData(100.0, 102.0, 99.0, 101.0, datetime.now()),
        MarketData(101.0, 103.0, 100.5, 102.5, datetime.now()),
        MarketData(102.5, 104.0, 102.0, 103.5, datetime.now()),
    ]
    
    # Get prediction
    prediction = agent.analyze_market_data(market_data)
    
    # Execute trade based on prediction
    current_price = market_data[-1].close
    agent.execute_trade(prediction, current_price)

if __name__ == "__main__":
    main() 
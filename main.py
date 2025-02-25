from trading_agent import TradeAgent, MarketData
from datetime import datetime
from data_source import get_market_data
import time

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
    
    while True:
        try:
            # Get market data from Binary.com
            market_data = get_market_data()
            
            # Get prediction
            prediction = agent.analyze_market_data(market_data)
            
            # Execute trade based on prediction
            current_price = market_data[-1].close
            agent.execute_trade(prediction, current_price)
            
            # Wait for 15 minutes before next analysis
            time.sleep(900)  # 900 seconds = 15 minutes
            
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            time.sleep(60)  # Wait a minute before retrying if there's an error

if __name__ == "__main__":
    main() 
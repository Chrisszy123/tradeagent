from typing import List, Dict
import numpy as np
from datetime import datetime
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from notification_service import NotificationService

class MarketData:
    def __init__(self, open: float, high: float, low: float, close: float, time: datetime):
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.time = time

class TradeAgent:
    def __init__(self, api_key: str):
        self.llm = ChatOpenAI(api_key=api_key)
        self.notification_service = NotificationService()
        self.current_position = None
        
    def analyze_market_data(self, market_data: List[MarketData]) -> str:
        # Prepare market data for LLM analysis
        data_description = self._prepare_market_description(market_data)
        
        # Create prompt for the LLM
        prompt = f"""
        Based on the following market data, analyze the probable market direction (UP/DOWN):
        
        {data_description}
        
        Consider price action, trends, and potential support/resistance levels.
        Respond with only 'UP' or 'DOWN' based on your analysis.
        """
        
        # Get prediction from LLM
        response = self.llm.predict_messages([HumanMessage(content=prompt)])
        prediction = response.content.strip().upper()
        
        return prediction
    
    def _prepare_market_description(self, market_data: List[MarketData]) -> str:
        description = "Recent price action:\n"
        for data in market_data[-5:]:  # Last 5 candles
            description += (
                f"Time: {data.time}, Open: {data.open}, High: {data.high}, "
                f"Low: {data.low}, Close: {data.close}\n"
            )
        return description
    
    def execute_trade(self, prediction: str, current_price: float):
        if prediction not in ['UP', 'DOWN']:
            return
            
        trade_message = ""
        if prediction == 'UP' and self.current_position != 'LONG':
            self.current_position = 'LONG'
            trade_message = f"Opening LONG position at {current_price}"
        elif prediction == 'DOWN' and self.current_position != 'SHORT':
            self.current_position = 'SHORT'
            trade_message = f"Opening SHORT position at {current_price}"
            
        if trade_message:
            self.notification_service.send_notification(trade_message) 
import websockets
import json
import asyncio
from datetime import datetime
from trading_agent import MarketData
from typing import List

class BinaryDataSource:
    def __init__(self):
        self.ws_url = "wss://ws.binaryws.com/websockets/v3?app_id=1089"
        self.request = {
            "ticks_history": "R_10",
            "adjust_start_time": 1,
            "count": 2000,
            "end": "latest",
            "granularity": 900,  # 15-minute candles
            "start": 1,
            "style": "candles"
        }

    async def get_market_data(self) -> List[MarketData]:
        async with websockets.connect(self.ws_url) as websocket:
            await websocket.send(json.dumps(self.request))
            response = await websocket.recv()
            data = json.loads(response)
            
            candles = data.get('candles', [])
            market_data = []
            
            for candle in candles:
                market_data.append(
                    MarketData(
                        open=float(candle['open']),
                        high=float(candle['high']),
                        low=float(candle['low']),
                        close=float(candle['close']),
                        time=datetime.fromtimestamp(candle['epoch'])
                    )
                )
            
            return market_data

    async def subscribe_to_candles(self, callback):
        """Subscribe to real-time candle updates"""
        subscribe_request = {
            "ticks_history": "R_10",
            "adjust_start_time": 1,
            "count": 1,
            "end": "latest",
            "granularity": 900,
            "start": 1,
            "style": "candles",
            "subscribe": 1
        }
        
        async with websockets.connect(self.ws_url) as websocket:
            await websocket.send(json.dumps(subscribe_request))
            
            while True:
                response = await websocket.recv()
                data = json.loads(response)
                
                if 'candles' in data:
                    candle = data['candles'][-1]
                    market_data = MarketData(
                        open=float(candle['open']),
                        high=float(candle['high']),
                        low=float(candle['low']),
                        close=float(candle['close']),
                        time=datetime.fromtimestamp(candle['epoch'])
                    )
                    await callback(market_data)

def get_market_data() -> List[MarketData]:
    """Synchronous wrapper for getting market data"""
    return asyncio.run(BinaryDataSource().get_market_data()) 
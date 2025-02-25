from typing import Optional
import smtplib
from email.mime.text import MIMEText
from telegram import Bot

class NotificationService:
    def __init__(self, email_config: Optional[dict] = None, telegram_config: Optional[dict] = None):
        self.email_config = email_config
        self.telegram_config = telegram_config
        
        if telegram_config:
            self.telegram_bot = Bot(token=telegram_config['token'])
    
    def send_notification(self, message: str):
        """Send notification through configured channels"""
        if self.email_config:
            self._send_email(message)
        if self.telegram_config:
            self._send_telegram(message)
    
    def _send_email(self, message: str):
        try:
            msg = MIMEText(message)
            msg['Subject'] = 'Trade Alert'
            msg['From'] = self.email_config['from_email']
            msg['To'] = self.email_config['to_email']
            
            with smtplib.SMTP_SSL(self.email_config['smtp_server'], self.email_config['smtp_port']) as server:
                server.login(self.email_config['username'], self.email_config['password'])
                server.send_message(msg)
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
    
    def _send_telegram(self, message: str):
        try:
            self.telegram_bot.send_message(
                chat_id=self.telegram_config['chat_id'],
                text=message
            )
        except Exception as e:
            print(f"Failed to send Telegram message: {str(e)}") 
"""
استخراج کانفیگ‌ها از کانال‌های تلگرام
"""

import asyncio
import json
import os
from telethon import TelegramClient
from config_parser import ConfigParser

class TelegramScraper:
    def __init__(self, api_id: str, api_hash: str):
        self.api_id = api_id
        self.api_hash = api_hash
        self.client = TelegramClient('session', api_id, api_hash)
    
    async def scrape_channel(self, channel: str, max_messages: int = 100) -> list:
        """استخراج کانفیگ از یک کانال"""
        configs = []
        
        try:
            print(f"📡 Scraping channel: @{channel}")
            
            async for message in self.client.iter_messages(channel, limit=max_messages):
                if message.text:
                    # استخراج کانفیگ‌ها از متن
                    extracted = ConfigParser.extract_configs(
                        message.text,
                        ['vless', 'ss', 'shadowsocks', 'socks']
                    )
                    
                    if extracted:
                        configs.extend(extracted)
                        print(f"  ✅ Found {len(extracted)} configs in message {message.id}")
            
            print(f"  📊 Total from @{channel}: {len(configs)} configs")
            
        except Exception as e:
            print(f"  ❌ Error in @{channel}: {e}")
        
        return configs
    
    async def scrape_all(self, channels: list, max_messages: int = 100) -> list:
        """استخراج از تمام کانال‌ها"""
        all_configs = []
        
        await self.client.start()
        
        for channel in channels:
            configs = await self.scrape_channel(channel, max_messages)
            all_configs.extend(configs)
            await asyncio.sleep(2)  # تأخیر برای جلوگیری از محدودیت API
        
        await self.client.disconnect()
        
        # حذف تکراری‌ها
        unique_configs = ConfigParser.deduplicate(all_configs)
        
        print(f"\n📈 Summary:")
        print(f"  Total collected: {len(all_configs)}")
        print(f"  After deduplication: {len(unique_configs)}")
        
        return unique_configs

async def main():
    # خواندن تنظیمات
    with open('configs/channels.json') as f:
        settings = json.load(f)
    
    # دریافت از environment variables
    api_id = os.getenv('TELEGRAM_API_ID')
    api_hash = os.getenv('TELEGRAM_API_HASH')
    
    if not api_id or not api_hash:
        print("❌ TELEGRAM_API_ID and TELEGRAM_API_HASH must be set!")
        return
    
    scraper = TelegramScraper(api_id, api_hash)
    
    configs = await scraper.scrape_all(
        settings['telegram_channels'],
        settings['test_settings']['max_messages_per_channel']
    )
    
    # ذخیره در فایل موقت
    with open('raw_configs.json', 'w', encoding='utf-8') as f:
        json.dump(configs, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Saved {len(configs)} configs to raw_configs.json")

if __name__ == '__main__':
    asyncio.run(main())

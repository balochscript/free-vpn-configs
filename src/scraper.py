"""
استخراج کانفیگ‌ها از کانال‌های تلگرام با Pyrogram
"""

import asyncio
import json
import os
from pyrogram import Client
from pyrogram.errors import FloodWait, ChannelPrivate, UsernameInvalid
from config_parser import ConfigParser

class TelegramScraper:
    def __init__(self, session_string):
        """ساخت client با session string"""
        self.app = Client(
            name="my_scraper",
            api_id=2040,
            api_hash="b18441a1ff607e10a989891a5462e627",
            session_string=session_string,
            in_memory=True
        )
    
    async def scrape_channel(self, channel: str, max_messages: int = 50) -> list:
        """استخراج کانفیگ از یک کانال"""
        configs = []
        
        try:
            print(f"📡 Scraping: @{channel}")
            
            count = 0
            async for message in self.app.get_chat_history(f"@{channel}", limit=max_messages):
                count += 1
                if message.text:
                    extracted = ConfigParser.extract_configs(
                        message.text,
                        ['vless', 'ss', 'shadowsocks']
                    )
                    
                    if extracted:
                        configs.extend(extracted)
                        print(f"  ✅ Message {message.id}: found {len(extracted)} configs")
            
            print(f"  📊 Checked {count} messages → {len(configs)} configs")
            
        except FloodWait as e:
            print(f"  ⏳ FloodWait {e.value}s")
            await asyncio.sleep(e.value)
            return await self.scrape_channel(channel, max_messages)
        
        except ChannelPrivate:
            print(f"  ❌ Private or not member")
        
        except UsernameInvalid:
            print(f"  ❌ Channel not found")
        
        except Exception as e:
            print(f"  ❌ Error: {e}")
        
        return configs
    
    async def scrape_all(self, channels: list, max_messages: int = 50) -> list:
        """استخراج از تمام کانال‌ها"""
        all_configs = []
        
        await self.app.start()
        
        try:
            me = await self.app.get_me()
            print(f"👤 Logged in: {me.first_name}")
        except Exception as e:
            print(f"❌ Login failed: {e}")
            return []
        
        for channel in channels:
            configs = await self.scrape_channel(channel, max_messages)
            all_configs.extend(configs)
            await asyncio.sleep(2)
        
        unique_configs = ConfigParser.deduplicate(all_configs)
        
        print(f"\n📈 Total: {len(all_configs)} → Unique: {len(unique_configs)}")
        
        await self.app.stop()
        
        return unique_configs

async def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, '..', 'configs', 'channels.json')
    
    print(f"📂 Config: {config_path}")
    
    if not os.path.exists(config_path):
        print(f"❌ Config not found!")
        return
    
    with open(config_path) as f:
        settings = json.load(f)
    
    session_string = os.getenv('PYROGRAM_SESSION')
    
    if not session_string:
        print("❌ No PYROGRAM_SESSION!")
        return
    
    print("✅ Session found")
    
    scraper = TelegramScraper(session_string)
    
    configs = await scraper.scrape_all(
        settings['telegram_channels'],
        settings['test_settings']['max_messages_per_channel']
    )
    
    output_path = os.path.join(current_dir, '..', 'raw_configs.json')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(configs, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Saved {len(configs)} configs")

if __name__ == '__main__':
    asyncio.run(main())

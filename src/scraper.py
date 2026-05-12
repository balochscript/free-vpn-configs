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
    def __init__(self):
        """
        Pyrogram از API داخلی خودش استفاده می‌کند
        نیازی به api_id و api_hash از my.telegram.org نیست
        """
        # بررسی session string از GitHub Secrets
        session_string = os.getenv('PYROGRAM_SESSION')
        
        if session_string:
            # استفاده از session موجود (برای GitHub Actions)
            self.app = Client(
                name="my_bot",
                session_string=session_string,
                in_memory=True
            )
            print("✅ Using existing session from environment")
        else:
            # ساخت session جدید (برای اولین بار)
            self.app = Client(
                name="my_bot",
                workdir="."
            )
            print("⚠️ Creating new session (you'll need to login)")
    
    async def scrape_channel(self, channel: str, max_messages: int = 100) -> list:
        """استخراج کانفیگ از یک کانال"""
        configs = []
        
        try:
            print(f"📡 Scraping channel: @{channel}")
            
            # دریافت پیام‌ها
            async for message in self.app.get_chat_history(
                chat_id=f"@{channel}",
                limit=max_messages
            ):
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
            
        except FloodWait as e:
            print(f"  ⏳ FloodWait: sleeping for {e.value} seconds")
            await asyncio.sleep(e.value)
            return await self.scrape_channel(channel, max_messages)
        
        except ChannelPrivate:
            print(f"  ❌ Channel @{channel} is private")
        
        except UsernameInvalid:
            print(f"  ❌ Channel @{channel} not found")
        
        except Exception as e:
            print(f"  ❌ Error in @{channel}: {e}")
        
        return configs
    
    async def scrape_all(self, channels: list, max_messages: int = 100) -> list:
        """استخراج از تمام کانال‌ها"""
        all_configs = []
        
        # شروع کلاینت
        await self.app.start()
        
        # دریافت اطلاعات حساب
        me = await self.app.get_me()
        print(f"👤 Logged in as: {me.first_name} (@{me.username or 'No username'})")
        
        for channel in channels:
            configs = await self.scrape_channel(channel, max_messages)
            all_configs.extend(configs)
            await asyncio.sleep(2)  # تأخیر برای جلوگیری از محدودیت
        
        # حذف تکراری‌ها
        unique_configs = ConfigParser.deduplicate(all_configs)
        
        print(f"\n📈 Summary:")
        print(f"  Total collected: {len(all_configs)}")
        print(f"  After deduplication: {len(unique_configs)}")
        
        # نمایش session string برای استفاده در GitHub Actions
        if not os.getenv('PYROGRAM_SESSION'):
            session_string = await self.app.export_session_string()
            print("\n" + "="*60)
            print("🔑 IMPORTANT: Save this session string in GitHub Secrets!")
            print("="*60)
            print(f"\nSecret Name: PYROGRAM_SESSION")
            print(f"Secret Value:\n{session_string}")
            print("\n" + "="*60)
        
        await self.app.stop()
        
        return unique_configs

async def main():
    # خواندن تنظیمات با مسیر مطلق
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, '..', 'configs', 'channels.json')
    
    with open(config_path) as f:
        settings = json.load(f)
    
    # دریافت session از environment
    session_string = os.getenv('PYROGRAM_SESSION')
    
    if not session_string:
        print("❌ PYROGRAM_SESSION not found in environment!")
        return
    
    print("✅ Session found, starting scraper...")
    
    scraper = TelegramScraper(session_string)
    
    configs = await scraper.scrape_all(
        settings['telegram_channels'],
        settings['test_settings']['max_messages_per_channel']
    )
    
    # ذخیره در مسیر صحیح
    output_path = os.path.join(current_dir, '..', 'raw_configs.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(configs, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Saved {len(configs)} configs to {output_path}")

if __name__ == '__main__':
    asyncio.run(main())

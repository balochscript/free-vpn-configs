import asyncio
import json
import os
from pyrogram import Client
from pyrogram.errors import FloodWait, ChannelPrivate, UsernameInvalid
from config_parser import ConfigParser

class TelegramScraper:
    def __init__(self, session_string):
        """
        ساخت کلاینت Telegram با استفاده از environment variables
        """
        # ✅ خواندن از GitHub Secrets / Environment Variables
        api_id = os.getenv('TELEGRAM_API_ID')
        api_hash = os.getenv('TELEGRAM_API_HASH')
        
        # بررسی وجود
        if not api_id:
            raise ValueError(
                "❌ TELEGRAM_API_ID environment variable is not set!\n"
                "Please add it to GitHub Secrets:\n"
                "Settings → Secrets and variables → Actions → New repository secret"
            )
        
        if not api_hash:
            raise ValueError(
                "❌ TELEGRAM_API_HASH environment variable is not set!\n"
                "Please add it to GitHub Secrets:\n"
                "Settings → Secrets and variables → Actions → New repository secret"
            )
        
        # نمایش بخشی از API برای تأیید (امن)
        print(f"🔑 API ID: {api_id}")
        print(f"🔐 API Hash: {api_hash[:8]}...{api_hash[-4:]}")
        
        # ساخت کلاینت Pyrogram
        self.app = Client(
            name="vpn_config_scraper",
            api_id=int(api_id),
            api_hash=api_hash,
            session_string=session_string,
            in_memory=True,
            no_updates=True  # ✅ رفع خطای "Peer id invalid"
        )
    
    async def scrape_channel(self, channel: str, max_messages: int = 50) -> list:
        """
        استخراج کانفیگ از یک کانال تلگرام
        """
        configs = []
        
        try:
            print(f"\n📡 Scraping: @{channel}")
            
            count = 0
            async for message in self.app.get_chat_history(f"@{channel}", limit=max_messages):
                count += 1
                
                # ✅ بررسی هم text و هم caption
                text_content = message.text or message.caption or ""
                
                if text_content:
                    extracted = ConfigParser.extract_configs(
                        text_content,
                        ['vless', 'ss', 'shadowsocks', 'trojan']
                    )
                    
                    if extracted:
                        configs.extend(extracted)
                        print(f"  ✅ Message {message.id}: found {len(extracted)} configs")
            
            print(f"  📊 Checked {count} messages → {len(configs)} configs")
            
        except FloodWait as e:
            print(f"  ⏳ FloodWait {e.value}s - waiting...")
            await asyncio.sleep(e.value)
            return await self.scrape_channel(channel, max_messages)
        
        except ChannelPrivate:
            print(f"  ❌ Channel is private or you're not a member")
        
        except UsernameInvalid:
            print(f"  ❌ Channel not found")
        
        except Exception as e:
            print(f"  ❌ Error: {type(e).__name__}: {e}")
        
        return configs
    
    async def scrape_all(self, channels: list, max_messages: int = 50) -> list:
        """
        استخراج کانفیگ از همه کانال‌ها
        """
        all_configs = []
        
        print("🚀 Starting Telegram client...")
        await self.app.start()
        
        try:
            me = await self.app.get_me()
            print(f"✅ Logged in as: {me.first_name}")
            if me.username:
                print(f"   Username: @{me.username}")
            print(f"   Phone: {me.phone_number}")
            print(f"   User ID: {me.id}")
        except Exception as e:
            print(f"❌ Failed to get account info: {e}")
            return []
        
        print(f"\n📚 Scraping {len(channels)} channels...")
        print("=" * 60)
        
        for idx, channel in enumerate(channels, 1):
            print(f"\n[{idx}/{len(channels)}] Channel: @{channel}")
            configs = await self.scrape_channel(channel, max_messages)
            all_configs.extend(configs)
            
            # تاخیر بین کانال‌ها
            if idx < len(channels):
                await asyncio.sleep(2)
        
        print("\n" + "=" * 60)
        print("📊 Deduplicating configs...")
        unique_configs = ConfigParser.deduplicate(all_configs)
        
        print(f"✅ Total collected: {len(all_configs)}")
        print(f"✅ Unique configs: {len(unique_configs)}")
        print(f"🗑️  Duplicates removed: {len(all_configs) - len(unique_configs)}")
        
        await self.app.stop()
        print("🛑 Telegram client stopped")
        
        return unique_configs


async def main():
    """
    تابع اصلی برای اجرای scraper
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, '..', 'configs', 'channels.json')
    
    print("╔" + "═" * 60 + "╗")
    print("║" + " " * 15 + "🔍 VPN Config Scraper" + " " * 24 + "║")
    print("╚" + "═" * 60 + "╝")
    print()
    
    print(f"📂 Loading config from: {config_path}")
    
    if not os.path.exists(config_path):
        print(f"❌ Config file not found!")
        return
    
    # خواندن تنظیمات
    with open(config_path, 'r', encoding='utf-8') as f:
        settings = json.load(f)
    
    print(f"✅ Config loaded successfully")
    print(f"   Channels: {len(settings['telegram_channels'])}")
    print(f"   Max messages per channel: {settings['test_settings']['max_messages_per_channel']}")
    print()
    
    # بررسی Session
    session_string = os.getenv('PYROGRAM_SESSION')
    
    if not session_string:
        print("❌ PYROGRAM_SESSION environment variable not set!")
        print("   Please add it to GitHub Secrets")
        return
    
    print(f"✅ Session string found (length: {len(session_string)} chars)")
    print()
    
    # شروع scraping
    try:
        scraper = TelegramScraper(session_string)
        
        configs = await scraper.scrape_all(
            settings['telegram_channels'],
            settings['test_settings']['max_messages_per_channel']
        )
        
        # ذخیره نتایج
        output_path = os.path.join(current_dir, '..', 'raw_configs.json')
        
        print(f"\n💾 Saving to: {output_path}")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(configs, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Successfully saved {len(configs)} configs")
        
        # نمایش خلاصه پروتکل‌ها
        protocols = {}
        for config in configs:
            protocol = config.get('protocol', 'unknown')
            protocols[protocol] = protocols.get(protocol, 0) + 1
        
        if protocols:
            print("\n📊 Config breakdown by protocol:")
            for protocol, count in sorted(protocols.items()):
                print(f"   {protocol}: {count}")
        
    except ValueError as e:
        print(f"\n❌ Configuration Error:")
        print(f"   {e}")
        return
    
    except Exception as e:
        print(f"\n❌ Unexpected error:")
        print(f"   {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print("\n" + "╔" + "═" * 60 + "╗")
    print("║" + " " * 20 + "✅ Scraping Complete!" + " " * 19 + "║")
    print("╚" + "═" * 60 + "╝")


if __name__ == '__main__':
    asyncio.run(main())

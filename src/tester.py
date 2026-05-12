"""
تست کردن کانفیگ‌ها و بررسی حجم
"""

import asyncio
import json
import subprocess
import tempfile
import time
import aiohttp
from concurrent.futures import ThreadPoolExecutor
import os

class ConfigTester:
    def __init__(self, config_path='/usr/local/bin/xray'):
        self.xray_path = config_path
        self.base_port = 10800
    
    def create_xray_config(self, config: dict, port: int) -> dict:
        """ساخت فایل کانفیگ Xray"""
        
        if config['protocol'] == 'vless':
            outbound = {
                "protocol": "vless",
                "settings": {
                    "vnext": [{
                        "address": config['server'],
                        "port": config['port'],
                        "users": [{
                            "id": config['uuid'],
                            "encryption": config.get('encryption', 'none')
                        }]
                    }]
                },
                "streamSettings": {
                    "network": config.get('type', 'tcp'),
                    "security": config.get('security', 'none')
                }
            }
            
            if config.get('sni'):
                outbound['streamSettings']['tlsSettings'] = {
                    "serverName": config['sni'],
                    "fingerprint": config.get('fp', '')
                }
        
        elif config['protocol'] in ['shadowsocks', 'ss']:
            outbound = {
                "protocol": "shadowsocks",
                "settings": {
                    "servers": [{
                        "address": config['server'],
                        "port": config['port'],
                        "method": config['method'],
                        "password": config['password']
                    }]
                }
            }
        
        else:
            return None
        
        xray_config = {
            "log": {"loglevel": "error"},
            "inbounds": [{
                "port": port,
                "protocol": "http",
                "settings": {"timeout": 0}
            }],
            "outbounds": [outbound]
        }
        
        return xray_config
    
    async def test_connection(self, config: dict, timeout: int = 15) -> dict:
        """تست اتصال یک کانفیگ"""
        result = {
            'config': config,
            'alive': False,
            'has_volume': False,
            'speed_mbps': 0,
            'latency_ms': 0
        }
        
        port = self.base_port + hash(f"{config['server']}:{config['port']}") % 1000
        
        try:
            # ساخت کانفیگ Xray
            xray_config = self.create_xray_config(config, port)
            if not xray_config:
                return result
            
            # نوشتن به فایل موقت
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                json.dump(xray_config, f)
                config_file = f.name
            
            # اجرای Xray
            process = subprocess.Popen(
                [self.xray_path, 'run', '-config', config_file],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            await asyncio.sleep(3)  # صبر برای آماده شدن
            
            # تست اتصال
            proxy_url = f"http://127.0.0.1:{port}"
            
            try:
                start_time = time.time()
                
                async with aiohttp.ClientSession() as session:
                    # تست سریع
                    async with session.get(
                        'http://www.gstatic.com/generate_204',
                        proxy=proxy_url,
                        timeout=aiohttp.ClientTimeout(total=timeout)
                    ) as response:
                        if response.status == 204:
                            result['alive'] = True
                            result['latency_ms'] = int((time.time() - start_time) * 1000)
                            
                            # تست حجم - دانلود فایل ۱۰ مگابایتی
                            print(f"  📥 Testing volume for {config['server']}...")
                            
                            start_download = time.time()
                            async with session.get(
                                'http://ipv4.download.thinkbroadband.com/10MB.zip',
                                proxy=proxy_url,
                                timeout=aiohttp.ClientTimeout(total=60)
                            ) as dl_response:
                                downloaded = 0
                                async for chunk in dl_response.content.iter_chunked(1024):
                                    downloaded += len(chunk)
                                
                                duration = time.time() - start_download
                                
                                # اگر حداقل ۵ مگابایت دانلود شد
                                if downloaded > 5 * 1024 * 1024:
                                    result['has_volume'] = True
                                    result['speed_mbps'] = round((downloaded * 8) / (duration * 1000000), 2)
                                    print(f"  ✅ Has volume! Speed: {result['speed_mbps']} Mbps")
                                else:
                                    print(f"  ⚠️ Limited volume: {downloaded / (1024*1024):.2f} MB")
            
            except asyncio.TimeoutError:
                print(f"  ⏱️ Timeout: {config['server']}")
            except Exception as e:
                print(f"  ❌ Connection error: {e}")
            
            # کشتن پروسه Xray
            process.kill()
            process.wait()
            
            # حذف فایل موقت
            os.unlink(config_file)
        
        except Exception as e:
            print(f"  ❌ Test error for {config.get('server', 'unknown')}: {e}")
        
        return result
    
    async def test_all(self, configs: list, max_concurrent: int = 5) -> list:
        """تست همزمان چندین کانفیگ"""
        print(f"\n🧪 Testing {len(configs)} configs (max {max_concurrent} concurrent)...")
        
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def test_with_semaphore(config):
            async with semaphore:
                return await self.test_connection(config)
        
        tasks = [test_with_semaphore(config) for config in configs]
        results = await asyncio.gather(*tasks)
        
        # فیلتر کردن فقط کانفیگ‌های سالم با حجم
        working = [r for r in results if r['alive'] and r['has_volume']]
        
        print(f"\n📊 Test Results:")
        print(f"  Total tested: {len(results)}")
        print(f"  Alive: {sum(1 for r in results if r['alive'])}")
        print(f"  With volume: {len(working)}")
        
        return working

async def main():
    # خواندن کانفیگ‌های خام
    with open('raw_configs.json') as f:
        configs = json.load(f)
    
    tester = ConfigTester()
    
    # تست کردن
    working_configs = await tester.test_all(configs, max_concurrent=10)
    
    # ذخیره نتیجه
    with open('working_configs.json', 'w', encoding='utf-8') as f:
        json.dump(working_configs, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Saved {len(working_configs)} working configs")

if __name__ == '__main__':
    asyncio.run(main())

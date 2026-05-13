import asyncio
import json
import subprocess
import tempfile
import time
import aiohttp
import os
from typing import Dict, List, Optional

class ConfigTester:
    """
    تست کننده کانفیگ‌ها با سه روش مختلف:
    1. Alive Test - فقط زنده بودن
    2. Volume Test - فقط حجم (100KB)
    3. Iran Test - بهینه برای ایران (DNS برتینا)
    """
    
    def __init__(self, xray_path='/usr/local/bin/xray'):
        self.xray_path = xray_path
        self.base_port = 10800
        
        # تنظیمات مختلف تست
        self.test_configs = {
            'alive': {
                'timeout': 30,
                'test_url': 'http://www.gstatic.com/generate_204',
                'dns': None,
                'min_volume': 0
            },
            'volume': {
                'timeout': 45,
                'test_url': 'http://ipv4.download.thinkbroadband.com/512KB.zip',
                'dns': None,
                'min_volume': 100 * 1024  # 100KB
            },
            'iran': {
                'timeout': 25,
                'test_url': 'http://search.bertina.ir',
                'dns': '193.186.32.32',  # DNS برتینا
                'min_volume': 50 * 1024  # 50KB
            }
        }
    
    def create_xray_config(self, config: dict, port: int, dns_server: Optional[str] = None) -> Optional[dict]:
        """ساخت کانفیگ Xray"""
        
        # ساخت outbound بر اساس پروتکل
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
                    "fingerprint": config.get('fp', 'chrome')
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
        
        elif config['protocol'] == 'trojan':
            outbound = {
                "protocol": "trojan",
                "settings": {
                    "servers": [{
                        "address": config['server'],
                        "port": config['port'],
                        "password": config['password']
                    }]
                },
                "streamSettings": {
                    "network": config.get('type', 'tcp'),
                    "security": config.get('security', 'tls')
                }
            }
            
            if config.get('sni'):
                outbound['streamSettings']['tlsSettings'] = {
                    "serverName": config['sni'],
                    "fingerprint": config.get('fp', 'chrome')
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
        
        # اضافه کردن DNS سفارشی
        if dns_server:
            xray_config["dns"] = {
                "servers": [
                    dns_server,
                    "1.1.1.1"
                ]
            }
        
        return xray_config
    
    async def test_config(
        self, 
        config: dict, 
        test_type: str = 'alive'
    ) -> Dict:
        """
        تست یک کانفیگ
        test_type: 'alive', 'volume', 'iran'
        """
        result = {
            'config': config,
            'alive': False,
            'has_volume': False,
            'speed_kbps': 0,
            'latency_ms': 0,
            'test_type': test_type
        }
        
        # دریافت تنظیمات تست
        test_settings = self.test_configs.get(test_type, self.test_configs['alive'])
        
        # پورت یونیک
        port = self.base_port + (hash(f"{config['server']}:{config['port']}") % 5000)
        
        try:
            # ساخت کانفیگ Xray
            xray_config = self.create_xray_config(
                config, 
                port, 
                test_settings['dns']
            )
            
            if not xray_config:
                return result
            
            # ذخیره در فایل موقت
            with tempfile.NamedTemporaryFile(
                mode='w', 
                suffix='.json', 
                delete=False
            ) as f:
                json.dump(xray_config, f)
                config_file = f.name
            
            # اجرای Xray
            process = subprocess.Popen(
                [self.xray_path, 'run', '-config', config_file],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            # صبر برای شروع
            await asyncio.sleep(3)
            
            proxy_url = f"http://127.0.0.1:{port}"
            
            try:
                async with aiohttp.ClientSession() as session:
                    # تست اتصال
                    start_time = time.time()
                    
                    async with session.get(
                        test_settings['test_url'],
                        proxy=proxy_url,
                        timeout=aiohttp.ClientTimeout(total=test_settings['timeout'])
                    ) as response:
                        if response.status in [200, 204]:
                            result['alive'] = True
                            result['latency_ms'] = int((time.time() - start_time) * 1000)
                            
                            # اگر نیاز به تست حجم داریم
                            if test_settings['min_volume'] > 0:
                                downloaded = 0
                                start_download = time.time()
                                
                                async for chunk in response.content.iter_chunked(8192):
                                    downloaded += len(chunk)
                                    
                                    if downloaded >= test_settings['min_volume']:
                                        break
                                
                                duration = time.time() - start_download
                                
                                if downloaded >= test_settings['min_volume'] and duration > 0:
                                    result['has_volume'] = True
                                    result['speed_kbps'] = int((downloaded / 1024) / duration)
            
            except asyncio.TimeoutError:
                pass
            except Exception:
                pass
            
            # بستن Xray
            process.kill()
            process.wait()
            
            # پاک کردن فایل موقت
            try:
                os.unlink(config_file)
            except:
                pass
        
        except Exception:
            pass
        
        return result
    
    async def test_all(
        self, 
        configs: list, 
        test_type: str = 'alive',
        max_concurrent: int = 8
    ) -> List[Dict]:
        """تست همه کانفیگ‌ها"""
        
        print(f"\n🧪 Testing {len(configs)} configs (Type: {test_type.upper()})")
        print(f"   Settings: {self.test_configs[test_type]}")
        print(f"   Concurrent: {max_concurrent}")
        print("=" * 70)
        
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def test_with_semaphore(idx, config):
            async with semaphore:
                print(f"  [{idx}/{len(configs)}] Testing {config['server']}:{config['port']}")
                result = await self.test_config(config, test_type)
                
                if result['alive']:
                    if result['has_volume']:
                        print(f"    ✅ Alive + Volume ({result['speed_kbps']} KB/s)")
                    else:
                        print(f"    ✅ Alive ({result['latency_ms']}ms)")
                else:
                    print(f"    ❌ Failed")
                
                return result
        
        tasks = [test_with_semaphore(i+1, cfg) for i, cfg in enumerate(configs)]
        results = await asyncio.gather(*tasks)
        
        # فیلتر نتایج
        alive_results = [r for r in results if r['alive']]
        volume_results = [r for r in results if r['has_volume']]
        
        print("\n" + "=" * 70)
        print(f"📊 Results ({test_type.upper()}):")
        print(f"   Total tested: {len(results)}")
        print(f"   Alive: {len(alive_results)}")
        print(f"   With volume: {len(volume_results)}")
        print("=" * 70)
        
        return results


async def main():
    """اجرای تست‌ها"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # مسیرها
    raw_path = os.path.join(current_dir, '..', 'raw_configs.json')
    config_path = os.path.join(current_dir, '..', 'configs', 'channels.json')
    
    # خواندن کانفیگ‌ها
    with open(raw_path) as f:
        configs = json.load(f)
    
    with open(config_path) as f:
        settings = json.load(f)
    
    print("╔" + "═" * 70 + "╗")
    print("║" + " " * 20 + "🧪 Config Tester" + " " * 33 + "║")
    print("╚" + "═" * 70 + "╝")
    print(f"\n📂 Loaded {len(configs)} configs")
    
    tester = ConfigTester()
    
    # نوع تست از environment variable
    test_type = os.getenv('TEST_TYPE', 'alive')
    concurrent = settings['test_settings'].get('concurrent_tests', 8)
    
    # اجرای تست
    results = await tester.test_all(configs, test_type, concurrent)
    
    # ذخیره نتایج
    output_path = os.path.join(current_dir, '..', f'tested_{test_type}.json')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Saved results to: tested_{test_type}.json")


if __name__ == '__main__':
    asyncio.run(main())

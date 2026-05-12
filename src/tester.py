import asyncio
import json
import subprocess
import tempfile
import time
import aiohttp
import os

class ConfigTester:
    def __init__(self, config_path='/usr/local/bin/xray'):
        self.xray_path = config_path
        self.base_port = 10800
    
    def create_xray_config(self, config: dict, port: int) -> dict:
        
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
                    "fingerprint": config.get('fp', '')
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
    
    async def test_connection(self, config: dict, min_volume_mb: int = 2, timeout: int = 10) -> dict:
        result = {
            'config': config,
            'alive': False,
            'has_volume': False,
            'speed_mbps': 0,
            'latency_ms': 0
        }
        
        port = self.base_port + hash(f"{config['server']}:{config['port']}") % 1000
        
        try:
            xray_config = self.create_xray_config(config, port)
            if not xray_config:
                return result
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                json.dump(xray_config, f)
                config_file = f.name
            
            process = subprocess.Popen(
                [self.xray_path, 'run', '-config', config_file],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            await asyncio.sleep(2)
            
            proxy_url = f"http://127.0.0.1:{port}"
            
            try:
                start_time = time.time()
                
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        'http://www.gstatic.com/generate_204',
                        proxy=proxy_url,
                        timeout=aiohttp.ClientTimeout(total=timeout)
                    ) as response:
                        if response.status == 204:
                            result['alive'] = True
                            result['latency_ms'] = int((time.time() - start_time) * 1000)
                            
                            print(f"  📥 Volume test: {config['server']}")
                            
                            start_download = time.time()
                            async with session.get(
                                'http://ipv4.download.thinkbroadband.com/5MB.zip',
                                proxy=proxy_url,
                                timeout=aiohttp.ClientTimeout(total=30)
                            ) as dl_response:
                                downloaded = 0
                                min_bytes = min_volume_mb * 1024 * 1024
                                
                                async for chunk in dl_response.content.iter_chunked(8192):
                                    downloaded += len(chunk)
                                    
                                    if downloaded >= min_bytes:
                                        break
                                
                                duration = time.time() - start_download
                                
                                if downloaded >= min_bytes:
                                    result['has_volume'] = True
                                    result['speed_mbps'] = round((downloaded * 8) / (duration * 1000000), 2)
                                    print(f"  ✅ Volume OK! {result['speed_mbps']} Mbps")
                                else:
                                    print(f"  ⚠️ Limited: {downloaded / (1024*1024):.1f} MB")
            
            except asyncio.TimeoutError:
                print(f"  ⏱️ Timeout: {config['server']}")
            except Exception as e:
                print(f"  ❌ Error: {type(e).__name__}")
            
            process.kill()
            process.wait()
            os.unlink(config_file)
        
        except Exception as e:
            print(f"  ❌ Test failed: {config.get('server', 'unknown')}")
        
        return result
    
    async def test_all(self, configs: list, min_volume_mb: int = 2, max_concurrent: int = 10) -> list:
        print(f"\n🧪 Testing {len(configs)} configs...")
        print(f"   Min volume: {min_volume_mb} MB")
        print(f"   Concurrent: {max_concurrent}")
        
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def test_with_semaphore(config):
            async with semaphore:
                return await self.test_connection(config, min_volume_mb)
        
        tasks = [test_with_semaphore(config) for config in configs]
        results = await asyncio.gather(*tasks)
        
        working = [r for r in results if r['alive'] and r['has_volume']]
        
        print(f"\n📊 Results:")
        print(f"   Tested: {len(results)}")
        print(f"   Alive: {sum(1 for r in results if r['alive'])}")
        print(f"   With volume: {len(working)}")
        
        return working

async def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    raw_path = os.path.join(current_dir, '..', 'raw_configs.json')
    config_path = os.path.join(current_dir, '..', 'configs', 'channels.json')
    
    with open(raw_path) as f:
        configs = json.load(f)
    
    with open(config_path) as f:
        settings = json.load(f)
    
    min_volume = settings['test_settings'].get('min_volume_mb', 2)
    concurrent = settings['test_settings'].get('concurrent_tests', 10)
    
    tester = ConfigTester()
    
    working_configs = await tester.test_all(configs, min_volume, concurrent)
    
    output_path = os.path.join(current_dir, '..', 'working_configs.json')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(working_configs, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Saved {len(working_configs)} configs")

if __name__ == '__main__':
    asyncio.run(main())

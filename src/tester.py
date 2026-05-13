import asyncio
import json
import subprocess
import tempfile
import time
import aiohttp
import os
import socket
from typing import Dict, List, Optional

class ConfigTester:
    
    def __init__(self, xray_path='/usr/local/bin/xray'):
        self.xray_path = xray_path
        self.base_port = 10800
        
        self.test_configs = {
            'tcping': {
                'timeout': 10,
                'retry': 2,
                'delay': 0.5
            },
            'realdelay': {
                'timeout': 30,
                'test_url': 'https://www.google.com/generate_204',
                'dns': '193.186.32.32',
                'retry': 2,
                'delay': 1
            }
        }
    
    def create_xray_config(self, config: dict, port: int, dns_server: Optional[str] = None) -> Optional[dict]:
        
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
            
            if config.get('security') in ['tls', 'reality']:
                tls_settings = {
                    "serverName": config.get('sni', config['server']),
                    "fingerprint": config.get('fp', 'chrome'),
                    "allowInsecure": False
                }
                
                if config.get('security') == 'tls':
                    outbound['streamSettings']['tlsSettings'] = tls_settings
                else:
                    outbound['streamSettings']['realitySettings'] = tls_settings
                    if config.get('pbk'):
                        outbound['streamSettings']['realitySettings']['publicKey'] = config['pbk']
                    if config.get('sid'):
                        outbound['streamSettings']['realitySettings']['shortId'] = config['sid']
        
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
                    "fingerprint": config.get('fp', 'chrome'),
                    "allowInsecure": False
                }
        
        elif config['protocol'] == 'vmess':
            outbound = {
                "protocol": "vmess",
                "settings": {
                    "vnext": [{
                        "address": config['server'],
                        "port": config['port'],
                        "users": [{
                            "id": config['uuid'],
                            "alterId": config.get('aid', 0),
                            "security": config.get('encryption', 'auto')
                        }]
                    }]
                },
                "streamSettings": {
                    "network": config.get('type', 'tcp'),
                    "security": config.get('security', 'none')
                }
            }
            
            if config.get('security') == 'tls' and config.get('sni'):
                outbound['streamSettings']['tlsSettings'] = {
                    "serverName": config['sni'],
                    "fingerprint": config.get('fp', 'chrome'),
                    "allowInsecure": False
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
        
        if dns_server:
            xray_config["dns"] = {
                "servers": [dns_server]
            }
        
        return xray_config
    
    async def tcp_ping(self, host: str, port: int, timeout: int = 10) -> tuple:
        try:
            start_time = time.time()
            
            loop = asyncio.get_event_loop()
            future = loop.run_in_executor(
                None,
                lambda: socket.create_connection((host, port), timeout=timeout)
            )
            
            sock = await asyncio.wait_for(future, timeout=timeout)
            latency = int((time.time() - start_time) * 1000)
            sock.close()
            
            return (True, latency)
        except:
            return (False, 0)
    
    async def test_real_delay(self, proxy_url: str, test_url: str, timeout: int) -> tuple:
        try:
            async with aiohttp.ClientSession() as session:
                start_time = time.time()
                async with session.get(
                    test_url,
                    proxy=proxy_url,
                    timeout=aiohttp.ClientTimeout(total=timeout),
                    ssl=False
                ) as response:
                    latency = int((time.time() - start_time) * 1000)
                    return (response.status in [200, 204], latency)
        except:
            return (False, 0)
    
    async def test_config(self, config: dict, test_type: str = 'tcping') -> Dict:
        result = {
            'config': config,
            'alive': False,
            'latency_ms': 0,
            'test_type': test_type
        }
        
        test_settings = self.test_configs.get(test_type)
        
        if test_type == 'tcping':
            for attempt in range(test_settings['retry']):
                is_alive, latency = await self.tcp_ping(
                    config['server'], 
                    config['port'], 
                    test_settings['timeout']
                )
                
                if is_alive:
                    result['alive'] = True
                    result['latency_ms'] = latency
                    return result
                
                if attempt < test_settings['retry'] - 1:
                    await asyncio.sleep(1)
            
            return result
        
        elif test_type == 'realdelay':
            port = self.base_port + (hash(f"{config['server']}:{config['port']}") % 5000)
            
            for attempt in range(test_settings['retry']):
                try:
                    xray_config = self.create_xray_config(config, port, test_settings['dns'])
                    
                    if not xray_config:
                        break
                    
                    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                        json.dump(xray_config, f)
                        config_file = f.name
                    
                    process = subprocess.Popen(
                        [self.xray_path, 'run', '-config', config_file],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                    
                    await asyncio.sleep(4)
                    
                    proxy_url = f"http://127.0.0.1:{port}"
                    
                    is_alive, latency = await self.test_real_delay(
                        proxy_url,
                        test_settings['test_url'],
                        test_settings['timeout']
                    )
                    
                    process.kill()
                    process.wait()
                    
                    try:
                        os.unlink(config_file)
                    except:
                        pass
                    
                    if is_alive:
                        result['alive'] = True
                        result['latency_ms'] = latency
                        return result
                    
                    if attempt < test_settings['retry'] - 1:
                        await asyncio.sleep(2)
                
                except Exception:
                    try:
                        process.kill()
                        process.wait()
                        os.unlink(config_file)
                    except:
                        pass
                    
                    if attempt < test_settings['retry'] - 1:
                        await asyncio.sleep(2)
                    continue
            
            return result
        
        return result
    
    async def test_all(self, configs: list, test_type: str = 'tcping', max_concurrent: int = 10) -> List[Dict]:
        
        titles = {
            'tcping': '⚡ TCPing Test',
            'realdelay': '🕐 Real Delay Test'
        }
        
        print(f"\n{titles.get(test_type, 'Test')}: {len(configs)} configs")
        print(f"   Settings: {self.test_configs[test_type]}")
        print(f"   Concurrent: {max_concurrent}")
        print("=" * 70)
        
        semaphore = asyncio.Semaphore(max_concurrent)
        test_settings = self.test_configs[test_type]
        
        async def test_with_semaphore(idx, config):
            async with semaphore:
                await asyncio.sleep(test_settings.get('delay', 0))
                
                print(f"  [{idx}/{len(configs)}] Testing {config['server']}:{config['port']}")
                result = await self.test_config(config, test_type)
                
                if result['alive']:
                    print(f"    ✅ Alive ({result['latency_ms']}ms)")
                else:
                    print(f"    ❌ Failed")
                
                return result
        
        tasks = [test_with_semaphore(i+1, cfg) for i, cfg in enumerate(configs)]
        results = await asyncio.gather(*tasks)
        
        alive_results = [r for r in results if r['alive']]
        
        print("\n" + "=" * 70)
        print(f"📊 Results ({test_type.upper()}):")
        print(f"   Total: {len(results)} | Alive: {len(alive_results)} | Failed: {len(results) - len(alive_results)}")
        
        if alive_results:
            avg_latency = sum(r['latency_ms'] for r in alive_results) // len(alive_results)
            print(f"   Average Latency: {avg_latency}ms")
        
        print("=" * 70)
        
        return results


async def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    raw_path = os.path.join(current_dir, '..', 'raw_configs.json')
    config_path = os.path.join(current_dir, '..', 'configs', 'channels.json')
    
    with open(raw_path) as f:
        configs = json.load(f)
    
    with open(config_path) as f:
        settings = json.load(f)
    
    print("╔" + "═" * 70 + "╗")
    print("║" + " " * 20 + "🧪 Config Tester" + " " * 33 + "║")
    print("╚" + "═" * 70 + "╝")
    print(f"\n📂 Loaded {len(configs)} configs")
    
    tester = ConfigTester()
    
    test_type = os.getenv('TEST_TYPE', 'tcping')
    concurrent = settings['test_settings'].get('concurrent_tests', 10)
    
    if test_type == 'realdelay':
        concurrent = min(concurrent, 6)
    
    results = await tester.test_all(configs, test_type, concurrent)
    
    output_path = os.path.join(current_dir, '..', f'tested_{test_type}.json')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Saved to: tested_{test_type}.json")


if __name__ == '__main__':
    asyncio.run(main())

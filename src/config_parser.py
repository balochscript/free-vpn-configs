"""
پارسر کانفیگ‌های مختلف V2ray
"""

import base64
import json
import re
from urllib.parse import urlparse, parse_qs, unquote
from typing import Dict, Optional

class ConfigParser:
    
    @staticmethod
    def parse_vless(url: str) -> Optional[Dict]:
        """پارس کردن لینک vless://"""
        try:
            # vless://UUID@SERVER:PORT?params#NAME
            url = url.replace('vless://', '')
            
            # جدا کردن نام (اختیاری)
            if '#' in url:
                url, name = url.split('#', 1)
                name = unquote(name)
            else:
                name = "VLESS Config"
            
            # جدا کردن پارامترها
            if '?' in url:
                main_part, params_part = url.split('?', 1)
            else:
                main_part, params_part = url, ''
            
            # UUID@SERVER:PORT
            uuid_server = main_part.split('@')
            if len(uuid_server) != 2:
                return None
                
            uuid = uuid_server[0]
            server_port = uuid_server[1].split(':')
            
            if len(server_port) != 2:
                return None
            
            server = server_port[0]
            
            # رفع خطای parsing port - حذف / و هر چیز بعد از آن
            try:
                port_clean = server_port[1].split('/')[0].split('?')[0]
                port = int(port_clean)
            except (ValueError, IndexError):
                print(f"Error parsing VLESS port: {server_port[1]}")
                return None
            
            # پارس پارامترها
            params = parse_qs(params_part)
            
            return {
                'protocol': 'vless',
                'uuid': uuid,
                'server': server,
                'port': port,
                'name': name,
                'encryption': params.get('encryption', ['none'])[0],
                'security': params.get('security', ['none'])[0],
                'type': params.get('type', ['tcp'])[0],
                'sni': params.get('sni', [''])[0],
                'fp': params.get('fp', [''])[0],
                'raw_link': f"vless://{url}"
            }
        except Exception as e:
            print(f"Error parsing VLESS: {e}")
            return None
    
    @staticmethod
    def parse_shadowsocks(url: str) -> Optional[Dict]:
        """پارس کردن لینک ss://"""
        try:
            # ss://BASE64#NAME یا ss://method:password@server:port#NAME
            url = url.replace('ss://', '').replace('shadowsocks://', '')
            
            # جدا کردن نام
            if '#' in url:
                url, name = url.split('#', 1)
                name = unquote(name)
            else:
                name = "SS Config"
            
            # تلاش برای decode کردن base64
            if '@' not in url:
                # اضافه کردن errors='ignore' برای رفع خطای UTF-8
                try:
                    decoded = base64.b64decode(url + '==').decode('utf-8', errors='ignore')
                    url = decoded
                except:
                    # اگر decode نشد، احتمالاً فرمت دیگری است
                    return None
            
            # method:password@server:port
            parts = url.split('@')
            if len(parts) != 2:
                return None
            
            method_password = parts[0].split(':')
            server_port = parts[1].split(':')
            
            if len(method_password) < 2 or len(server_port) != 2:
                return None
            
            return {
                'protocol': 'shadowsocks',
                'method': method_password[0],
                'password': ':'.join(method_password[1:]),
                'server': server_port[0],
                'port': int(server_port[1]),
                'name': name,
                'raw_link': f"ss://{url}"
            }
        except Exception as e:
            print(f"Error parsing SS: {e}")
            return None
    
    @staticmethod
    def parse_trojan(url: str) -> Optional[Dict]:
        """پارس کردن لینک trojan://"""
        try:
            # trojan://PASSWORD@SERVER:PORT?params#NAME
            url = url.replace('trojan://', '')
            
            # جدا کردن نام
            if '#' in url:
                url, name = url.split('#', 1)
                name = unquote(name)
            else:
                name = "Trojan Config"
            
            # جدا کردن پارامترها
            if '?' in url:
                main_part, params_part = url.split('?', 1)
            else:
                main_part, params_part = url, ''
            
            # PASSWORD@SERVER:PORT
            parts = main_part.split('@')
            if len(parts) != 2:
                return None
            
            password = parts[0]
            server_port = parts[1].split(':')
            
            if len(server_port) != 2:
                return None
            
            server = server_port[0]
            port = int(server_port[1])
            
            # پارس پارامترها
            params = parse_qs(params_part)
            
            return {
                'protocol': 'trojan',
                'password': password,
                'server': server,
                'port': port,
                'name': name,
                'security': params.get('security', ['tls'])[0],
                'sni': params.get('sni', [''])[0],
                'type': params.get('type', ['tcp'])[0],
                'fp': params.get('fp', [''])[0],
                'raw_link': f"trojan://{url}"
            }
        except Exception as e:
            print(f"Error parsing Trojan: {e}")
            return None
    
    @staticmethod
    def extract_configs(text: str, protocols: list) -> list:
        """استخراج تمام کانفیگ‌ها از متن"""
        configs = []
        
        # الگوهای مختلف
        patterns = {
            'vless': r'vless://[^\s\)]+',
            'ss': r'ss://[A-Za-z0-9+/=]+(?:#[^\s\)]*)?',
            'shadowsocks': r'shadowsocks://[^\s\)]+',
            'socks': r'socks[45]?://[^\s\)]+',
            'trojan': r'trojan://[^\s\)]+'
        }
        
        for protocol in protocols:
            if protocol in patterns:
                matches = re.findall(patterns[protocol], text, re.IGNORECASE)
                
                for match in matches:
                    # حذف کاراکترهای اضافی در انتها
                    match = match.rstrip('.,;:!?')
                    
                    parsed = None
                    if protocol == 'vless':
                        parsed = ConfigParser.parse_vless(match)
                    elif protocol in ['ss', 'shadowsocks']:
                        parsed = ConfigParser.parse_shadowsocks(match)
                    elif protocol == 'trojan':
                        parsed = ConfigParser.parse_trojan(match)
                    # اضافه کردن پارسر socks در صورت نیاز
                    
                    if parsed:
                        configs.append(parsed)
        
        return configs
    
    @staticmethod
    def deduplicate(configs: list) -> list:
        """حذف کانفیگ‌های تکراری بر اساس server:port"""
        seen = set()
        unique = []
        
        for config in configs:
            key = f"{config['server']}:{config['port']}"
            if key not in seen:
                seen.add(key)
                unique.append(config)
        
        return unique

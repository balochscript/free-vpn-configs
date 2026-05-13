import base64
import json
import re
from urllib.parse import parse_qs, unquote
from typing import Dict, Optional, List

class ConfigParser:
    
    @staticmethod
    def parse_vless(url: str) -> Optional[Dict]:
        try:
            url = url.replace('vless://', '')
            
            if '#' in url:
                url, name = url.split('#', 1)
                name = unquote(name)
            else:
                name = "VLESS Config"
            
            if '?' in url:
                main_part, params_part = url.split('?', 1)
            else:
                main_part, params_part = url, ''
            
            uuid_server = main_part.split('@')
            if len(uuid_server) != 2:
                return None
                
            uuid = uuid_server[0]
            server_port = uuid_server[1].split(':')
            
            if len(server_port) != 2:
                return None
            
            server = server_port[0]
            
            try:
                port_clean = server_port[1].split('/')[0].split('?')[0]
                port = int(port_clean)
            except (ValueError, IndexError):
                return None
            
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
                'pbk': params.get('pbk', [''])[0],
                'sid': params.get('sid', [''])[0]
            }
        except Exception as e:
            return None
    
    @staticmethod
    def parse_vmess(url: str) -> Optional[Dict]:
        try:
            url = url.replace('vmess://', '')
            
            decoded = base64.b64decode(url + '==').decode('utf-8', errors='ignore')
            data = json.loads(decoded)
            
            return {
                'protocol': 'vmess',
                'uuid': data.get('id', ''),
                'server': data.get('add', ''),
                'port': int(data.get('port', 0)),
                'aid': int(data.get('aid', 0)),
                'encryption': data.get('scy', 'auto'),
                'name': data.get('ps', 'VMess Config'),
                'type': data.get('net', 'tcp'),
                'security': data.get('tls', 'none'),
                'sni': data.get('sni', '')
            }
        except Exception as e:
            return None
    
    @staticmethod
    def parse_shadowsocks(url: str) -> Optional[Dict]:
        try:
            url = url.replace('ss://', '').replace('shadowsocks://', '')
            
            if '#' in url:
                url, name = url.split('#', 1)
                name = unquote(name)
            else:
                name = "SS Config"
            
            if '@' not in url:
                try:
                    decoded = base64.b64decode(url + '==').decode('utf-8', errors='ignore')
                    url = decoded
                except:
                    return None
            
            parts = url.split('@')
            if len(parts) != 2:
                return None
            
            method_password = parts[0].split(':')
            server_port = parts[1].split(':')
            
            if len(method_password) < 2 or len(server_port) != 2:
                return None
            
            port_clean = server_port[1].split('/')[0].split('?')[0]
            
            return {
                'protocol': 'shadowsocks',
                'method': method_password[0],
                'password': ':'.join(method_password[1:]),
                'server': server_port[0],
                'port': int(port_clean),
                'name': name
            }
        except Exception as e:
            return None
    
    @staticmethod
    def parse_trojan(url: str) -> Optional[Dict]:
        try:
            url = url.replace('trojan://', '')
            
            if '#' in url:
                url, name = url.split('#', 1)
                name = unquote(name)
            else:
                name = "Trojan Config"
            
            if '?' in url:
                main_part, params_part = url.split('?', 1)
            else:
                main_part, params_part = url, ''
            
            parts = main_part.split('@')
            if len(parts) != 2:
                return None
            
            password = parts[0]
            server_port = parts[1].split(':')
            
            if len(server_port) != 2:
                return None
            
            server = server_port[0]
            port_clean = server_port[1].split('/')[0].split('?')[0]
            port = int(port_clean)
            
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
                'fp': params.get('fp', [''])[0]
            }
        except Exception as e:
            return None
    
    @staticmethod
    def parse_json_config(json_str: str) -> Optional[Dict]:
        try:
            data = json.loads(json_str)
            
            if 'outbounds' not in data:
                return None
            
            for outbound in data['outbounds']:
                if outbound.get('tag') != 'proxy':
                    continue
                
                protocol = outbound.get('protocol', '').lower()
                settings = outbound.get('settings', {})
                stream_settings = outbound.get('streamSettings', {})
                
                if protocol == 'socks':
                    servers = settings.get('servers', [])
                    if not servers:
                        continue
                    
                    server = servers[0]
                    return {
                        'protocol': 'socks',
                        'server': server.get('address'),
                        'port': int(server.get('port', 0)),
                        'name': data.get('remarks', 'SOCKS Config')
                    }
                
                elif protocol == 'shadowsocks':
                    servers = settings.get('servers', [])
                    if not servers:
                        continue
                    
                    server = servers[0]
                    return {
                        'protocol': 'shadowsocks',
                        'server': server.get('address'),
                        'port': int(server.get('port', 0)),
                        'method': server.get('method'),
                        'password': server.get('password'),
                        'name': data.get('remarks', 'SS Config')
                    }
                
                elif protocol == 'vmess':
                    vnext = settings.get('vnext', [])
                    if not vnext:
                        continue
                    
                    server = vnext[0]
                    users = server.get('users', [])
                    if not users:
                        continue
                    
                    user = users[0]
                    config = {
                        'protocol': 'vmess',
                        'server': server.get('address'),
                        'port': int(server.get('port', 0)),
                        'uuid': user.get('id'),
                        'aid': int(user.get('alterId', 0)),
                        'encryption': user.get('security', 'auto'),
                        'name': data.get('remarks', 'VMess Config')
                    }
                    
                    if stream_settings:
                        config['type'] = stream_settings.get('network', 'tcp')
                        config['security'] = stream_settings.get('security', 'none')
                        
                        if config['security'] == 'tls':
                            tls_settings = stream_settings.get('tlsSettings', {})
                            config['sni'] = tls_settings.get('serverName', '')
                    
                    return config
                
                elif protocol == 'vless':
                    vnext = settings.get('vnext', [])
                    if not vnext:
                        continue
                    
                    server = vnext[0]
                    users = server.get('users', [])
                    if not users:
                        continue
                    
                    user = users[0]
                    config = {
                        'protocol': 'vless',
                        'server': server.get('address'),
                        'port': int(server.get('port', 0)),
                        'uuid': user.get('id'),
                        'encryption': user.get('encryption', 'none'),
                        'name': data.get('remarks', 'VLESS Config')
                    }
                    
                    if stream_settings:
                        config['type'] = stream_settings.get('network', 'tcp')
                        config['security'] = stream_settings.get('security', 'none')
                        
                        if config['security'] in ['tls', 'reality']:
                            settings_key = 'tlsSettings' if config['security'] == 'tls' else 'realitySettings'
                            security_settings = stream_settings.get(settings_key, {})
                            config['sni'] = security_settings.get('serverName', '')
                            config['fp'] = security_settings.get('fingerprint', 'chrome')
                            
                            if config['security'] == 'reality':
                                config['pbk'] = security_settings.get('publicKey', '')
                                config['sid'] = security_settings.get('shortId', '')
                    
                    return config
                
                elif protocol == 'trojan':
                    servers = settings.get('servers', [])
                    if not servers:
                        continue
                    
                    server = servers[0]
                    config = {
                        'protocol': 'trojan',
                        'server': server.get('address'),
                        'port': int(server.get('port', 0)),
                        'password': server.get('password'),
                        'name': data.get('remarks', 'Trojan Config')
                    }
                    
                    if stream_settings:
                        config['type'] = stream_settings.get('network', 'tcp')
                        config['security'] = stream_settings.get('security', 'tls')
                        
                        if config['security'] == 'tls':
                            tls_settings = stream_settings.get('tlsSettings', {})
                            config['sni'] = tls_settings.get('serverName', '')
                    
                    return config
            
            return None
        except:
            return None
    
    @staticmethod
    def extract_configs(text: str, protocols: list) -> List[Dict]:
        configs = []
        
        patterns = {
            'vless': r'vless://[^\s\)\]<>"]+',
            'vmess': r'vmess://[^\s\)\]<>"]+',
            'ss': r'ss://[A-Za-z0-9+/=]+(?:#[^\s\)\]<>"]*)?',
            'shadowsocks': r'shadowsocks://[^\s\)\]<>"]+',
            'trojan': r'trojan://[^\s\)\]<>"]+'
        }
        
        for protocol in protocols:
            if protocol in patterns:
                matches = re.findall(patterns[protocol], text, re.IGNORECASE)
                
                for match in matches:
                    match = match.rstrip('.,;:!?')
                    
                    parsed = None
                    if protocol == 'vless':
                        parsed = ConfigParser.parse_vless(match)
                    elif protocol == 'vmess':
                        parsed = ConfigParser.parse_vmess(match)
                    elif protocol in ['ss', 'shadowsocks']:
                        parsed = ConfigParser.parse_shadowsocks(match)
                    elif protocol == 'trojan':
                        parsed = ConfigParser.parse_trojan(match)
                    
                    if parsed and parsed.get('server') and parsed.get('port'):
                        configs.append(parsed)
        
        json_pattern = r'\{[^{}]*"outbounds"[^{}]*\[[^\]]+\][^{}]*\}'
        json_matches = re.findall(json_pattern, text, re.DOTALL)
        
        for json_match in json_matches:
            try:
                brace_count = 0
                end_pos = 0
                for i, char in enumerate(json_match):
                    if char == '{':
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            end_pos = i + 1
                            break
                
                if end_pos > 0:
                    full_json = json_match[:end_pos]
                    parsed = ConfigParser.parse_json_config(full_json)
                    if parsed and parsed.get('server') and parsed.get('port'):
                        configs.append(parsed)
            except:
                continue
        
        return configs
    
    @staticmethod
    def deduplicate(configs: list) -> list:
        seen = set()
        unique = []
        
        for config in configs:
            key = f"{config['server']}:{config['port']}"
            if key not in seen:
                seen.add(key)
                unique.append(config)
        
        return unique

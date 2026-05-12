import base64
import json

def generate_subscription(configs: list, name_suffix: str = "") -> str:
    links = []
    
    if len(configs) == 0:
        placeholder = "vless://00000000-0000-0000-0000-000000000000@127.0.0.1:443?encryption=none&security=none&type=tcp#%E2%9D%8C%20%DA%A9%D8%A7%D9%86%D9%81%DB%8C%DA%AF%DB%8C%20%D9%BE%DB%8C%D8%AF%D8%A7%20%D9%86%D8%B4%D8%AF%20-%20%D8%A8%D8%B9%D8%AF%D8%A7%20%D8%A8%D8%B1%D9%88%D8%B2%D8%B1%D8%B3%D8%A7%D9%86%DB%8C%20%DA%A9%D9%86%DB%8C%D8%AF"
        links.append(placeholder)
    else:
        for config_data in configs:
            config = config_data['config']
            
            speed_info = f" | {config_data.get('speed_mbps', 0)}Mbps" if config_data.get('speed_mbps') else ""
            
            if config['protocol'] == 'vless':
                link = f"vless://{config['uuid']}@{config['server']}:{config['port']}"
                params = []
                
                if config.get('encryption'):
                    params.append(f"encryption={config['encryption']}")
                if config.get('security'):
                    params.append(f"security={config['security']}")
                if config.get('type'):
                    params.append(f"type={config['type']}")
                if config.get('sni'):
                    params.append(f"sni={config['sni']}")
                if config.get('fp'):
                    params.append(f"fp={config['fp']}")
                
                if params:
                    link += '?' + '&'.join(params)
                
                name = f"{config['name']}{speed_info}{name_suffix}"
                link += f"#{name}"
                
            elif config['protocol'] in ['shadowsocks', 'ss']:
                userinfo = f"{config['method']}:{config['password']}"
                encoded = base64.b64encode(userinfo.encode()).decode()
                link = f"ss://{encoded}@{config['server']}:{config['port']}"
                name = f"{config['name']}{speed_info}{name_suffix}"
                link += f"#{name}"
            
            elif config['protocol'] == 'trojan':
                link = f"trojan://{config['password']}@{config['server']}:{config['port']}"
                params = []
                
                if config.get('security'):
                    params.append(f"security={config['security']}")
                if config.get('type'):
                    params.append(f"type={config['type']}")
                if config.get('sni'):
                    params.append(f"sni={config['sni']}")
                if config.get('fp'):
                    params.append(f"fp={config['fp']}")
                
                if params:
                    link += '?' + '&'.join(params)
                
                name = f"{config['name']}{speed_info}{name_suffix}"
                link += f"#{name}"
            
            links.append(link)
    
    all_links = '\n'.join(links)
    encoded = base64.b64encode(all_links.encode()).decode()
    
    return encoded

def create_html_page(alive_count: int, working_count: int, last_update: str) -> str:
    raw_link_all = "https://raw.githubusercontent.com/balochscript/free-vpn-configs/gh-pages/subscription-all.txt"
    raw_link_volume = "https://raw.githubusercontent.com/balochscript/free-vpn-configs/gh-pages/subscription.txt"
    
    html = f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>کانفیگ‌های رایگان</title>
    <style>
        * {{ font-family: Tahoma, Arial, sans-serif; margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            min-height: 100vh;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        }}
        h1 {{ text-align: center; font-size: 2.5em; margin-bottom: 10px; }}
        .stats {{
            text-align: center;
            font-size: 1.2em;
            margin: 20px 0;
            padding: 15px;
            background: rgba(255,255,255,0.2);
            border-radius: 10px;
        }}
        .link-section {{
            margin: 30px 0;
            padding: 20px;
            background: rgba(255,255,255,0.15);
            border-radius: 10px;
        }}
        .link-box {{
            background: rgba(0,0,0,0.3);
            padding: 15px;
            border-radius: 10px;
            margin: 15px 0;
            word-break: break-all;
            font-family: monospace;
            font-size: 0.9em;
            direction: ltr;
            text-align: left;
        }}
        .copy-btn {{
            background: #4CAF50;
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            margin: 10px 5px;
            transition: all 0.3s;
        }}
        .copy-btn:hover {{ background: #45a049; transform: scale(1.05); }}
        .badge {{
            display: inline-block;
            background: #ff6b6b;
            padding: 5px 15px;
            border-radius: 15px;
            font-size: 0.9em;
            margin: 5px;
        }}
        .success {{ background: #51cf66; }}
        .info {{ background: #339af0; }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            opacity: 0.8;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 کانفیگ‌های رایگان</h1>
        
        <div class="stats">
            <div>✅ کانفیگ‌های سالم: <strong>{alive_count}</strong></div>
            <div>📦 با حجم واقعی: <strong>{working_count}</strong></div>
            <div>🔄 آخرین بروزرسانی: <strong>{last_update}</strong></div>
            <div style="margin-top: 10px;">
                <span class="badge success">✅ تست شده</span>
                <span class="badge info">🔄 هر ۵ ساعت</span>
            </div>
        </div>
        
        <div class="link-section">
            <h2>📱 لینک ۱: همه کانفیگ‌های سالم (Alive)</h2>
            <p style="margin: 10px 0; font-size: 0.95em;">
                <span class="badge info">ℹ️ {alive_count} کانفیگ - بدون تست حجم</span>
            </p>
            <div class="link-box" id="linkall">{raw_link_all}</div>
            <button class="copy-btn" onclick="copy('linkall')">📋 کپی لینک</button>
        </div>
        
        <div class="link-section">
            <h2>📦 لینک ۲: فقط با حجم واقعی (توصیه می‌شود)</h2>
            <p style="margin: 10px 0; font-size: 0.95em;">
                <span class="badge success">✅ {working_count} کانفیگ - با حجم تست‌شده</span>
            </p>
            <div class="link-box" id="linkvolume">{raw_link_volume}</div>
            <button class="copy-btn" onclick="copy('linkvolume')">📋 کپی لینک</button>
        </div>
        
        <div class="footer">
            <p>⭐ اگر مفید بود، یک استار بدید!</p>
            <p><a href="https://github.com/balochscript/free-vpn-configs" style="color: white;">GitHub</a></p>
            <p style="margin-top: 10px; opacity: 0.7;">Made with ❤️ for free internet</p>
        </div>
    </div>
    
    <script>
        function copy(id) {{
            const text = document.getElementById(id).textContent.trim();
            navigator.clipboard.writeText(text).then(() => {{
                alert('✅ کپی شد!');
            }});
        }}
    </script>
</body>
</html>"""
    return html

if __name__ == '__main__':
    import os
    from datetime import datetime
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    alive_path = os.path.join(current_dir, '..', 'alive_configs.json')
    working_path = os.path.join(current_dir, '..', 'working_configs.json')
    
    try:
        with open(alive_path) as f:
            alive_configs = json.load(f)
    except:
        alive_configs = []
    
    try:
        with open(working_path) as f:
            working_configs = json.load(f)
    except:
        working_configs = []
    
    sub_all = generate_subscription(alive_configs)
    sub_volume = generate_subscription(working_configs)
    
    with open('subscription-all.txt', 'w') as f:
        f.write(sub_all)
    
    with open('subscription.txt', 'w') as f:
        f.write(sub_volume)
    
    print(f"✅ Generated subscription-all.txt with {len(alive_configs)} configs")
    print(f"✅ Generated subscription.txt with {len(working_configs)} configs")
    
    html = create_html_page(
        len(alive_configs),
        len(working_configs),
        datetime.now().strftime('%Y-%m-%d %H:%M UTC')
    )
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("✅ Generated index.html")

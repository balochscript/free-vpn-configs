import base64
import json

def generate_subscription(configs: list) -> str:
    links = []
    
    if len(configs) == 0:
        placeholder = "vless://00000000-0000-0000-0000-000000000000@127.0.0.1:443?encryption=none&security=none&type=tcp#%E2%9D%8C%20%DA%A9%D8%A7%D9%86%D9%81%DB%8C%DA%AF%20%D8%B3%D8%A7%D9%84%D9%85%DB%8C%20%DB%8C%D8%A7%D9%81%D8%AA%20%D9%86%D8%B4%D8%AF%20-%20%D9%84%D8%B7%D9%81%D8%A7%20%D8%A8%D8%B9%D8%AF%D8%A7%20%D8%A8%D8%B1%D9%88%D8%B2%D8%B1%D8%B3%D8%A7%D9%86%DB%8C%20%DA%A9%D9%86%DB%8C%D8%AF"
        links.append(placeholder)
    else:
        for config_data in configs:
            config = config_data['config']
            
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
                
                name = f"{config['name']} | {config_data['speed_mbps']}Mbps"
                link += f"#{name}"
                
            elif config['protocol'] in ['shadowsocks', 'ss']:
                userinfo = f"{config['method']}:{config['password']}"
                encoded = base64.b64encode(userinfo.encode()).decode()
                link = f"ss://{encoded}@{config['server']}:{config['port']}"
                link += f"#{config['name']} | {config_data['speed_mbps']}Mbps"
            
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
                
                name = f"{config['name']} | {config_data['speed_mbps']}Mbps"
                link += f"#{name}"
            
            links.append(link)
    
    all_links = '\n'.join(links)
    encoded = base64.b64encode(all_links.encode()).decode()
    
    return encoded

def create_html_page(config_count: int, last_update: str) -> str:
    raw_link = "https://raw.githubusercontent.com/balochscript/free-vpn-configs/gh-pages/subscription.txt"
    pages_link = "https://balochscript.github.io/free-vpn-configs/subscription.txt"
    
    html = f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>کانفیگ‌های رایگان با حجم</title>
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
        .copy-btn:active {{ transform: scale(0.95); }}
        .guide {{
            background: rgba(255,255,255,0.15);
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }}
        .guide h3 {{ margin-bottom: 15px; }}
        .guide ol, .guide ul {{ padding-right: 20px; }}
        .guide li {{ margin: 10px 0; line-height: 1.6; }}
        .badge {{
            display: inline-block;
            background: #ff6b6b;
            padding: 5px 15px;
            border-radius: 15px;
            font-size: 0.9em;
            margin: 5px;
        }}
        .success {{ background: #51cf66; }}
        .warning {{ background: #ffd43b; color: #333; }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            opacity: 0.8;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 کانفیگ‌های رایگان با حجم</h1>
        
        <div class="stats">
            <div>📊 تعداد کانفیگ: <strong>{config_count}</strong></div>
            <div>🔄 آخرین بروزرسانی: <strong>{last_update}</strong></div>
            <div style="margin-top: 10px;">
                <span class="badge success">✅ تست شده</span>
                <span class="badge success">✅ با حجم</span>
                <span class="badge">🔄 هر ۵ ساعت</span>
            </div>
        </div>
        
        <div class="link-section">
            <h2>📱 لینک اشتراک (برای ایران)</h2>
            <p style="margin: 10px 0;">این لینک در ایران فیلتر نیست:</p>
            <div class="link-box" id="rawlink">{raw_link}</div>
            <button class="copy-btn" onclick="copyRaw()">📋 کپی لینک Raw</button>
            
            <h3 style="margin-top: 25px;">📱 لینک جایگزین (GitHub Pages)</h3>
            <p style="margin: 10px 0; font-size: 0.9em;">
                <span class="badge warning">⚠️ ممکن است فیلتر باشد</span>
            </p>
            <div class="link-box" id="pageslink">{pages_link}</div>
            <button class="copy-btn" onclick="copyPages()">📋 کپی لینک Pages</button>
        </div>
        
        <div class="guide">
            <h3>🔧 راهنمای استفاده ترکیبی (V2rayNG + Psiphon)</h3>
            <ol>
                <li><strong>تنظیم V2rayNG:</strong>
                    <ul>
                        <li>منو → تنظیمات</li>
                        <li>Local proxy port: <code>10808</code></li>
                        <li>Mode: <code>Proxy only</code></li>
                    </ul>
                </li>
                <li><strong>اضافه کردن ساب‌لینک:</strong>
                    <ul>
                        <li>دکمه ➕ → اضافه کردن اشتراک</li>
                        <li>لینک Raw بالا را وارد کنید</li>
                        <li>بروزرسانی → انتخاب کانفیگ → اتصال</li>
                    </ul>
                </li>
                <li><strong>تنظیم Psiphon:</strong>
                    <ul>
                        <li>Options → VPN Settings</li>
                        <li>Only tunnel selected apps ✓</li>
                        <li>Select apps → تلگرام ✓ (V2rayNG ✗)</li>
                        <li>Proxy Settings → HTTP Proxy ✓</li>
                        <li>Host: <code>127.0.0.1</code>, Port: <code>10808</code></li>
                        <li>Start Psiphon</li>
                    </ul>
                </li>
            </ol>
        </div>
        
        <div class="guide">
            <h3>⚡ نکات مهم</h3>
            <ul>
                <li>✅ لینک Raw در ایران فیلتر نیست</li>
                <li>✅ همه کانفیگ‌ها دارای حجم تست‌شده هستند</li>
                <li>✅ هر ۵ ساعت بروزرسانی خودکار</li>
                <li>⚠️ اگر "کانفیگ یافت نشد" دیدید، بعداً بروزرسانی کنید</li>
            </ul>
        </div>
        
        <div class="footer">
            <p>⭐ اگر مفید بود، یک استار بدید!</p>
            <p><a href="https://github.com/balochscript/free-vpn-configs" style="color: white;">GitHub Repository</a></p>
            <p style="margin-top: 15px; opacity: 0.7;">Made with ❤️ for free internet</p>
        </div>
    </div>
    
    <script>
        function copyRaw() {{
            const link = document.getElementById('rawlink').textContent.trim();
            navigator.clipboard.writeText(link).then(() => {{
                alert('✅ لینک Raw کپی شد!');
            }});
        }}
        
        function copyPages() {{
            const link = document.getElementById('pageslink').textContent.trim();
            navigator.clipboard.writeText(link).then(() => {{
                alert('✅ لینک Pages کپی شد!');
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
    working_path = os.path.join(current_dir, '..', 'working_configs.json')
    
    try:
        with open(working_path) as f:
            configs = json.load(f)
    except:
        configs = []
    
    subscription = generate_subscription(configs)
    
    with open('subscription.txt', 'w') as f:
        f.write(subscription)
    
    print(f"✅ Generated subscription with {len(configs)} configs")
    
    html = create_html_page(
        len(configs),
        datetime.now().strftime('%Y-%m-%d %H:%M UTC')
    )
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("✅ Generated index.html")

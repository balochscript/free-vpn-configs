"""
ابزارهای کمکی
"""

import base64
import json

def generate_subscription(configs: list) -> str:
    """تولید ساب‌لینک استاندارد V2ray"""
    links = []
    
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
            
            # اضافه کردن نام + سرعت
            name = f"{config['name']} | {config_data['speed_mbps']}Mbps"
            link += f"#{name}"
            
        elif config['protocol'] in ['shadowsocks', 'ss']:
            # method:password@server:port
            userinfo = f"{config['method']}:{config['password']}"
            encoded = base64.b64encode(userinfo.encode()).decode()
            link = f"ss://{encoded}@{config['server']}:{config['port']}"
            link += f"#{config['name']} | {config_data['speed_mbps']}Mbps"
        
        links.append(link)
    
    # تبدیل به Base64
    all_links = '\n'.join(links)
    encoded = base64.b64encode(all_links.encode()).decode()
    
    return encoded

def create_html_page(config_count: int, last_update: str) -> str:
    """ساخت صفحه HTML"""
    html = f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>کانفیگ‌های رایگان با حجم</title>
    <style>
        * {{ font-family: Tahoma, Arial; }}
        body {{ 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            max-width: 800px;
            margin: 0 auto;
        }}
        .container {{
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
        .link-box {{
            background: rgba(0,0,0,0.3);
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
            word-break: break-all;
            font-family: monospace;
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
        .guide {{
            background: rgba(255,255,255,0.15);
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }}
        .guide ol {{ padding-right: 20px; }}
        .guide li {{ margin: 10px 0; line-height: 1.6; }}
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
        </div>
        
        <h2>📱 لینک اشتراک (Subscription Link)</h2>
        <div class="link-box" id="sublink">
            https://YOUR_USERNAME.github.io/YOUR_REPO/subscription.txt
        </div>
        <button class="copy-btn" onclick="copyLink()">📋 کپی لینک</button>
        
        <div class="guide">
            <h3>🔧 راهنمای استفاده ترکیبی با Psiphon</h3>
            <ol>
                <li><strong>Psiphon</strong> را نصب و اجرا کنید</li>
                <li>منتظر بمانید تا Psiphon وصل شود</li>
                <li>در <strong>V2rayNG</strong> یا <strong>Nekobox</strong>:</li>
                <ul>
                    <li>گزینه "اضافه کردن اشتراک" را انتخاب کنید</li>
                    <li>لینک بالا را وارد کنید</li>
                    <li>به تنظیمات → Routing بروید</li>
                    <li>فعال کنید: "Route all traffic through proxy"</li>
                </ul>
                <li>یک کانفیگ را انتخاب کنید و متصل شوید</li>
                <li>از حجم رایگان لذت ببرید! 🎉</li>
            </ol>
        </div>
        
        <div class="guide">
            <h3>⚡ نکات مهم</h3>
            <ul>
                <li>همه کانفیگ‌ها دارای حجم تست‌شده هستند</li>
                <li>برای بهترین نتیجه، از حالت ترکیبی استفاده کنید</li>
                <li>هر ۴ ساعت یکبار بروزرسانی می‌شود</li>
                <li>اگر کانفیگی کار نکرد، کانفیگ دیگری امتحان کنید</li>
            </ul>
        </div>
        
        <div class="footer">
            <p>⭐ اگر مفید بود، استار دادن فراموش نشه!</p>
            <p>Made with ❤️ for free internet</p>
        </div>
    </div>
    
    <script>
        function copyLink() {{
            const link = document.getElementById('sublink').textContent.trim();
            navigator.clipboard.writeText(link).then(() => {{
                alert('✅ لینک کپی شد!');
            }});
        }}
    </script>
</body>
</html>"""
    return html

if __name__ == '__main__':
    # ساخت فایل‌های نهایی
    with open('working_configs.json') as f:
        configs = json.load(f)
    
    # تولید ساب‌لینک
    subscription = generate_subscription(configs)
    
    with open('subscription.txt', 'w') as f:
        f.write(subscription)
    
    print(f"✅ Generated subscription with {len(configs)} configs")
    
    # ساخت صفحه HTML
    from datetime import datetime
    html = create_html_page(
        len(configs),
        datetime.now().strftime('%Y-%m-%d %H:%M')
    )
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("✅ Generated index.html")

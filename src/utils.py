import base64
import json
import os
from datetime import datetime
from typing import List, Dict

def generate_subscription(configs: list, sub_type: str = "alive") -> str:
    """
    ساخت subscription link
    sub_type: alive, volume, iran, recent
    """
    links = []
    
    if len(configs) == 0:
        # پیغام خطا به صورت کانفیگ
        placeholder = (
            "vless://00000000-0000-0000-0000-000000000000@127.0.0.1:443"
            "?encryption=none&security=none&type=tcp"
            "#%E2%9D%8C%20No%20Configs%20-%20Try%20Later"
        )
        links.append(placeholder)
    else:
        for idx, config_data in enumerate(configs, 1):
            # اگر فقط config است (نه نتیجه تست)
            if 'config' in config_data:
                config = config_data['config']
                speed = config_data.get('speed_kbps', 0)
                latency = config_data.get('latency_ms', 0)
            else:
                config = config_data
                speed = 0
                latency = 0
            
            # اضافه کردن اطلاعات به نام
            name_parts = [config['name']]
            
            if speed > 0:
                name_parts.append(f"{speed}KB/s")
            elif latency > 0:
                name_parts.append(f"{latency}ms")
            
            # نوع subscription
            type_tags = {
                'alive': '🟢',
                'volume': '📦',
                'iran': '🇮🇷',
                'recent': '🆕'
            }
            name_parts.append(type_tags.get(sub_type, ''))
            
            final_name = ' | '.join(name_parts)
            
            # ساخت لینک بر اساس پروتکل
            if config['protocol'] == 'vless':
                link = f"vless://{config['uuid']}@{config['server']}:{config['port']}"
                params = []
                
                for key in ['encryption', 'security', 'type', 'sni', 'fp']:
                    if config.get(key):
                        params.append(f"{key}={config[key]}")
                
                if params:
                    link += '?' + '&'.join(params)
                
                link += f"#{final_name}"
                
            elif config['protocol'] in ['shadowsocks', 'ss']:
                # ✅ اصلاح شده - encoding درست
                userinfo = f"{config['method']}:{config['password']}"
                userinfo_b64 = base64.b64encode(userinfo.encode()).decode()
                link = f"ss://{userinfo_b64}@{config['server']}:{config['port']}#{final_name}"
            
            elif config['protocol'] == 'trojan':
                link = f"trojan://{config['password']}@{config['server']}:{config['port']}"
                params = []
                
                for key in ['security', 'type', 'sni', 'fp']:
                    if config.get(key):
                        params.append(f"{key}={config[key]}")
                
                if params:
                    link += '?' + '&'.join(params)
                
                link += f"#{final_name}"
            
            else:
                continue
            
            links.append(link)
    
    # تبدیل به base64
    all_links = '\n'.join(links)
    encoded = base64.b64encode(all_links.encode()).decode()
    
    return encoded


def create_html_page(stats: Dict[str, int], last_update: str) -> str:
    """ساخت صفحه HTML"""
    
    base_url = "https://raw.githubusercontent.com/balochscript/free-vpn-configs/gh-pages"
    
    html = f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 کانفیگ‌های رایگان VPN</title>
    <style>
        * {{ 
            font-family: 'Segoe UI', Tahoma, Arial, sans-serif; 
            margin: 0; 
            padding: 0; 
            box-sizing: border-box; 
        }}
        
        body {{ 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(15px);
            border-radius: 25px;
            padding: 40px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        }}
        
        h1 {{ 
            text-align: center; 
            font-size: 2.8em; 
            margin-bottom: 15px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .subtitle {{
            text-align: center;
            font-size: 1.2em;
            opacity: 0.9;
            margin-bottom: 30px;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 30px 0;
        }}
        
        .stat-card {{
            background: rgba(255,255,255,0.2);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
        }}
        
        .stat-number {{
            font-size: 2.5em;
            font-weight: bold;
            display: block;
        }}
        
        .stat-label {{
            font-size: 0.9em;
            opacity: 0.9;
            margin-top: 5px;
        }}
        
        .link-section {{
            margin: 25px 0;
            padding: 25px;
            background: rgba(255,255,255,0.15);
            border-radius: 15px;
            border-left: 5px solid;
        }}
        
        .link-section.alive {{ border-color: #51cf66; }}
        .link-section.volume {{ border-color: #339af0; }}
        .link-section.iran {{ border-color: #ffd43b; }}
        .link-section.recent {{ border-color: #ff6b6b; }}
        
        .link-section h2 {{
            font-size: 1.5em;
            margin-bottom: 10px;
        }}
        
        .link-section p {{
            margin: 10px 0;
            opacity: 0.95;
        }}
        
        .link-box {{
            background: rgba(0,0,0,0.4);
            padding: 15px;
            border-radius: 10px;
            margin: 15px 0;
            word-break: break-all;
            font-family: 'Courier New', monospace;
            font-size: 0.85em;
            direction: ltr;
            text-align: left;
            max-height: 100px;
            overflow-y: auto;
        }}
        
        .copy-btn {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            margin: 10px 5px;
            transition: all 0.3s;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }}
        
        .copy-btn:hover {{ 
            transform: scale(1.05);
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        }}
        
        .badge {{
            display: inline-block;
            padding: 5px 15px;
            border-radius: 15px;
            font-size: 0.85em;
            margin: 5px;
            font-weight: bold;
        }}
        
        .badge.alive {{ background: #51cf66; }}
        .badge.volume {{ background: #339af0; }}
        .badge.iran {{ background: #ffd43b; color: #333; }}
        .badge.recent {{ background: #ff6b6b; }}
        
        .update-time {{
            text-align: center;
            margin: 30px 0;
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid rgba(255,255,255,0.2);
        }}
        
        .footer a {{
            color: white;
            text-decoration: none;
            margin: 0 10px;
            transition: opacity 0.3s;
        }}
        
        .footer a:hover {{ opacity: 0.7; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 کانفیگ‌های رایگان VPN</h1>
        <p class="subtitle">بروزرسانی خودکار هر 5 ساعت</p>
        
        <div class="stats">
            <div class="stat-card">
                <span class="stat-number">{stats.get('alive', 0)}</span>
                <span class="stat-label">🟢 فقط زنده</span>
            </div>
            <div class="stat-card">
                <span class="stat-number">{stats.get('volume', 0)}</span>
                <span class="stat-label">📦 با حجم</span>
            </div>
            <div class="stat-card">
                <span class="stat-number">{stats.get('iran', 0)}</span>
                <span class="stat-label">🇮🇷 ایران</span>
            </div>
            <div class="stat-card">
                <span class="stat-number">{stats.get('recent', 75)}</span>
                <span class="stat-label">🆕 اخیر</span>
            </div>
        </div>
        
        <div class="update-time">
            🕐 آخرین بروزرسانی: <strong>{last_update}</strong>
        </div>
        
        <!-- Alive -->
        <div class="link-section alive">
            <h2>🟢 لینک 1: فقط زنده بودن (Alive Only)</h2>
            <p>
                <span class="badge alive">✅ {stats.get('alive', 0)} کانفیگ</span>
                <span class="badge alive">⏱️ Timeout: 30s</span>
            </p>
            <p>تست شده فقط برای زنده بودن - سریع‌ترین گزینه</p>
            <div class="link-box" id="link-alive">{base_url}/subscription-alive.txt</div>
            <button class="copy-btn" onclick="copy('link-alive')">📋 کپی لینک</button>
        </div>
        
        <!-- Volume -->
        <div class="link-section volume">
            <h2>📦 لینک 2: با حجم واقعی (Volume Test)</h2>
            <p>
                <span class="badge volume">✅ {stats.get('volume', 0)} کانفیگ</span>
                <span class="badge volume">📥 Test: 100KB</span>
            </p>
            <p>تست شده برای دانلود واقعی - با کیفیت بالا</p>
            <div class="link-box" id="link-volume">{base_url}/subscription-volume.txt</div>
            <button class="copy-btn" onclick="copy('link-volume')">📋 کپی لینک</button>
        </div>
        
        <!-- Iran -->
        <div class="link-section iran">
            <h2>🇮🇷 لینک 3: بهینه برای ایران (Iran Optimized)</h2>
            <p>
                <span class="badge iran">✅ {stats.get('iran', 0)} کانفیگ</span>
                <span class="badge iran">🌐 DNS: برتینا</span>
            </p>
            <p>تست شده با DNS برتینا - بهترین گزینه برای کاربران ایرانی</p>
            <div class="link-box" id="link-iran">{base_url}/subscription-iran.txt</div>
            <button class="copy-btn" onclick="copy('link-iran')">📋 کپی لینک</button>
        </div>
        
        <!-- Recent -->
        <div class="link-section recent">
            <h2>🆕 لینک 4: آخرین کانفیگ‌ها (Recent 75)</h2>
            <p>
                <span class="badge recent">📋 75 کانفیگ</span>
                <span class="badge recent">⚡ بدون تست</span>
            </p>
            <p>75 کانفیگ اخیر بدون هیچ فیلتری - ممکن است برخی کار نکنند</p>
            <div class="link-box" id="link-recent">{base_url}/subscription-recent.txt</div>
            <button class="copy-btn" onclick="copy('link-recent')">📋 کپی لینک</button>
        </div>
        
        <div class="footer">
            <p>⭐ اگر مفید بود، یک استار بدید!</p>
            <p>
                <a href="https://github.com/balochscript/free-vpn-configs" target="_blank">📦 GitHub</a>
                <a href="https://github.com/balochscript/free-vpn-configs/issues" target="_blank">🐛 گزارش مشکل</a>
                <a href="https://www.bertina.ir/dns" target="_blank">🌐 DNS برتینا</a>
            </p>
            <p style="margin-top: 15px; opacity: 0.7; font-size: 0.9em;">
                Made with ❤️ for free internet | v2.0
            </p>
        </div>
    </div>
    
    <script>
        function copy(id) {{
            const text = document.getElementById(id).textContent.trim();
            navigator.clipboard.writeText(text).then(() => {{
                alert('✅ لینک کپی شد!\\n\\nحالا در اپلیکیشن V2rayNG:\\n1. دکمه + را بزنید\\n2. اضافه کردن اشتراک را انتخاب کنید\\n3. Ctrl+V کنید');
            }}).catch(() => {{
                prompt('لینک را کپی کنید:', text);
            }});
        }}
    </script>
</body>
</html>"""
    
    return html


def main():
    """ساخت فایل‌های subscription"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("╔" + "═" * 70 + "╗")
    print("║" + " " * 18 + "📦 Subscription Generator" + " " * 27 + "║")
    print("╚" + "═" * 70 + "╝\n")
    
    # مسیرها
    files = {
        'alive': os.path.join(current_dir, '..', 'tested_alive.json'),
        'volume': os.path.join(current_dir, '..', 'tested_volume.json'),
        'iran': os.path.join(current_dir, '..', 'tested_iran.json'),
        'recent': os.path.join(current_dir, '..', 'recent_configs.json')
    }
    
    stats = {}
    
    # ساخت subscriptions
    for sub_type, file_path in files.items():
        try:
            with open(file_path) as f:
                data = json.load(f)
            
            # فیلتر کردن
            if sub_type == 'recent':
                # فقط کانفیگ‌ها (بدون فیلتر)
                filtered = data
            elif sub_type == 'alive':
                # فقط alive
                filtered = [item for item in data if item.get('alive')]
            else:
                # alive + has_volume
                filtered = [item for item in data if item.get('alive') and item.get('has_volume')]
            
            stats[sub_type] = len(filtered)
            
            # ساخت subscription
            sub_content = generate_subscription(filtered, sub_type)
            
            # ذخیره
            output_file = f'subscription-{sub_type}.txt'
            with open(output_file, 'w') as f:
                f.write(sub_content)
            
            print(f"✅ {output_file}: {len(filtered)} configs")
            
        except FileNotFoundError:
            print(f"⚠️  {sub_type}: File not found, creating empty")
            stats[sub_type] = 0
            with open(f'subscription-{sub_type}.txt', 'w') as f:
                f.write(generate_subscription([], sub_type))
    
    # ساخت HTML
    html = create_html_page(stats, datetime.now().strftime('%Y-%m-%d %H:%M UTC'))
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("✅ index.html: Created")
    
    print("\n" + "╔" + "═" * 70 + "╗")
    print("║" + " " * 25 + "✅ Complete!" + " " * 34 + "║")
    print("╚" + "═" * 70 + "╝")


if __name__ == '__main__':
    main()

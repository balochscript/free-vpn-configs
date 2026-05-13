import base64
import json
import os
from datetime import datetime
from typing import List, Dict

def generate_subscription(configs: list, sub_type: str = "alive") -> str:
    links = []
    
    if len(configs) == 0:
        placeholder = (
            "vless://00000000-0000-0000-0000-000000000000@127.0.0.1:443"
            "?encryption=none&security=none&type=tcp"
            "#%E2%9D%8C%20No%20Configs%20-%20Try%20Later"
        )
        links.append(placeholder)
    else:
        for idx, config_data in enumerate(configs, 1):
            if 'config' in config_data:
                config = config_data['config']
                speed = config_data.get('speed_kbps', 0)
                latency = config_data.get('latency_ms', 0)
            else:
                config = config_data
                speed = 0
                latency = 0
            
            name_parts = [config['name']]
            
            if speed > 0:
                name_parts.append(f"{speed}KB/s")
            elif latency > 0:
                name_parts.append(f"{latency}ms")
            
            type_tags = {
                'tcping': '⚡',
                'alive': '🟢',
                'volume': '📦',
                'iran': '🇮🇷',
                'recent': '🆕'
            }
            name_parts.append(type_tags.get(sub_type, ''))
            
            final_name = ' | '.join(name_parts)
            
            if config['protocol'] == 'vless':
                link = f"vless://{config['uuid']}@{config['server']}:{config['port']}"
                params = []
                
                for key in ['encryption', 'security', 'type', 'sni', 'fp', 'pbk', 'sid']:
                    if config.get(key):
                        params.append(f"{key}={config[key]}")
                
                if params:
                    link += '?' + '&'.join(params)
                
                link += f"#{final_name}"
                
            elif config['protocol'] in ['shadowsocks', 'ss']:
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
            
            elif config['protocol'] == 'vmess':
                link = f"vmess://{config['uuid']}@{config['server']}:{config['port']}"
                params = []
                
                for key in ['encryption', 'security', 'type', 'sni', 'fp']:
                    if config.get(key):
                        params.append(f"{key}={config[key]}")
                
                if config.get('aid'):
                    params.append(f"aid={config['aid']}")
                
                if params:
                    link += '?' + '&'.join(params)
                
                link += f"#{final_name}"
            
            else:
                continue
            
            links.append(link)
    
    all_links = '\n'.join(links)
    encoded = base64.b64encode(all_links.encode()).decode()
    
    return encoded


def create_html_page(stats: Dict[str, int], last_update: str) -> str:
    
    base_url = "https://raw.githubusercontent.com/balochscript/free-vpn-configs/gh-pages"
    
    html = f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 کانفیگ‌های رایگان VPN - BalochScript</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;700;900&display=swap" rel="stylesheet">
    <style>
        * {{ 
            font-family: 'Vazirmatn', 'Segoe UI', Tahoma, sans-serif; 
            margin: 0; 
            padding: 0; 
            box-sizing: border-box; 
        }}
        
        body {{ 
            background: linear-gradient(135deg, #239B56 0%, #E74C3C 50%, #3498DB 100%);
            background-size: 400% 400%;
            animation: gradientMove 15s ease infinite;
            color: white;
            padding: 20px;
            min-height: 100vh;
        }}
        
        @keyframes gradientMove {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}
        
        .container {{
            max-width: 1100px;
            margin: 0 auto;
            background: rgba(255,255,255,0.12);
            backdrop-filter: blur(20px);
            border-radius: 30px;
            padding: 45px;
            box-shadow: 0 10px 40px 0 rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(255,255,255,0.18);
        }}
        
        .slogan {{
            text-align: center;
            font-size: 1.4em;
            font-weight: 700;
            margin-bottom: 25px;
            padding: 20px;
            background: linear-gradient(90deg, #239B56, #E74C3C, #3498DB);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: 0 0 30px rgba(255,255,255,0.5);
            animation: pulse 3s ease-in-out infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; transform: scale(1); }}
            50% {{ opacity: 0.9; transform: scale(1.02); }}
        }}
        
        h1 {{ 
            text-align: center; 
            font-size: 3em; 
            font-weight: 900;
            margin-bottom: 15px;
            text-shadow: 3px 3px 6px rgba(0,0,0,0.4);
            letter-spacing: 1px;
        }}
        
        .subtitle {{
            text-align: center;
            font-size: 1.3em;
            font-weight: 500;
            opacity: 0.95;
            margin-bottom: 35px;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 18px;
            margin: 35px 0;
        }}
        
        .stat-card {{
            background: rgba(255,255,255,0.25);
            padding: 25px;
            border-radius: 18px;
            text-align: center;
            transition: all 0.3s;
            border: 1px solid rgba(255,255,255,0.3);
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        }}
        
        .stat-number {{
            font-size: 2.8em;
            font-weight: 900;
            display: block;
        }}
        
        .stat-label {{
            font-size: 1em;
            font-weight: 500;
            opacity: 0.95;
            margin-top: 8px;
        }}
        
        .link-section {{
            margin: 28px 0;
            padding: 28px;
            background: rgba(255,255,255,0.18);
            border-radius: 18px;
            border-right: 6px solid;
            transition: all 0.3s;
        }}
        
        .link-section:hover {{
            background: rgba(255,255,255,0.25);
            transform: translateX(-5px);
        }}
        
        .link-section.tcping {{ border-color: #F1C40F; }}
        .link-section.alive {{ border-color: #2ECC71; }}
        .link-section.volume {{ border-color: #3498DB; }}
        .link-section.iran {{ border-color: #E74C3C; }}
        .link-section.recent {{ border-color: #9B59B6; }}
        
        .link-section h2 {{
            font-size: 1.7em;
            font-weight: 700;
            margin-bottom: 12px;
        }}
        
        .link-section p {{
            margin: 12px 0;
            opacity: 0.97;
            font-size: 1.05em;
            line-height: 1.6;
        }}
        
        .link-box {{
            background: rgba(0,0,0,0.5);
            padding: 18px;
            border-radius: 12px;
            margin: 18px 0;
            word-break: break-all;
            font-family: 'Courier New', 'Vazirmatn', monospace;
            font-size: 0.9em;
            direction: ltr;
            text-align: left;
            max-height: 110px;
            overflow-y: auto;
            border: 1px solid rgba(255,255,255,0.2);
        }}
        
        .link-box::-webkit-scrollbar {{
            width: 8px;
        }}
        
        .link-box::-webkit-scrollbar-track {{
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
        }}
        
        .link-box::-webkit-scrollbar-thumb {{
            background: rgba(255,255,255,0.4);
            border-radius: 10px;
        }}
        
        .copy-btn {{
            background: linear-gradient(135deg, #239B56 0%, #E74C3C 50%, #3498DB 100%);
            background-size: 200% 200%;
            color: white;
            border: none;
            padding: 14px 35px;
            border-radius: 30px;
            cursor: pointer;
            font-size: 17px;
            font-weight: 700;
            margin: 12px 6px;
            transition: all 0.4s;
            box-shadow: 0 5px 20px rgba(0,0,0,0.3);
        }}
        
        .copy-btn:hover {{ 
            transform: scale(1.08);
            box-shadow: 0 8px 30px rgba(0,0,0,0.4);
            background-position: 100% 0;
        }}
        
        .badge {{
            display: inline-block;
            padding: 7px 18px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 700;
            margin: 6px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.2);
        }}
        
        .badge.tcping {{ background: #F1C40F; color: #000; }}
        .badge.alive {{ background: #2ECC71; color: #fff; }}
        .badge.volume {{ background: #3498DB; color: #fff; }}
        .badge.iran {{ background: #E74C3C; color: #fff; }}
        .badge.recent {{ background: #9B59B6; color: #fff; }}
        
        .update-time {{
            text-align: center;
            margin: 35px 0;
            font-size: 1.2em;
            font-weight: 500;
            opacity: 0.95;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 45px;
            padding-top: 25px;
            border-top: 2px solid rgba(255,255,255,0.3);
        }}
        
        .footer a {{
            color: white;
            text-decoration: none;
            margin: 0 12px;
            font-weight: 500;
            transition: all 0.3s;
            font-size: 1.05em;
        }}
        
        .footer a:hover {{ 
            opacity: 0.7;
            transform: scale(1.1);
        }}
        
        .iran-flag {{
            font-size: 1.5em;
            margin: 0 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="slogan">
            🇮🇷 زنده باد جمهوری اسلامی ایران | زنده باد بلوچستان 🦁
        </div>
        
        <h1>🚀 کانفیگ‌های رایگان VPN</h1>
        <p class="subtitle">⚡ بروزرسانی خودکار هر 5 ساعت | ساخته شده با ❤️</p>
        
        <div class="stats">
            <div class="stat-card">
                <span class="stat-number">{stats.get('tcping', 0)}</span>
                <span class="stat-label">⚡ تست سریع</span>
            </div>
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
                <span class="stat-number">{stats.get('recent', 100)}</span>
                <span class="stat-label">🆕 اخیر</span>
            </div>
        </div>
        
        <div class="update-time">
            🕐 آخرین بروزرسانی: <strong>{last_update}</strong>
        </div>
        
        <div class="link-section tcping">
            <h2>⚡ لینک 1: تست سریع TCP (TCPing)</h2>
            <p>
                <span class="badge tcping">✅ {stats.get('tcping', 0)} کانفیگ</span>
                <span class="badge tcping">🚀 سریع‌ترین</span>
                <span class="badge tcping">⏱️ Timeout: 30s</span>
            </p>
            <p><strong>فقط اتصال TCP تست شده</strong> - برای فیلتر سریع کانفیگ‌ها</p>
            <div class="link-box" id="link-tcping">{base_url}/subscription-tcping.txt</div>
            <button class="copy-btn" onclick="copy('link-tcping')">📋 کپی لینک</button>
        </div>
        
        <div class="link-section alive">
            <h2>🟢 لینک 2: فقط زنده بودن (Alive Test)</h2>
            <p>
                <span class="badge alive">✅ {stats.get('alive', 0)} کانفیگ</span>
                <span class="badge alive">🌐 HTTP Test</span>
                <span class="badge alive">⏱️ Timeout: 45s</span>
            </p>
            <p><strong>تست شده با Google</strong> - اتصال HTTP کامل</p>
            <div class="link-box" id="link-alive">{base_url}/subscription-alive.txt</div>
            <button class="copy-btn" onclick="copy('link-alive')">📋 کپی لینک</button>
        </div>
        
        <div class="link-section volume">
            <h2>📦 لینک 3: با حجم واقعی (Volume Test)</h2>
            <p>
                <span class="badge volume">✅ {stats.get('volume', 0)} کانفیگ</span>
                <span class="badge volume">📥 Download: 50KB+</span>
                <span class="badge volume">🔗 GitHub</span>
            </p>
            <p><strong>تست شده با دانلود از GitHub</strong> - بالاترین کیفیت</p>
            <div class="link-box" id="link-volume">{base_url}/subscription-volume.txt</div>
            <button class="copy-btn" onclick="copy('link-volume')">📋 کپی لینک</button>
        </div>
        
        <div class="link-section iran">
            <h2>🇮🇷 لینک 4: بهینه برای ایران (Iran Optimized)</h2>
            <p>
                <span class="badge iran">✅ {stats.get('iran', 0)} کانفیگ</span>
                <span class="badge iran">🌐 DNS برتینا</span>
                <span class="badge iran">📥 Download: 80KB+</span>
            </p>
            <p><strong>تست شده با سرور ایران (Bertina)</strong> - پیشنهاد ویژه برای کاربران ایرانی</p>
            <div class="link-box" id="link-iran">{base_url}/subscription-iran.txt</div>
            <button class="copy-btn" onclick="copy('link-iran')">📋 کپی لینک</button>
        </div>
        
        <div class="link-section recent">
            <h2>🆕 لینک 5: آخرین کانفیگ‌ها (Recent 100)</h2>
            <p>
                <span class="badge recent">📋 100 کانفیگ</span>
                <span class="badge recent">⚡ بدون تست</span>
                <span class="badge recent">🔄 جدیدترین‌ها</span>
            </p>
            <p><strong>100 کانفیگ اخیر بدون فیلتر</strong> - ممکن است برخی کار نکنند</p>
            <div class="link-box" id="link-recent">{base_url}/subscription-recent.txt</div>
            <button class="copy-btn" onclick="copy('link-recent')">📋 کپی لینک</button>
        </div>
        
        <div class="footer">
            <p style="font-size: 1.2em; font-weight: 700; margin-bottom: 15px;">
                ⭐ اگر مفید بود، یک استار بدید!
            </p>
            <p>
                <a href="https://github.com/balochscript/free-vpn-configs" target="_blank">📦 GitHub Repository</a>
                <a href="https://github.com/balochscript/free-vpn-configs/issues" target="_blank">🐛 گزارش مشکل</a>
                <a href="https://www.bertina.ir/dns" target="_blank">🌐 DNS برتینا</a>
            </p>
            <p style="margin-top: 20px; opacity: 0.8; font-size: 1em; font-weight: 500;">
                Made with <span class="iran-flag">🇮🇷</span> for Free Internet | v3.0 | BalochScript
            </p>
        </div>
    </div>
    
    <script>
        function copy(id) {{
            const text = document.getElementById(id).textContent.trim();
            navigator.clipboard.writeText(text).then(() => {{
                alert('✅ لینک با موفقیت کپی شد!\\n\\n📱 مراحل افزودن در V2rayNG:\\n\\n1️⃣ دکمه + را بزنید\\n2️⃣ گزینه "اضافه کردن اشتراک" را انتخاب کنید\\n3️⃣ لینک را Paste کنید (Ctrl+V)\\n4️⃣ دکمه تایید را بزنید\\n\\n✨ موفق باشید!');
            }}).catch(() => {{
                const input = document.createElement('textarea');
                input.value = text;
                document.body.appendChild(input);
                input.select();
                document.execCommand('copy');
                document.body.removeChild(input);
                alert('✅ لینک کپی شد!\\n\\nلینک: ' + text);
            }});
        }}
    </script>
</body>
</html>"""
    
    return html


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("╔" + "═" * 70 + "╗")
    print("║" + " " * 18 + "📦 Subscription Generator" + " " * 27 + "║")
    print("╚" + "═" * 70 + "╝\n")
    
    files = {
        'tcping': os.path.join(current_dir, '..', 'tested_tcping.json'),
        'alive': os.path.join(current_dir, '..', 'tested_alive.json'),
        'volume': os.path.join(current_dir, '..', 'tested_volume.json'),
        'iran': os.path.join(current_dir, '..', 'tested_iran.json'),
        'recent': os.path.join(current_dir, '..', 'recent_configs.json')
    }
    
    stats = {}
    
    for sub_type, file_path in files.items():
        try:
            with open(file_path) as f:
                data = json.load(f)
            
            if sub_type == 'recent':
                filtered = data
            elif sub_type in ['tcping', 'alive']:
                filtered = [item for item in data if item.get('alive')]
            else:
                filtered = [item for item in data if item.get('alive') and item.get('has_volume')]
            
            stats[sub_type] = len(filtered)
            
            sub_content = generate_subscription(filtered, sub_type)
            
            output_file = f'subscription-{sub_type}.txt'
            with open(output_file, 'w') as f:
                f.write(sub_content)
            
            print(f"✅ {output_file}: {len(filtered)} configs")
            
        except FileNotFoundError:
            print(f"⚠️  {sub_type}: File not found, creating empty")
            stats[sub_type] = 0
            with open(f'subscription-{sub_type}.txt', 'w') as f:
                f.write(generate_subscription([], sub_type))
    
    html = create_html_page(stats, datetime.now().strftime('%Y-%m-%d %H:%M UTC'))
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("✅ index.html: Created")
    
    print("\n" + "╔" + "═" * 70 + "╗")
    print("║" + " " * 25 + "✅ Complete!" + " " * 34 + "║")
    print("╚" + "═" * 70 + "╝")


if __name__ == '__main__':
    main()

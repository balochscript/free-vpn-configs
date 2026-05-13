# 🚀 Free VPN Configs

**ساب‌لینک اتوماتیک کانفیگ‌های رایگان V2Ray با تست هوشمند**

[![Update Status](https://github.com/balochscript/free-vpn-configs/workflows/Update%20Free%20VPN%20Configs/badge.svg)](https://github.com/balochscript/free-vpn-configs/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<div align="center">

### 🇮🇷 زنده باد ایران اسلامی | زنده باد بلوچستان 🦁

</div>

---

## ✨ ویژگی‌ها

- ✅ **3 نوع ساب‌لینک** برای نیازهای مختلف
- ✅ **بروزرسانی خودکار** هر 5 ساعت یکبار
- ✅ **تست دقیق** با TCPing و Real Delay
- ✅ **بهینه شده برای ایران** با DNS برتینا
- ✅ **پروتکل‌ها:** VLESS, VMess, Shadowsocks, Trojan
- ✅ **کاملاً رایگان و متن‌باز**

---

## 📱 لینک‌های اشتراک

### ⚡ لینک 1: TCPing - سریع‌ترین

```
https://raw.githubusercontent.com/balochscript/free-vpn-configs/gh-pages/subscription-tcping.txt
```

- **مناسب برای:** فیلتر سریع کانفیگ‌ها
- **روش تست:** فقط اتصال TCP (10 ثانیه)
- **ویژگی:** سریع‌ترین روش، بدون Xray

---

### 🕐 لینک 2: Real Delay - بهترین کیفیت ⭐

```
https://raw.githubusercontent.com/balochscript/free-vpn-configs/gh-pages/subscription-realdelay.txt
```

- **مناسب برای:** استفاده روزمره، کیفیت بالا
- **روش تست:** HTTP واقعی با Google + DNS برتینا
- **ویژگی:** تاخیر دقیق (میلی‌ثانیه)، تست کامل
- **DNS برتینا:** `193.186.32.32`
- **💡 پیشنهاد می‌شود!**

---

### 🆕 لینک 3: Recent 100 - بدون فیلتر

```
https://raw.githubusercontent.com/balochscript/free-vpn-configs/gh-pages/subscription-recent.txt
```

- **مناسب برای:** آزمایش کانفیگ‌های جدید
- **روش تست:** بدون تست - مستقیم از کانال‌ها
- **تعداد ثابت:** 100 کانفیگ
- **⚠️ ممکن است برخی کار نکنند**

---

### 🌐 صفحه وب پروژه

```
https://balochscript.github.io/free-vpn-configs/
```

**امکانات:**
- آمار لحظه‌ای کانفیگ‌ها
- کپی آسان لینک‌ها
- رابط کاربری زیبا فارسی
- نمایش زمان بروزرسانی

---

## 🔧 راهنمای استفاده

### 📲 روش 1: نصب ساده در V2rayNG (Android)

**گام 1: نصب اپلیکیشن**
- V2rayNG را از [Google Play](https://play.google.com/store/apps/details?id=com.v2ray.ang) یا [GitHub](https://github.com/2dust/v2rayNG/releases) دانلود کنید

**گام 2: افزودن اشتراک**
1. اپ را باز کنید
2. دکمه `+` (بالا سمت راست) را بزنید
3. گزینه **"Subscribe"** را انتخاب کنید
4. در قسمت **Remarks** یک نام دلخواه بنویسید (مثلاً `Free VPN`)
5. در قسمت **URL** یکی از لینک‌های بالا را Paste کنید
6. روی ✅ بزنید

**گام 3: بروزرسانی و اتصال**
1. روی `⋮` کنار اشتراک بزنید
2. **"Update subscription"** را بزنید
3. یک کانفیگ با پینگ کم انتخاب کنید
4. دکمه پایین صفحه را بزنید تا متصل شوید

✅ **متصل شدید!**

---

### 🚀 روش 2: ترکیب V2rayNG + Psiphon (پیشنهاد ویژه)

**این روش حجم رایگان Psiphon را برای تلگرام و سایر برنامه‌ها فعال می‌کند**

**در اکثر نقاط با اینترنت ایرانسل و همراه اول تست شده و کار می‌کند.**

#### قسمت A: تنظیم V2rayNG

**1. تنظیمات Core:**
- وارد V2rayNG شوید
- منوی `☰` (سه خط) → **Settings**
- پیدا کردن **Core Settings**
- تنظیم پورت پروکسی:
```
Local proxy port: 10808
```

**2. تنظیمات Advanced:**
- در همان صفحه Settings
- قسمت **Advanced Settings**
- تغییر حالت از VPN به Proxy:
```
Mode: Proxy only
```
- دکمه **OK** را بزنید

**3. اتصال به کانفیگ:**
- به صفحه اصلی برگردید
- یک کانفیگ از اشتراک انتخاب کنید
- دکمه اتصال را بزنید (باید وصل شود)

---

#### قسمت B: تنظیم Psiphon

**1. دانلود Psiphon:**
- [Psiphon Pro](https://psiphon.ca/en/download.html) را نصب کنید

**2. تنظیمات VPN:**
- Psiphon → **Options**
- قسمت **VPN Settings**:
  - ✅ فعال کنید: `Only tunnel selected apps`
  - روی **Select apps** بزنید
  - از لیست **تلگرام** را تیک بزنید
  - برنامه‌های دیگر (اختیاری): اینستاگرام، واتساپ، ...
  - ⚠️ **V2rayNG را تیک نزنید!**

**3. تنظیمات Proxy:**
- یک قدم برگردید
- قسمت **Proxy Settings**:
  - ✅ فعال کنید: `Connect through an HTTP Proxy`
  - انتخاب کنید: `Use the following settings`
  - وارد کنید:
```
Host address: 127.0.0.1
Port: 10808
```

**4. اتصال نهایی:**
- روی دکمه **Start** بزنید
- چند دقیقه صبر کنید تا متصل شود
- ✅ تمام!

---

#### ✅ نتیجه نهایی

**مسیر اتصال:**
```
تلگرام → Psiphon (حجم رایگان) → V2rayNG → اینترنت
```

**مزایا:**
- 🎉 تلگرام و برنامه‌های انتخابی از حجم رایگان Psiphon استفاده می‌کنند
- ⚡ سایر برنامه‌ها از اینترنت عادی استفاده می‌کنند (بدون VPN)
- 💰 صرفه‌جویی در حجم اینترنت
- 🚀 سرعت بالا برای تلگرام

**⚠️ نکته:** این تنظیمات فقط یک‌بار لازم است. بعد از این:
1. V2rayNG را به کانفیگ وصل کنید
2. Psiphon را Start کنید
3. ✅ آماده!

---

### 🍎 روش 3: نصب در iOS

**V2Box (رایگان):**
1. از App Store نصب کنید
2. `+` → **Subscribe**
3. لینک را Paste کنید
4. Update → انتخاب کانفیگ → Connect

**Shadowrocket:**
1. از App Store خریداری کنید ($2.99)
2. `+` (بالا سمت راست)
3. **Type:** Subscribe
4. **URL:** لینک را Paste کنید
5. Done → اتصال

---

### 💻 روش 4: نصب در Windows

**V2rayN:**
1. [V2rayN](https://github.com/2dust/v2rayN/releases) را دانلود و نصب کنید
2. منوی **Subscription** → **Subscribe setting**
3. **Add** را بزنید
4. در **URL** لینک را Paste کنید
5. **OK** → **Update Subscription**
6. یک کانفیگ انتخاب کنید
7. دکمه **Enter** را بزنید

---

## 💡 سوالات متداول

### ❓ کدام لینک را استفاده کنم؟

**توصیه بر اساس نیاز:**

- **در ایران هستید؟** → 🕐 Real Delay (DNS برتینا)
- **سرعت مهم است؟** → ⚡ TCPing
- **گزینه بیشتر می‌خواهید؟** → 🆕 Recent 100
- **نمی‌دانم چی انتخاب کنم؟** → 🕐 Real Delay

### ❓ چرا برخی کار نمی‌کنند؟

**دلایل رایج:**
- سرور پر یا خاموش شده است
- IP سرور فیلتر شده
- محدودیت سرعت یا ترافیک
- مشکل اینترنت محلی

**راه‌حل:**
1. چند کانفیگ مختلف تست کنید
2. اشتراک را بروزرسانی کنید
3. از لینک دیگری استفاده کنید
4. چند ساعت بعد دوباره امتحان کنید

### ❓ تفاوت TCPing و Real Delay چیست؟

| ویژگی | TCPing ⚡ | Real Delay 🕐 |
|--------|----------|---------------|
| **سرعت تست** | خیلی سریع | متوسط |
| **دقت** | کم | بالا |
| **روش** | فقط TCP | HTTP واقعی |
| **تعداد** | بیشتر | کمتر اما بهتر |
| **توصیه** | فیلتر اولیه | استفاده روزانه |

### ❓ DNS برتینا چیست؟

**DNS رایگان ضد تحریم ایران:**
- IP: `193.186.32.32`
- دور زدن تحریم‌ها
- سرعت 3ms برای cache
- 100% پایداری
- رایگان برای همیشه
- وب‌سایت: [bertina.ir/dns](https://www.bertina.ir/dns)

**مزیت:** دسترسی به سایت‌های بین‌المللی بدون VPN (برای برخی سایت‌ها)

### ❓ چگونه سرعت را بهبود دهم؟

**نکات مهم:**

1. **انتخاب کانفیگ:**
   - کانفیگ‌هایی با latency کمتر (10-100ms)
   - از Real Delay استفاده کنید

2. **تنظیمات V2rayNG:**
   - Settings → Routing → Domain Strategy → `AsIs`
   - Settings → Core Settings → Enable Mux ✅

3. **استفاده از ترکیب:**
   - روش V2rayNG + Psiphon را امتحان کنید
   - برای تلگرام سرعت خوبی دارد

4. **بهینه‌سازی:**
   - در ساعات کم‌تردد استفاده کنید
   - چند کانفیگ تست کنید
   - از سرورهای نزدیک‌تر استفاده کنید

### ❓ هر چند وقت بروزرسانی می‌شود؟

**خودکار:**
- هر 5 ساعت یکبار
- توسط GitHub Actions
- زمان دقیق در سایت نمایش داده می‌شود

**دستی:**
- V2rayNG: `⋮` کنار اشتراک → Update subscription
- هر زمان که بخواهید

### ❓ آیا امن است؟

**⚠️ هشدار امنیتی:**

این کانفیگ‌ها **رایگان و عمومی** هستند، بنابراین:

**❌ استفاده نکنید برای:**
- بانک‌داری و تراکنش‌های مالی
- ورود به حساب‌های حساس (ایمیل، شبکه‌های اجتماعی اصلی)
- ارسال اطلاعات شخصی/محرمانه
- فعالیت‌های حساس

**✅ مناسب است برای:**
- مرور عمومی وب
- تماشای ویدیو
- دانلود فایل
- دسترسی به سایت‌های فیلتر شده
- شبکه‌های اجتماعی (بدون ورود به حساب‌های مهم)

**💡 توصیه:** برای امنیت بیشتر از VPN پولی استفاده کنید.

### ❓ "کانفیگ یافت نشد" می‌بینم!

**راه‌حل:**

1. **صبر کنید:** 2-3 ساعت صبر کنید (ممکن است در زمان تست باشد)
2. **بروزرسانی دستی:** اشتراک را دستی Update کنید
3. **Recent استفاده کنید:** از لینک Recent 100 استفاده کنید
4. **پاک و دوباره اضافه کنید:** اشتراک را حذف و دوباره اضافه کنید

### ❓ چرا پینگ برخی بالاست؟

**دلایل:**

- سرور دور است (مثلاً اروپا/آمریکا)
- سرور شلوغ است
- مسیر شبکه طولانی است
- محدودیت ISP

**راه‌حل:** کانفیگ دیگری با پینگ کمتر انتخاب کنید.

### ❓ می‌توانم در تلگرام استفاده کنم؟

**بله!** ولی:

**روش 1: مستقیم**
- Proxy تلگرام را روی System خالی بگذارید
- V2rayNG را اجرا کنید
- تلگرام از طریق VPN سیستم متصل می‌شود

**روش 2: ترکیبی (پیشنهاد)** ⭐
- از روش V2rayNG + Psiphon استفاده کنید
- حجم رایگان Psiphon برای تلگرام
- سرعت و پایداری بیشتر

**نکته:** برای صرفه‌جویی در حجم VPN، از MTProto Proxy اختصاصی تلگرام استفاده کنید.

### ❓ آیا در ایرانسل/همراه اول کار می‌کند؟

**بله!** به خصوص با روش ترکیبی:

- ✅ **ایرانسل:** کار می‌کند
- ✅ **همراه اول:** کار می‌کند
- ✅ **رایتل:** کار می‌کند
- ⚠️ **شاتل موبایل:** ممکن است محدودیت داشته باشد

**💡 توصیه:** روش V2rayNG + Psiphon را امتحان کنید.

---

## ⚠️ سلب مسئولیت

این پروژه **فقط برای اهداف آموزشی و دسترسی آزاد به اطلاعات** ایجاد شده است.

- استفاده از VPN در برخی کشورها **محدودیت قانونی** دارد
- کاربران **مسئول رعایت قوانین کشور خود** هستند
- کانفیگ‌ها از **منابع عمومی** جمع‌آوری شده‌اند
- **هیچ تضمینی** برای امنیت، حریم خصوصی یا سرعت وجود ندارد
- از این سرویس **مسئولانه** استفاده کنید
- سازندگان **هیچ مسئولیتی** در قبال نحوه استفاده ندارند

**استفاده از این پروژه به معنای پذیرش شرایط فوق است.**

---

## 🤝 مشارکت

### 🆕 افزودن کانال جدید

فایل `configs/channels.json` را ویرایش کنید:

```json
{
  "telegram_channels": [
    "mitivpn",
    "Configir98",
    "VIPV2rayNGNP",
    "saministamm",
    "zhw_x_club",
    "blackRay",
    "AzadInternet_TV",
    "proxymtprotoir",
    "AarazV2ray",
    "V2rayEnglish",
    "v2psiiphon",
    "KurdConfing",
    "Vpn_jet7",
    "Channel Id آیدی کانال را اینجا بگذارید"
  ],
  "supported_protocols": ["vless", "vmess", "ss", "shadowsocks", "trojan"],
  "test_settings": {
    "concurrent_tests": 12,
    "connection_timeout": 10,
    "volume_test_enabled": true,
    "min_volume_mb": 2,
    "max_messages_per_channel": 100
  }
}
```

**برای افزودن کانال:**
1. نام کانال را به لیست `telegram_channels` اضافه کنید
2. Pull Request بفرستید
3. بعد از بررسی، merge می‌شود

سپس Pull Request بفرستید.

### 🐛 گزارش مشکل

از [Issues](https://github.com/balochscript/free-vpn-configs/issues) استفاده کنید.

**قبل از گزارش:**
- بررسی کنید مشکل قبلاً گزارش نشده باشد
- اطلاعات کامل بدهید (سیستم‌عامل، نسخه اپ، لاگ)

### 💬 بحث و پیشنهاد

از [Discussions](https://github.com/balochscript/free-vpn-configs/discussions) استفاده کنید.

**موضوعات:**
- پیشنهاد ویژگی جدید
- سوال فنی
- بحث عمومی
- کمک به دیگران

---

## 📜 مجوز

**MIT License** - استفاده آزاد برای همه

متن کامل: [LICENSE](LICENSE)

```
استفاده تجاری ✅
تغییر و توزیع ✅
استفاده شخصی ✅
بدون تضمین ⚠️
```

---

## 📞 ارتباط و لینک‌های مفید

### 🔗 لینک‌های پروژه

- 📦 **مخزن GitHub:** [balochscript/free-vpn-configs](https://github.com/balochscript/free-vpn-configs)
- 🌐 **وب‌سایت:** [balochscript.github.io/free-vpn-configs](https://balochscript.github.io/free-vpn-configs)
- 🐛 **گزارش باگ:** [Issues](https://github.com/balochscript/free-vpn-configs/issues)
- 💬 **بحث و گفتگو:** [Discussions](https://github.com/balochscript/free-vpn-configs/discussions)

### 🌐 منابع مفید

- 🌍 **DNS برتینا:** [bertina.ir/dns](https://www.bertina.ir/dns)
- 📱 **V2rayNG:** [GitHub](https://github.com/2dust/v2rayNG)
- 💻 **V2rayN:** [GitHub](https://github.com/2dust/v2rayN)
- 📚 **Psiphon:** [psiphon.ca](https://psiphon.ca)
- 📖 **راهنمای V2Ray:** [v2ray.com](https://www.v2ray.com)

---

## ⭐ حمایت از پروژه

اگر این پروژه برایتان **مفید** بود:

1. ⭐ **یک Star بدهید** (بالای صفحه/حتما ستاره را بزنید)
2. 🔄 **با دوستان خود به اشتراک بگذارید و تنها خوری نکنید**
3. 🐛 **باگ‌ها را گزارش کنید**
4. 💡 **ایده‌های خود را مطرح کنید**
5. 🤝 **در توسعه مشارکت کنید**
6. 📢 **در شبکه‌های اجتماعی معرفی کنید**

**هر ستاره انگیزه‌ای برای ادامه کار است! 🙏**

---

## 📈 آمار GitHub

![Stars](https://img.shields.io/github/stars/balochscript/free-vpn-configs?style=social)
![Forks](https://img.shields.io/github/forks/balochscript/free-vpn-configs?style=social)
![Issues](https://img.shields.io/github/issues/balochscript/free-vpn-configs)
![License](https://img.shields.io/github/license/balochscript/free-vpn-configs)
![Last Commit](https://img.shields.io/github/last-commit/balochscript/free-vpn-configs)

---

<div align="center">

## 🌟 Made with ❤️ for Free Internet from Balochistan

### 🇮🇷 زنده باد ایران اسلامی | زنده باد بلوچستان 🦁

**نسخه 1.0** | **2025**

**دسترسی آزاد به اطلاعات حق همه است**

---

[![Star History](https://img.shields.io/github/stars/balochscript/free-vpn-configs?style=social)](https://github.com/balochscript/free-vpn-configs)

**⭐ اگر مفید بود، حتماً Star بدهید!**

</div>

---

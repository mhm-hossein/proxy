import asyncio
from telethon import TelegramClient, events, Button
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors.rpcerrorlist import UserNotParticipantError
import requests

# اطلاعات ربات شما
api_id = 24084970
api_hash = 'b1c654a94f360d5a9822188276cc733d'
bot_token = '7271781762:AAH0pG5QngFVelQvinHaZjZ4wspJ7HCgzTE'

# ایجاد یک کلاینت تلگرام با استفاده از توکن ربات
client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)

# شناسه کانال یا یوزرنیم کانال
channel_username = '@External_Net'

# URL های پروکسی‌ها
urls = {
    'usa': 'https://raw.githubusercontent.com/soroushmirzaei/telegram-proxies-collector/main/countries/us/proxies',
    'germany': 'https://raw.githubusercontent.com/soroushmirzaei/telegram-proxies-collector/main/countries/de/proxies',
    'france': 'https://raw.githubusercontent.com/soroushmirzaei/telegram-proxies-collector/main/countries/fr/proxies',
    'uk': 'https://raw.githubusercontent.com/soroushmirzaei/telegram-proxies-collector/main/countries/uk/proxies',
    'italy': 'https://raw.githubusercontent.com/soroushmirzaei/telegram-proxies-collector/main/countries/it/proxies',
    'turkey': 'https://raw.githubusercontent.com/soroushmirzaei/telegram-proxies-collector/main/countries/tr/proxies',
    'hong_kong': 'https://raw.githubusercontent.com/soroushmirzaei/telegram-proxies-collector/main/countries/hk/proxies',
    'israel': 'https://raw.githubusercontent.com/soroushmirzaei/telegram-proxies-collector/main/countries/il/proxies',
    'brazil': 'https://raw.githubusercontent.com/soroushmirzaei/telegram-proxies-collector/main/countries/br/proxies',
    'canada': 'https://raw.githubusercontent.com/soroushmirzaei/telegram-proxies-collector/main/countries/ca/proxies',
    'china': 'https://raw.githubusercontent.com/soroushmirzaei/telegram-proxies-collector/main/countries/cn/proxies',
    'netherlands': 'https://raw.githubusercontent.com/soroushmirzaei/telegram-proxies-collector/main/countries/nl/proxies',
    'singapore': 'https://raw.githubusercontent.com/soroushmirzaei/telegram-proxies-collector/main/countries/sg/proxies',
    'spain': 'https://raw.githubusercontent.com/soroushmirzaei/telegram-proxies-collector/main/countries/es/proxies',
    'ukraine': 'https://raw.githubusercontent.com/soroushmirzaei/telegram-proxies-collector/main/countries/ua/proxies',
    'ipv4': 'https://raw.githubusercontent.com/soroushmirzaei/telegram-proxies-collector/main/layers/ipv4',
    'ipv6': 'https://raw.githubusercontent.com/soroushmirzaei/telegram-proxies-collector/main/layers/ipv6'
}

# دیکشنری برای نگهداری وضعیت هر کاربر
user_states = {}
user_locks = {}

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    user_id = event.sender_id

    try:
        # بررسی اینکه آیا کاربر عضو کانال است یا خیر
        participant = await client(GetParticipantRequest(channel_username, user_id))
        
        # پیام خوش‌آمد به کاربر
        welcome_message = (
            "👋 سلام!\n\n"
            "به **ربات Proxy Collector** خوش آمدید! 🌐\n\n"
            "این ربات به شما کمک می‌کند تا به سادگی و سرعت به لیست پروکسی‌های مختلف دسترسی پیدا کنید.\n"
            "🔍 برای مشاهده لیست پروکسی‌های کشورهای مختلف، از دکمه‌های زیر استفاده کنید."
        )
        buttons = [
            [Button.inline("🇺🇸 آمریکا", b'usa'), Button.inline("🇩🇪 آلمان", b'germany')],
            [Button.inline("🇫🇷 فرانسه", b'france'), Button.inline("🇬🇧 انگلیس", b'uk')],
            [Button.inline("🇮🇹 ایتالیا", b'italy'), Button.inline("🇹🇷 ترکیه", b'turkey')],
            [Button.inline("🇭🇰 هنگ کنگ", b'hong_kong'), Button.inline("🇮🇱 اسرائیل", b'israel')],
            [Button.inline("🇧🇷 برزیل", b'brazil'), Button.inline("🇨🇦 کانادا", b'canada')],
            [Button.inline("🇨🇳 چین", b'china'), Button.inline("🇳🇱 هلند", b'netherlands')],
            [Button.inline("🇸🇬 سنگاپور", b'singapore'), Button.inline("🇪🇸 اسپانیا", b'spain')],
            [Button.inline("🇺🇦 اوکراین", b'ukraine'), Button.inline("🌐 آی‌پی‌وی۴", b'ipv4')],
            [Button.inline("🌐 آی‌پی‌وی۶", b'ipv6')],
            [Button.inline("👨‍💻 سازنده", b'creator_info')]
        ]
        await event.reply(welcome_message, buttons=buttons)

    except UserNotParticipantError:
        # اگر کاربر عضو کانال نبود
        await event.reply('📢 برای استفاده از این ربات، لطفاً ابتدا عضو کانال @External_Net شوید.')
    except Exception as e:
        # اگر خطای دیگری رخ داد
        await event.reply(f'🚨 مشکلی رخ داد: {str(e)}')

@client.on(events.CallbackQuery)
async def callback(event):
    user_id = event.sender_id
    data = event.data.decode('utf-8')

    if user_id not in user_locks:
        user_locks[user_id] = asyncio.Lock()

    async with user_locks[user_id]:
        if data in urls:
            await send_proxies(event, data)
        elif data == 'next':
            await send_next_proxy(event)
        elif data == 'previous':
            await send_previous_proxy(event)
        elif data == 'home':
            await send_home(event)
        elif data == 'creator_info':
            await send_creator_info(event)

# تابع مشترک برای ارسال پروکسی‌ها
async def send_proxies(event, country_code):
    user_id = event.sender_id

    try:
        # بررسی اینکه آیا کاربر عضو کانال است یا خیر
        participant = await client(GetParticipantRequest(channel_username, user_id))

        # دریافت محتوا از URL مربوط به کشور
        url = urls[country_code]
        response = requests.get(url)
        response.raise_for_status()

        # محتوای دریافتی
        content = response.text.strip()

        # تقسیم محتوا به خطوط
        proxies = content.splitlines()

        if not proxies:
            # اگر پروکسی موجود نبود
            await event.reply('❌ پروکسی برای نمایش وجود ندارد.')
            return

        # ذخیره وضعیت کاربر (موقعیت فعلی در لیست)
        user_states[user_id] = {
            'proxies': proxies,
            'index': 0,
            'country_code': country_code
        }

        # ارسال اولین صفحه شامل 5 پروکسی
        await send_current_proxy(event, user_id)

    except requests.exceptions.RequestException:
        # ارسال یک پیام کلی به جای ارسال متن کامل خطا
        await event.reply('❌ پروکسی برای نمایش وجود ندارد.')
    except Exception as e:
        # ارسال یک پیام کلی به جای ارسال متن کامل خطا
        await event.reply('⚠️ مشکلی در اجرای دستور رخ داد. لطفاً دوباره تلاش کنید.')

# تابع برای ارسال پروکسی فعلی
async def send_current_proxy(event, user_id):
    state = user_states.get(user_id)

    if state:
        proxies = state['proxies']
        index = state['index']
        start = index * 5
        end = start + 5

        # بررسی اینکه آیا پروکسی‌ها برای صفحه جاری وجود دارند
        if start < len(proxies):
            # انتخاب پروکسی‌ها برای صفحه جاری
            current_proxies = proxies[start:end]

            # اضافه کردن خط فاصله بین پروکسی‌ها
            message = '\n\n'.join(current_proxies)

            # اضافه کردن دکمه‌های بعدی، قبلی و صفحه اصلی
            buttons = []
            if (index + 1) * 5 < len(proxies):
                buttons.append(Button.inline("صفحه بعدی", b'next'))
            if index > 0:
                buttons.append(Button.inline("صفحه قبلی", b'previous'))
            buttons.append(Button.inline("صفحه اصلی", b'home'))

            await event.reply(message, buttons=buttons)
        else:
            await event.reply('❌ پروکسی برای نمایش وجود ندارد.')

@client.on(events.CallbackQuery(pattern=b'next'))
async def send_next_proxy(event):
    user_id = event.sender_id
    state = user_states.get(user_id)

    if state:
        # چک کردن اگر پروکسی‌های بیشتری برای نمایش وجود دارد
        if (state['index'] + 1) * 5 < len(state['proxies']):
            # افزایش ایندکس برای نمایش صفحه بعدی
            state['index'] += 1
            await send_current_proxy(event, user_id)
        else:
            await event.reply('❌ پروکسی برای نمایش وجود ندارد.')

@client.on(events.CallbackQuery(pattern=b'previous'))
async def send_previous_proxy(event):
    user_id = event.sender_id
    state = user_states.get(user_id)

    if state and state['index'] > 0:
        # کاهش ایندکس برای نمایش صفحه قبلی
        state['index'] -= 1
        await send_current_proxy(event, user_id)
    else:
        await event.reply('❌ صفحه قبلی وجود ندارد.')

# تابع برای ارسال کاربر به صفحه اصلی
async def send_home(event):
    user_id = event.sender_id
    await start(event)

# تابع برای نمایش اطلاعات سازنده
async def send_creator_info(event):
    creator_message = (
        "👨‍💻 این ربات توسط @mhm_moz ساخته شده است.\n"
        "📢 کانال: @External_Net"
    )
    await event.reply(creator_message)

# دستور /about برای نمایش اطلاعات درباره ربات
@client.on(events.NewMessage(pattern='/about'))
async def about(event):
    about_message = (
        "\U00002139 این ربات توسط @mhm_moz طراحی شده است.\n\n"
        "\U0001F4A1 هدف این ربات ارائه پروکسی‌های مختلف برای استفاده در تلگرام است.\n"
        "\U0001F517 برای استفاده از دستورات مختلف، از دکمه‌های شیشه‌ای استفاده کنید."
    )
    await event.reply(about_message)

# شروع کلاینت
client.start()
client.run_until_disconnected()
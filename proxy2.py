from telethon import TelegramClient, events
from telethon.tl.functions.channels import GetParticipantRequest
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
    'ukraine': 'https://raw.githubusercontent.com/soroushmirzaei/telegram-proxies-collector/main/countries/ua/proxies'
}

# دیکشنری برای نگهداری وضعیت هر کاربر
user_states = {}

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    user_id = event.sender_id

    try:
        # بررسی اینکه آیا کاربر عضو کانال است یا خیر
        participant = await client(GetParticipantRequest(channel_username, user_id))
        
        # پیام خوش‌آمد به کاربر
        welcome_message = (
            "👋 خوش آمدید به ربات Proxy Collector!\n\n"
            "✨ شما عضو کانال @External_Net هستید و اکنون می‌توانید از خدمات ربات استفاده کنید.\n"
            "برای دریافت لیست پروکسی‌های کشور های مختلف، دستور /list را ارسال کنید."
        )
        await event.reply(welcome_message)

    except:
        # اگر کاربر عضو کانال نبود
        await event.reply('🚨 برای استفاده از ربات، ابتدا باید در کانال @External_Net عضو شوید.')

@client.on(events.NewMessage(pattern='/list'))
async def send_proxy_list(event):
    user_id = event.sender_id

    try:
        # بررسی اینکه آیا کاربر عضو کانال است یا خیر
        participant = await client(GetParticipantRequest(channel_username, user_id))

        # لیست کشورها و دستورات
        proxy_list = (
            "\U0001F30D لیست پروکسی‌های موجود:\n\n"
            "\U0001F1FA\U0001F1F8 آمریکا: /usa\n"
            "\U0001F1E9\U0001F1EA آلمان: /germany\n"
            "\U0001F1EB\U0001F1F7 فرانسه: /france\n"
            "\U0001F1EC\U0001F1E7 انگلیس: /uk\n"
            "\U0001F1EE\U0001F1F9 ایتالیا: /italy\n"
            "\U0001F1F9\U0001F1F7 ترکیه: /turkey\n"
            "\U0001F1ED\U0001F1F0 هنگ کنگ: /hong_kong\n"
            "\U0001F1EE\U0001F1F1 اسرائیل: /israel\n"
            "\U0001F1E7\U0001F1F7 برزیل: /brazil\n"
            "\U0001F1E8\U0001F1E6 کانادا: /canada\n"
            "\U0001F1E8\U0001F1F3 چین: /china\n"
            "\U0001F1F3\U0001F1F1 هلند: /netherlands\n"
            "\U0001F1F8\U0001F1EC سنگاپور: /singapore\n"
            "\U0001F1EA\U0001F1F8 اسپانیا: /spain\n"
            "\U0001F1FA\U0001F1E6 اوکراین: /ukraine\n"
        )
        await event.reply(proxy_list)

    except:
        # اگر کاربر عضو کانال نبود
        await event.reply('\U0001F6A8 برای استفاده از این دستور، ابتدا باید در کانال @External_Net عضو شوید.')

# دستورات برای هر کشور
@client.on(events.NewMessage(pattern='/usa'))
async def send_usa_proxies(event):
    await send_proxies(event, 'usa')

@client.on(events.NewMessage(pattern='/germany'))
async def send_germany_proxies(event):
    await send_proxies(event, 'germany')

@client.on(events.NewMessage(pattern='/france'))
async def send_france_proxies(event):
    await send_proxies(event, 'france')

@client.on(events.NewMessage(pattern='/uk'))
async def send_uk_proxies(event):
    await send_proxies(event, 'uk')

@client.on(events.NewMessage(pattern='/italy'))
async def send_italy_proxies(event):
    await send_proxies(event, 'italy')

@client.on(events.NewMessage(pattern='/turkey'))
async def send_turkey_proxies(event):
    await send_proxies(event, 'turkey')

@client.on(events.NewMessage(pattern='/hong_kong'))
async def send_hong_kong_proxies(event):
    await send_proxies(event, 'hong_kong')

@client.on(events.NewMessage(pattern='/israel'))
async def send_israel_proxies(event):
    await send_proxies(event, 'israel')

@client.on(events.NewMessage(pattern='/brazil'))
async def send_brazil_proxies(event):
    await send_proxies(event, 'brazil')

@client.on(events.NewMessage(pattern='/canada'))
async def send_canada_proxies(event):
    await send_proxies(event, 'canada')

@client.on(events.NewMessage(pattern='/china'))
async def send_china_proxies(event):
    await send_proxies(event, 'china')

@client.on(events.NewMessage(pattern='/netherlands'))
async def send_netherlands_proxies(event):
    await send_proxies(event, 'netherlands')

@client.on(events.NewMessage(pattern='/singapore'))
async def send_singapore_proxies(event):
    await send_proxies(event, 'singapore')

@client.on(events.NewMessage(pattern='/spain'))
async def send_spain_proxies(event):
    await send_proxies(event, 'spain')

@client.on(events.NewMessage(pattern='/ukraine'))
async def send_ukraine_proxies(event):
    await send_proxies(event, 'ukraine')

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
            await event.reply('❌ پروکسی برای این کشور در حال حاضر موجود نمی‌باشد.')
            return

        # ذخیره وضعیت کاربر (موقعیت فعلی در لیست)
        user_states[user_id] = {
            'proxies': proxies,
            'index': 0,
            'country_code': country_code
        }

        # ارسال اولین صفحه شامل 10 پروکسی
        await send_current_proxy(event, user_id)

    except Exception as e:
        # ارسال یک پیام کلی به جای ارسال متن کامل خطا
        await event.reply('⚠️ مشکلی در اجرای دستور رخ داد. لطفاً دوباره تلاش کنید.')

# تابع برای ارسال پروکسی فعلی
async def send_current_proxy(event, user_id):
    state = user_states.get(user_id)

    if state:
        proxies = state['proxies']
        index = state['index']
        start = index * 10
        end = start + 10

        # بررسی اینکه آیا پروکسی‌ها برای صفحه جاری وجود دارند
        if start < len(proxies):
            # انتخاب پروکسی‌ها برای صفحه جاری
            current_proxies = proxies[start:end]

            # اضافه کردن خط فاصله بین پروکسی‌ها
            message = '\n\n'.join(current_proxies)

            # اضافه کردن دکمه‌های بعدی و قبلی
            message += '\n\nبرای دیدن صفحه بعدی /next و برای دیدن صفحه قبلی /previous را ارسال کنید.'

            await event.reply(message)
        else:
            await event.reply('⚠️ پروکسی بیشتری برای نمایش وجود ندارد.')

@client.on(events.NewMessage(pattern='/next'))
async def send_next_proxy(event):
    user_id = event.sender_id
    state = user_states.get(user_id)

    if state:
        # افزایش ایندکس برای نمایش صفحه بعدی
        state['index'] += 1
        await send_current_proxy(event, user_id)

@client.on(events.NewMessage(pattern='/previous'))
async def send_previous_proxy(event):
    user_id = event.sender_id
    state = user_states.get(user_id)

    if state and state['index'] > 0:
        # کاهش ایندکس برای نمایش صفحه قبلی
        state['index'] -= 1
        await send_current_proxy(event, user_id)

# دستور /about برای نمایش اطلاعات درباره ربات
@client.on(events.NewMessage(pattern='/about'))
async def about(event):
    about_message = (
        "\U00002139 این ربات توسط @mhm_moz طراحی شده است.\n\n"
        "\U0001F4A1 هدف این ربات ارائه پروکسی‌های مختلف برای استفاده در تلگرام است.\n"
        "\U0001F517 برای استفاده از دستورات مختلف، از /list استفاده کنید."
    )
    await event.reply(about_message)

# شروع کلاینت
client.start()
client.run_until_disconnected()
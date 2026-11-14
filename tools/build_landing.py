#!/usr/bin/env python3
"""Збирає лендінг chepeti.com: index.html (uk) і en/index.html з одного шаблону.
Ілюстрації й знак беруться з застосунку (chepeti-app/src/ui/art), кольори в них — CSS-змінні сайту, тож темна тема працює сама.
Запуск з кореня репозиторію: python3 chepeti-web/tools/build_landing.py
Тексти міняти тут, у T; згенеровані HTML руками не правити."""
import html, json, re
from pathlib import Path

WEB = Path(__file__).resolve().parents[1]
ART = WEB.parent / 'chepeti-app/src/ui/art'
PLAY = 'https://play.google.com/store/apps/details?id=com.chepeti.app'
LIVE = 'https://p.chepeti.com/7pMdRuCH4Ah'  # живий приклад: Rex, review-акаунт, режим «Загубилась»
ICON_PLAY = 'https://cdn.simpleicons.org/googleplay/ffffff'
ICON_APPLE = 'https://cdn.simpleicons.org/apple/8F8579'


def svg_from(ts: str, name: str | None = None) -> str:
    s = (ART / ts).read_text(encoding='utf-8')
    if name:
        m = re.search(r"'%s':\s*`([\s\S]*?)`" % re.escape(name), s)
    else:
        m = re.search(r'`([\s\S]*?)`', s)
    return m.group(1)


ILL = {n: svg_from('illustrations.ts', n) for n in ('welcome', 'no-sharing', 'protection')}
MARK = svg_from('mark.ts')
LOGO = (WEB / 'assets' / 'logo.svg').read_text().strip()  # логотип-напис від власника (14.11), колір із currentColor

T = {
 'uk': dict(
  lang='uk', root='/', other='/en/', other_label='EN', locale='uk_UA',
  title='Chepeti: щеплення, ліки й аналізи улюбленця в одному застосунку',
  desc='Нагадування про ліки й щеплення, аналізи на графіку, документи, спільний доступ для сім’ї і QR на нашийник, щоб знайти загубленого улюбленця.',
  nav=['Можливості', 'Тарифи', 'Питання'],
  play='Google Play', soon='App Store', soon_small='скоро',
  h1='Здоров’я улюбленця в одному застосунку',
  lead='Нагадає про ліки й щеплення, покаже аналізи на графіку, а QR на нашийнику допоможе повернути загубленого.',
  tour=[('Усе про улюбленця на одному екрані', 'Візити, лікування, щеплення, аналізи, документи й щоденник. Найближче видно одразу.', '03-pet',
         [('calendar-blank', 'Візити й висновки лікаря'), ('syringe', 'Нагадування про щеплення'), ('file-text', 'Документи під рукою'), ('notebook', 'Щоденник спостережень')]),
        ('Контакти під рукою', 'Записуйте контакти людей, які піклуються про улюбленця, або знаходьте заклади на мапі й телефонуйте в один дотик.', '13-places',
         [('first-aid', 'Ветклініки'), ('scissors', 'Грумери'), ('storefront', 'Зоомагазини'), ('bed', 'Готелі'), ('dog', 'Дресирувальники')]),
        ('Нагадає вчасно', 'Про візит, щеплення, аналіз і ліки. А ще про будь-яку свою справу.', '18-reminders',
         [('bell-ringing', 'Зателефонувати в клініку'), ('bell-ringing', 'Здати аналіз сечі'), ('bell-ringing', 'Час щеплення: міксоматоз')]),
        ('Лікування', 'Розумне лікування з нагадуванням про кожну дозу й журналом прийомів.', '05-med',
         [('check-circle', 'Зафіксувати прийом'), ('calendar-check', 'Щоденні прийоми'), ('arrows-clockwise', 'Інтервальні прийоми'), ('hand-pointing', 'Прийоми за потребою'), ('camera', 'Фото препаратів'), ('list-checks', 'Журнал: хто й коли дав')]),
        ('Аналізи на графіку', 'Показники з лініями норми: видно, як змінюється креатинін чи глюкоза від аналізу до аналізу.', '07-analyses', 'AN')],
  tests_h2='Аналізи на графіку',
  tests_sub='Показники крові й сечі з лініями норми. Видно, як змінюється креатинін чи глюкоза від аналізу до аналізу.',
  tests_points=['Лінії норми', 'Останній проти попереднього', 'Перерахунок одиниць', 'Об’єднання однакових показників'],
  chart_caption='Креатинін Барсіка за рік',
  an_hint='Наведіть на аналіз', an_tap='Торкніться аналізу',
  theme='Світла чи темна тема',
  lost_eyebrow='Якщо загубився',
  lost_h2='QR на нашийнику приведе додому',
  lost_sub='Хто знайде тварину, сканує жетон телефоном і бачить сторінку «Мене шукають». Що на ній видно, обираєте ви, а адреси там немає ніколи.',
  steps=['Створіть QR у застосунку й надрукуйте жетон на нашийник.',
         'Тварина загубилась: увімкніть режим «Мене шукають».',
         'Хто знайде, відсканує жетон і подзвонить вам. Ви бачите, скільки разів його сканували.'],
  live='Відкрити живий приклад', qr_caption='Відскануйте: це справжня сторінка',
  meds_h2='Більше ніяких «а ти вже дав?»',
  meds_sub='Графік прийому, нагадування вчасно і журнал, де видно, хто з сім’ї і коли дав ліки.',
  meds_note='<b>З Premium</b> «Дано» можна натиснути прямо в сповіщенні, не відкриваючи застосунок.',
  fam_h2='Доглядайте разом',
  fam_sub='Дайте доступ сім’ї, ветеринару чи догсітеру. Кожному відкрийте лише потрібні розділи й вирішіть, чи може він вносити зміни.',
  who=['Сім’я', 'Ветеринар', 'Догсітер', 'Заводчик'],
  who_note=['Ведуть усе разом із вами', 'Бачить повну медкартку: візити, аналізи, лікування й документи', 'Бачить лише обрану тварину й відмічає прийом ліків, а ви бачите це в журналі', 'Бачить щеплення й візити цуценяти зі свого розплідника'],
  levels=['Повний доступ', 'Тільки перегляд'],
  fam_facts=['Заберете доступ, а все, що людина внесла, лишиться у вас.', 'Учасник видалив запис чи документ? Він 30 днів чекає у вашому кошику, і його можна повернути.', 'Права змінюються одразу, і людина отримує сповіщення.'],
  fam_prem='Доступ відкриває власник із Premium. Запрошеним підписка не потрібна, а спільна тварина не займає їхній безкоштовний ліміт.',
  alt_share='Екран «Спільний доступ»: троє учасників з різними правами',
  more_h2='І все інше, що варто пам’ятати',
  cells=[('Візити', 'Висновок лікаря, що забули спитати, і нагадування про наступний прийом.'),
         ('Щеплення', 'Нагадає заздалегідь і покаже, що вже прострочено.'),
         ('Документи', 'Ветпаспорт, рецепти, результати. Фото з камери чи файл, усе біля потрібного запису.'),
         ('Медична картка PDF', 'Уся історія одним файлом для нового ветеринара.'),
         ('Щоденник', 'Апетит, поведінка, настрій. З датою й фото, щоб пам’ятати, коли це почалось.'),
         ('Ветклініки поруч', 'Довідник клінік, грумінгу й зоомагазинів на мапі, з годинами роботи.')],
  priv_h2='Ваші дані лишаються вашими',
  facts=[('Без реєстрації', 'Дані лежать на телефоні. Акаунт потрібен лише для хмарної копії, QR і спільного доступу.'),
         ('Аналітика лише за згодою', 'Перемикачі вимкнені, доки ви самі їх не ввімкнете.'),
         ('Видалення одним дотиком', 'Видалити всі дані можна в застосунку або на сайті.')],
  plans_h2='Почніть безкоштовно',
  plans_sub='Основне доступне без оплати, з рекламою. З Premium можливостей більше, і 7 днів його можна спробувати без оплати. Ціни в Google Play, у вашій валюті.',
  prem_chip='Premium',
  feats=[('heartbeat', 'Медкартка', 'Візити, лікування, щеплення, аналізи, документи й щоденник', 0),
         ('bell-ringing', 'Нагадування', 'Про ліки, щеплення, візити й повторні аналізи', 0),
         ('chart-line-up', 'Аналізи на графіку', 'Як змінюються показники від аналізу до аналізу', 0),
         ('qr-code', 'QR на нашийник', 'І режим «Мене шукають», якщо тварина загубилась', 0),
         ('map-pin', 'Довідник закладів', 'Ветклініки, грумери, зоомагазини й готелі', 0),
         ('paw-print', 'Скільки завгодно тварин', 'Безкоштовно одна тварина', 1),
         ('users', 'Спільний доступ', 'Сім’я, ветеринар чи догсітер бачать потрібне', 1),
         ('check-circle', 'Відмітка зі сповіщення', 'Прийом ліків, не відкриваючи застосунок', 1),
         ('list-checks', 'Журнал прийому', 'Хто й коли дав ліки', 1),
         ('cloud-check', 'Документи в хмарі', 'Записи зберігаються й без Premium, а з ним ще й файли документів, до 1 ГБ із Premium+', 1),
         ('file-pdf', 'PDF для лікаря', 'Уся історія одним файлом', 1),
         ('prohibit', 'Без реклами', 'В усьому застосунку', 1)],
  faq_h2='Питання',
  faq=[('Чи працює без інтернету?', 'Так. Дані лежать на телефоні, нагадування приходять і без мережі. Інтернет потрібен для хмарної копії, спільного доступу й сторінки QR.'),
       ('Чи є версія для iPhone?', 'Готуємо. Зараз Chepeti є в Google Play, версія для iPhone з’явиться в App Store.'),
       ('Що буде з даними, якщо я зміню телефон?', 'Якщо ви додали й підтвердили email, увійдіть в акаунт на новому телефоні, і повернуться всі записи: візити, лікування, щеплення, аналізи, щоденник. З Premium повернуться ще й файли документів.'),
       ('Хто бачить мої дані?', 'Лише ви. Без реєстрації все лежить на телефоні, акаунт потрібен тільки для хмарної копії, QR і спільного доступу. Аналітика вмикається лише за вашою згодою, а видалити все можна одним дотиком у застосунку.'),
       ('Для яких тварин підходить?', 'Коти, собаки, кролики, гризуни, птахи, рептилії та інші.'),
       ('Як видалити акаунт і дані?', 'У застосунку: Профіль, далі «Дані і приватність». Або на сторінці <a href="/delete-account.html">видалення акаунта</a>.')],
  final_h2='Додайте першого улюбленця',
  final_p='Завантажте Chepeti, це займе менше хвилини. Реєстрація не потрібна.',
  foot=[('Конфіденційність', '/privacy.html'), ('Умови використання', '/terms.html'), ('Видалення акаунта', '/delete-account.html')],
  alt_pet='Профіль кота Барсіка в Chepeti: візити, лікування, щеплення, аналізи, документи',
  alt_lost='Сторінка «Мене шукають» для пса Рекса після сканування QR',
  alt_med='Курс ліків: прийоми на сьогодні з кнопкою «Дано»', alt_log='Журнал прийому: хто і коли дав ліки',
  alt_chart='Графік креатиніну з лініями норми', alt_visits='Список візитів до ветеринара', alt_vac='Список щеплень з нагадуваннями',
  qr_alt='QR-код живого прикладу',
 ),
 'en': dict(
  lang='en', root='/en/', other='/', other_label='UA', locale='en_US',
  title='Chepeti: your pet’s vaccines, meds and tests in one app',
  desc='Medication and vaccine reminders, lab results on a chart, documents, family sharing and a QR collar tag to bring a lost pet home.',
  nav=['Features', 'Pricing', 'FAQ'],
  play='Google Play', soon='App Store', soon_small='soon',
  h1='Your pet’s health in one app',
  lead='Reminds you about meds and vaccines, charts lab results, and a QR tag on the collar helps bring a lost pet home.',
  tour=[('Everything about your pet on one screen', 'Visits, treatment, vaccinations, tests, documents and diary. What’s next is right there.', '03-pet',
         [('calendar-blank', 'Visits and vet notes'), ('syringe', 'Vaccine reminders'), ('file-text', 'Documents at hand'), ('notebook', 'Observation diary')]),
        ('Contacts at hand', 'Keep the people who care for your pet in one place, or find places on the map and call in one tap.', '13-places',
         [('first-aid', 'Vet clinics'), ('scissors', 'Groomers'), ('storefront', 'Pet shops'), ('bed', 'Pet hotels'), ('dog', 'Trainers')]),
        ('Reminds you on time', 'About visits, vaccines, tests and meds. And about anything else you need.', '18-reminders',
         [('bell-ringing', 'Call the clinic'), ('bell-ringing', 'Take a urine test'), ('bell-ringing', 'Vaccine time: myxomatosis')]),
        ('Treatment', 'Smart treatment with a reminder for every dose and a dose log.', '05-med',
         [('check-circle', 'Mark a dose as given'), ('calendar-check', 'Daily doses'), ('arrows-clockwise', 'Every few days'), ('hand-pointing', 'As needed'), ('camera', 'Medicine photos'), ('list-checks', 'Log: who gave it and when')]),
        ('Lab results on a chart', 'Values with reference lines: see how creatinine or glucose changes from test to test.', '07-analyses', 'AN')],
  tests_h2='Lab results on a chart',
  tests_sub='Blood and urine values with reference lines. See how creatinine or glucose changes from test to test.',
  tests_points=['Reference lines', 'Latest vs previous', 'Unit conversion', 'Merging duplicate values'],
  chart_caption='Barsik’s creatinine over a year',
  an_hint='Hover over a test', an_tap='Tap a test',
  theme='Light or dark theme',
  lost_eyebrow='If your pet gets lost',
  lost_h2='A QR tag that leads home',
  lost_sub='Whoever finds your pet scans the tag and sees an “I’m lost” page. You choose what it shows, and your address is never there.',
  steps=['Create a QR in the app and print a collar tag.',
         'Pet missing? Turn on “I’m lost” mode.',
         'The finder scans the tag and calls you. You see how many times it was scanned.'],
  live='Open the live example', qr_caption='Scan it: this is a real page',
  meds_h2='No more “did you already give it?”',
  meds_sub='Dose schedules, reminders on time and a log that shows who in the family gave the medicine and when.',
  meds_note='<b>With Premium</b> tap “Given” right in the notification, without opening the app.',
  fam_h2='Care for them together',
  fam_sub='Share with family, your vet or a pet sitter. Open only the sections each person needs and decide whether they can make changes.',
  who=['Family', 'Vet', 'Pet sitter', 'Breeder'],
  who_note=['Keep track of everything with you', 'Sees the full medical record: visits, tests, treatment and documents', 'Sees only the pet you choose and marks each dose, which you see in the log', 'Follows the vaccinations and vet visits of a puppy from their kennel'],
  levels=['Full access', 'View only'],
  fam_facts=['Remove access any time, and everything they added stays with you.', 'If someone deletes a record or document, it waits in your trash for 30 days so you can restore it.', 'New permissions apply at once, and the person gets a notification.'],
  fam_prem='Sharing is opened by an owner with Premium. Invited people don’t need a subscription, and a shared pet doesn’t count toward their free limit.',
  alt_share='The “Shared access” screen: three people with different permissions',
  more_h2='And everything else worth remembering',
  cells=[('Vet visits', 'The vet’s conclusion, what you forgot to ask, and a reminder for the next visit.'),
         ('Vaccinations', 'Reminds you ahead of time and shows what’s overdue.'),
         ('Documents', 'Vet passport, prescriptions, results. A photo or a file, kept next to the right record.'),
         ('Medical card PDF', 'The whole history in one file for a new vet.'),
         ('Diary', 'Appetite, behaviour, mood. With date and photo, so you remember when it started.'),
         ('Vet clinics nearby', 'A map of clinics, groomers and pet shops with opening hours.')],
  priv_h2='Your data stays yours',
  facts=[('No sign-up needed', 'Data lives on your phone. An account is only for cloud backup, QR and sharing.'),
         ('Analytics only with consent', 'Toggles stay off until you turn them on.'),
         ('Delete in one tap', 'Delete all your data in the app or on the website.')],
  plans_h2='Start for free',
  plans_sub='Everything essential is free, with ads. Premium adds more, and you can try it free for 7 days. Prices are shown in Google Play in your currency.',
  prem_chip='Premium',
  feats=[('heartbeat', 'Health record', 'Visits, treatment, vaccinations, tests, documents and diary', 0),
         ('bell-ringing', 'Reminders', 'For meds, vaccinations, visits and follow-up tests', 0),
         ('chart-line-up', 'Lab results on a chart', 'See how values change from test to test', 0),
         ('qr-code', 'QR collar tag', 'And “I’m lost” mode if your pet goes missing', 0),
         ('map-pin', 'Places directory', 'Vet clinics, groomers, pet shops and hotels', 0),
         ('paw-print', 'As many pets as you like', 'One pet on the free plan', 1),
         ('users', 'Shared access', 'Family, your vet or a pet sitter see what they need', 1),
         ('check-circle', 'Mark from the notification', 'Log a dose without opening the app', 1),
         ('list-checks', 'Dose log', 'Who gave the medicine, and when', 1),
         ('cloud-check', 'Documents in the cloud', 'Records are backed up even without Premium; with it, document files too, up to 1 GB with Premium+', 1),
         ('file-pdf', 'PDF for your vet', 'The whole history in one file', 1),
         ('prohibit', 'No ads', 'Anywhere in the app', 1)],
  faq_h2='FAQ',
  faq=[('Does it work offline?', 'Yes. Data lives on your phone and reminders arrive without a connection. You need internet for cloud backup, sharing and the QR page.'),
       ('Is there an iPhone version?', 'It’s on the way. Chepeti is on Google Play now, and the iPhone version is coming to the App Store.'),
       ('What happens to my data if I change phones?', 'If you’ve added and confirmed your email, sign in on the new phone and all your records come back: visits, treatment, vaccinations, tests and diary. With Premium, your document files come back too.'),
       ('Who can see my data?', 'Only you. Without an account everything stays on your phone; an account is only for cloud backup, QR and sharing. Analytics turn on only with your consent, and you can delete everything in one tap in the app.'),
       ('Which pets does it support?', 'Cats, dogs, rabbits, rodents, birds, reptiles and more.'),
       ('How do I delete my account and data?', 'In the app: Profile, then “Data and privacy”. Or on the <a href="/en/delete-account.html">account deletion page</a>.')],
  final_h2='Add your first pet',
  final_p='Get Chepeti, it takes less than a minute. No sign-up needed.',
  foot=[('Privacy', '/en/privacy.html'), ('Terms of Use', '/en/terms.html'), ('Delete account', '/en/delete-account.html')],
  alt_pet='Barsik the cat’s profile in Chepeti: visits, treatment, vaccinations, tests, documents',
  alt_lost='The “I’m lost” page for Rex the dog after scanning the QR',
  alt_med='A medication course: today’s doses with a “Given” button', alt_log='Dose log: who gave the medicine and when',
  alt_chart='Creatinine chart with reference range', alt_visits='List of vet visits', alt_vac='List of vaccinations with reminders',
  qr_alt='QR code of the live example',
 ),
}


import datetime as _dt
_SHOT = _dt.date(2026, 11, 13)
_DATES = [(_SHOT - _dt.timedelta(days=(14 - i) * 24 + 3)) for i in range(15)]
GLU = [5.1, 5.6, 4.8, 6.2, 5.9, 7.4, 9.1, 8.6, 6.8, 6.1, 5.7, 5.4, 6.0, 5.8, 5.5]
CRE = [118, 124, 121, 135, 142, 150, 168, 181, 176, 205, 219, 196, 184, 172, 165]
ALT = [45, 52, 48, 61, 58, 74, 96, 138, 112, 88, 70, 64, 59, 55, 51]
MON = {'uk': ['січ', 'лют', 'бер', 'кві', 'тра', 'чер', 'лип', 'сер', 'вер', 'жов', 'лис', 'гру'],
       'en': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']}


def an_data(t: dict) -> str:
    L = t['lang']
    uk = L == 'uk'
    d = lambda x: f'{x.day} {MON[L][x.month - 1]} {x.year}' if uk else f'{x.day} {MON[L][x.month - 1]} {x.year}'
    data = {
        'dec': ',' if uk else '.', 'prev': 'попередній' if uk else 'previous', 'norm': 'Норма' if uk else 'Reference',
        'dates': [f'{x.day:02d}.{x.month:02d}' for x in _DATES],
        'metrics': [
            {'name': 'Креатинін' if uk else 'Creatinine', 'unit': 'мкмоль/л' if uk else 'µmol/L', 'v': CRE, 'ref': [71, 212]},
            {'name': 'Глюкоза' if uk else 'Glucose', 'unit': 'ммоль/л' if uk else 'mmol/L', 'v': GLU, 'ref': [3.9, 8.3]},
            {'name': 'АЛТ' if uk else 'ALT', 'unit': 'Од/л' if uk else 'U/L', 'v': ALT, 'ref': [12, 130]},
        ],
        'rows': [
            {'title': 'Біохімія' if uk else 'Blood chemistry', 'date': d(_DATES[14]), 'series': 14},
            {'title': 'Біохімія' if uk else 'Blood chemistry', 'date': d(_DATES[13]), 'series': 13},
            {'title': 'Сеча' if uk else 'Urinalysis', 'date': d(_SHOT - _dt.timedelta(days=35)),
             'vals': [['pH', '6,8' if uk else '6.8'], ['Питома вага' if uk else 'Specific gravity', '1.035']]},
            {'title': 'Кров (загальний аналіз)' if uk else 'Complete blood count', 'date': d(_SHOT - _dt.timedelta(days=40)),
             'vals': [['Лейкоцити' if uk else 'White blood cells', '14,2×10⁹/л' if uk else '14.2×10⁹/L']]},
        ],
    }
    return html.escape(json.dumps(data, ensure_ascii=False))


# Рядки на скриншоті списку аналізів (у % висоти кадру), однакові для uk і en.
AN_ROWS = [(32.3, 10), (43.8, 10), (55.3, 13.3), (70.3, 15.8)]


# Приклади прав для ролей на лендінгу (у застосунку ролей немає: права ставлять вручну, тут лише ілюстрація).
ROLES = [0, 1, 0, 1]  # рівень для кожної ролі: 0 повний, 1 тільки перегляд


def ph(ic: str) -> str:
    return f'<i style="--ic:url(https://unpkg.com/@phosphor-icons/core@2.1.1/assets/regular/{ic}.svg)"></i>'


def badge(ic: str, tx: str, m: int) -> str:
    return f'<div class="badge" style="--m:{m}"><i style="--ic:url(https://unpkg.com/@phosphor-icons/core@2.1.1/assets/regular/{ic}.svg)"></i><b>{html.escape(tx)}</b></div>'


def ver(name: str) -> str:
    import hashlib
    return hashlib.md5((WEB / 'assets' / name).read_bytes()).hexdigest()[:8]


def page(t: dict) -> str:
    L = t['lang']
    a = '/assets/'
    shot = lambda n: f"{a}screens/{L}-{n}.webp"
    ul = lambda xs: ''.join(f'<li>{html.escape(x)}</li>' for x in xs)
    btn_play = f'<a class="btn btn-primary" href="{PLAY}" rel="noopener"><img class="mono" src="{ICON_PLAY}" alt="" width="20" height="20">{t["play"]}</a>'
    btn_soon = f'<span class="btn btn-soon" aria-disabled="true"><img src="{ICON_APPLE}" alt="" width="20" height="20">{t["soon"]} <small>{t["soon_small"]}</small></span>'
    cells = t['cells']
    ld = {
        '@context': 'https://schema.org', '@type': 'MobileApplication', 'name': 'Chepeti',
        'operatingSystem': 'Android', 'applicationCategory': 'LifestyleApplication', 'inLanguage': ['uk', 'en'],
        'description': t['desc'], 'url': f"https://chepeti.com{t['root']}", 'installUrl': PLAY,
        'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'USD'},
    }
    faq_ld = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': re.sub('<[^>]+>', '', ans)}} for q, ans in t['faq']]}
    return f'''<!DOCTYPE html>
<html lang="{L}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(t['title'])}</title>
<meta name="description" content="{html.escape(t['desc'])}">
<link rel="canonical" href="https://chepeti.com{t['root']}">
<link rel="alternate" hreflang="uk" href="https://chepeti.com/">
<link rel="alternate" hreflang="en" href="https://chepeti.com/en/">
<link rel="alternate" hreflang="x-default" href="https://chepeti.com/en/">
<meta name="theme-color" content="#FAF8F5" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#19120E" media="(prefers-color-scheme: dark)">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(t['title'])}">
<meta property="og:description" content="{html.escape(t['desc'])}">
<meta property="og:url" content="https://chepeti.com{t['root']}">
<meta property="og:image" content="https://chepeti.com{a}og-{L}.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta property="og:locale" content="{t['locale']}">
<link rel="icon" href="{a}favicon.png">
<link rel="preload" href="{a}fonts/Mulish_700Bold.ttf" as="font" type="font/ttf" crossorigin>
<link rel="stylesheet" href="{a}landing.css?v={ver("landing.css")}">
<script>document.documentElement.classList.add('js');try{{var th=localStorage.getItem('theme');if(th)document.documentElement.dataset.theme=th}}catch(e){{}}</script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js" defer></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js" defer></script>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(faq_ld, ensure_ascii=False)}</script>
</head>
<body>
<header class="top"><div class="wrap">
  <a class="brand" href="{t['root']}">{LOGO}</a>
  <nav aria-label="{t['nav'][0]}"><a href="#lost">{t['nav'][0]}</a><a href="#plans">{t['nav'][1]}</a><a href="#faq">{t['nav'][2]}</a></nav>
  <button class="theme" type="button" aria-label="{t['theme']}" title="{t['theme']}"><i class="sun"></i><i class="moon"></i></button>
  <a class="lang" href="{t['other']}" hreflang="{'en' if L == 'uk' else 'uk'}">{t['other_label']}</a>
  <a class="btn btn-primary btn-sm" href="{PLAY}" rel="noopener">{t['play']}</a>
</div></header>

<main>
<section class="tour"><div class="tour-stage">
  <div class="tour-intro"><div class="wrap">
    <h1>{t['h1']}</h1>
    <p class="lead">{t['lead']}</p>
    <div class="cta-row">{btn_play}{btn_soon}</div>
    <div class="dog" aria-hidden="true">
      <img class="eye eye-l" src="{a}dog/eye-l.webp" alt="" width="226" height="226">
      <img class="eye eye-r" src="{a}dog/eye-r.webp" alt="" width="226" height="226">
      <img class="head" src="{a}dog/head.webp" alt="" width="1100" height="1100" fetchpriority="high">
    </div>
  </div></div>
  <div class="tour-card" data-an="{an_data(t)}"><div class="tour-steps" aria-hidden="true">{'<span></span>' * len(t['tour'])}</div><div class="tour-grid">
    <div class="tour-texts">{''.join(f'<div><h3>{h}</h3><p>{p}</p></div>' for h, p, *_ in t['tour'])}</div>
    <div class="tour-tilt"><div class="tour-phone"><div class="screens">{''.join(f'<img src="{shot(img)}" alt="{html.escape(h)}" width="600" height="1333"{' fetchpriority="high"' if k == 0 else ' loading="lazy"'}>' for k, (h, p, img, pts) in enumerate(t['tour']))}{''.join(f'<button type="button" class="an-spot" style="top:{y}%;height:{h}%" aria-label="{t['an_hint']} {k + 1}"></button>' for k, (y, h) in enumerate(AN_ROWS))}</div></div></div>
    <div class="tour-badges">{''.join(('<div class="badge-set an-set"><div class="an-tip" aria-live="polite"></div></div>') if pts == 'AN' else '<div class="badge-set">' + ''.join(badge(ic, tx, m) for m, (ic, tx) in enumerate(pts)) + '</div>' for h, p, img, pts in t['tour'])}</div>
  </div></div>
</div></section>

<section class="lost" id="lost"><div class="wrap">
  <div class="lost-visual reveal">
    <div class="paw">
      <img class="paw-arm" src="{a}paw/paw.webp" alt="" width="670" height="904" loading="lazy">
      <span class="paw-tag"><img src="{a}paw/badge.webp" alt="" width="670" height="904" loading="lazy"><a class="paw-qr" href="{LIVE}" rel="noopener"><img src="{a}paw/qr.svg" alt="{t['qr_alt']}" width="29" height="29" loading="lazy"></a></span>
      <img class="paw-ring" src="{a}paw/ring.webp" alt="" width="670" height="904" loading="lazy">
      <span class="paw-cap">{t['qr_caption']}</span>
    </div>
  </div>
  <div class="reveal" style="--i:1">
    <p class="eyebrow">{t['lost_eyebrow']}</p>
    <h2 style="margin-top:12px">{t['lost_h2']}</h2>
    <p class="sub">{t['lost_sub']}</p>
    <ol class="steps">{ul(t['steps'])}</ol>
    <a href="{LIVE}" rel="noopener">{t['live']}</a>
  </div>
</div></section>

<section class="family"><div class="wrap">
  <div class="fam-visual reveal"><div class="phone"><img src="{shot('19-sharing')}" alt="{html.escape(t['alt_share'])}" width="600" height="1333" loading="lazy" style="object-position:top"></div></div>
  <div class="reveal" style="--i:1">
    <h2>{t['fam_h2']}</h2>
    <p class="sub">{t['fam_sub']}</p>
    <ul class="roles">{''.join(f'<li><b>{w}</b><span class="lv{lv}">{ph(('shield', 'eye')[lv])}{t['levels'][lv]}</span><p>{t['who_note'][k]}</p></li>' for k, (w, lv) in enumerate(zip(t['who'], ROLES)))}</ul>
    <ul class="fam-facts">{''.join(f'<li>{x}</li>' for x in t['fam_facts'])}</ul>
    <p class="fam-prem">{t['fam_prem']}</p>
  </div>
</div></section>

<section class="more"><div class="wrap">
  <h2 class="reveal">{t['more_h2']}</h2>
  <div class="bento">
    <div class="cell shot reveal"><h3>{cells[0][0]}</h3><p>{cells[0][1]}</p><img src="{shot('10-visits')}" alt="{html.escape(t['alt_visits'])}" width="600" height="1333" loading="lazy"></div>
    <div class="cell shot reveal" style="--i:1"><h3>{cells[1][0]}</h3><p>{cells[1][1]}</p><img src="{shot('09-vaccines')}" alt="{html.escape(t['alt_vac'])}" width="600" height="1333" loading="lazy"></div>
    <div class="cell tint docs reveal" style="--i:2"><h3>{cells[2][0]}</h3><p>{cells[2][1]}</p><div class="formats" aria-hidden="true">{''.join(f'<span><img src="{a}file-{x}.svg" alt="" width="56" height="56"></span>' for x in ('pdf', 'jpg', 'docx'))}</div></div>
    <div class="cell reveal" style="--i:3"><h3>{cells[3][0]}</h3><p>{cells[3][1]}</p></div>
    <div class="cell reveal" style="--i:2"><h3>{cells[4][0]}</h3><p>{cells[4][1]}</p></div>
    <div class="cell tint reveal" style="--i:3"><h3>{cells[5][0]}</h3><p>{cells[5][1]}</p></div>
  </div>
</div></section>

<section class="plans" id="plans"><div class="wrap">
  <h2 class="reveal">{t['plans_h2']}</h2>
  <p class="sub reveal">{t['plans_sub']}</p>
  <ul class="feats">{''.join(f'<li class="reveal{" pro" if pro else ""}" style="--i:{k % 3}">{ph(ic)}<b>{h}</b><p>{tx}</p>{f'<span class="pro-chip">{ph("crown-simple")}{t["prem_chip"]}</span>' if pro else ''}</li>' for k, (ic, h, tx, pro) in enumerate(t['feats']))}</ul>
</div></section>

<section class="faq" id="faq"><div class="wrap">
  <h2>{t['faq_h2']}</h2>
  {''.join(f'<details><summary>{q}</summary><p>{ans}</p></details>' for q, ans in t['faq'])}
</div></section>

<section class="final"><div class="wrap reveal">
  <div><h2>{t['final_h2']}</h2><p>{t['final_p']}</p></div>
  {btn_play}
</div></section>
</main>

<footer><div class="wrap">
  {''.join(f'<a href="{u}">{n}</a>' for n, u in t['foot'])}
  <a href="mailto:support@chepeti.com">support@chepeti.com</a>
  <span class="copy">© 2026 Chepeti</span>
</div></footer>
<script src="{a}landing.js?v={ver("landing.js")}" defer></script>
<script src="{a}tour.js?v={ver("tour.js")}" defer></script>
<script src="{a}analyses.js?v={ver("analyses.js")}" defer></script>
<script src="{a}dog.js?v={ver("dog.js")}" defer></script>
</body>
</html>
'''


# Висячі короткі слова (в, й, а, з, на, I, a, to…) не лишаються в кінці рядка: нерозривний пробіл після них.
SHORT = re.compile(r'(?<![\w<\-/])([A-Za-zА-Яа-яІіЇїЄєҐґ]{1,2}) ')


def tie(x):
    if isinstance(x, str):
        return x if x.startswith(('/', 'http')) or '<' in x and '>' in x and 'href' in x else SHORT.sub('\\1\u00a0', x)
    if isinstance(x, list):
        return [tie(v) for v in x]
    if isinstance(x, tuple):
        return tuple(tie(v) for v in x)
    if isinstance(x, dict):
        return {k: (v if k in ('lang', 'root', 'other', 'locale', 'foot') else tie(v)) for k, v in x.items()}
    return x


if __name__ == '__main__':
    for L, t in T.items():
        t = tie(t)
        out = WEB / ('index.html' if L == 'uk' else 'en/index.html')
        s = page(t)
        assert '—' not in s.replace(MARK, '').replace(''.join(ILL.values()), '') and '–' not in s, 'довге тире в текстах'
        out.write_text(s, encoding='utf-8')
        print(out.relative_to(WEB), len(s) // 1024, 'KB')

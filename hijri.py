"""Misri (Fatemi) tabular Hijri calendar, as used by the Dawoodi Bohra community.

Odd months have 30 days, even months 29; Zul Hijjah gets a 30th day in the eleven
leap years of each 30-year cycle. Pure arithmetic, no network, no dependencies.
`HIJRI_OFFSET_DAYS` in config can nudge the result if the school ever needs to.
"""
from datetime import date

LEAP_YEARS = {2, 5, 8, 10, 13, 16, 19, 21, 24, 27, 29}
EPOCH_JDN = 1948439  # 1 Moharram 1 AH (Misri epoch)

MONTHS = [
    ('Moharram al-Haraam', 'محرم الحرام'),
    ('Safar al-Muzaffar', 'صفر المظفر'),
    ('Rabi al-Awwal', 'ربيع الأول'),
    ('Rabi al-Aakhar', 'ربيع الآخر'),
    ('Jumada al-Ula', 'جمادى الأولى'),
    ('Jumada al-Ukhra', 'جمادى الأخرى'),
    ('Rajab al-Asab', 'رجب الأصب'),
    ('Shabaan al-Karim', 'شعبان الكريم'),
    ('Shehrullah al-Moazzam', 'شهر الله المعظم'),
    ('Shawwal al-Mukarram', 'شوال المكرم'),
    ('Zul Qadah al-Haraam', 'ذو القعدة الحرام'),
    ('Zul Hijjah al-Haraam', 'ذو الحجة الحرام'),
]
AR_DIGITS = str.maketrans('0123456789', '٠١٢٣٤٥٦٧٨٩')


def _jdn(d: date) -> int:
    return d.toordinal() + 1721425


def _year_days(y):
    return 355 if ((y - 1) % 30) + 1 in LEAP_YEARS else 354


def _month_days(y, m):
    if m == 12 and ((y - 1) % 30) + 1 in LEAP_YEARS:
        return 30
    return 30 if m % 2 == 1 else 29


def to_hijri(d: date, offset: int = 0):
    days = _jdn(d) + offset - EPOCH_JDN
    cycles, days = divmod(days, 10631)  # 30-year cycle length
    y = cycles * 30 + 1
    while days >= _year_days(y):
        days -= _year_days(y); y += 1
    m = 1
    while days >= _month_days(y, m):
        days -= _month_days(y, m); m += 1
    return y, m, days + 1


def hijri_parts(d: date, offset: int = 0):
    y, m, dd = to_hijri(d, offset)
    en, ar = MONTHS[m - 1]
    return dict(day=dd, month=m, year=y, month_en=en, month_ar=ar,
                ar=f'{str(dd).translate(AR_DIGITS)} {ar} {str(y).translate(AR_DIGITS)}هـ',
                en=f'{dd} {en} {y}H')

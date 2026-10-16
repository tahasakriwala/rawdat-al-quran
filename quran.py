"""Reference data for the Hifz tracker: 114 surahs, 30 juz, 604 Madani pages."""

# (arabic, transliteration, ayahs, starting page in the 604-page Madani mushaf)
SURAHS = [
    ('الفاتحة', 'al-Fatiha', 7, 1), ('البقرة', 'al-Baqarah', 286, 2), ('آل عمران', 'Aal Imran', 200, 50),
    ('النساء', 'al-Nisa', 176, 77), ('المائدة', 'al-Maidah', 120, 106), ('الأنعام', 'al-Anam', 165, 128),
    ('الأعراف', 'al-Araf', 206, 151), ('الأنفال', 'al-Anfal', 75, 177), ('التوبة', 'al-Tawbah', 129, 187),
    ('يونس', 'Yunus', 109, 208), ('هود', 'Hud', 123, 221), ('يوسف', 'Yusuf', 111, 235),
    ('الرعد', 'al-Rad', 43, 249), ('إبراهيم', 'Ibrahim', 52, 255), ('الحجر', 'al-Hijr', 99, 262),
    ('النحل', 'al-Nahl', 128, 267), ('الإسراء', 'al-Isra', 111, 282), ('الكهف', 'al-Kahf', 110, 293),
    ('مريم', 'Maryam', 98, 305), ('طه', 'Taha', 135, 312), ('الأنبياء', 'al-Anbiya', 112, 322),
    ('الحج', 'al-Hajj', 78, 332), ('المؤمنون', 'al-Muminun', 118, 342), ('النور', 'al-Nur', 64, 350),
    ('الفرقان', 'al-Furqan', 77, 359), ('الشعراء', 'al-Shuara', 227, 367), ('النمل', 'al-Naml', 93, 377),
    ('القصص', 'al-Qasas', 88, 385), ('العنكبوت', 'al-Ankabut', 69, 396), ('الروم', 'al-Rum', 60, 404),
    ('لقمان', 'Luqman', 34, 411), ('السجدة', 'al-Sajdah', 30, 415), ('الأحزاب', 'al-Ahzab', 73, 418),
    ('سبأ', 'Saba', 54, 428), ('فاطر', 'Fatir', 45, 434), ('يس', 'Yasin', 83, 440),
    ('الصافات', 'al-Saffat', 182, 446), ('ص', 'Sad', 88, 453), ('الزمر', 'al-Zumar', 75, 458),
    ('غافر', 'Ghafir', 85, 467), ('فصلت', 'Fussilat', 54, 477), ('الشورى', 'al-Shura', 53, 483),
    ('الزخرف', 'al-Zukhruf', 89, 489), ('الدخان', 'al-Dukhan', 59, 496), ('الجاثية', 'al-Jathiyah', 37, 499),
    ('الأحقاف', 'al-Ahqaf', 35, 502), ('محمد', 'Muhammad', 38, 507), ('الفتح', 'al-Fath', 29, 511),
    ('الحجرات', 'al-Hujurat', 18, 515), ('ق', 'Qaf', 45, 518), ('الذاريات', 'al-Dhariyat', 60, 520),
    ('الطور', 'al-Tur', 49, 523), ('النجم', 'al-Najm', 62, 526), ('القمر', 'al-Qamar', 55, 528),
    ('الرحمن', 'al-Rahman', 78, 531), ('الواقعة', 'al-Waqiah', 96, 534), ('الحديد', 'al-Hadid', 29, 537),
    ('المجادلة', 'al-Mujadilah', 22, 542), ('الحشر', 'al-Hashr', 24, 545), ('الممتحنة', 'al-Mumtahanah', 13, 549),
    ('الصف', 'al-Saff', 14, 551), ('الجمعة', 'al-Jumuah', 11, 553), ('المنافقون', 'al-Munafiqun', 11, 554),
    ('التغابن', 'al-Taghabun', 18, 556), ('الطلاق', 'al-Talaq', 12, 558), ('التحريم', 'al-Tahrim', 12, 560),
    ('الملك', 'al-Mulk', 30, 562), ('القلم', 'al-Qalam', 52, 564), ('الحاقة', 'al-Haqqah', 52, 566),
    ('المعارج', 'al-Maarij', 44, 568), ('نوح', 'Nuh', 28, 570), ('الجن', 'al-Jinn', 28, 572),
    ('المزمل', 'al-Muzzammil', 20, 574), ('المدثر', 'al-Muddaththir', 56, 575), ('القيامة', 'al-Qiyamah', 40, 577),
    ('الإنسان', 'al-Insan', 31, 578), ('المرسلات', 'al-Mursalat', 50, 580), ('النبأ', 'al-Naba', 40, 582),
    ('النازعات', 'al-Naziat', 46, 583), ('عبس', 'Abasa', 42, 585), ('التكوير', 'al-Takwir', 29, 586),
    ('الانفطار', 'al-Infitar', 19, 587), ('المطففين', 'al-Mutaffifin', 36, 587), ('الانشقاق', 'al-Inshiqaq', 25, 589),
    ('البروج', 'al-Buruj', 22, 590), ('الطارق', 'al-Tariq', 17, 591), ('الأعلى', 'al-Ala', 19, 591),
    ('الغاشية', 'al-Ghashiyah', 26, 592), ('الفجر', 'al-Fajr', 30, 593), ('البلد', 'al-Balad', 20, 594),
    ('الشمس', 'al-Shams', 15, 595), ('الليل', 'al-Layl', 21, 595), ('الضحى', 'al-Duha', 11, 596),
    ('الشرح', 'al-Sharh', 8, 596), ('التين', 'al-Tin', 8, 597), ('العلق', 'al-Alaq', 19, 597),
    ('القدر', 'al-Qadr', 5, 598), ('البينة', 'al-Bayyinah', 8, 598), ('الزلزلة', 'al-Zalzalah', 8, 599),
    ('العاديات', 'al-Adiyat', 11, 599), ('القارعة', 'al-Qariah', 11, 600), ('التكاثر', 'al-Takathur', 8, 600),
    ('العصر', 'al-Asr', 3, 601), ('الهمزة', 'al-Humazah', 9, 601), ('الفيل', 'al-Fil', 5, 601),
    ('قريش', 'Quraysh', 4, 602), ('الماعون', 'al-Maun', 7, 602), ('الكوثر', 'al-Kawthar', 3, 602),
    ('الكافرون', 'al-Kafirun', 6, 603), ('النصر', 'al-Nasr', 3, 603), ('المسد', 'al-Masad', 5, 603),
    ('الإخلاص', 'al-Ikhlas', 4, 604), ('الفلق', 'al-Falaq', 5, 604), ('الناس', 'al-Nas', 6, 604),
]
assert len(SURAHS) == 114 and sum(s[2] for s in SURAHS) == 6236

TOTAL_PAGES = 604
AR_DIGITS = str.maketrans('0123456789', '٠١٢٣٤٥٦٧٨٩')


def juz_pages(j):
    """First and last Madani page of juz j (1..30)."""
    if j == 1:
        return 1, 21
    if j == 30:
        return 582, 604
    start = 22 + 20 * (j - 2)
    return start, start + 19


def juz_of_page(p):
    for j in range(1, 31):
        a, b = juz_pages(j)
        if a <= p <= b:
            return j
    return 30


def surah_of_page(p):
    idx = 0
    for i, s in enumerate(SURAHS):
        if s[3] <= p:
            idx = i
    return idx + 1


def surah_list():
    return [dict(n=i + 1, ar=a, en=e, ayahs=n, page=p) for i, (a, e, n, p) in enumerate(SURAHS)]


def ar_num(n):
    return str(n).translate(AR_DIGITS)

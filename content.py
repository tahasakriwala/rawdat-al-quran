"""Everything the public site says. Text is taken from rawdatalquran.com; media lists live in data/*.json."""
import json
import os
from functools import lru_cache

BASE = os.path.dirname(os.path.abspath(__file__))
UPLOADS_MARK = '/wp-content/uploads/'

SCHOOL = dict(
    name='Rawdat al-Quran al-Kareem',
    name_ar='روضة القرآن الكريم',
    short='Rawdat',
    tagline='A Dynamic Approach to Learning',
    parent='Mahad al-Zahra · Aljamea-tus-Saifiyah',
    address=['1st and 2nd floor, Khatau Mansion', 'Oomer Park, Warden Road', 'Mumbai 400026', 'India'],
    phone='022-23620551 / 2 / 3',
    phone_href='+912223620551',
    map_embed='https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3773.235500710495!2d72.80222951489951!3d18.965204087151534!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3be7ce757ea30593%3A0xd7017a0ecd251ba7!2sRAWDAT+AL-QURAN!5e0!3m2!1sen!2s!4v1542040177687',
    map_link='https://maps.google.com/?q=RAWDAT+AL-QURAN+Warden+Road+Mumbai',
    links=dict(
        fees='https://fees.easebuzz.in/view/RawdatOCLPV',
        reports='http://www.rawdatalquran.com/reports/login.php',
        webmail='https://rawdatalquran.com/webmail',
        tahfeez_portal='https://script.google.com/macros/s/AKfycby47W5GbXR-tZPip8uiRFqLr6ptDEu316vRw-owBkR44VPqOLQnMgjMzX5EMlplDG1Z/exec',
    ),
    timings=dict(hifz=('07:30', '08:45'), school=('08:30', '15:10'), lunch=('13:30', '13:50')),
    class_size='18 – 20 students per class',
)

AYAH_14_24 = dict(
    ar='أَلَمْ تَرَ كَيْفَ ضَرَبَ اللَّهُ مَثَلًا كَلِمَةً طَيِّبَةً كَشَجَرَةٍ طَيِّبَةٍ أَصْلُهَا ثَابِتٌ وَفَرْعُهَا فِي السَّمَاءِ',
    en='See how Allah coins a similitude: A Kalemah Tayyebah (a good word) is like a good tree, its root set firm, its branches reaching into heaven.',
    ref='14:24',
)

ACHIEVEMENTS = [
    dict(value='26', label='Haafiz', note='students who have completed hifz al-Quran'),
    dict(value='14', label='Mathlathon Toppers', note='top ranks in the Mathlathon'),
    dict(value='Award', label='Best Innovative School', note='in Child Development'),
]

HOME_ABOUT = [
    'Rawdat al-Quran al-Kareem, a beginning of a new academic programme initiated by Mahad al-Zahra dedicated to the education of al-Quran al-Kareem. It is befitting that this programme should make its home in the city adorned by Rawdat Taherah, the mausoleum of al-Dai al-Ajal Syedna Taher Saifuddin RA wherein lies the entire Quran engraved upon marble slabs embellished with gold and precious stones.',
    'Keeping in line with Aljamea-tus-Saifiyah’s philosophy of combining revered, past traditions with what is contemporary and beneficial to the cause of education, Mahad al-Zahra has over the years developed various methods to aid in the memorisation, learning and teaching of al-Quran al-Kareem for members of the Dawoodi Bohra community of all ages and backgrounds. Rawdat al-Quran al-Kareem is founded upon a unique pedagogy developed by Mahad al-Zahra specifically for children from the ages of four to twelve.',
]

WHY = [
    'At Rawdat al-Quran al-Kareem, learning is through understanding. Our endeavor is to initiate scholastic progression through vibrant and dynamic teaching methodologies based on thematic instruction, wherein every learner becomes a keen and enthusiastic partaker in the learning process. In simple words, a theme acts as “conceptual glue” for the learners, providing an environment that fosters and encourages process learning and active involvement of all learners. Learners learn through different modes, styles and multiple intelligences.',
    'The Theme or Central idea is derived from al-Quran, which acts as a pivot of Learning Centre, connecting knowledge of all disciplines into a bigger picture.',
]

ACTIVITIES = 'Mahad al-Zahra enjoys a rich history of academic and cultural experiences. In keeping with its ideology, Rawdat al-Quran al-Kareem will become a unique educational centre for young learners. Here the child’s academic and personal growth will be enhanced through the teachings of al-Quran al-Kareem. This pedagogy integrates many values, the foremost being that a Mumin’s child is nurtured in an environment of faith and wisdom. A unique curriculum has been designed under which the child will be taught to develop his/her physical, mental and emotional acumen.'

CAMPUS = 'Rawdat’s commitment to enhance learning is also evident in the environment created by the infrastructure. A quick walk through the corridors will give the visitor a sense of the school culture. Soothing colors soothe senses, state of the art classrooms equipped with varied, age appropriate resources ensure a hands on and minds on experience for the students. Although we stress on experiencing concepts live, every class is equipped with a projector as well. Shelves adorn books related to units of study. The imperfect, hand made charts encourage to pursue and make mistakes to learn. The newly built library grows its collection for every child, and the ratio keeps increasing every year.'

CAMPUS_FEATURES = [
    ('Soothing colours', 'Palettes chosen to calm the senses and settle young minds.'),
    ('Hands on, minds on', 'Age-appropriate resources in every classroom for experiential learning.'),
    ('A projector in every class', 'Concepts are lived first, then extended on screen.'),
    ('Shelves for every unit', 'Books related to each unit of study, within reach.'),
    ('Handmade charts', 'Imperfect by design, so children feel free to try, err and learn.'),
    ('A growing library', 'Newly built, with more books per child every year.'),
]

ABOUT = dict(
    founder_quote='I named it Mahad al-Zahra so that it may receive the barakat and blessings of Moulatona Fatema al-Zahra, to whom this Dawat is associated. The Mahad has been established in order to provide education of the science of recitation (in accordance with the laws of tajweed), to facilitate the memorisation of the Quran Majeed and to offer a means to study of its knowledge. It is also responsible for providing education regarding contemporary fields of knowledge and languages so as to highlight the all-encompassing nature of the Quran and the greatness of Islam. I thank Allah Ta’ala for it is through His grace that construction has begun and I pray to Him that studies within this institution begin soon and in accordance with my expectations.',
    founder_source='Excerpts from al-Kalemaat al-Nooraniyah 1397H',
    founder='al-Dai al-Ajal Syedna Mohammed Burhanuddin RA',
    vision=[
        'In 1381H/1961AD al-Dai al-Ajal Syedna Taher Saifuddin RA inaugurated the new campus of Aljamea-tus-Saifiyah in Surat. This educational re-orientation and new campus heralded a fresh chapter in the history of the academy. Proceeding with these developments, 52nd Dai, al-Dai al-Ajal Syedna Mohammed Burhanuddin RA widened the dimensions of teaching and learning. In 1396H/1976AD Syedna al-Dai al-Ajal RA established an institute for the study of Quranic Arts and Sciences known as “Mahad al-Zahra”. This institute served to facilitate accurate memorisation of al-Quran, and at the same time, aid students’ understanding of its underlying meanings and intricacies.',
        'In order to provide insight into Aljamea’s educational system and to allow younger children from the Dawoodi Bohra community to obtain the barakat that lies therein, Mahad al-Zahra – Aljamea-tus-Saifiyah with the raza Mubarak of al-Dai al-Ajal Syedna Mohammed Burhanuddin RA and Syedna Aali Qadr Mufaddal Saifuddin TUS has launched a new centre for learning in Mumbai intended for children aged between four and twelve.',
        'It is befitting that this programme makes its home in the city adorned by Rawdat Taherah, the mausoleum of al-Dai al-Ajal Syedna Taher Saifuddin RA wherein lies the entire Quran engraved upon marble slabs embellished with gold and precious stones.',
        'So, keeping in line with Aljamea-tus-Saifiyah’s philosophy of combining revered, past traditions with what is contemporary and beneficial to the cause of education, Mahad al-Zahra has over the years developed various methods to aid in the memorisation, learning and teaching of al-Quran al-Kareem for members of the Dawoodi Bohra community of all ages and backgrounds.',
        'Rawdat al-Quran al-Kareem is founded upon a unique pedagogy developed by Mahad al-Zahra specifically for younger children. At Rawdat al-Quran al-Kareem, a student along with committing the Quran to memory, will simultaneously be exposed to all those forms of knowledge that branch from the Quran and are important for his development at that particular age. Year after year, he will develop academically, culturally and socially so as to achieve what Allah Ta’ala has portrayed in the following aayat kareemah:',
    ],
    belief=[
        'At Rawdat al-Quran al-Kareem, we believe in the immense energy, virtue and skills each child offers to the class. Each child is a subject that has to be studied the same way Math, Science or English has to be studied. Thus, the role of a Rawdat al-Quran teacher and its curriculum is to understand each child and provide an environment of R.E.L.A.X — Respect, Empathy, Love and Appreciation. This would eventually lead to the discovery of the X factor of each child.',
        'Al-Quran al-Kareem is the pivot around which our curriculum revolves. Memorizing al-Quran and cultivating infinite love for its values are at the very core. Our curriculum implies modern and traditional pedagogy to facilitate conceptual understanding and skill building in all subject areas. Experiential, hands on and minds on activities that include field trips engage students in the learning process and empower them to take charge of their learning and monitor their own progress.',
        'Subjects like Sports, Art, Handwork, Band, Zikre Husain and Cooking are a part of mainstream curricula. They give students a creative space and medium for self expression while equipping them with life skills, team work and collaboration. They instill a sense of accomplishment, relaxation and providing relaxing variation in the day.',
    ],
    smile='All this and more eventually sum up in a very simple way, a beautiful smile on each lovely innocent face. The smile that speaks a thousand words. The smile that connotes an insatiable love for learning. The smile that tells us “Yes, we are blossoming into lovely flowers”.',
)

RELAX = [
    ('R', 'Respect', 'احترام', 'Every child is honoured as a whole person, with a voice in the class.'),
    ('E', 'Empathy', 'تعاطف', 'Teachers study each child the way one studies a subject: closely and with care.'),
    ('L', 'Love', 'محبة', 'Infinite love for al-Quran and its values sits at the very core.'),
    ('A', 'Appreciation', 'تقدير', 'Effort is noticed and celebrated, so confidence keeps growing.'),
    ('X', 'The X factor', 'الموهبة', 'The environment that lets each child’s unique gift come to light.'),
]

PRINCIPAL_MESSAGE = [
    'It gives me immense joy to welcome you to our website and to share with you the spirit of Rawdat al-Quran al-Kareem—a place where every child grows, explores and discovers the world around them, finding meaning in the light of al-Quran al-Kareem.',
    'It is both a privilege and an honour for me to serve as the Principal of Rawdat al-Quran al-Kareem. As an educator, I have always believed that the true acquisition of knowledge is about nurturing minds, shaping character, inspiring curiosity, and helping every child discover their potential and purpose.',
    'At our school, al-Quran al-Majeed is at the heart of all that we do. It is the guiding light through which our students explore knowledge, make connections across subjects, and develop values, wisdom and a deeper understanding of the world around them.',
    'Our pedagogy encourages children to be curious and engaged learners—to think confidently, act with discipline, embrace creativity and innovation, and continually reflect upon their learning in the light of al-Quran al-Kareem and the teachings of Awliya Kiram. We believe that every child possesses unique potential, and it is our responsibility as educators to recognise and nurture that potential, providing an environment in which it can flourish.',
    'As we prepare our students for an ever-changing world, our endeavour remains steadfast: to nurture minds that think, hearts that care, and souls that remain deeply connected to al-Quran al-Majeed.',
]

# Curriculum, arranged as the Kalemah Tayyebah tree (14:24): roots, trunk, branches, leaves, fruit.
CURRICULUM = [
    dict(key='roots', part='Roots', part_ar='أصلها ثابت', title='Tahfeez al-Quran al-Kareem', ar='تحفيظ القرآن الكريم',
         blurb='The root set firm. Memorisation and recitation of al-Quran anchor every day, beginning with the morning Hifz class.',
         items=['Memorization of Quran', 'Tajweed', 'Tarteel', 'A’hkaam']),
    dict(key='trunk', part='Trunk', part_ar='الساق', title='Arabic & Islamic Studies', ar='اللغة العربية والدراسات الإسلامية',
         blurb='The trunk that carries the Quran’s language and knowledge up into every other subject.',
         items=['Arabic Language', 'Arabic Grammar', 'Uloom al-Quran', 'Fiqeh', 'Akhbar', 'Adab', 'Tadreeb', 'Dirasat Islamiyah']),
    dict(key='branches', part='Branches', part_ar='وفرعها في السماء', title='Core Academics', ar='المواد الأكاديمية',
         blurb='Branches reaching outward: an internationally benchmarked Cambridge programme, taught thematically around a Quranic central idea.',
         items=['Cambridge English', 'Cambridge Science', 'Cambridge Mathematics', 'Cambridge Economics', 'Cambridge Environmental Studies',
                'Cambridge Global Perspectives', 'Cambridge Business Studies', 'Scholastic Mathematics', 'Cambridge Art & Design']),
    dict(key='leaves', part='Leaves', part_ar='الأوراق', title='Wellbeing & Learning Habits', ar='العادات والرفاهية',
         blurb='The leaves that breathe: daily rhythms for reading, movement, play and social-emotional growth.',
         items=['SEL', 'Dear Time', 'Reading Program 1-1', 'Movement', 'Garden Time', 'Free Play']),
    dict(key='blossoms', part='Blossoms', part_ar='الأزهار', title='Co-Curricular Activities', ar='الأنشطة المصاحبة',
         blurb='Blossoms of self-expression, building life skills, teamwork and confidence.',
         items=['English Public Speaking', 'Arabic Public Speaking', 'Art', 'Wood work', 'Calligraphy', 'Cooking',
                'Basket Ball / Football / Table Tennis', 'Hand work']),
    dict(key='fruit', part='Fruit', part_ar='الثمار', title='Learning Beyond Walls', ar='التعلم خارج الفصل',
         blurb='The fruit that is shared: trips and khidmat that carry learning out into the world.',
         items=['EDU Field Trip', 'Outdoor Trip', 'Beach Cleanups']),
]
OTHER_INFO = [
    ('Additional languages', 'Hindi · Marathi'),
    ('Strength', '18 – 20 students per class'),
    ('School time', '8:30 am to 3:10 pm'),
    ('Morning Hifz class', '7:30 am to 8:45 am'),
    ('Lunch time', '1:30 pm to 1:50 pm'),
]

# "A day at Rawdat": only the times the school publishes are fixed; labels between them describe the published programme.
DAY = [
    ('07:30', '08:45', 'Morning Hifz class', 'حلقة الحفظ', 'Sabaq, revision and recitation before the day begins.'),
    ('08:30', '13:30', 'Learning blocks', 'الدروس', 'Thematic Cambridge academics and Arabic & Islamic studies around the central idea.'),
    ('13:30', '13:50', 'Lunch time', 'الغداء', 'A shared meal, with adab at the table.'),
    ('13:50', '15:10', 'Afternoon programme', 'الأنشطة', 'Co-curriculars, reading, movement and garden time.'),
]

ADMISSION = dict(
    intro=[
        'Rawdat al-Quran al-Kareem School welcomes all learners who identify with the vision, mission and philosophy of the school as part of its family and are looking closely at the exciting opportunities available here.',
        'Learners are ordinarily eligible for admission to Rawdat al-Quran al-Kareem only if they satisfy the school’s age criteria. Admission into the educational programme at Junior KG level is therefore based on learner’s age as on 1st June, that is four years and above.',
    ],
    steps=[
        ('Secure the Admission Kit', 'The Admissions Office will be happy to assist you to understand the admission process which begins when you secure the Admission Kit, comprising detailed information on school policies and processes.'),
        ('Submit the application', 'Once you have read and understood the documents in the Admission Kit, submit the complete Application for Admission form to the Admission Office along with all the required documents.'),
        ('Parent interaction', 'The Admission Panel invites parents to interact with the panel.'),
        ('An hour of fun activities', 'The Admission Panel invites your child for an hour of fun activities.'),
        ('Decision in 4–6 weeks', 'Within 4–6 weeks of the interaction, you will be notified via telephone and email if your child has been granted admission.'),
        ('Confirm the seat', 'Confirm the seat by paying the applicable fees as advised by the Admissions Office within 5 working days. Your fee receipt confirms your child’s admission.'),
    ],
)

FOOTER_LINKS = [('Admission', 'site.admissions'), ('Achievements', 'site.about'), ('Projects', 'site.events'), ('Visit us', 'site.contact')]


@lru_cache(maxsize=None)
def data(name):
    with open(os.path.join(BASE, 'data', f'{name}.json'), encoding='utf-8') as f:
        return json.load(f)


def local_media_path(url):
    if not url or UPLOADS_MARK not in url:
        return None
    return 'media/' + url.split(UPLOADS_MARK, 1)[1]


@lru_cache(maxsize=4096)
def media_exists(rel):
    return os.path.exists(os.path.join(BASE, 'static', rel))

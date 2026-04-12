"""
Seed leadership rows from the previously hardcoded LeadershipView data.
Idempotent — skips if rows already exist.
"""
import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select
from app.database import AsyncSessionLocal
from app.models.leader import Leader


LEADERS = [
    # ── Rector ──
    dict(group="rector", sort_order=0,
         name_uz="Akmal Rahimov", name_ru="Акмаль Рахимов", name_en="Akmal Rahimov",
         position_uz="Rektor", position_ru="Ректор", position_en="Rector",
         degree_uz="Pedagogika fanlari doktori",
         degree_ru="Доктор педагогических наук",
         degree_en="Doctor of Pedagogical Sciences",
         bio_uz="25 yillik ta'lim sohasidagi tajribaga ega. 100+ ilmiy maqola va 8 ta monografiya muallifi.",
         bio_ru="Имеет 25-летний опыт в сфере образования. Автор более 100 научных статей и 8 монографий.",
         bio_en="Has 25 years of experience in education. Author of 100+ scientific articles and 8 monographs.",
         email="rektor@xiuedu.uz", phone="+998 71 200 00 00",
         photo="https://picsum.photos/seed/xiu-rector/600/750"),

    # ── Prorectors ──
    dict(group="prorector", sort_order=1,
         name_uz="Dilnoza Karimova", name_ru="Дильноза Каримова", name_en="Dilnoza Karimova",
         position_uz="Birinchi prorektor", position_ru="Первый проректор", position_en="First vice-rector",
         degree_uz="Iqtisodiyot fanlari nomzodi",
         degree_ru="Кандидат экономических наук",
         degree_en="PhD in Economics",
         bio_uz="Universitet strategik rivojlanish va akademik sifat bo'yicha ekspert.",
         bio_ru="Эксперт по стратегическому развитию университета и академическому качеству.",
         bio_en="Expert in university strategic development and academic quality.",
         email="d.karimova@xiuedu.uz", phone="+998 71 200 00 02"),
    dict(group="prorector", sort_order=2,
         name_uz="Sherzod Tursunov", name_ru="Шерзод Турсунов", name_en="Sherzod Tursunov",
         position_uz="Ilm-fan ishlari bo'yicha prorektor",
         position_ru="Проректор по научной работе",
         position_en="Vice-rector for research",
         degree_uz="Fizika-matematika fanlari doktori",
         degree_ru="Доктор физико-математических наук",
         degree_en="Doctor of Physical and Mathematical Sciences",
         bio_uz="80+ ilmiy maqola muallifi. AI va ma'lumotlar fanlari bo'yicha xalqaro grantlar yutgan.",
         bio_ru="Автор 80+ научных статей. Получил международные гранты по AI и наукам о данных.",
         bio_en="Author of 80+ scientific articles. Won international grants in AI and data science.",
         email="s.tursunov@xiuedu.uz", phone="+998 71 200 00 03"),
    dict(group="prorector", sort_order=3,
         name_uz="Jasur Aliyev", name_ru="Жасур Алиев", name_en="Jasur Aliyev",
         position_uz="Xalqaro hamkorlik bo'yicha prorektor",
         position_ru="Проректор по международному сотрудничеству",
         position_en="Vice-rector for international affairs",
         degree_uz="Xalqaro munosabatlar nomzodi",
         degree_ru="Кандидат наук по международным отношениям",
         degree_en="PhD in International Relations",
         bio_uz="50+ xalqaro hamkorlik shartnomalari ishtirokchisi. Erasmus+ va DAAD dasturlari koordinatori.",
         bio_ru="Участник 50+ международных соглашений. Координатор программ Erasmus+ и DAAD.",
         bio_en="Participant in 50+ international cooperation agreements. Coordinator of Erasmus+ and DAAD programs.",
         email="j.aliyev@xiuedu.uz", phone="+998 71 200 00 04"),

    # ── Deans ──
    dict(group="dean", sort_order=4,
         name_uz="Nodira Yusupova", name_ru="Нодира Юсупова", name_en="Nodira Yusupova",
         position_uz="Pedagogika fakulteti dekani",
         position_ru="Декан педагогического факультета",
         position_en="Dean of the Faculty of Pedagogy",
         degree_uz="Pedagogika fanlari nomzodi",
         degree_ru="Кандидат педагогических наук",
         degree_en="PhD in Pedagogy",
         bio_uz="Pedagogika sohasida 20 yillik tajriba, zamonaviy ta'lim metodikalari muallifi.",
         bio_ru="20-летний опыт в педагогике, автор современных образовательных методик.",
         bio_en="20 years of experience in pedagogy, author of modern educational methodologies.",
         email="n.yusupova@xiuedu.uz", phone="+998 71 200 00 12"),
    dict(group="dean", sort_order=5,
         name_uz="Botir Jo'rayev", name_ru="Ботир Жураев", name_en="Botir Jo'rayev",
         position_uz="Iqtisodiyot fakulteti dekani",
         position_ru="Декан экономического факультета",
         position_en="Dean of the Faculty of Economics",
         degree_uz="MBA, xalqaro biznes mutaxassisi",
         degree_ru="MBA, специалист по международному бизнесу",
         degree_en="MBA, international business specialist",
         bio_uz="AQSH va Yevropa biznes maktablarida tajriba olgan, 12 ta startupga maslahatchi.",
         bio_ru="Опыт в бизнес-школах США и Европы, консультант 12 стартапов.",
         bio_en="Experience at US and European business schools, consultant to 12 startups.",
         email="b.jurayev@xiuedu.uz", phone="+998 71 200 00 14"),
    dict(group="dean", sort_order=6,
         name_uz="Malika Rasulova", name_ru="Малика Расулова", name_en="Malika Rasulova",
         position_uz="Filologiya fakulteti dekani",
         position_ru="Декан филологического факультета",
         position_en="Dean of the Faculty of Philology",
         degree_uz="Lingvistika doktori",
         degree_ru="Доктор лингвистических наук",
         degree_en="Doctor of Linguistics",
         bio_uz="15 ta tilni biladi, Cambridge English Examiner.",
         bio_ru="Владеет 15 языками, экзаменатор Cambridge English.",
         bio_en="Speaks 15 languages, Cambridge English Examiner.",
         email="m.rasulova@xiuedu.uz", phone="+998 71 200 00 16"),

    # ── Department heads ──
    dict(group="department_head", sort_order=7,
         name_uz="Aziz Sobirov", name_ru="Азиз Собиров", name_en="Aziz Sobirov",
         position_uz="Boshlang'ich ta'lim kafedrasi mudiri",
         position_ru="Заведующий кафедрой начального образования",
         position_en="Head of the Department of Primary Education",
         degree_uz="Pedagogika fanlari nomzodi",
         degree_ru="Кандидат педагогических наук",
         degree_en="PhD in Pedagogy",
         bio_uz="", bio_ru="", bio_en="",
         email="a.sobirov@xiuedu.uz"),
    dict(group="department_head", sort_order=8,
         name_uz="Gulnoza Xasanova", name_ru="Гульноза Хасанова", name_en="Gulnoza Xasanova",
         position_uz="Lingvistika kafedrasi mudiri",
         position_ru="Заведующая кафедрой лингвистики",
         position_en="Head of the Department of Linguistics",
         degree_uz="Tarjimashunoslik bo'yicha mutaxassis",
         degree_ru="Специалист по переводоведению",
         degree_en="Translation studies specialist",
         bio_uz="", bio_ru="", bio_en="",
         email="g.xasanova@xiuedu.uz"),
    dict(group="department_head", sort_order=9,
         name_uz="Olimjon Karimov", name_ru="Олимжон Каримов", name_en="Olimjon Karimov",
         position_uz="Menejment kafedrasi mudiri",
         position_ru="Заведующий кафедрой менеджмента",
         position_en="Head of the Department of Management",
         degree_uz="Menejment fanlari nomzodi",
         degree_ru="Кандидат наук по менеджменту",
         degree_en="PhD in Management",
         bio_uz="", bio_ru="", bio_en="",
         email="o.karimov@xiuedu.uz"),
    dict(group="department_head", sort_order=10,
         name_uz="Saida Mahmudova", name_ru="Саида Махмудова", name_en="Saida Mahmudova",
         position_uz="Ingliz tili kafedrasi mudiri",
         position_ru="Заведующая кафедрой английского языка",
         position_en="Head of the Department of English",
         degree_uz="Filologiya nomzodi (ingliz tili)",
         degree_ru="Кандидат филологических наук (английский)",
         degree_en="PhD in English Philology",
         bio_uz="", bio_ru="", bio_en="",
         email="s.mahmudova@xiuedu.uz"),
]


async def main():
    async with AsyncSessionLocal() as session:
        existing = (await session.execute(select(Leader))).first()
        if existing:
            print("Leaders already seeded — skipping")
            return
        for data in LEADERS:
            session.add(Leader(enabled=True, **data))
        await session.commit()
        print(f"Seeded {len(LEADERS)} leaders")


if __name__ == "__main__":
    asyncio.run(main())

import asyncio
from services import AsyncSessionLocal
from models import Category, Product

async def seed_data():
    async with AsyncSessionLocal() as session:
        # Создаём категории
        drinks = Category(name="Напитки", slug="drinks")
        alco = Category(name="Алкоголь", slug="alcohol")
        sigs = Category(name="Сигареты", slug="cigarettes")
        tea = Category(name="Чай / кофе", slug="tea")
        crups = Category(name="Крупы", slug="cereals")
        fabrics = Category(name="Полуфабрикаты", slug="semi_finished_products")
        conservs = Category(name="Консервы", slug="canned_goods")
        noodle = Category(name="Лапша / Макароны", slug="noodles")
        bread = Category(name="Хлеб", slug="bread")
        butter = Category(name="Масло", slug="butter")
        vegs = Category(name="Овощи", slug="vegetables")

        session.add_all([drinks, alco, sigs, tea, crups, fabrics, conservs, noodle, bread, butter, vegs])
        await session.commit()

        # Создаём товары
        products = [
            Product(name="Coca-Cola 1.5 литра", price=12500, category_id=drinks.id, photo_url="https://..."),
            Product(name="Fanta 1.5 литра", price=14000, category_id=drinks.id),
            Product(name="Pepsi 1.5 литра", price=13000, category_id=drinks.id),
            Product(name="Минеральная вода Hydrolife 1.5 литра", price=3000, category_id=drinks.id),
            Product(name="Квас Боярский 1.5 литра", price=6000, category_id=drinks.id),

            Product(name="Виски Johnny Walker Red label 40% 500ml", price=550000, category_id=alco.id),
            Product(name="Виски White Horse 40% 750ml", price=800000, category_id=alco.id),
            Product(name="Водка Ташкент 500ml", price=55000, category_id=alco.id),

            Product(name="Pall Mall синий", price=13000, category_id=sigs.id),
            Product(name="Kent Original", price=20000, category_id=sigs.id),
            Product(name="Lucky strike original blue", price=13000, category_id=sigs.id),

            Product(name="Maccoffee original 150 гр", price=45000, category_id=tea.id),
            Product(name="Кофе Jacobs Monarch 500 гр", price=150000, category_id=tea.id),
            Product(name="Чай Ташкент черный оригинальный 100 гр", price=13000, category_id=tea.id),

            Product(name="Сахар песок 1 кг", price=12000, category_id=crups.id),
            Product(name="Рис Аланга 1 кг", price=12000, category_id=crups.id),
            Product(name="Гречка 1 кг", price=15000, category_id=crups.id),
            Product(name="Соль крупная йодированная 1 кг", price=3000, category_id=crups.id),

            Product(name="Пельмени Makiz из говядины 500 гр", price=20000, category_id=fabrics.id),
            Product(name="Котлеты из мраморной говядины 500 гр", price=55000, category_id=fabrics.id),

            Product(name="Алтайская говядина 525 гр", price=55000, category_id=conservs.id),
            Product(name="Сардинелла Caija 240 гр", price=18000, category_id=conservs.id),
            Product(name="Килька балтийская 240 гр", price=10000, category_id=conservs.id),

            Product(name="Макароны макфа 400 гр", price=8000, category_id=noodle.id),
            Product(name="Лапша Doshirak говядина 90 гр", price=7000, category_id=noodle.id),

            Product(name="Буханка хлеба 400 гр", price=3000, category_id=bread.id),
            Product(name="Патыр 500 гр", price=6000, category_id=bread.id),
            Product(name="Патыр 350 гр", price=4000, category_id=bread.id),

            Product(name="Масло хлопковое рафинированное Lazzat 1000 мл", price=14000, category_id=butter.id),
            Product(name="Масло растительное Щедрое лето 1 л.", price=20000, category_id=butter.id),

            Product(name="Картофель 1 кг", price=5000, category_id=vegs.id),
            Product(name="Морковь желтая 1 кг", price=6000, category_id=vegs.id),
        ]

        session.add_all(products)
        await session.commit()
        print("✅ Данные добавлены")

if __name__ == "__main__":
    asyncio.run(seed_data())
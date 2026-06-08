import random
from sqlalchemy.orm import Session
from app.config import SessionLocal, engine, Base
from app.countries.models import Country
from app.categories.models import Category
from app.clients.models import Client

def seed_database():
    print("Starting database seeding...")

    db = SessionLocal()

    try:
        Base.metadata.create_all(bind=engine)

        country_names = ["Colombia", "Mexico", "España", "Argentina"]
        created_countries = []
        for name in country_names:
            country = db.query(Country).filter(Country.name == name).first()
            if not country:
                country = Country(name=name)
                db.add(country)
                db.flush()
            created_countries.append(country)
        
        category_names = ["Premium", "Regular", "VIP", "Wholesaler"]
        created_categories = []
        for name in category_names:
            category = db.query(Category).filter(Category.name == name).first()
            if not category:
                category = Category(name=name)
                db.add(category)
                db.flush()
            created_categories.append(category)

        db.commit()

        if db.query(Client).count() == 0:
            cities = ["Bogota", "Medellin", "Guadalajara", "Ciudad de Mexico", "Barcelona", "Madrid", "Buenos Aires", "Cordoba"]
            sample_names = [
                "Andres Gonzalez", "Carlos Cubillos", "Karen Escalante", "Johan Caicedo", "Diana Gomez",
                "Sharick Martinez", "Alexa Jimenez", "Mateo Urbano", "Camila Torres", "Edwin Moron"
            ]

            print("Generating 30 sample clients...")
            for i in range(1, 31):
                client_name = f"{random.choice(sample_names)} {i}"
                random_city = random.choice(cities)
                random_country = random.choice(created_countries)
                random_category = random.choice(created_categories)

                new_client = Client(
                    name_client = client_name,
                    city = random_city,
                    user_created = "admin_seed",
                    is_active = True,
                    country_id = random_country.id,
                    category_id = random_category.id
                )
                db.add(new_client)

            db.commit()
            print("Successfully inserted 30 sample clients")
        else:
            print("Database already contains clients. Skipping client creation.")

    except Exception as e:
        print(f"An error ocurred during seeding: {e}")
        db.rollback()
    finally:
        db.close()
        print("Seeding process finished.")

if __name__ == "__main__":
    seed_database()
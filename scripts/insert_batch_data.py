# scripts/insert_batch_data.py
import sys, os, random, uuid
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.app import db, models
from passlib.context import CryptContext

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

session = db.SessionLocal()

def create_user(email, password, user_type, full_name):
    hashed = pwd_ctx.hash(password)
    u = models.User(email=email, password_hash=hashed, user_type=user_type, full_name=full_name)
    session.add(u)
    session.flush()  # get id
    return u

def create_property_for_seller(seller_id, name, city_id, area_sqft, bhk, listing_score, is_furnished):
    prop = models.Property(
        seller_id=seller_id,
        property_name=name,
        city_id=city_id,
        area_sqft=area_sqft,
        bhk=bhk,
        listing_score=listing_score,
        is_furnished=is_furnished
    )
    session.add(prop)
    session.flush()
    return prop

def create_favourite(user_id, property_id):
    fav = models.Favourite(user_id=user_id, property_id=property_id)
    session.add(fav)

def random_city():
    return random.choice([1,2,3,4,5,6,7])

def main(num_sellers=20, props_per_seller=5, num_buyers=200, favs_per_buyer=3):
    try:
        created_sellers = []
        for i in range(num_sellers):
            email = f"seller{i+1}@example.com"
            u = create_user(email, "Test1234", "seller", f"Seller {i+1}")
            created_sellers.append(u.id)

        created_props = []
        for sid in created_sellers:
            for j in range(props_per_seller):
                name = f"Sample {uuid.uuid4().hex[:6]} by seller {sid}"
                city = random_city()
                area = random.randint(400, 3000)
                bhk = random.choice([1,2,3,4])
                score = round(random.uniform(5.0, 9.0), 1)
                is_f = random.choice([True, False])
                p = create_property_for_seller(sid, name, city, area, bhk, score, is_f)
                created_props.append(p.id)

        created_buyers = []
        for b in range(num_buyers):
            email = f"buyer{b+1}@example.com"
            u = create_user(email, "Test1234", "buyer", f"Buyer {b+1}")
            created_buyers.append(u.id)

        # favourites
        for buyer_id in created_buyers:
            favs = random.sample(created_props, min(favs_per_buyer, len(created_props)))
            for pid in favs:
                create_favourite(buyer_id, pid)

        session.commit()
        print(f"Inserted: sellers={len(created_sellers)}, properties={len(created_props)}, buyers={len(created_buyers)}")
    except Exception as e:
        session.rollback()
        print("Error:", e)
    finally:
        session.close()

if __name__ == "__main__":
    # Defaults match recommended medium test
    main(num_sellers=20, props_per_seller=5, num_buyers=200, favs_per_buyer=3)

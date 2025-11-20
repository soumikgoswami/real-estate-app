import sys
import os

# Ensure project root is on sys.path so `backend` package can be imported
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.app import db, models

session = db.SessionLocal()
try:
    sample = [
        dict(property_name='Luxury 3BHK in Koramangala', city_id=1, area_sqft=1500, bhk=3, is_furnished=True, listing_score=8.5),
        dict(property_name='Cozy 2BHK in T. Nagar', city_id=2, area_sqft=900, bhk=2, is_furnished=False, listing_score=7.0),
        dict(property_name='Spacious 4BHK in Dwarka', city_id=3, area_sqft=2200, bhk=4, is_furnished=True, listing_score=8.0),
        dict(property_name='Compact 1BHK in Banjara Hills', city_id=4, area_sqft=600, bhk=1, is_furnished=False, listing_score=6.5),
        dict(property_name='Family 3BHK in Andheri West', city_id=7, area_sqft=1400, bhk=3, is_furnished=True, listing_score=7.8),
    ]

    created = []
    for p in sample:
        prop = models.Property(**p)
        session.add(prop)
        session.flush()
        created.append(prop.id)
    session.commit()
    print('Inserted properties with IDs:', created)
except Exception as e:
    session.rollback()
    print('Error inserting sample properties:', e)
finally:
    session.close()

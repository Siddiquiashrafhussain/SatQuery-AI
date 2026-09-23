import os
import sys

# Add backend to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.domain import Base, Scene, ScenePair, User
from app.core.config import settings
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed_demo_data():
    print(f"Seeding demo data into {settings.DATABASE_URL}")
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # 1. Create a demo user if not exists
        user = db.query(User).filter(User.email == "demo@satquery.ai").first()
        if not user:
            user = User(
                email="demo@satquery.ai",
                hashed_password=pwd_context.hash("demo123")
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            print("Demo user created: demo@satquery.ai")
            
        # 2. Add sample Optical Scene
        scene1 = db.query(Scene).filter(Scene.filename == "demo_optical_1.tif").first()
        if not scene1:
            from geoalchemy2.elements import WKTElement
            scene1 = Scene(
                user_id=user.id,
                filename="demo_optical_1.tif",
                storage_path="/app/storage/demo_optical_1.tif",
                sensor_type="optical",
                crs="EPSG:4326",
                bounds=WKTElement("POLYGON((0 0, 10 0, 10 10, 0 10, 0 0))", srid=4326),
                provider_id="S2A_MSIL2A_20230101"
            )
            db.add(scene1)
            db.commit()
            print("Demo Optical Scene seeded.")
            
        # 3. Add sample SAR Scene
        scene2 = db.query(Scene).filter(Scene.filename == "demo_sar_1.tif").first()
        if not scene2:
            from geoalchemy2.elements import WKTElement
            scene2 = Scene(
                user_id=user.id,
                filename="demo_sar_1.tif",
                storage_path="/app/storage/demo_sar_1.tif",
                sensor_type="sar",
                crs="EPSG:4326",
                bounds=WKTElement("POLYGON((0 0, 10 0, 10 10, 0 10, 0 0))", srid=4326),
                provider_id="S1A_IW_GRDH_20230101"
            )
            db.add(scene2)
            db.commit()
            print("Demo SAR Scene seeded.")
            
        print("Demo seeding complete!")
        
    except Exception as e:
        db.rollback()
        print(f"Error seeding data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_demo_data()

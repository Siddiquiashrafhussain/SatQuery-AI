import sys
import os
from sqlalchemy.orm import Session
from datetime import datetime

# Add the parent directory of backend to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.api.deps import SessionLocal
from app.models.domain import User, Scene
from app.core import security
from geoalchemy2.shape import from_shape
from shapely.geometry import box

def seed():
    db: Session = SessionLocal()
    
    # Check if user exists
    user = db.query(User).filter(User.email == "test@satquery.ai").first()
    if not user:
        user = User(
            email="test@satquery.ai",
            hashed_password=security.get_password_hash("password123")
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"Created user {user.email}")
    else:
        print(f"User {user.email} already exists")

    # Check if scene exists
    scene = db.query(Scene).filter(Scene.filename == "dummy_scene.tif").first()
    if not scene:
        geom = from_shape(box(0, 0, 10, 10), srid=4326)
        scene = Scene(
            user_id=user.id,
            filename="dummy_scene.tif",
            storage_path="/app/storage/dummy_scene.tif",
            crs="EPSG:4326",
            bounds=geom,
            bands=3,
            resolution=10.0
        )
        db.add(scene)
        db.commit()
        db.refresh(scene)
        print(f"Created dummy scene for {user.email}")
    else:
        print("Dummy scene already exists")

    db.close()

if __name__ == "__main__":
    seed()

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, JSON
from sqlalchemy.orm import declarative_base, relationship
from geoalchemy2 import Geometry

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    scenes = relationship("Scene", back_populates="owner")
    queries = relationship("Query", back_populates="owner")

class Scene(Base):
    __tablename__ = "scenes"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    filename = Column(String, nullable=False)
    storage_path = Column(String, nullable=False)
    crs = Column(String)
    bounds = Column(Geometry('POLYGON', srid=4326))
    bands = Column(Integer)
    resolution = Column(Float)
    preprocessing_status = Column(String, default="pending")
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    
    sensor_type = Column(String, default="optical")
    sar_polarization = Column(String, nullable=True)
    sar_acquisition_mode = Column(String, nullable=True)
    sar_incidence_angle = Column(Float, nullable=True)
    
    owner = relationship("User", back_populates="scenes")
    queries = relationship("Query", back_populates="scene")

class Query(Base):
    __tablename__ = "queries"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    scene_id = Column(Integer, ForeignKey("scenes.id"))
    query_text = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    owner = relationship("User", back_populates="queries")
    scene = relationship("Scene", back_populates="queries")
    analysis_results = relationship("AnalysisResult", back_populates="query")

class AnalysisResult(Base):
    __tablename__ = "analysis_results"
    id = Column(Integer, primary_key=True, index=True)
    query_id = Column(Integer, ForeignKey("queries.id"))
    result_text = Column(String, nullable=False)
    confidence_score = Column(Float)
    mask_path = Column(String, nullable=True)
    bounding_boxes = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    query = relationship("Query", back_populates="analysis_results")

class ScenePair(Base):
    __tablename__ = "scene_pairs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    before_scene_id = Column(Integer, ForeignKey("scenes.id"))
    after_scene_id = Column(Integer, ForeignKey("scenes.id"))
    coregistration_status = Column(String, default="pending")
    before_aligned_path = Column(String, nullable=True)
    after_aligned_path = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User")
    before_scene = relationship("Scene", foreign_keys=[before_scene_id])
    after_scene = relationship("Scene", foreign_keys=[after_scene_id])
    change_results = relationship("ChangeResult", back_populates="scene_pair")

class ChangeResult(Base):
    __tablename__ = "change_results"
    id = Column(Integer, primary_key=True, index=True)
    scene_pair_id = Column(Integer, ForeignKey("scene_pairs.id"))
    mask_path = Column(String, nullable=False)
    summary_text = Column(String, nullable=False)
    confidence = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    scene_pair = relationship("ScenePair", back_populates="change_results")

class ExecutionTrace(Base):
    __tablename__ = "execution_traces"
    id = Column(Integer, primary_key=True, index=True)
    query_id = Column(Integer, ForeignKey("queries.id"))
    plan_json = Column(JSON, nullable=False)
    steps_json = Column(JSON, nullable=False)
    verification_result_json = Column(JSON, nullable=True)
    total_latency_ms = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    query = relationship("Query")

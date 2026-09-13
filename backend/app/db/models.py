from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, JSON
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    
    # Relationships
    projects = relationship("Project", back_populates="owner")

class Project(Base):
    __tablename__ = "projects"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    owner_id = Column(String, ForeignKey("users.id"))
    name = Column(String)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    owner = relationship("User", back_populates="projects")
    jobs = relationship("AnalysisJob", back_populates="project")
    datasets = relationship("Dataset", back_populates="project")

class Dataset(Base):
    __tablename__ = "datasets"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, ForeignKey("projects.id"))
    filename = Column(String)
    modality = Column(String) # e.g., optical, sar
    crs = Column(String)
    width = Column(Integer)
    height = Column(Integer)
    bands = Column(Integer)
    acquisition_time = Column(DateTime, nullable=True)
    storage_path = Column(String)
    
    # Future Phase: PostGIS Integration
    # boundary = Column(Geometry('POLYGON', srid=4326))
    
    # Relationships
    project = relationship("Project", back_populates="datasets")

class AnalysisJob(Base):
    __tablename__ = "analysis_jobs"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, ForeignKey("projects.id"))
    query = Column(String)
    task = Column(String)
    status = Column(String) # pending, running, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    project = relationship("Project", back_populates="jobs")
    steps = relationship("ExecutionStep", back_populates="job")
    result = relationship("AnalysisResult", back_populates="job", uselist=False)

class AnalysisResult(Base):
    __tablename__ = "analysis_results"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id = Column(String, ForeignKey("analysis_jobs.id"))
    answer = Column(String)
    confidence_score = Column(Float, nullable=True)
    confidence_reasoning = Column(String, nullable=True)
    evidence = Column(JSON, nullable=True) # e.g., references to bounding boxes, masks
    spatial_outputs = Column(JSON, nullable=True)
    
    # Relationships
    job = relationship("AnalysisJob", back_populates="result")

class ExecutionStep(Base):
    __tablename__ = "execution_steps"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id = Column(String, ForeignKey("analysis_jobs.id"))
    step = Column(Integer) # Ordering sequence
    component = Column(String) # e.g., 'Query Understanding', 'Model Selection'
    status = Column(String)
    duration = Column(Float, nullable=True) # in seconds
    metadata_ = Column("metadata", JSON, nullable=True) # Alias to avoid conflicting with Base.metadata
    
    # Relationships
    job = relationship("AnalysisJob", back_populates="steps")

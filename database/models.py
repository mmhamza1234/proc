"""
Hamada Tool V2 - Database Models
SQLAlchemy models for the procurement system
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    filename = Column(String(255), nullable=False)
    original_name = Column(String(255), nullable=False)
    document_type = Column(String(100))  # tender, po, invoice, etc.
    upload_date = Column(DateTime, default=datetime.utcnow)
    processed = Column(Boolean, default=False)
    extracted_data = Column(Text)  # JSON string
    workflow_stage = Column(Integer, default=1)
    project_id = Column(Integer, ForeignKey('projects.id'))

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    client = Column(String(255))
    status = Column(String(100), default="active")
    current_stage = Column(Integer, default=1)
    estimated_value = Column(Float)
    deadline = Column(DateTime)
    created_date = Column(DateTime, default=datetime.utcnow)

    # Relationships
    documents = relationship("Document", backref="project")
    orders = relationship("Order", backref="project")

class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    contact_person = Column(String(255))
    email = Column(String(255))
    phone = Column(String(50))
    country = Column(String(100))
    specialization = Column(Text)
    rating = Column(Float, default=5.0)
    total_orders = Column(Integer, default=0)
    completed_orders = Column(Integer, default=0)
    created_date = Column(DateTime, default=datetime.utcnow)

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    supplier_id = Column(Integer, ForeignKey('suppliers.id'))
    order_number = Column(String(100), unique=True)
    status = Column(String(100), default="pending")
    total_amount = Column(Float)
    currency = Column(String(10), default="USD")
    order_date = Column(DateTime, default=datetime.utcnow)
    expected_delivery = Column(DateTime)

    # Relationships
    supplier = relationship("Supplier", backref="orders")

class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    supplier_id = Column(Integer, ForeignKey('suppliers.id'))
    subject = Column(String(255))
    body = Column(Text)
    sent_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default="sent")  # sent, delivered, read

class WorkflowStage(Base):
    __tablename__ = "workflow_stages"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    stage_number = Column(Integer, nullable=False)
    stage_name = Column(String(255), nullable=False)
    status = Column(String(50), default="pending")  # pending, in_progress, completed
    started_date = Column(DateTime)
    completed_date = Column(DateTime)
    notes = Column(Text)

# Database setup
def create_database():
    """Create database and tables"""
    database_url = os.getenv("DATABASE_URL", "sqlite:///hamada_tool.db")
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    return engine

def get_session():
    """Get database session"""
    engine = create_database()
    Session = sessionmaker(bind=engine)
    return Session()

if __name__ == "__main__":
    # Create database
    engine = create_database()
    print("✅ Database created successfully!")
    print(f"📊 Tables created: {list(Base.metadata.tables.keys())}")

from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    company = Column(String, nullable=True)
    account = Column(String, nullable=True)
    department = Column(String, nullable=True)
    role = Column(String, nullable=True)
    phone = Column(String, nullable=True, unique=True)
    notes = Column(String, nullable=True)


# Example SQLAlchemy engine and session creation
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

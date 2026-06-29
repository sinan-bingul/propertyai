"""
db models
"""

from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase 
from sqlalchemy import ForeignKey 
from datetime import datetime 

class Base(DeclarativeBase):
    pass 

class Documents(Base):
    __tablename__ = "documents"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    path: Mapped[str]
    upload_date: Mapped[datetime]

class DocumentChunks(Base):
    __tablename__ = "document_chunks"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id"))
    chunk: Mapped[str]
    page_number: Mapped[int]
    update_date: Mapped[datetime]

class DocumentProperties(Base):
    __tablename__ = "document_properties"

    id: Mapped[int] = mapped_column(primary_key=True)
    property_name: Mapped[str]
    property_value: Mapped[int]

    
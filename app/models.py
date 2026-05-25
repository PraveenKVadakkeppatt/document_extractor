from datetime import datetime
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy import Column,Integer,String,DateTime,ForeignKey,Float


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    filepath = Column(String(750),nullable=False)
    filetype = Column(String(50),nullable=False)
    status = Column(String(50),default="PENDING")
    error_message = Column(String(1000), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    purchase_order = relationship("PurchaseOrder", back_populates="document")



class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"))

    po_number = Column(String(100), nullable=True)
    vendor_details = Column(String(1000), nullable=True)
    order_date = Column(String(100), nullable=True)
    delivery_date = Column(String(100), nullable=True)
    deliver_to = Column(String(1000), nullable=True)

    document = relationship("Document",back_populates="purchase_order")
    line_items = relationship("LineItem", back_populates="purchase_order")



class LineItem(Base):
    __tablename__ = "line_items"

    id = Column(Integer, primary_key=True, index=True)
    purchase_order_id = Column(Integer, ForeignKey("purchase_orders.id"))

    item_name = Column(String(255), nullable=True)
    quantity = Column(Float, nullable=True)
    rate = Column(Float, nullable=True)
    tax_percent = Column(Float, nullable=True)
    tax_amount = Column(Float, nullable=True)
    total_amount = Column(Float, nullable=True)

    purchase_order = relationship("PurchaseOrder", back_populates="line_items")

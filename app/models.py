import datetime
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, 
    Text, DateTime, ForeignKey
)
from sqlalchemy.orm import relationship
from app.database import Base

class Customer(Base):
    """Customer entity tracking phone number, preferred language, and conversation state."""
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=True)
    address = Column(Text, nullable=True)
    language = Column(String(10), default="sd")  # 'sd' = Sindhi, 'ur' = Urdu, 'en' = English
    conversation_state = Column(String(50), default="IDLE")  # State machine tracker
    state_data = Column(Text, default="{}")  # JSON encoded data for multi-step flows
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships
    orders = relationship("Order", back_populates="customer", cascade="all, delete-orphan")
    messages = relationship("Message", back_populates="customer", cascade="all, delete-orphan")


class Product(Base):
    """Product catalog item with multilingual names, descriptions, and pricing."""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=False)
    name_sd = Column(String(150), nullable=False)  # Sindhi Name
    name_ur = Column(String(150), nullable=False)  # Urdu Name
    name_en = Column(String(150), nullable=False)  # English Name
    description_sd = Column(Text, nullable=True)
    description_ur = Column(Text, nullable=True)
    description_en = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    category = Column(String(100), default="General")
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Helper method for localized name
    def get_localized_name(self, lang: str = "sd") -> str:
        if lang == "sd" and self.name_sd:
            return self.name_sd
        elif lang == "ur" and self.name_ur:
            return self.name_ur
        return self.name_en or self.name_sd or self.name_ur

    def get_localized_description(self, lang: str = "sd") -> str:
        if lang == "sd" and self.description_sd:
            return self.description_sd
        elif lang == "ur" and self.description_ur:
            return self.description_ur
        return self.description_en or self.description_sd or self.description_ur


class Order(Base):
    """Customer order details and status lifecycle."""
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(50), unique=True, index=True, nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    customer_name = Column(String(100), nullable=False)
    customer_phone = Column(String(50), nullable=False)
    delivery_address = Column(Text, nullable=False)
    total_amount = Column(Float, default=0.0)
    status = Column(String(30), default="PENDING")  # PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED
    payment_method = Column(String(50), default="Cash on Delivery")
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships
    customer = relationship("Customer", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    """Items included in an order."""
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    product_name = Column(String(150), nullable=False)
    unit_price = Column(Float, nullable=False)
    quantity = Column(Integer, default=1)
    subtotal = Column(Float, nullable=False)

    # Relationship
    order = relationship("Order", back_populates="items")


class Message(Base):
    """Communication history log."""
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    phone_number = Column(String(50), nullable=False)
    direction = Column(String(20), nullable=False)  # INCOMING or OUTGOING
    message_type = Column(String(30), default="text")
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    customer = relationship("Customer", back_populates="messages")


class AgentHandoff(Base):
    """Requests initiated by users requiring human agent assistance."""
    __tablename__ = "agent_handoffs"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    customer_phone = Column(String(50), nullable=False)
    customer_name = Column(String(100), nullable=True)
    reason = Column(Text, nullable=True)
    status = Column(String(30), default="OPEN")  # OPEN, RESOLVED, CLOSED
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

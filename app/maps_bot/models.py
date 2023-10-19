from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    phone_number = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    is_deleted = Column(Integer, default=0)
    is_active = Column(Integer, default=1)
    is_admin = Column(Integer, default=0)
    is_super_admin = Column(Integer, default=0)
    is_email_verified = Column(Integer, default=0)
    is_phone_verified = Column(Integer, default=0)
    is_email_subscribed = Column(Integer, default=0)
    is_phone_subscribed = Column(Integer, default=0)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Lead(Base):
    __tablename__ = 'leads'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    score = Column(Float)
    number_of_opinions = Column(Integer)
    phone_number = Column(String(255))
    website = Column(String(255))
    email = Column(String(255))
    country_scraped = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return "<Lead(name='%s', email='%s', phone='%s')>" % (
            self.name, self.email, self.phone)


class UserLeads(Base):
    __tablename__ = 'user_leads'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    lead_id = Column(Integer, ForeignKey('leads.id'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="leads")
    lead = relationship("Lead", back_populates="users")

    def __repr__(self):
        return "<UserLeads(user_id='%s', lead_id='%s')>" % (
            self.user_id, self.lead_id)


class WhatsappMessagesHistory(Base):
    __tablename__ = 'whatsapp_history'

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String(255))
    user_id = Column(Integer, ForeignKey('users.id'))
    lead_id = Column(Integer, ForeignKey('leads.id'))
    sent_at = Column(DateTime(timezone=True), server_default=func.now())

    relationship("Lead", back_populates="whatsapp_history")
    relationship("User", back_populates="whatsapp_history")

    def __repr__(self):
        return "<WhatsappHistory(message='%s')>" % (
            self.message)


class WhatsappLists(Base):
    __tablename__ = 'whatsapp_lists'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    lead_id = Column(Integer, ForeignKey('leads.id'))
    list_name = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    relationship("Lead", back_populates="whatsapp_lists")
    relationship("User", back_populates="whatsapp_lists")

    def __repr__(self):
        return "<WhatsappLists(name='%s', user='%s')>" % (
            self.name, self.user_id)

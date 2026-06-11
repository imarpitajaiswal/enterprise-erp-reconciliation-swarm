import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, String, Float, DateTime
from app.config import settings

Base = declarative_base()

class EnterpriseInvoiceRecord(Base):
    __tablename__ = "sap_invoice_ledger"
    
    invoice_id = Column(String, primary_key=True, index=True)
    vendor_name = Column(String, nullable=False)
    recorded_amount = Column(Float, nullable=False)
    currency = Column(String, default="INR")
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

engine = create_async_engine(settings.DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_enterprise_db_schema():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
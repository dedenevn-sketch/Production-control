from datetime import datetime, date
from typing import Optional, List

from sqlalchemy import ForeignKey, UniqueConstraint, Index, String, DateTime, Date, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func
from core.database import Base
from data.models.product import Product
from data.models.work_center import WorkCenter


# Для ForwardRef, если Product определён позже, можно использовать строки
class Batch(Base):
    __tablename__ = "batches"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Статус
    is_closed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    closed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Описание задания
    task_description: Mapped[str] = mapped_column(String, nullable=False)
    work_center_id: Mapped[int] = mapped_column(ForeignKey("work_centers.id"), nullable=False)
    shift: Mapped[str] = mapped_column(String, nullable=False)
    team: Mapped[str] = mapped_column(String, nullable=False)

    # Идентификация партии
    batch_number: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    batch_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)

    # Продукция
    nomenclature: Mapped[str] = mapped_column(String, nullable=False)
    ekn_code: Mapped[str] = mapped_column(String, nullable=False)

    # Временные рамки
    shift_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    shift_end: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    # Метаданные
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    # Связи
    products: Mapped[List["Product"]] = relationship(back_populates="batch")  # предполагается, что в Product есть batch_id
    work_center: Mapped["WorkCenter"] = relationship(back_populates="batches")  # обратная связь в WorkCenter

    # Составные индексы и ограничения
    __table_args__ = (
        UniqueConstraint('batch_number', 'batch_date', name='uq_batch_number_date'),
        Index('idx_batch_closed', 'is_closed'),
        Index('idx_batch_shift_times', 'shift_start', 'shift_end'),
    )

    def __repr__(self) -> str:
        return f"<Batch(id={self.id}, batch_number={self.batch_number}, batch_date={self.batch_date})>"
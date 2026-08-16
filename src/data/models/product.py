from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, Index, String, Boolean, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func

from core.database import Base
from data.models.batch import Batch


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    unique_code: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    batch_id: Mapped[int] = mapped_column(ForeignKey("batches.id"), nullable=False, index=True)

    # Агрегация
    is_aggregated: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)
    aggregated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Метаданные
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    # Связи
    batch: Mapped["Batch"] = relationship(back_populates="products")

    __table_args__ = (
        Index('idx_product_batch_aggregated', 'batch_id', 'is_aggregated'),
    )

    def __repr__(self) -> str:
        return f"<Product(id={self.id}, unique_code='{self.unique_code}', batch_id={self.batch_id})>"
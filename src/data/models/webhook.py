from datetime import datetime
from typing import List, Optional

from sqlalchemy import String, Boolean, Integer, DateTime, ARRAY, JSON, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base


class WebhookSubscription(Base):
    __tablename__ = "webhook_subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    url: Mapped[str] = mapped_column(String, nullable=False)
    events: Mapped[List[str]] = mapped_column(ARRAY(String), nullable=False)
    secret_key: Mapped[str] = mapped_column(String, nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    retry_count: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    timeout: Mapped[int] = mapped_column(Integer, default=10, nullable=False)

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

    # Связь с доставками
    deliveries: Mapped[List["WebhookDelivery"]] = relationship(
        back_populates="subscription",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<WebhookSubscription(id={self.id}, url='{self.url}', is_active={self.is_active})>"


class WebhookDelivery(Base):
    __tablename__ = "webhook_deliveries"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    subscription_id: Mapped[int] = mapped_column(
        ForeignKey("webhook_subscriptions.id"),
        nullable=False,
        index=True
    )
    event_type: Mapped[str] = mapped_column(String, nullable=False)
    payload: Mapped[dict] = mapped_column(JSON, nullable=False)

    status: Mapped[str] = mapped_column(String, nullable=False)  # "pending", "success", "failed"
    attempts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    response_status: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    response_body: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    delivered_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Связь с подпиской
    subscription: Mapped["WebhookSubscription"] = relationship(back_populates="deliveries")

    def __repr__(self) -> str:
        return f"<WebhookDelivery(id={self.id}, subscription_id={self.subscription_id}, status='{self.status}')>"
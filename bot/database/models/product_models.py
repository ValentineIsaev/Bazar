from .base import Base

from sqlalchemy.orm import Mapped, mapped_column

class ProductBase(Base):
    id: Mapped[int] = mapped_column(primary_key=True)

    id_product: Mapped[int]
    seller_id: Mapped[int]
    name_product: Mapped[str]
    catalog: Mapped[str]
    price: Mapped[str]

    description: Mapped[str]

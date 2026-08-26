from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker


DATABASE_URL = "sqlite:///./khanz_subscriptions.db"


engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


Base = declarative_base()


class Product(Base):

    __tablename__ = "products"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(150),
        nullable=False
    )

    category = Column(
        String(50),
        nullable=False
    )

    description = Column(
        Text,
        nullable=False
    )

    price = Column(
        String(50),
        default="Contact us"
    )

    icon = Column(
        String(20),
        default="⭐"
    )

    # Product logo path
    logo = Column(
        String(500),
        nullable=True
    )

    whatsapp = Column(
        String(255),
        nullable=True
    )

    active = Column(
        Boolean,
        default=True
    )


Base.metadata.create_all(
    bind=engine
)
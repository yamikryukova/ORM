import sqlalchemy
import json
from pprint import pprint
from sqlalchemy import (
    create_engine, MetaData, Table, Integer, String,
    Column, DateTime, ForeignKey, Numeric, ForeignKeyConstraint
)
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from prettytable import PrettyTable

DSN = "postgresql://postgres:1234@localhost:5432/bookstore"
engine = create_engine(DSN)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Shop(Base):
    __tablename__ = 'shops'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)


class Publisher(Base):
    __tablename__ = 'publishers'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    def __repr__(self):
        return f"Publisher(id={self.id}, name={self.name})"


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    id_publisher = Column(Integer(), nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(['id_publisher'], ['publishers.id']),
    )


class Stock(Base):
    __tablename__ = 'stocks'
    id = Column(Integer, primary_key=True)
    count = Column(Integer, nullable=False)
    id_book = Column(Integer(), nullable=False)
    id_shop = Column(Integer(), nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(['id_book'], ['books.id']),
        ForeignKeyConstraint(['id_shop'], ['shops.id']),
    )


class Sale(Base):
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True)
    price = Column(Integer, nullable=False)
    count = Column(Integer, nullable=False)
    date_sale = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    id_stock = Column(Integer(), nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(['id_stock'], ['stocks.id']),
    )


Base.metadata.create_all(engine)

def pretty_output(results):
    table = PrettyTable()
    table.field_names = results[0]
    table.align = 'l'
    table.add_rows(results[1:])
    print(table)


publisher_id = int(input("Введите идентификатор издателя "))
query = (
    session.query(Sale)
    .join(Stock)
    .join(Book)
    .join(Publisher)
    .all()
         )


for item in query:
    stock = session.query(Stock).filter_by(id=item.id_stock).one()
    shop = session.query(Shop).filter_by(id=stock.id_shop).one()
    book = session.query(Book).filter_by(id=stock.id_book).one()
    print(book.title, shop.name, item.price, item.date_sale.date(), sep=" | ")

session.close()
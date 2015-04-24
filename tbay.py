from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('postgresql://REB:REB@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

# item_bid_table = Table('item_bid_association', Base.metadata,
#     Column('item_id', Integer, ForeignKey('items.id')),
#     Column('bid_id', Integer, ForeignKey('bids.id'))
# )

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)

    seller_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    # bids = relationship('Bid', secondary='item_bid_association', backref='item')
    bids = relationship('Bid', backref='item')


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)

    items = relationship("Item", backref="seller")
    bids = relationship("Bid", backref="bidder")

class Bid(Base):
    __tablename__ = "bids"

    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)

    bidder_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)

Base.metadata.create_all(engine)

user1 = User(name="User1", password="password")
user2 = User(name="User2", password="password")
user3 = User(name="User3", password="password")
session.add_all([user1, user2, user3])
session.commit()

item1 = Item(name="baseball", description="Signed Babe Ruth baseball", seller=user1)
session.add(item1)
session.commit()

bid1 = Bid(amount=200, bidder=user2, item=item1)
bid2 = Bid(amount=300, bidder=user3, item=item1)
session.add_all([bid1, bid2])
session.commit()

high_bid = session.query(Bid).order_by(Bid.amount.desc()).first()
print "The highest by was $%i" % high_bid.amount
print "The highest bid was made by: %s" % high_bid.bidder.name




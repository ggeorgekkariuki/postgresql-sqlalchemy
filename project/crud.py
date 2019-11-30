from sqlalchemy import create_engine
import config, model
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import connexion
import yaml
from sqlalchemy import and_, or_

engine = create_engine(config.DATABASE_URI)

# Global
Session = sessionmaker(bind=engine)

def recreate_database():
    model.Base.metadata.drop_all(engine)
    model.Base.metadata.create_all(engine)

# CREATE A ROW
book = model.Book(
    title= 'Deep Learning',
    author= 'Ian Goodfellow',
    pages=775,
    published=datetime(2016, 11, 18)
)

recreate_database()
s = Session()
s.add(book)
s.commit()

# QUERYING ROWS/ READ/ SELECT
print(s.query(model.Book).first())

# Close all sessions and recreate the db
s.close_all()
recreate_database()

# Create a new session
s = Session()

file = 'books.yaml'
# file = 'project/books.yaml'

for data in yaml.load_all(open(file)):
    book = model.Book(**data)
    s.add(book)

s.commit()

s.close_all()

# r = s.query(model.Book)

# Using ilike
# print(r.filter(model.Book.title.ilike('deep learning')).first())

# using between()
# start_date = datetime(2012, 1, 25)
# end_date = datetime(2015, 12, 30)

# Using AND() OR()
# and_operator = r.filter(
#     and_(
#         model.Book.pages > 500,
#         model.Book.published > datetime(2015, 5, 1)
#     )
# ).all()
# print(and_operator)

# Order By
# print(r.order_by(model.Book.pages.desc()).all())


# This small script will ask the user in the command line to add prices for each book
# s = Session()

# books = s.query(model.Book).all()

# for book in books:
#     price = input(f"Price for '{book.title}': $")
#     book.price = price
#     s.add(book)

# s.commit()
# s.close()

# The CONTEXT MANAGER
from contextlib import contextmanager
@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    else:
        session.close()

with session_scope() as s:
    books = s.query(model.Book).all()

    for book in books:
        price = input(f"Price for '{book.title}': $")
        book.price = price
        s.add(book)

    titles = s.query(model.Book.title, model.Book.price).all()
    print(titles)
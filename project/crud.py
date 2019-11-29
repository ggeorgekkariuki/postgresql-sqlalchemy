from sqlalchemy import create_engine
import config, model
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import connexion
import yaml
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
file = 'project/books.yaml'

for data in yaml.load_all(open(file)):
    book = model.Book(**data)
    s.add(book)

s.commit()

print(s.query(model.Book).all())
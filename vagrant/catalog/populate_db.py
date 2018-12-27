from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
import datetime

## IMPORT DATABASE CLASSES FOR THIS PROJECT
## from database_setup import Base, Collections, Items, Authors, Subject, User, People
from models import Base, User, Category, Item

engine = create_engine('sqlite:///itemCatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

## ADD A USER
newUser = User(name = 'Zachary Oleitschuk', email = '123zoleitschuk@gmail.com')
session.add(newUser)
session.commit()

currentUser = session.query(User).filter_by(email = '123zoleitschuk@gmail.com').one()

categoryList = ['Colors', 'Holidays', 'Days of the Week']
for category in categoryList:
    new_category = Category(name = category, user_id = currentUser.id)
    session.add(new_category)
    session.commit()

## ADD SAMPLE ITEMS
items = [
    {'name': 'Sunday', 'category':'Days of the Week', 'description':'First day in the week.'},
    {'name': 'Monday', 'category':'Days of the Week', 'description':'Second day in the week.'},
    {'name': 'Tuesday', 'category':'Days of the Week', 'description':'Third day in the week.'},
    {'name': 'Wednesday', 'category':'Days of the Week', 'description':'Forth day in the week.'},
    {'name': 'Thursday', 'category':'Days of the Week', 'description':'Fifth day in the week.'},
    {'name': 'Friday', 'category':'Days of the Week', 'description':'Sixth day in the week.'},
    {'name': 'Saturday', 'category':'Days of the Week', 'description':'Seventh and final day in the week.'},
    {'name': 'Red', 'category':'Colors', 'description':'First color in the rainbow.'},
    {'name': 'Orange', 'category':'Colors', 'description':'Second color in the rainbow.'},
    {'name': 'Yellow', 'category':'Colors', 'description':'Third color in the rainbow.'},
    {'name': 'Green', 'category':'Colors', 'description':'Forth color in the rainbow.'},
    {'name': 'Blue', 'category':'Colors', 'description':'Fifth color in the rainbow.'},
    {'name': 'Indigo', 'category':'Colors', 'description':'Sixth color in the rainbow.'},
    {'name': 'Violet', 'category':'Colors', 'description':'Final and seventh color in the rainbow.'},
    {'name': 'Christmas', 'category':'Holidays', 'description':'Dec 25'},
    {'name': 'New Years', 'category':'Holidays', 'description':'Jan 1'},
    {'name': 'Halloween', 'category':'Holidays', 'description':'Oct 31'},
    {'name': 'Canada Day', 'category':'Holidays', 'description':'July 1'},
    {'name': 'Rememberance Day', 'category':'Holidays', 'description':'Nov 11'},
]

for item in items:
    newItem = Item(name = item['name'],
                    description = item['description'],
                    category_id = session.query(Category).filter_by(name = item['category']).one().id,
                    user_id=currentUser.id,
                )

    session.add(newItem)
    session.commit()
"""
Module docstring here.
"""
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Category, Item

app = Flask(__name__)

engine = create_engine('sqlite:///itemCatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/catalog/')
def Catalog():
    """
    Method docstring here.
    """
    categories = session.query(Category).all()
    items = session.query(Item).all()
    output = '<div><strong>Categories:</strong>'
    for category in categories:
        output += category.name
    output += '</div><div><strong>Items:</strong>'
    for item in items:
        output += item.name
    output += '</div>'
    return output

@app.route('/item/<int:item_id>/')
def catalog_item(item_id):
    """
    Method docstring here.
    """
    return 'Item_id: {}'.format(item_id)

@app.route('/category/<int:category_id>/')
def catalog_category(category_id):
    """
    Method docstring here.
    """
    return 'Category_id: {}'.format(category_id)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)

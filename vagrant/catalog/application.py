"""
Module docstring here.
"""
from flask import Flask, render_template, request
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
def catalog():
    """
    Method docstring here.
    """
    categories = session.query(Category).all()
    items = session.query(Item).all()
    return render_template('public_catalog.html', items=items, categories=categories)

@app.route('/category/<int:category_id>/')
def catalog_category(category_id):
    """
    Method docstring here.
    """
    # TODO: get full category object and pass into template.
    return render_template('category.html', category_id=category_id)

@app.route('/category/<int:category_id>/edit/', methods=['GET', 'POST'])
def edit_category(category_id):
    """
    Method docstring here.
    """
    # TODO: get full category object and pass into template.
    if request.method == 'POST':
        print('EDIT Category requires helper method to be written.')
    else:
        return render_template('edit_category.html', category_id=category_id)

@app.route('/category/<int:category_id>/delete/', methods=['GET', 'POST'])
def delete_category(category_id):
    """
    Method docstring here.
    """
    # TODO: get full category object and pass into template.
    if request.method == 'POST':
        print('DELETE Category requires helper method to be written.')
    else:
        return render_template('delete_category.html', category_id=category_id)

@app.route('/item/<int:item_id>/')
def catalog_item(item_id):
    """
    Method docstring here.
    """
    # TODO: get full item object and pass into template.
    return render_template('item.html', item_id=item_id)

@app.route('/item/<int:item_id>/edit/', methods=['GET', 'POST'])
def edit_item(item_id):
    """
    Method docstring here.
    """
    # TODO: get full item object and pass into template.
    if request.method == 'POST':
        print('EDIT Item requires helper method to be written.')
    else:
        return render_template('edit_item.html', item_id=item_id)

@app.route('/item/<int:item_id>/delete/', methods=['GET', 'POST'])
def delete_item(item_id):
    """
    Method docstring here.
    """
    # TODO: get full item object and pass into template.
    if request.method == 'POST':
        print('DELETE Item requires helper method to be written.')
    else:
        return render_template('delete_item.html', item_id=item_id)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)

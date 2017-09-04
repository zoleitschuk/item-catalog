"""
Module docstring here.
"""
from flask import Flask, render_template, request, redirect, url_for, flash
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
def show_catalog():
    """
    Method docstring here.
    """
    categories = session.query(Category).all()
    items = session.query(Item).all()
    return render_template('public_catalog.html', items=items, categories=categories)

@app.route('/category/<int:category_id>/')
def show_category(category_id):
    """
    Method docstring here.
    """
    category = session.query(Category).filter_by(id=category_id).one()
    return render_template('category.html', category=category)

@app.route('/category/new/', methods=['GET', 'POST'])
def new_category():
    """
    Method docstring here.
    """
    if request.method == 'POST':
        new_category = Category(name=request.form['name'])
        session.add(new_category)
        flash('New Category %s Successfully Created' % new_category.name)
        session.commit()
        return redirect(url_for('show_catalog'))
    else:
        return render_template('new_category.html')

@app.route('/category/<int:category_id>/edit/', methods=['GET', 'POST'])
def edit_category(category_id):
    """
    Method docstring here.
    """
    edited_category = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        print('EDIT Category requires helper method to be written.')
    else:
        return render_template('edit_category.html', category=edited_category)

@app.route('/category/<int:category_id>/delete/', methods=['GET', 'POST'])
def delete_category(category_id):
    """
    Method docstring here.
    """
    deleted_category = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        print('DELETE Category requires helper method to be written.')
    else:
        return render_template('delete_category.html', category=deleted_category)

@app.route('/item/<int:item_id>/')
def show_item(item_id):
    """
    Method docstring here.
    """
    item = session.query(Item).filter_by(id=item_id).one()
    return render_template('item.html', item=item)

@app.route('/item/new/', methods=['GET', 'POST'])
def new_item():
    """
    Method docstring here.
    """
    if request.method == 'POST':
        new_item = Item(
            name=request.form['name'],
            description=request.form['description'],
            category_id=request.form['category_id'],
        )
        session.add(new_item)
        flash('New Item %s Successfully Created' % new_item.name)
        session.commit()
        return redirect(url_for('show_catalog'))
    else:
        return render_template('new_item.html')

@app.route('/item/<int:item_id>/edit/', methods=['GET', 'POST'])
def edit_item(item_id):
    """
    Method docstring here.
    """
    edited_item = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        print('EDIT Item requires helper method to be written.')
    else:
        return render_template('edit_item.html', item=edited_item)

@app.route('/item/<int:item_id>/delete/', methods=['GET', 'POST'])
def delete_item(item_id):
    """
    Method docstring here.
    """
    deleted_item = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        print('DELETE Item requires helper method to be written.')
    else:
        return render_template('delete_item.html', item=deleted_item)

if __name__ == '__main__':
    app.secret_key = 'shh_its_a_secret'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)

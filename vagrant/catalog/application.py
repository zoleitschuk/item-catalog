"""
Module docstring here.
"""
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Category, Item

app = Flask(__name__)

engine = create_engine('sqlite:///itemCatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# JSON APIs to view Catalog Information
@app.route('/api/v01/catalog/JSON/')
def catalog_JSON():
    """
    Method docstring here.
    """
    items = session.query(Item).all()
    return jsonify(items=[i.serialize for i in items])

@app.route('/api/v01/item/<int:item_id>/JSON/')
def item_JSON(item_id):
    """
    Method docstring here.
    """
    item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(item=item.serialize)

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
        if request.form['name']:
            edited_category.name = request.form['name']
        session.add(edited_category)
        session.commit()
        flash('Restaurant Successfully Edited %s' % edited_category.name)
        return redirect(url_for('show_catalog'))
    else:
        return render_template('edit_category.html', category=edited_category)

@app.route('/category/<int:category_id>/delete/', methods=['GET', 'POST'])
def delete_category(category_id):
    """
    Method docstring here.
    """
    category_to_delete = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        session.delete(category_to_delete)
        flash('%s Successfully Deleted' % category_to_delete.name)
        session.commit()
        return redirect(url_for('show_catalog'))
    else:
        return render_template('delete_category.html', category=category_to_delete)

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
        if request.form['name']:
            edited_item.name = request.form['name']
        if request.form['description']:
            edited_item.description = request.form['description']
        if request.form['category_id']:
            edit_item.category_id = request.form['category_id']
        session.add(edited_item)
        session.commit()
        flash('Restaurant Successfully Edited %s' % edited_item.name)
        return redirect(url_for('show_catalog'))
    else:
        return render_template('edit_item.html', item=edited_item)

@app.route('/item/<int:item_id>/delete/', methods=['GET', 'POST'])
def delete_item(item_id):
    """
    Method docstring here.
    """
    item_to_delete = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(item_to_delete)
        flash('%s Successfully Deleted' % item_to_delete.name)
        session.commit()
        return redirect(url_for('show_catalog'))
    else:
        return render_template('delete_item.html', item=item_to_delete)

if __name__ == '__main__':
    app.secret_key = 'shh_its_a_secret'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)

"""
Module docstring here.
"""
import random
import string
import json
import httplib2
import requests

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response
from flask import session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

from models import Base, Category, Item

app = Flask(__name__)

engine = create_engine('sqlite:///itemCatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']

# Create anti-forgery state token
@app.route('/login')
def showLogin():
    """
    Method docstring here.
    """
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    """
    Method docstring here.
    """
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1].decode())
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print('done!')
    return output

@app.route('/gdisconnect')
def gdisconnect():
    """
    Method docstring here.
    """
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash('Successfully disconnected.')
        return redirect(url_for('show_catalog'))
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        flash('Failed to revoke token for given user.')
        return redirect(url_for('show_catalog'))

# JSON APIs to view Item Catalog Information
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

# Item Catalog Pages
@app.route('/')
@app.route('/catalog/')
def show_catalog():
    """
    Method docstring here.
    """
    categories = session.query(Category).all()
    items = [i.serialize for i in session.query(Item).all()]

    return render_template('catalog.html', items=items, categories=categories, login_session=login_session)

@app.route('/category/<int:category_id>/')
def show_category(category_id):
    """
    Method docstring here.
    """
    category = session.query(Category).filter_by(id=category_id).one()
    return render_template('category.html', category=category, login_session=login_session)

@app.route('/category/new/', methods=['GET', 'POST'])
def new_category():
    """
    Method docstring here.
    """
    if 'username' not in login_session:
        flash('Please login in order to add categories')
        return redirect(url_for('show_catalog'))
    
    if request.method == 'POST':
        new_category = Category(name=request.form['name'])
        session.add(new_category)
        flash('New Category {} Successfully Created'.format(new_category.name))
        session.commit()
        return redirect(url_for('show_catalog'))
    else:
        return render_template('category_new.html', login_session=login_session)

@app.route('/category/<int:category_id>/edit/', methods=['GET', 'POST'])
def edit_category(category_id):
    """
    Method docstring here.
    """
    if 'username' not in login_session:
        flash('Please login in order to edit categories')
        return redirect(url_for('show_catalog'))
    
    edited_category = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        if 'btn_submit' in request.form:
            if request.form['name']:
                edited_category.name = request.form['name']
                session.add(edited_category)
                session.commit()
                flash('Category Successfully Edited {}'.format(edited_category.name))
        else:
            flash('Category Edit {} Was Cancelled'.format(edited_category.name))
        return redirect(url_for('show_catalog'))
    else:
        return render_template('category_edit.html', category=edited_category, login_session=login_session)

@app.route('/category/<int:category_id>/delete/', methods=['GET', 'POST'])
def delete_category(category_id):
    """
    Method docstring here.
    """
    if 'username' not in login_session:
        flash('Please login in order to delete categories')
        return redirect(url_for('show_catalog'))
    
    category_to_delete = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        if 'btn_submit' in request.form:
            items_to_delete =session.query(Item).filter_by(category_id=category_to_delete.id)
            for item in items_to_delete:
                session.delete(item)
            session.delete(category_to_delete)
            flash('{} Successfully Deleted'.format(category_to_delete.name))
            session.commit()
        else:
            flash('Delete {} Cancelled'.format(category_to_delete.name))
        return redirect(url_for('show_catalog'))
    else:
        return render_template('category_delete.html', category=category_to_delete, login_session=login_session)

@app.route('/item/<int:item_id>/')
def show_item(item_id):
    """
    Method docstring here.
    """
    item = session.query(Item).filter_by(id=item_id).one()
    return render_template('item.html', item=item.serialize, login_session=login_session)

@app.route('/item/new/', methods=['GET', 'POST'])
def new_item():
    """
    Method docstring here.
    """
    if 'username' not in login_session:
        flash('Please login in order to add items')
        return redirect(url_for('show_catalog'))

    if request.method == 'POST':
        new_item = Item(
            name=request.form['name'],
            description=request.form['description'],
            category_id=request.form['category_id'],
        )
        session.add(new_item)
        flash('New Item {} Successfully Created'.format(new_item.name))
        session.commit()
        return redirect(url_for('show_catalog'))
    else:
        categories = session.query(Category).all()
        return render_template('item_new.html', categories=categories, login_session=login_session)

@app.route('/item/<int:item_id>/edit/', methods=['GET', 'POST'])
def edit_item(item_id):
    """
    Method docstring here.
    """
    if 'username' not in login_session:
        flash('Please login in order to edit items')
        return redirect(url_for('show_catalog'))

    edited_item = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        if 'btn_submit' in request.form:
            if request.form['name']:
                edited_item.name = request.form['name']
            if request.form['description']:
                edited_item.description = request.form['description']
            if request.form['category_id']:
                edited_item.category_id = request.form['category_id']
            session.add(edited_item)
            session.commit()
            flash('Item Successfully Edited {}'.format(edited_item.name))
        else:
            flash('Edit Item {} Was Cancelled'.format(edited_item.name))
        return redirect(url_for('show_catalog'))
    else:
        categories = session.query(Category).all()
        return render_template('item_edit.html', item=edited_item, categories=categories, login_session=login_session)

@app.route('/item/<int:item_id>/delete/', methods=['GET', 'POST'])
def delete_item(item_id):
    """
    Method docstring here.
    """
    if 'username' not in login_session:
        flash('Please login in order to delete items')
        return redirect(url_for('show_catalog'))

    item_to_delete = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        if 'btn_submit' in request.form:
            session.delete(item_to_delete)
            flash('{} Successfully Deleted'.format(item_to_delete.name))
            session.commit()
        else:
            flash('Delete Item {} Cancelled'.format(item_to_delete.name))
        return redirect(url_for('show_catalog'))
    else:
        return render_template('item_delete.html', item=item_to_delete, login_session=login_session)

if __name__ == '__main__':
    app.secret_key = 'shh_its_a_secret'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)

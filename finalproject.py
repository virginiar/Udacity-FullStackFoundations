from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Fake Restaurants
"""
restaurant = {"name": "The CRUDdy Crab", "id": "1"}

restaurants = [
    {"name": "The CRUDdy Crab", "id": "1"},
    {"name": "Blue Burgers", "id": "2"},
    {"name": "Taco Hut", "id": "3"},
]
"""

# Fake Menu Items
"""
items = [
    {
        "name": "Cheese Pizza",
        "description": "made with fresh cheese",
        "price": "$5.99",
        "course": "Entree",
        "id": "1",
    },
    {
        "name": "Chocolate Cake",
        "description": "made with Dutch Chocolate",
        "price": "$3.99",
        "course": "Dessert",
        "id": "2",
    },
    {
        "name": "Caesar Salad",
        "description": "with fresh organic vegetables",
        "price": "$5.99",
        "course": "Entree",
        "id": "3",
    },
    {
        "name": "Iced Tea",
        "description": "with lemon",
        "price": "$.99",
        "course": "Beverage",
        "id": "4",
    },
    {
        "name": "Spinach Dip",
        "description": "creamy dip with fresh spinach",
        "price": "$1.99",
        "course": "Appetizer",
        "id": "5",
    },
]

item = {
    "name": "Cheese Pizza",
    "description": "made with fresh cheese",
    "price": "$5.99",
    "course": "Entree",
}
"""

# Show all the restaurants
@app.route("/")
@app.route("/restaurants")
def showRestaurants():
    #return "This page will show all my restaurants"
    restaurants = session.query(Restaurant).all()
    return render_template("restaurants.html", restaurants=restaurants)


# Add a new restaurant
@app.route("/restaurant/new", methods=["GET", "POST"])
def newRestaurant():
    #return "This page will be for making a new restaurant"
    if request.method == "POST":
        restaurant = Restaurant(
            name = request.form["name"]
        )
        session.add(restaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template("newRestaurant.html")

# Edit a restaurant
@app.route("/restaurant/<int:restaurant_id>/edit",  methods=["GET", "POST"])
def editRestaurant(restaurant_id):
    #return "This page will be for editing restaurant %s" % restaurant_id
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == "POST":
        if request.form["name"]:
            restaurant.name = request.form["name"]
        session.add(restaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template("editRestaurant.html", restaurant=restaurant)


# Delete a restaurant
@app.route("/restaurant/<int:restaurant_id>/delete", methods=["GET", "POST"])
def deleteRestaurant(restaurant_id):
    #return "This page will be for deleting restaurant %s" % restaurant_id
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == "POST":
        session.delete(restaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('deleteRestaurant.html', restaurant = restaurant)


# Show a restaurant menu
@app.route("/restaurant/<int:restaurant_id>/")
@app.route("/restaurant/<int:restaurant_id>/menu")
def showMenu(restaurant_id):
    #return "This page is the menu for restaurant %s" % restaurant_id
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return render_template('menu.html', restaurant = restaurant, items = items)


# Create a new menu item
@app.route("/restaurant/<int:restaurant_id>/menu/new", methods=["GET", "POST"])
def newMenuItem(restaurant_id):
    #return "This page is for making a new menu item for restaurant %s" % restaurant_id
    if request.method == "POST":
        item = MenuItem(
            name = request.form["name"],
            description = request.form["description"],
            price = request.form["price"],
            course = request.form["course"],
            restaurant_id = restaurant_id
        )
        session.add(item)
        session.commit()
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('newMenuItem.html', restaurant_id = restaurant_id)


# Edit a menu item
@app.route("/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit", methods=["GET", "POST"])
def editMenuItem(restaurant_id, menu_id):
    #return "This page is for editing menu item %s" % menu_id
    item = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == "POST":
        if request.form["name"]:
            item.name = request.form["name"]
        if request.form["description"]:
            item.description = request.form["description"]
        if request.form["price"]:
            item.price = request.form["price"]
        if request.form["course"]:
            item.course = request.form["course"]
        session.add(item)
        session.commit()
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('editMenuItem.html', restaurant_id = restaurant_id, item = item)


# Delete a menu item
@app.route("/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete", methods=["GET", "POST"])
def deleteMenuItem(restaurant_id, menu_id):
    #return "This page is for deleting menu item %s" % menu_id
    item = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == "POST":
        session.delete(item)
        session.commit()
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('deleteMenuItem.html', restaurant_id = restaurant_id, item = item)


# An API Endpoint for show all the restaurants
@app.route("/restaurants/JSON")
def jsonShowRestaurants():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurants=[i.serialize for i in restaurants])


# An API Endpoint for show a restaurant menu
@app.route("/restaurant/<int:restaurant_id>/menu/JSON")
def jsonShowMenu(restaurant_id):
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])

# An API Endpoint for show a menu item
@app.route("/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON")
def jsonShowMenuItem(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem=[item.serialize])


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=5000)

from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

@app.route("/beverages.html")
def beverages():
    return render_template("beverages.html")

@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/homepage.html")
def homepage2():
    return render_template("homepage.html")

@app.route("/bbc.html")
def bbc():
    return render_template("bbc.html")

@app.route("/vc.html")
def vc():
    return render_template("vc.html")

@app.route("/jc.html")
def jc():
    return render_template("jc.html")

@app.route("/tantra.html")
def tantra():
    return render_template("tantra.html")

@app.route("/canteens.html")
def canteens():
    return render_template("canteens.html")

@app.route("/categories.html")
def categories():
    return render_template("categories.html")

@app.route("/cart1.html")
def cart1():
    return render_template("cart1.html")

@app.route("/desserts.html")
def desserts():
    return render_template("desserts.html")

@app.route("/savouries.html")
def savouries():
    return render_template("savouries.html")

@app.route('/store_data', methods=['POST'])


def store_data():
    data = request.get_json()

    conn = sqlite3.connect('mydatabase.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY AUTOINCREMENT, item TEXT, canteen TEXT, category TEXT, price TEXT, unit INTEGER DEFAULT 1)")
    
    # Check if item already exists in database
    cur.execute("SELECT * FROM items WHERE item = ?", (data['item'],))
    result = cur.fetchone()
    if result is not None:
        # If item already exists, increment the unit value
        cur.execute("UPDATE items SET unit = unit + 1 WHERE item = ?", (data['item'],))
        conn.commit()
        conn.close()
        response = {'status': 'success', 'message': f"Item quantity has been increased to {result[5]+1} units"}
    else:
        # If item doesn't exist, insert a new row
        cur.execute("INSERT INTO items (item, canteen, category, price) VALUES (?, ?, ?, ?)", (data['item'], data['canteen'], data['category'], data['price']))
        conn.commit()
        conn.close()
        response = {'status': 'success', 'message': 'Item added to Cart'}
    
    return jsonify(response)

@app.route('/append_data', methods=['POST'])
def append_data():
    data = request.get_json()
    # Connect to the original database
    conn_old = sqlite3.connect('mydatabase.db')
    cur_old = conn_old.cursor()

    # Connect to the new database
    conn_new = sqlite3.connect('delivery.db')
    cur_new = conn_new.cursor()

    # Create 'deliveries' table if it doesn't exist
    cur_new.execute("CREATE TABLE IF NOT EXISTS deliveries (id INTEGER PRIMARY KEY AUTOINCREMENT, item TEXT, canteen TEXT, category TEXT, price TEXT, unit INTEGER DEFAULT 1, name TEXT, contact TEXT, hostel TEXT, room TEXT)")

    # Retrieve data from the original database
    cur_old.execute("SELECT * FROM items")
    items = cur_old.fetchall()

    # Insert data into the new database
    for item in items:
        cur_new.execute("INSERT INTO deliveries (item, canteen, category, price, unit, name, contact, hostel, room) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (item[1], item[2], item[3], item[4], item[5], data['name'], data['contact'], data['hostel'], data['room']))

    # Commit and close the connections
    conn_new.commit()
    conn_new.close()
    conn_old.close()

    # Delete data from the original database
    conn_old = sqlite3.connect('mydatabase.db')
    cur_old = conn_old.cursor()
    cur_old.execute("DELETE FROM items")
    conn_old.commit()
    conn_old.close()

    # Return a JSON response
    response = {'status': 'success', 'message': 'Order Has Been Placed'}
    return jsonify(response)



@app.route('/delete_item/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    conn = sqlite3.connect('delivery.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM deliveries WHERE id=?", (item_id,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success', 'message': 'Order Has Been Assigned'})



@app.route('/cart.html')
def cart():
    conn = sqlite3.connect('mydatabase.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM items")
    final_value = 0
    rows = cur.fetchall()
    items = []
    for row in rows:
        price = int(row[4][4:]) # Strip 'Rs' from price and convert to integer
        total_value = price * row[5] # Multiply price by units to get total value
        final_value = final_value + total_value
        items.append({'id': row[0], 'item': row[1], 'canteen': row[2], 'category': row[3], 'price': price, 'unit': row[5], 'total_value': total_value})
    conn.close()
    return render_template('cart.html', items=items, final_value=final_value)

@app.route('/deliver.html')
def deliver():
    conn = sqlite3.connect('delivery.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM deliveries")
    rows = cur.fetchall()
    items = []
    for row in rows:
        price = int(row[4][4:])
        total_value = price * row[5]
        items.append({'id': row[0], 'item': row[1], 'canteen': row[2], 'category': row[3], 'price': price, 'unit': row[5], 'total_value': total_value, 'name': row[6], 'contact': row[7], 'hostel': row[8], 'room': row[9]})
    conn.close()
    return render_template('deliver.html', items=items)

@app.route('/update_unit', methods=['POST'])
def update_unit():
    data = request.get_json()

    conn = sqlite3.connect('mydatabase.db')
    cur = conn.cursor()
    
    # Update the unit value
    if data['unit'] > 1:
        cur.execute("UPDATE items SET unit = ? WHERE item = ?", (data['unit'] - 1, data['item']))
        conn.commit()
        conn.close()
        response = {'status': 'success', 'message': 'Item quantity has been decreased'}
    else:
        cur.execute("DELETE FROM items WHERE item = ?", (data['item'],))
        conn.commit()
        conn.close()
        response = {'status': 'success', 'message': 'Item removed from Cart'}
    
    return jsonify(response)


@app.route('/update_unit2', methods=['POST'])
def update_unit2():
    data = request.get_json()

    conn = sqlite3.connect('mydatabase.db')
    cur = conn.cursor()
    
    # Update the unit value
    if data['unit'] > 1:
        cur.execute("UPDATE items SET unit = ? WHERE item = ?", (data['unit'] + 1, data['item']))
        conn.commit()
        conn.close()
        response = {'status': 'success', 'message': 'Item quantity has been increased'}
    else:
        cur.execute("UPDATE items SET unit = ? WHERE item = ?", (data['unit'] + 1, data['item']))
        conn.commit()
        conn.close()
        response = {'status': 'success', 'message': 'Item quantity has been increased'}
    
    return jsonify(response)

# @app.route('/store_data', methods=['POST'])
# def store_data():
#     data = request.get_json()

#     conn = sqlite3.connect('mydatabase.db')
#     cur = conn.cursor()
#     cur.execute("CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY AUTOINCREMENT, item TEXT, canteen TEXT, category TEXT, price TEXT, unit INTEGER DEFAULT 1)")
    
#     # Check if item already exists in database
#     cur.execute("SELECT * FROM items WHERE item = ?", (data['item'],))
#     result = cur.fetchone()
#     if result is not None:
#         # If item already exists, increment the unit value
#         cur.execute("UPDATE items SET unit = unit + 1 WHERE item = ?", (data['item'],))
#         conn.commit()
#         conn.close()
#         response = {'status': 'success', 'message': f"Item quantity has been increased to {result[5]+1} units"}
#     else:
#         # If item doesn't exist, insert a new row
#         cur.execute("INSERT INTO items (item, canteen, category, price) VALUES (?, ?, ?, ?)", (data['item'], data['canteen'], data['category'], data['price']))
#         conn.commit()

#         # Fetch all rows from the items table
#         cur.execute("SELECT * FROM items")
#         rows = cur.fetchall()

#         conn.close()
#         response = {'status': 'success', 'message': 'Item added to Cart'}
    
#     # Pass the rows to the cart.html template
#     return render_template("cart.html", rows=rows)



if __name__ == '__main__':
    app.run(debug=True)
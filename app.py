from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import date
from flask import flash
app = Flask(__name__)

app.secret_key = "plant_nursery_secret_key"
# ----Database Connection--------
def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="patolesanika",
        database="plant_nursery"
    )
    return conn

#----------------Home PAGE--------

@app.route('/home')
def home():
    return render_template('index.html')

#====about=====
@app.route('/about')
def about():
    return render_template('about.html')
#----------- Login Page-----------------
@app.route("/login")
def login():
    return render_template("login.html")

#------------ Login Page admin -------------
@app.route("/adminlogin")
def login_ad():
    return render_template("adminlogin.html")

#------------ Catalog Page-----------------
@app.route('/catalog')
def catalog():
    return render_template('catalog.html')





# ----------------Register Page-----------
@app.route("/register")
def register():
    return render_template("register.html")

# -------------Register Page admin-----------
@app.route("/registeradmin")
def register_ad():
    return render_template("adminregistration.html")


#----------------Pots------------------

@app.route('/potcatalog')
def potcatalog():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            item_id,
            item_name,
            price,
            stock,
            image
        FROM items
        WHERE category_id = 2
        ORDER BY item_id DESC
    """)

    pots = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'potcatalog.html',
        pots=pots
    )


#----------------Seeds------------------

@app.route('/seedcatalog')
def seedcatalog():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            item_id,
            item_name,
            price,
            stock,
            image
        FROM items
        WHERE category_id = 4
        ORDER BY item_id DESC
    """)

    seeds = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'seedcatalog.html',
        seeds=seeds
    )

@app.route('/fertilizercatalog')
def fertilizercatalog():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            item_id,
            item_name,
            price,
            stock,
            image
        FROM items
        WHERE category_id = 3
        ORDER BY item_id DESC
    """)

    fertilizers = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'fertilizercatalog.html',
        fertilizers=fertilizers
    )
#-----------indoor Plants---------------------
@app.route("/indoorplant")
def indoorplant():

    conn = get_db_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            item_id,
            item_name,
            price,
            stock,
            image
        FROM items
        WHERE category_id = 1
        AND plant_category_id = 1
        ORDER BY item_id DESC
    """)

    plants = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "indoorplant.html",
        plants=plants
    )



#-------flowering plants---------
@app.route("/flowerplant")
def flowerplant():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            item_id,
            item_name,
            price,
            stock,
            image
        FROM items
        WHERE category_id = 1
          AND plant_category_id = 2
        ORDER BY item_id DESC
    """)

    plants = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "flowerplant.html",
        plants=plants
    )


#-------fruit plants---------
@app.route("/fruitplant")
def fruitplant():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            item_id,
            item_name,
            price,
            stock,
            image
        FROM items
        WHERE category_id = 1
          AND plant_category_id = 4
        ORDER BY item_id DESC
    """)

    plants = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "fruitplant.html",
        plants=plants
    )
#-------Medicinal plants---------
@app.route("/medicinalplant")
def medicinalplant():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            item_id,
            item_name,
            price,
            stock,
            image
        FROM items
        WHERE category_id = 1
          AND plant_category_id = 3
        ORDER BY item_id DESC
    """)

    plants = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "medicinalplant.html",
        plants=plants
    )


#---------- Save Registration -------------
@app.route("/register", methods=["GET","POST"])
def register_user():

    fullname = request.form["fullname"]
    email = request.form["email"]
    mobile = request.form["mobile"]
    username = request.form["username"]
    password = request.form["password"]
    confirm = request.form["confirm_password"]
    hashed_password = generate_password_hash(password)
    if password != confirm:
        return "Password Does Not Match"

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        INSERT INTO users
        (fullname,email,mobile,username,password)
        VALUES(%s,%s,%s,%s,%s)
        """,
        (fullname,email,mobile,username,hashed_password))

        conn.commit()

    except mysql.connector.IntegrityError:
        conn.close()
        return "Username or Email Already Exists"
    cursor.close()
    conn.close()

    return redirect(url_for("login"))


#---------- Login Verification--------------
@app.route("/login", methods=["POST"])
def login_user():

    username = request.form["username"]
    password = request.form["password"]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM users
    WHERE username=%s
    """,
    (username,))

    user = cursor.fetchone()
    cursor.close()
    conn.close()
    # user name found or not
    if user is None: 
        return """ <script> alert("Username not found!"); window.location.href = "/login"; </script> """
    
     # Password stored in database
    stored_password = user[5]

    # check hashed password

    if check_password_hash(stored_password, password):
        session["user_id"] = user[0]
        session["username"] = user[4]
        
        return redirect(url_for("home"))

    else:
        return "<h2>Invalid Username or Password</h2>"

# ---------------- DASHBOARD ----------------


@app.route('/user')
def dashboard():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # CART COUNT
    cursor.execute("""
        SELECT COALESCE(SUM(quantity), 0) AS cart_count
        FROM cart
        WHERE id = %s
    """, (user_id,))

    cart_data = cursor.fetchone()

    cart_count = cart_data['cart_count']

    # ORDER COUNT
    order_count = 0

    # WISHLIST COUNT
    wishlist_count = 0

    cursor.close()
    conn.close()

    return render_template(
        'user_dashboard.html',
        cart_count=cart_count,
        order_count=order_count,
        wishlist_count=wishlist_count
    )



#------------ Logout User---------

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))






# ================ ADD TO CART ================

@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():

    # Check if user is logged in
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    # Get item ID from form
    item_id = request.form.get("item_id")

    if not item_id:
        return "Item ID is missing", 400

    try:
        item_id = int(item_id)
    except ValueError:
        return "Invalid Item ID", 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:

        # -----------------------------------------
        # Get product directly from items table
        # -----------------------------------------

        cursor.execute("""
            SELECT
                item_id,
                item_name,
                price,
                stock,
                image
            FROM items
            WHERE item_id = %s
        """, (item_id,))

        product = cursor.fetchone()

        # Product doesn't exist
        if product is None:
            cursor.close()
            conn.close()
            return "Product not found", 404

        # -----------------------------------------
        # Check stock
        # -----------------------------------------

        if product["stock"] <= 0:
            cursor.close()
            conn.close()
            return "Product is out of stock", 400

        # -----------------------------------------
        # Check if product already exists in cart
        # -----------------------------------------

        cursor.execute("""
            SELECT cart_id, quantity
            FROM cart
            WHERE id = %s
            AND item_id = %s
        """, (user_id, item_id))

        existing_cart = cursor.fetchone()

        # -----------------------------------------
        # Product already in cart
        # -----------------------------------------

        if existing_cart:

            # Don't allow quantity to exceed stock
            if existing_cart["quantity"] >= product["stock"]:
                cursor.close()
                conn.close()
                return "Maximum available stock already added to cart", 400

            cursor.execute("""
                UPDATE cart
                SET quantity = quantity + 1
                WHERE cart_id = %s
                AND id = %s
            """, (
                existing_cart["cart_id"],
                user_id
            ))

        # -----------------------------------------
        # Product not in cart
        # -----------------------------------------

        else:

            cursor.execute("""
                INSERT INTO cart
                (id, item_id, quantity)
                VALUES (%s, %s, %s)
            """, (
                user_id,
                item_id,
                1
            ))

        conn.commit()

    except Exception as e:

        conn.rollback()

        print("ADD TO CART ERROR:", e)

        cursor.close()
        conn.close()

        return f"Error adding product to cart: {e}", 500

    cursor.close()
    conn.close()

    # Go to cart page
    return redirect(url_for("cart"))
#================ CART PAGE ================

@app.route("/cart")
def cart():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            cart.cart_id,
            cart.item_id,
            cart.quantity,
            items.item_name,
            items.price,
            items.image
        FROM cart
        JOIN items
        ON cart.item_id = items.item_id
        WHERE cart.id = %s
    """, (user_id,))

    cart_items = cursor.fetchall()

    total = 0

    for item in cart_items:
        total += float(item["price"]) * item["quantity"]

    cursor.close()
    conn.close()

    return render_template(
        "cart.html",
        cart=cart_items,
        total=total
    )

#================ REMOVE FROM CART ================

@app.route("/remove_from_cart/<int:cart_id>")
def remove_from_cart(cart_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM cart
        WHERE cart_id = %s
        AND id = %s
    """, (
        cart_id,
        user_id
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("cart"))


# ================ INCREASE QUANTITY ================

@app.route("/increase_quantity/<int:cart_id>")
def increase_quantity(cart_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE cart
        SET quantity = quantity + 1
        WHERE cart_id = %s
        AND id = %s
    """, (
        cart_id,
        user_id
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("cart"))


# ================ DECREASE QUANTITY ================

@app.route("/decrease_quantity/<int:cart_id>")
def decrease_quantity(cart_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE cart
        SET quantity = quantity - 1
        WHERE cart_id = %s
        AND id = %s
        AND quantity > 1
    """, (
        cart_id,
        user_id
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("cart"))
# =========================================================
# MY ORDERS
# =========================================================

@app.route("/order")
def order():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM orders
        WHERE user_id = %s
        ORDER BY order_id DESC
    """, (user_id,))

    orders = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "order.html",
        orders=orders
    )

#------------------------ Forget password------------------------------


@app.route("/forgot", methods=["GET", "POST"])
def forgot():
    if request.method == "POST":
        email = request.form["email"]
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]
        hashed_password = generate_password_hash(new_password)

         # Check new password and confirm password
        if new_password != confirm_password:
            return render_template(
                "forgot.html",
                error="Password does not match."
            )

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email = %s",
            (email,)
        )
        user = cursor.fetchone()

        if user is None:

            cursor.close()
            conn.close()

            return render_template(
                "forgot.html",
                error="Email address not found."
            )

        # Hash the NEW password
        hashed_password = generate_password_hash(new_password)

        # Update password
        cursor.execute(
            """
            UPDATE users
            SET password = %s
            WHERE email = %s
            """,
            (hashed_password, email)
        )

        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for("login_user"))

    return render_template("forgot.html")
#-------------------------Registration Admin-----------------------------

@app.route("/registeradmin", methods=["GET", "POST"])
def register_admin():

    if request.method == "POST":

        fullname = request.form["fullname"]
        email = request.form["email"]
        mobile = request.form["mobile"]
        username = request.form["username"]
        password = request.form["password"]
        confirm = request.form["confirm_password"]

        # Check password
        if password != confirm:
            return "Password Does Not Match"

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            # Check existing username or email
            cursor.execute("""
                SELECT username, email
                FROM admin
                WHERE username = %s OR email = %s
            """, (username, email))

            existing_admin = cursor.fetchone()

            if existing_admin:
                cursor.close()
                conn.close()
                return "Username or Email Already Exists"

            # Hash password
            hashed_password = generate_password_hash(password)

            # Insert admin record
            cursor.execute("""
                INSERT INTO admin
                (full_name, email, username, password)
                VALUES (%s, %s, %s, %s)
            """, (
                fullname,
                email,
                username,
                hashed_password
            ))

            conn.commit()

            return redirect(url_for("login_admin"))

        except mysql.connector.Error as e:
            conn.rollback()
            print("Admin registration error:", e)
            return "Registration failed. Check the Flask terminal."

        finally:
            cursor.close()
            conn.close()

    return render_template("adminregistration.html")

# -------------------Login Verification admin-----------------

@app.route("/adminlogin", methods=["GET","POST"])
def login_admin():

    username = request.form["username"]
    password = request.form["password"]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM admin
    WHERE username=%s
    """,
    (username,))

    admin = cursor.fetchone()
    cursor.close()
    conn.close()
    # user name found or not
    if admin is None: 
        return """ <script> alert("Username not found!"); window.location.href = "/login"; </script> """
    
    # check hashed password

    if check_password_hash(admin[4], password):
        session["admin_id"] = admin[0]
        session["admin_username"] = admin[3]
        
        return redirect(url_for("admin_dashboard"))

    else:
        return "<h2>Invalid Username or Password</h2>"


#--------------admin dashboard--------------------
@app.route('/admin_dashboard')
def admin_dashboard():
    username=session.get('username')

    if 'admin_id' not in session:
        return redirect(url_for('login_admin'))

    return render_template('admindashboard.html',username=username)



#--------------Admin logout-------------

@app.route('/admin_logout')
def admin_logout():

    session.pop('admin_id', None)
    session.pop('admin_username', None)

    return redirect(url_for('login_admin'))








#----------------Admin-users,plants,pots,seeds,fertilizers----------------------
@app.route('/manage-user')
def admin_users():
    if 'admin_id' not in session:
        return redirect(url_for('login_admin'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users")

    users = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('admin_users.html', users=users)



@app.route('/admin/orders')
def admin_orders():

    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))

    conn = get_db_connection()
    
    cursor = conn.cursor(dictionary=True)

    # Get all orders
    cursor.execute("""
        SELECT *
        FROM orders
        ORDER BY order_id DESC
    """)

    orders = cursor.fetchall()

    # Get items for each order
    for order in orders:

        cursor.execute(""" 
            SELECT plant_name, price, quantity, item_total
            FROM order_items
            WHERE order_id = %s
        """, (order['order_id'],))

        order['items'] = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('admin_orders.html', orders=orders)



@app.route('/admin/update-order-status/<int:order_id>', methods=['POST'])
def update_order_status(order_id):

    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))

    status = request.form['status']

    conn = get_db_connection()

    cursor = conn.cursor()

    cursor.execute("""
        UPDATE orders
        SET status = %s
        WHERE order_id = %s
    """, (status, order_id))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('admin_orders'))

@app.route('/admin/plants')
def admin_plants():

    if 'admin_id' not in session:
        return redirect(url_for('login_admin'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
       SELECT 
       items.item_id, 
       items.item_name, 
       items.price, 
       items.stock, 
       items.category_id, 
       category.category_name, 
       items.plant_category_id, 
       plant_category.plant_category_name, 
       items.image FROM items LEFT JOIN category ON items.category_id = category.category_id LEFT JOIN plant_category ON items.plant_category_id = plant_category.plant_category_id WHERE items.category_id = 1 ORDER BY items.item_id DESC
    """)

    plants = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'admin_plants.html',
        plants=plants
    )

@app.route('/admin/pots')
def admin_pots():

    if 'admin_id' not in session:
        return redirect(url_for('login_admin'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            items.item_id,
            items.item_name,
            items.price,
            items.stock,
            items.image,
            items.category_id,
            category.category_name
        FROM items
        LEFT JOIN category
            ON items.category_id = category.category_id
        WHERE items.category_id = 2
        ORDER BY items.item_id DESC
    """)

    pots = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'admin_pots.html',
        pots=pots
    )




@app.route('/admin/seeds')
def admin_seeds():

    if 'admin_id' not in session:
        return redirect(url_for('login_admin'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            items.item_id,
            items.item_name,
            items.price,
            items.stock,
            items.image,
            items.category_id,
            category.category_name
        FROM items
        LEFT JOIN category
            ON items.category_id = category.category_id
        WHERE items.category_id = 4
        ORDER BY items.item_id DESC


      
    """)

    seeds = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'admin_seeds.html',
        seeds=seeds
    )

@app.route('/admin/fertilizers')
def admin_fertilizers():

    if 'admin_id' not in session:
        return redirect(url_for('login_admin'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            items.item_id,
            items.item_name,
            items.price,
            items.stock,
            items.image,
            items.category_id,
            category.category_name
        FROM items
        LEFT JOIN category
            ON items.category_id = category.category_id
        WHERE items.category_id = 3
        ORDER BY items.item_id DESC
    """)

    fertilizers = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'admin_fertilizers.html',
        fertilizers=fertilizers
    )


@app.route('/admin/issue')
def admin_issue():
    if 'admin_id' not in session:
        return redirect(url_for('login_admin'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM issue")

    issues = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('contact_table.html', issues=issues)
#------------------ Add plant,pots,seeds and fertilizers-------------

@app.route('/admin/add-plant/<item_type>', methods=['GET', 'POST'])
def add_plant(item_type):

    # Check admin login
    if 'admin_id' not in session:
        return redirect(url_for('login_admin'))

    # Create database connection
    conn = get_db_connection()

    # Dictionary cursor
    cursor = conn.cursor(dictionary=True)

    # Get categories from database
    cursor.execute("""
        SELECT category_id, category_name
        FROM category
    """)

    categories = cursor.fetchall()

    print("CATEGORIES:", categories)

    # If form is submitted
    if request.method == 'POST':

        item_name = request.form['item_name']
        price = request.form['price']
        stock = request.form['stock']

        # Category selected from dropdown
        category_id = request.form['category_id']

        # Plant category
        plant_category_id = request.form.get('plant_category_id')  or None

       
        # Get uploaded image
        image_file = request.files.get('image')

        image_name = None

        if image_file and image_file.filename != '':

            # Secure filename
            image_name = secure_filename(
                image_file.filename
            )

            # Image folder
            image_folder = os.path.join(
                app.root_path,
                'static',
                'images'
            )

            # Create folder if it doesn't exist
            os.makedirs(
                image_folder,
                exist_ok=True
            )

            # Save image
            image_file.save(
                os.path.join(
                    image_folder,
                    image_name
                )
            )

        # Insert into items table
        cursor.execute("""
            INSERT INTO items
            (
                category_id,
                item_name,
                price,
                stock,
                plant_category_id,
                image
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            category_id,
            item_name,
            price,
            stock,
            plant_category_id,
            image_name
        ))

                # Get automatically generated item_id
        item_id = cursor.lastrowid

        # -------------------------
        # INSERT INTO PLANTS
        # -------------------------

        cursor.execute("""
            INSERT INTO plants
            (plant_name, item_id)
            VALUES (%s, %s)
        """, (
            item_name,
            item_id
        ))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for('admin_plants'))

    cursor.close()
    conn.close()

    # Send categories to HTML
    return render_template(
        'add.html',
        item_type=item_type,
        categories=categories
    )





@app.route('/admin/add-pot', methods=['GET', 'POST'])
def add_pot():

    # Check admin login
    if 'admin_id' not in session:
        return redirect(url_for('login_admin'))

    # Create database connection
    conn = get_db_connection()

    # Dictionary cursor
    cursor = conn.cursor(dictionary=True)

    
    # Get categories from database
    cursor.execute("""
        SELECT category_id, category_name
        FROM category
    """)

    categories = cursor.fetchall()

    print("CATEGORIES:", categories)

    # If form is submitted
    if request.method == 'POST':

        item_name = request.form['item_name']
        price = request.form['price']
        stock = request.form['stock']

        # Pot category_id is 2
        category_id = 2

        # Pot does not have plant category
        plant_category_id = None

        # Get uploaded image
        image_file = request.files.get('image')

        image_name = None

        if image_file and image_file.filename != '':

            # Secure filename
            image_name = secure_filename(
                image_file.filename
            )

            # Image folder
            image_folder = os.path.join(
                app.root_path,
                'static',
                'images'
            )

            # Create folder if it doesn't exist
            os.makedirs(
                image_folder,
                exist_ok=True
            )

            # Save image
            image_file.save(
                os.path.join(
                    image_folder,
                    image_name
                )
            )

        # Insert into items table
        cursor.execute("""
            INSERT INTO items
            (
                category_id,
                item_name,
                price,
                stock,
                plant_category_id,
                image
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            category_id,
            item_name,
            price,
            stock,
            plant_category_id,
            image_name
        ))
        # Get generated item_id
        item_id = cursor.lastrowid

        # Insert into pots
        cursor.execute("""
            INSERT INTO pots
            (pot_type, item_id)
            VALUES (%s, %s)
        """, (
            item_name,
            item_id
        ))
        conn.commit()

        cursor.close()
        conn.close()

        # Go to Manage Pots
        return redirect(url_for('admin_pots'))

    cursor.close()
    conn.close()

    # Use the same add.html
    return render_template(
        'add.html',
        item_type='pot',
        categories=categories
    )


@app.route('/admin/add-seed', methods=['GET', 'POST'])
def add_seed():

    # Check admin login
    if 'admin_id' not in session:
        return redirect(url_for('login_admin'))

    # Create database connection
    conn = get_db_connection()

    # Dictionary cursor
    cursor = conn.cursor(dictionary=True)

    # Get categories from database
    cursor.execute("""
        SELECT category_id, category_name
        FROM category
    """)

    categories = cursor.fetchall()

    print("CATEGORIES:", categories)

    # If form is submitted
    if request.method == 'POST':

        item_name = request.form['item_name']
        price = request.form['price']
        stock = request.form['stock']

        # Seed category_id is 3
        category_id = 4

        # Seed does not have plant category
        plant_category_id = None

        # Get uploaded image
        image_file = request.files.get('image')

        image_name = None

        if image_file and image_file.filename != '':

            # Secure filename
            image_name = secure_filename(
                image_file.filename
            )

            # Image folder
            image_folder = os.path.join(
                app.root_path,
                'static',
                'images'
            )

            # Create folder if it doesn't exist
            os.makedirs(
                image_folder,
                exist_ok=True
            )

            # Save image
            image_file.save(
                os.path.join(
                    image_folder,
                    image_name
                )
            )

        # Insert into items table
        cursor.execute("""
            INSERT INTO items
            (
                category_id,
                item_name,
                price,
                stock,
                plant_category_id,
                image
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            category_id,
            item_name,
            price,
            stock,
            plant_category_id,
            image_name
        ))
         # Get generated item_id
        item_id = cursor.lastrowid

        # Insert into seeds
        cursor.execute("""
            INSERT INTO seeds
            (seed_name, item_id)
            VALUES (%s, %s)
        """, (
            item_name,
            item_id
        ))

        conn.commit()

        cursor.close()
        conn.close()

        # Go to Manage Seeds
        return redirect(url_for('admin_seeds'))

    cursor.close()
    conn.close()

    # Use the same add.html
    return render_template(
        'add.html',
        item_type='seed',
        categories=categories
    )


@app.route('/admin/add-fertilizer', methods=['GET', 'POST'])
def add_fertilizer():

    # Check admin login
    if 'admin_id' not in session:
        return redirect(url_for('login_admin'))

    # Create database connection
    conn = get_db_connection()

    # Dictionary cursor
    cursor = conn.cursor(dictionary=True)

    # Get categories from database
    cursor.execute("""
        SELECT category_id, category_name
        FROM category
    """)

    categories = cursor.fetchall()

    print("CATEGORIES:", categories)

    # If form is submitted
    if request.method == 'POST':

        item_name = request.form['item_name']
        price = request.form['price']
        stock = request.form['stock']

        # Fertilizer category_id
        category_id = 3

        # Fertilizer does not have plant category
        plant_category_id = None

        # Get uploaded image
        image_file = request.files.get('image')

        image_name = None

        if image_file and image_file.filename != '':

            # Secure filename
            image_name = secure_filename(
                image_file.filename
            )

            # Image folder
            image_folder = os.path.join(
                app.root_path,
                'static',
                'images'
            )

            # Create folder if it doesn't exist
            os.makedirs(
                image_folder,
                exist_ok=True
            )

            # Save image
            image_file.save(
                os.path.join(
                    image_folder,
                    image_name
                )
            )

        # Insert into items table
        cursor.execute("""
            INSERT INTO items
            (
                category_id,
                item_name,
                price,
                stock,
                plant_category_id,
                image
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            category_id,
            item_name,
            price,
            stock,
            plant_category_id,
            image_name
        ))
         # Get generated item_id
        item_id = cursor.lastrowid

        # Insert into fertilizers
        cursor.execute("""
            INSERT INTO fertilizer
            (fertilizer_name, item_id)
            VALUES (%s, %s)
        """, (
            item_name,
            item_id
        ))

        

        conn.commit()

        cursor.close()
        conn.close()

        # Go to Manage Fertilizers
        return redirect(url_for('admin_fertilizers'))

    cursor.close()
    conn.close()

    # Use the same add.html
    return render_template(
        'add.html',
        item_type='fertilizer',
        categories=categories
    )

#--------------- Delete plant ----------------

@app.route('/admin/delete-plant/<int:item_id>')
def delete_plant(item_id):

    # Check admin login
    if 'admin_id' not in session:
        return redirect(url_for('login_admin'))

    conn = get_db_connection()
    cursor = conn.cursor()

    

    # Delete plant from database
    cursor.execute(
        "DELETE FROM items WHERE item_id = %s",
        (item_id,)
    )

    conn.commit()

    
    cursor.close()
    conn.close()

    return redirect(url_for('admin_plants'))


@app.route('/admin/delete-pot/<int:item_id>')
def delete_pot(item_id):

    # Check admin login
    if 'admin_id' not in session:
        return redirect(url_for('login_admin'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Delete pot from database
    cursor.execute(
        """
        DELETE FROM items
        WHERE item_id = %s
        AND category_id = 2
        """,
        (item_id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('admin_pots'))



@app.route('/admin/delete-seed/<int:item_id>')
def delete_seed(item_id):

    if 'admin_id' not in session:
        return redirect(url_for('login_admin'))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM items
        WHERE item_id = %s
        AND category_id = 4
    """, (item_id,))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('admin_seeds'))



@app.route('/admin/delete-fertilizer/<int:item_id>')
def delete_fertilizer(item_id):

    if 'admin_id' not in session:
        return redirect(url_for('login_admin'))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM items
        WHERE item_id = %s
        AND category_id = 3
    """, (item_id,))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('admin_fertilizers'))
# ===== Contact / Issue =====

@app.route("/contact", methods=["POST"])
def contact():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    # Check user exists

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, fullname, email
        FROM users
        WHERE id = %s
    """, (user_id,))

    user = cursor.fetchone()

    if user is None:

        session.clear()

        cursor.close()
        conn.close()

        return redirect(url_for("login"))

    name = request.form.get("name", user["fullname"])
    email = request.form.get("email", user["email"])
    product_name = request.form.get("pro_name", "")

    issue_date = request.form.get("issue_date", "")

    # Check issue date
    today = date.today().isoformat()

    if issue_date != today:
        cursor.close()
        conn.close()
        return "Only today's date is allowed."

    issue_type = request.form.get(
        "issue_type",
        request.form.get("issue", "")
    )

    message = request.form.get("message", "")

    image_name = None

    # Image only for damaged plant

    image = request.files.get("image")

    if issue_type == "Damaged Plant" and image and image.filename:

        image_name = secure_filename(image.filename)

        image_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            image_name
        )

        image.save(image_path)

    cursor.execute("""
        INSERT INTO issue
        (
            id,
            name,
            email,
            product_name,
            issue_date,
            issue_type,
            message,
            image
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        user_id,
        name,
        email,
        product_name,
        issue_date,
        issue_type,
        message,
        image_name
    ))

    conn.commit()
    flash("✓ Message Sent Successfully!")
    cursor.close()
    conn.close()

    return redirect(url_for("catalog"))
# ===== Contact Table =====

@app.route("/contact_table")
def contact_table():

    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            issue_id,
            id,
            name,
            email,
            product_name,
            issue_date,
            issue_type,
            message,
            image
        FROM issue
        ORDER BY issue_id DESC
    """)

    issues = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "contact_table.html",
        issues=issues
    )

#=======Indoor Plant Guidance==========

@app.route('/indoorgui')
def indoorgui():
    return render_template('indoor.html')



#=======Medicinal Plant Guidance==========

@app.route('/medicinalgui')
def medicinalgui():
    return render_template('medicinal.html')




#=======Fruit Plant Guidance==========

@app.route('/fruitgui')
def fruitgui():
    return render_template('fruits.html')



#=======Flower Plant Guidance==========

@app.route('/flowergui')
def flowergui():
    return render_template('flowers.html')

# ==========================================
# DELIVERY PAGE
# ==========================================

@app.route("/delivery", methods=["GET", "POST"])
def delivery():

    if request.method == "POST":

        address_line1 = request.form.get(
            "address_line1",
            ""
        ).strip()

        address_line2 = request.form.get(
            "address_line2",
            ""
        ).strip()

        city = request.form.get(
            "city",
            ""
        ).strip()

        pincode = request.form.get(
            "pincode",
            ""
        ).strip()

        state = request.form.get(
            "state",
            ""
        ).strip()

        country = request.form.get(
            "country",
            "India"
        ).strip()


        # ==================================
        # VALIDATION
        # ==================================

        if not address_line1:

            return render_template(
                "delivery.html",
                error="Please enter Address Line 1."
            )


        if not city:

            return render_template(
                "delivery.html",
                error="Please enter City."
            )


        if not pincode.isdigit() or len(pincode) != 6:

            return render_template(
                "delivery.html",
                error="Please enter a valid 6-digit Pincode."
            )


        if not state:

            return render_template(
                "delivery.html",
                error="Please select State."
            )


        # ==================================
        # SAVE DELIVERY DETAILS IN SESSION
        # ==================================

        session["delivery"] = {

            "address_line1": address_line1,

            "address_line2": address_line2,

            "city": city,

            "pincode": pincode,

            "state": state,

            "country": country

        }


        # Go to payment

        return redirect(
            url_for("payment")
        )


    return render_template(
        "delivery.html"
    )



# ==========================================
# PAYMENT PAGE
# ==========================================

@app.route("/payment", methods=["GET", "POST"])
def payment():

    # User must be logged in
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Delivery details must exist
    if "delivery" not in session:
        return redirect(url_for("delivery"))

    user_id = session["user_id"]

    # ======================================
    # GET CART FROM DATABASE
    # ======================================

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            cart.cart_id,
            cart.item_id,
            cart.quantity,
            items.item_name,
            items.price,
            items.image
        FROM cart
        JOIN items
            ON cart.item_id = items.item_id
        WHERE cart.id = %s
    """, (user_id,))

    cart_items = cursor.fetchall()

    cursor.close()
    connection.close()

    # ======================================
    # CHECK EMPTY CART
    # ======================================

    if not cart_items:
        return redirect(url_for("cart"))

    # ======================================
    # CALCULATE TOTAL
    # ======================================

    subtotal = 0

    for item in cart_items:
        item["item_total"] = float(item["price"]) * item["quantity"]
        subtotal += item["item_total"]

    total_amount = subtotal

    # ======================================
    # PLACE ORDER
    # ======================================

    if request.method == "POST":

        payment_method = request.form.get("payment_method", "")

        allowed_methods = [
            "Cash on Delivery",
            "UPI / Net Banking",
            "Credit / Debit Card"
        ]

        # ==================================
        # PAYMENT VALIDATION
        # ==================================

        if payment_method not in allowed_methods:

            return render_template(
                "payment.html",
                cart_items=cart_items,
                subtotal=subtotal,
                total_amount=total_amount,
                error="Please select a valid payment method."
            )

        delivery = session["delivery"]

        connection = None
        cursor = None

        try:

            # ==================================
            # DATABASE CONNECTION
            # ==================================

            connection = get_db_connection()
            cursor = connection.cursor()

            # ==================================
            # GET USERNAME
            # ==================================

            cursor.execute("""
                SELECT username
                FROM users
                WHERE id = %s
            """, (user_id,))

            user = cursor.fetchone()

            if user:
                username = user[0]
            else:
                username = session.get("username", "Guest")

            # ==================================
            # INSERT ORDER
            # ==================================

            sql = """
                INSERT INTO orders
                (
                    
                    username,
                    address_line1,
                    address_line2,
                    city,
                    pincode,
                    state,
                    country,
                    payment_method,
                    subtotal,
                    total_amount,
                    status
                )
                VALUES
                (
                    
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
            """

            values = (
                
                username,
                delivery["address_line1"],
                delivery["address_line2"],
                delivery["city"],
                delivery["pincode"],
                delivery["state"],
                delivery["country"],
                payment_method,
                subtotal,
                total_amount,
                "Placed"
            )

            cursor.execute(sql, values)

            # Get order ID
            order_id = cursor.lastrowid

            # ==================================
            # INSERT ORDER ITEMS
            # ==================================

            for item in cart_items:

                cursor.execute("""
                    INSERT INTO order_items
                    (
                        order_id,
                        plant_name,
                        price,
                        quantity,
                        item_total
                    )
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    order_id,
                    item["item_name"],
                    item["price"],
                    item["quantity"],
                    item["item_total"]
                ))

            # ==================================
            # CLEAR USER CART
            # ==================================

            cursor.execute("""
                DELETE FROM cart
                WHERE id = %s
            """, (user_id,))

            # ==================================
            # SAVE DATABASE
            # ==================================

            connection.commit()

            # Remove delivery information
            session.pop("delivery", None)

            # ==================================
            # SUCCESS PAGE
            # ==================================

            return redirect(
                url_for(
                    "order_success",
                    order_id=order_id
                )
            )

        except mysql.connector.Error as error:

            if connection:
                connection.rollback()

            print("Database Error:", error)

            return render_template(
                "payment.html",
                cart_items=cart_items,
                subtotal=subtotal,
                total_amount=total_amount,
                error="Order could not be placed. Please check your database."
            )

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()

    # ======================================
    # OPEN PAYMENT PAGE
    # ======================================

    return render_template(
        "payment.html",
        cart_items=cart_items,
        subtotal=subtotal,
        total_amount=total_amount
    )

# ==========================================
# ORDER SUCCESS
# ==========================================

@app.route("/order-success/<int:order_id>")
def order_success(order_id):

    return render_template(

        "order_success.html",

        order_id=order_id

    )

# ==========================================
# MY ORDERS
# ==========================================

@app.route("/my_order")
def my_order():

    username = session.get("username", "Guest")

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Get orders
    cursor.execute("""
        SELECT *
        FROM orders
        WHERE username = %s
        ORDER BY order_date DESC
    """, (username,))

    orders = cursor.fetchall()

    # Get plants for every order
    for order in orders:

        cursor.execute("""
            SELECT
                plant_name,
                price,
                quantity,
                item_total
            FROM order_items
            WHERE order_id = %s
        """, (order["order_id"],))

        order["items"] = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "my_order.html",
        orders=orders
    )

        
if __name__ == "__main__":
    app.run(debug=True)





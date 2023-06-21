from flask import Flask, request, render_template, session, redirect, url_for
from flask_session import Session
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required
import sqlite3
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'elasesornic@gmail.com'
app.config['MAIL_PASSWORD'] = 'rkhhzmwdrqzsjyvu'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = 'clave_secreta'
Session(app)
db = SQL("sqlite:///base.db")

def get_user_name(user_id):
    if user_id is None:
        return None
    user = db.execute("SELECT name FROM users WHERE id = ?", user_id)
    if user:
        return user[0]["name"]
    return None

def get_money(user_id):
    if user_id is None:
        return None
    user = db.execute("SELECT money FROM users WHERE id = ?", user_id)
    if user:
        return user[0]["money"]
    return None

@app.route("/")
def index():
    user_logged_in = False
    user_name = None
    money = None

    if "user_id" in session:
        user_logged_in = True
        user_name = get_user_name(session["user_id"])
        money = get_money(session["user_id"])

    return render_template("index.html", user_logged_in=user_logged_in, user_name=user_name, money=money)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        name = request.form.get("nombre")
        last_name = request.form.get("apellido")
        email = request.form.get("correo")
        password = request.form.get("password")
        confirm = request.form.get("confirmation")

        if not name or not last_name or not email or not password or not confirm:
            return render_template("register.html", error="Debe proporcionar todos los campos")
        elif password != confirm:
            return render_template("register.html", error="Las contraseñas no coinciden")
        else:

            msg = Message("Message from your site",sender='elasesornic@gmail.com', recipients=[email])
            msg.body = "se pudp"
            msg.html = render_template('email.html', name=name, email=email)
            mail.send(msg)
            
            
            db.execute("""INSERT INTO users (name, last_name, mail, hash, money) VALUES (?, ?, ?, ?, ?)""",
                       name, last_name, email, generate_password_hash(password), 15000)
            rows = db.execute("SELECT id FROM users WHERE mail = ?", email)
            session["user_id"] = rows[0]["id"]
            return redirect("/")
    else:
        return render_template("register.html")

@app.route('/registrarse')
def registrarse():
    return redirect("/register")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        correo = request.form.get("correo")
        contraseña = request.form.get("contraseña")

        if not correo:
            return render_template("index.html", error="Debe proporcionar el correo electrónico")
        elif not contraseña:
            return render_template("index.html", error="Debe proporcionar la contraseña")

        rows = db.execute("SELECT * FROM users WHERE mail = ?", correo)

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], contraseña):
            return render_template("index.html", error="Correo y/o contraseña inválidos")

        session["user_id"] = rows[0]["id"]

        if session["user_id"] == 1:
            return redirect("/admin")

        return redirect("/")
    else:
        return render_template("index.html")

@app.route("/catalogo", methods=["GET", "POST"])
def catalogo():
    user_logged_in = False
    user_name = None
    money = None

    if "user_id" in session:
        user_logged_in = True
        user_name = get_user_name(session["user_id"])
        money = get_money(session["user_id"])

    return render_template("catalogpdf.html", user_logged_in=user_logged_in, user_name=user_name, money=money)

@app.route("/send", methods=["GET", "POST"])
def send():
    if request.method == "POST":
        name = request.form.get("nombre")
        price = request.form.get("price")
        stock = request.form.get("stock")
        description = request.form.get("description")
        category = request.form.get("category")
        url = request.form.get("url")

        if not name or not price or not stock or not description or not category or not url:
            render_template("apology.html")

        stock = int(request.form.get("stock"))

        if stock < 0 or not isinstance(stock, int):
            render_template("apology.html")

        db.execute("INSERT INTO products (name, stock, price, description, id_category, url) VALUES(?, ?, ?, ?, ?, ?)",
                    name, stock, price, description, category, url)

        # Guardar las especificaciones en la base de datos
        product_id = db.execute("SELECT id FROM products ORDER BY id DESC LIMIT 1")[0]["id"]

        for key in request.form:
            if key.startswith("attribute") and request.form[key]:
                attribute_num = key.replace("attribute", "")
                attribute = request.form[key]
                value = request.form.get("value" + attribute_num)
                db.execute("INSERT INTO product_specifications (product_id, attribute, value) VALUES (?, ?, ?)",
                           product_id, attribute, value)

        return render_template("send.html")
    else:
        if session.get("user_id") is None:
            return redirect("/login")
        if session["user_id"] == 1:
            return render_template("send.html")
        else:
            return redirect("/")

@app.route("/stock", methods=["GET", "POST"])
def stock():
    if request.method == "POST":
        id = request.form.get("product")
        stock = request.form.get("stock")

        if not id or not stock:
            return("apology.html")

        db.execute("UPDATE products SET stock = ? WHERE id = ?", stock, id)

        products = db.execute("SELECT * FROM products")
        return render_template("stock.html", products = products)
    else:
        if session.get("user_id") is None:
            return redirect("/login")
        if session["user_id"] == 1:
            products = db.execute("SELECT * FROM products")
            return render_template("stock.html", products = products)
        else:
            return redirect("/")

@app.route('/admin')
def admin():
    if session.get("user_id") is None:
        return redirect("/login")
    if session["user_id"] == 1:
        return render_template("admin.html")
    else:
        return redirect("/")

@app.route('/quienes')
def quienes():
    user_logged_in = False
    user_name = None
    money = None

    if "user_id" in session:
        user_logged_in = True
        user_name = get_user_name(session["user_id"])
        money = get_money(session["user_id"])

    return render_template("quienes.html", user_logged_in=user_logged_in, user_name=user_name, money=money)


@app.route('/contacto')
def contacto():
    user_logged_in = False
    user_name = None
    money = None

    if "user_id" in session:
        user_logged_in = True
        user_name = get_user_name(session["user_id"])
        money = get_money(session["user_id"])

    return render_template("contacto.html", user_logged_in=user_logged_in, user_name=user_name, money=money)

# Rutas adicionales relacionadas con los productos (proporcionadas en tu código original)
@app.route("/products", defaults={'page': 1})
@app.route("/products/<int:page>")
def products(page=1):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()

    # Calcular el índice inicial y final de los productos para la página actual
    products_per_page = 12  # Define la cantidad de productos por página
    start_index = (page - 1) * products_per_page
    end_index = start_index + products_per_page

    # Consulta SQL con límites para la paginación
    cursor.execute('SELECT * FROM products LIMIT ?, ?', (start_index, products_per_page))
    products = cursor.fetchall()

    # Calcular el número total de páginas requeridas
    cursor.execute('SELECT COUNT(*) FROM products')
    total_products = cursor.fetchone()[0]
    total_pages = (total_products // products_per_page) + (total_products % products_per_page > 0)

    conn.close()

    user_logged_in = False
    user_name = None
    money = None

    if "user_id" in session:
        user_logged_in = True
        user_name = get_user_name(session["user_id"])
        money = get_money(session["user_id"])


    return render_template('details.html', products=products, total_pages=total_pages, current_page=page, user_logged_in=user_logged_in, user_name=user_name, money=money)
    # ...

@app.route("/product/<int:product_id>")
def product(product_id):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    product = cursor.fetchone()

    product_specifications = db.execute("SELECT * FROM product_specifications WHERE product_id = ?", product_id)

    cursor.execute('SELECT * FROM products WHERE id_category = ? AND id != ? ORDER BY RANDOM() LIMIT 6', (product[5], product_id))
    related_products = cursor.fetchall()

    conn.close()

    user_logged_in = False
    user_name = None
    money = None

    if "user_id" in session:
        user_logged_in = True
        user_name = get_user_name(session["user_id"])
        money = get_money(session["user_id"])

    return render_template('products.html', product=product, product_specifications=product_specifications,
                           related_products=related_products, user_logged_in=user_logged_in, user_name=user_name,
                           money=money)

@app.route("/products_by_category/<int:category_id>", defaults={'page': 1})
@app.route("/products_by_category/<int:category_id>/<int:page>")
def products_by_category(category_id, page=1):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()

    # Calcular el índice inicial y final de los productos para la página actual
    products_per_page = 12  # Define la cantidad de productos por página
    start_index = (page - 1) * products_per_page
    end_index = start_index + products_per_page

    # Consulta SQL con límites para la paginación
    cursor.execute('SELECT * FROM products WHERE id_category = ? LIMIT ?, ?', (category_id, start_index, products_per_page))
    products = cursor.fetchall()

    # Calcular el número total de páginas requeridas
    cursor.execute('SELECT COUNT(*) FROM products WHERE id_category = ?', (category_id,))
    total_products = cursor.fetchone()[0]
    total_pages = (total_products // products_per_page) + (total_products % products_per_page > 0)

    conn.close()

    user_logged_in = False
    user_name = None
    money = None

    if "user_id" in session:
        user_logged_in = True
        user_name = get_user_name(session["user_id"])
        money = get_money(session["user_id"])

    return render_template('products_by_category.html', products=products, total_pages=total_pages, current_page=page, category_id=category_id, user_logged_in=user_logged_in, user_name=user_name, money=money)

@app.route('/search', defaults={'page': 1})
@app.route('/search/<int:page>')
def search(page=1):
    texto_busqueda = request.args.get('texto_busqueda', '')

    # Calcular el índice inicial y final de los productos para la página actual
    products_per_page = 12  # Define la cantidad de productos por página
    start_index = (page - 1) * products_per_page
    end_index = start_index + products_per_page

    # Realiza la consulta a la base de datos con límites para la paginación
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE name LIKE ? LIMIT ?, ?", ('%' + texto_busqueda + '%', start_index, products_per_page))
    resultados = cursor.fetchall()

    # Calcular el número total de productos encontrados
    cursor.execute("SELECT COUNT(*) FROM products WHERE name LIKE ?", ('%' + texto_busqueda + '%',))
    total_products = cursor.fetchone()[0]
    total_pages = (total_products // products_per_page) + (total_products % products_per_page > 0)

    conn.close()

    user_logged_in = False
    user_name = None
    money = None

    if "user_id" in session:
        user_logged_in = True
        user_name = get_user_name(session["user_id"])
        money = get_money(session["user_id"])

    return render_template('search.html', resultados=resultados, total_pages=total_pages, current_page=page, user_logged_in=user_logged_in, user_name=user_name, money=money)

@app.route('/confirm', methods=["GET", "POST"])
def confirm():
    if request.method == "POST":
        return render_template('confirm.html')
    else:
        return render_template('confirm.html')


if __name__ == '__main__':
    app.run(debug=True)


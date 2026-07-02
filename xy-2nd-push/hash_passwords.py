from werkzeug.security import generate_password_hash
from flask_mysqldb import MySQL
from app import create_app, mysql

app = create_app()

users = [
    ("admin123", 1),   # System Administrator
    ("pswdo123", 2),   # PSWDO Administrator
    ("cswdo123", 3),   # Urdaneta CSWDO
    ("cswdo123", 4),   # Santa Barbara MSWDO
    ("cswdo123", 5),   # Calasiao MSWDO
]

with app.app_context():
    cur = mysql.connection.cursor()
    for password, user_id in users:
        hashed = generate_password_hash(password)
        cur.execute("UPDATE users SET password = %s WHERE user_id = %s", (hashed, user_id))
    mysql.connection.commit()
    cur.close()
    print("Passwords hashed successfully.")
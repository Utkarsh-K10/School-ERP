# models/user_model.py

from config.mysql_connection import get_connection
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_admin(username, password):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM admin WHERE username=%s", (username,))
    if cursor.fetchone():
        print("Admin already exists.")
        return

    hashed_pw = hash_password(password)
    cursor.execute("INSERT INTO admin (username, password_hash) VALUES (%s, %s)", (username, hashed_pw))
    connection.commit()
    print("✅ Admin created successfully.")
    cursor.close()
    connection.close()

def verify_admin(username, password):
    connection = get_connection()
    cursor = connection.cursor()
    hashed_pw = hash_password(password)

    cursor.execute("SELECT * FROM admin WHERE username=%s AND password_hash=%s", (username, hashed_pw))
    result = cursor.fetchone()

    cursor.close()
    connection.close()
    return result is not None

# Temporary script to create admin
if __name__ == "__main__":
    create_admin("admin", "admin123")

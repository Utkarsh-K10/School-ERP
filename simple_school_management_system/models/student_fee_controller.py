# models/student_fee_controller.py
from config.mysql_connection import get_connection

def get_student_by_uid(uid):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students WHERE student_uid = %s", (uid,))
    student = cursor.fetchone()
    conn.close()
    return student

def get_all_students():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students ORDER BY student_uid ASC")
    students = cursor.fetchall()
    conn.close()
    return students

def get_latest_fee_record(uid):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT * FROM fee_payments 
        WHERE student_uid = %s 
        ORDER BY submission_date DESC 
        LIMIT 1
    """
    cursor.execute(query, (uid,))
    record = cursor.fetchone()
    conn.close()
    return record

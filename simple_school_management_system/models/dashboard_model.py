# models/dashboard_model.py

from config.db_config import create_connection

def get_stats():
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0] or 0

    cursor.execute("SELECT COALESCE(SUM(received), 0) FROM student_fee")
    total_collected = cursor.fetchone()[0] or 0

    cursor.execute("SELECT COALESCE(SUM(outstanding), 0) FROM student_fee")
    total_outstanding = cursor.fetchone()[0] or 0

    cursor.close()
    connection.close()

    return {
        "total_students": total_students,
        "total_collected": total_collected,
        "total_outstanding": total_outstanding
    }

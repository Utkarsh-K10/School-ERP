# models/student_fee_controller.py

from config.db_config import create_connection

def get_student_by_uid(uid):
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM students WHERE student_uid = %s", (uid,))
    student = cursor.fetchone()

    cursor.close()
    conn.close()
    return student

def add_student_fee(data):
    try:
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO student_fee (
                student_uid, total_fee, discount, received, outstanding,
                late_fee, submission_date
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            data['student_uid'], data['total_fee'], data['discount'],
            data['received'], data['outstanding'],
            data['late_fee'], data['submission_date']
        ))

        conn.commit()
        cursor.close()
        conn.close()
        return True, "Fee record saved successfully."
    except Exception as e:
        return False, str(e)

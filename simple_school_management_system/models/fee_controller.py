# models/fee_controller.py

from config.mysql_connection import get_connection

def add_fee_structure(class_, section, tuition, transport, activity, admission, total):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO fee_structure (class, section, tuition_fee, transport_fee,
                                activity_fee, admission_fee, total_fee)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (class_, section, tuition, transport, activity, admission, total))
    conn.commit()
    cursor.close()
    conn.close()

def get_all_fee_structures():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT class, section, tuition_fee, transport_fee,
            activity_fee, admission_fee, total_fee
        FROM fee_structure
        ORDER BY class, section
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def get_fee_structure_by_class_section(class_, section):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM fee_structure WHERE class=%s AND section=%s
    """, (class_, section))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result


def delete_fee_structure(class_, section):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM fee_structure WHERE class=%s AND section=%s", (class_, section))
    conn.commit()
    cursor.close()
    conn.close()

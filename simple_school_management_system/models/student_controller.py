# models/student_controller.py

from config.db_config import create_connection

def get_next_student_uid():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    count = cursor.fetchone()[0] + 1
    cursor.close()
    conn.close()
    return f"RKMS{count:04d}"

def register_student(data):
    try:
        conn = create_connection()
        cursor = conn.cursor()

        sql = """
        INSERT INTO students (
            student_uid, name, class, section, dob, father_name, mother_name,
            adhar_no, under_rte, apar_id, medium, roll_no, session, address,
            whatsapp_no, guardian_contact, bank_account, ifsc_code,
            subject_group, school_house
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (
            data['student_uid'], data['name'], data['class'], data['section'], data['dob'],
            data['father_name'], data['mother_name'], data['adhar_no'],
            data['under_rte'] == "Yes", data['apar_id'], data['medium'], data['roll_no'],
            data['session'], data['address'], data['whatsapp_no'],
            data['guardian_contact'], data['bank_account'], data['ifsc_code'],
            data.get('subject_group'), data.get('school_house')
        ))

        conn.commit()
        cursor.close()
        conn.close()
        return True, f"Student {data['name']} registered successfully with UID {data['student_uid']}"

    except Exception as e:
        return False, f"Error: {e}"

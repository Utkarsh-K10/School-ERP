# models/init_db.py
from config.db_config import create_connection

def initialize_db():
    connection = create_connection()
    if connection is None:
        print("Database connection failed.")
        return

    cursor = connection.cursor()

    queries = [
        """
        CREATE TABLE IF NOT EXISTS admin (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50),
            password_hash TEXT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_uid VARCHAR(20) UNIQUE,
            name VARCHAR(100),
            class VARCHAR(10),
            section VARCHAR(5),
            dob DATE,
            father_name VARCHAR(100),
            mother_name VARCHAR(100),
            adhar_no VARCHAR(12),
            under_rte BOOLEAN,
            apar_id VARCHAR(20),
            medium ENUM('Hindi', 'English'),
            roll_no INT,
            session VARCHAR(20),
            subject_group ENUM('Maths', 'Bio', 'Arts', 'Commerce') DEFAULT NULL,
            school_house ENUM('Himalaya', 'Satpura', 'Nilgiri', 'Vindhyanchal') DEFAULT NULL,
            address TEXT,
            whatsapp_no VARCHAR(15),
            guardian_contact VARCHAR(15),
            bank_account VARCHAR(20),
            ifsc_code VARCHAR(15)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS fee_structure (
            id INT AUTO_INCREMENT PRIMARY KEY,
            class VARCHAR(10),
            section VARCHAR(5),
            tuition_fee DECIMAL(10,2),
            transport_fee DECIMAL(10,2),
            activity_fee DECIMAL(10,2),
            admission_fee DECIMAL(10,2),
            total_fee DECIMAL(10,2)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS student_fee (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_uid VARCHAR(20),
            total_fee DECIMAL(10,2),
            discount DECIMAL(10,2),
            received DECIMAL(10,2),
            outstanding DECIMAL(10,2),
            late_fee DECIMAL(10,2),
            submission_date DATE,
            FOREIGN KEY (student_uid) REFERENCES students(student_uid)
        )
        """
    ]

    for query in queries:
        cursor.execute(query)

    connection.commit()
    cursor.close()
    connection.close()
    print("✅ Database tables initialized successfully.")

# Run this script directly to initialize
if __name__ == "__main__":
    initialize_db()

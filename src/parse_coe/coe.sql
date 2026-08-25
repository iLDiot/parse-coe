CREATE TABLE confirmation_of_enrolment (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    -- Provider
    provider_name VARCHAR(255) NOT NULL,
    provider_cicros_code VARCHAR(20),
    email VARCHAR(255),

    -- Course
    coe_code VARCHAR(100) UNIQUE,
    course_name VARCHAR(255) NOT NULL,
    course_code VARCHAR(30),
    course_level VARCHAR(100),
    course_start_date DATE,
    course_end_date DATE,

    -- Fees
    total_tuition_fee VARCHAR(20),

    -- Student
    provider_student_id VARCHAR(50),
    family_name VARCHAR(100),
    given_name VARCHAR(255),
    gender VARCHAR(30),
    date_of_birth DATE,
    country_of_birth VARCHAR(100),
    nationality VARCHAR(100),

    -- System
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);
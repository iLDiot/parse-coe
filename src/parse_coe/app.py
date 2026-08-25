from pathlib import Path
from datetime import datetime
import argparse
import pymupdf
import mysql.connector
import re
import sys

parser = argparse.ArgumentParser(description="Parse CoE files and save them to a database", prog="parse-coe")

parser.add_argument("--file", help="Select PDF to parse coe")

args = parser.parse_args()

def main():
    if args.file:      
        file = args.file
        text = ""
        with pymupdf.open(file) as document:
            for page in document:
                text += page.get_text()
                # print(text)
        if "Overseas Student Confirmation-of-Enrolment" not in text:
            sys.exit(f"❌ Error: file name: {file}. Is not a Confirmation of Enrolment document.")
                
        search_coe_code = re.search(r"(.*?)\s+Overseas Student Confirmation-of-Enrolment",text)
        coe_code = search_coe_code.group(1).strip() if search_coe_code else 'Course Code Not Found'
        
        search_provider_name = re.search(r"Provider:\s+(.*?)\[" ,text) 
        provider_name = search_provider_name.group(1).strip() if search_provider_name else 'Provider Name Not Found' 
       
        search_provider_cicros_code = re.search(r"Provider:.*?\[(.*?)\] " ,text) 
        provider_cicros_code = search_provider_cicros_code.group(1).strip() if search_provider_cicros_code else 'Provider Cicros Code Not Found' 
       
        search_email = re.search(r"Email:(.*?)\s+Course:" ,text) 
        email = search_email.group(1).strip() if search_email else 'Email Address Not Found' 

        search_course_name = re.search(r"Course:\s+(.*?)\s+\[",text)
        course_name = search_course_name.group(1).strip() if search_course_name else 'Course Name Not Found'
                                                                  
        search_course_code = re.search(r"Course:.*?\[(.*?)\]",text)
        course_code = search_course_code.group(1).strip() if search_course_code else 'Course Code Not Found'
                     
        search_course_level = re.search(r"Course Level:(.*?)\s+Course Start Date:",text)
        course_level = search_course_level.group(1).strip() if search_course_level else 'Course Level Not Found'
               
        search_course_start_date = re.search(r"Course Start Date:\s+(.*?)\s+Course End Date:", text)
        format_course_start_date = search_course_start_date.group(1).strip() if search_course_start_date else 'Course Start Date Not Found'
        course_start_date = datetime.strptime(format_course_start_date, "%d/%m/%Y").date()
        
        search_course_end_date = re.search(r"Course End Date:\s+(.*?)\s+", text)
        format_course_end_date = search_course_end_date.group(1).strip() if search_course_end_date else 'Course End Date Not Found'
        course_end_date = datetime.strptime(format_course_end_date, "%d/%m/%Y").date()

        search_total_tuition_fee = re.search(r"Total Tuition Fee:\s+(.*?\s)\s+",text)
        total_tuition_fee = search_total_tuition_fee.group(1).strip() if search_total_tuition_fee else 'Total Tuition Fee Not Found'
                
        search_provider_student_id = re.search(r"Provider Student Id:\s+(.*?\s)\s+", text)
        provider_student_id = search_provider_student_id.group(1) if search_provider_student_id else 'Provider Student ID Not Found'
        
        search_gender = re.search(r"Gender:\s+(.*?\s)\s+",text)
        gender = search_gender.group(1).strip() if search_gender else 'Gender Not Found'
        
        search_date_of_birth = re.search(r"Date of Birth:\s+(.*?\s)\s+",text)
        parse_date_of_birth = search_date_of_birth.group(1).strip() if search_date_of_birth else 'Date of Birth Not Found'
        date_of_birth = datetime.strptime(parse_date_of_birth, "%d/%m/%Y").date()
               
        search_country_of_birth = re.search(r"Country of Birth:\s+(.*?\s)\s+", text)
        country_of_birth = search_country_of_birth.group(1).strip() if search_country_of_birth else 'Country of Birth Not Found' 
        
        search_nationality = re.search(r"Nationality:\s+(.*?\s)\s+", text)
        nationality = search_nationality.group(1).strip() if search_nationality else 'Nationality Not Found'
        
        search_family_name = re.search(r"Family Name:\s+(.*?\s)\s+", text)
        family_name = search_family_name.group(1).strip() if search_family_name else 'Family Name Not Found'
        
        search_given_name = re.search(r"Given Names:\s+(.*?\s)\s+", text)
        given_name = search_given_name.group(1).strip() if search_given_name else 'Given Name Not Found'
        
        
        try:            
            connection = mysql.connector.connect(
                host = 'localhost',
                user = 'admin',
                password = 'Root@123!',
                database = 'ioa_core'
            )
        
            if connection.is_connected():
                # print(" Connected to MySQL")
                pass
                
            cursor = connection.cursor()
            
            sql = """
                        INSERT INTO confirmation_of_enrolment (
                            provider_name,
                            provider_cicros_code,
                            email,
                            coe_code,
                            course_name,
                            course_code,
                            course_level,
                            course_start_date,
                            course_end_date,
                            total_tuition_fee,
                            provider_student_id,
                            family_name,
                            given_name,
                            gender,
                            date_of_birth,
                            country_of_birth,
                            nationality
                        )
                        VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s, %s, %s, %s, %s
                        )
                    """
            
            values = (
                        provider_name, 
                        provider_cicros_code, 
                        email,
                        coe_code, 
                        course_name,
                        course_code, 
                        course_level,
                        course_start_date,
                        course_end_date,
                        total_tuition_fee,
                        provider_student_id,
                        family_name,
                        given_name,
                        gender,
                        date_of_birth,
                        country_of_birth,
                        nationality                     
                        
                    )
            
            cursor.execute(sql, values)
            connection.commit()
            print(f"✅ CoE Record {coe_code} saved to the database successfully.")

            
        except Exception as error:
                print(f"❌ MySQL  failed: {error}")


if __name__ == "__main__":
    main() 



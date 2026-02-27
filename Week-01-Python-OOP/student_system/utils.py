import csv
import os
from models import Student

class DataHandler:
    
    @staticmethod
    def save_students(filename, students):
        """حفظ قائمة الطلاب في ملف CSV"""
        try:
            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                # كتابة العناوين (Header)
                writer.writerow(['Name', 'ID', 'Grades'])
                for s in students:
                    # تحويل قائمة الدرجات إلى نص مفصول بفاصلة لسهولة التخزين
                    grades_str = ",".join(map(str, s.get_grades()))
                    writer.writerow([s.name, s.student_id, grades_str])
            print(f"Data saved successfully to {filename}.")
        except Exception as e:
            print(f"Error saving data: {e}")

    @staticmethod
    def load_students(filename):
        """تحميل الطلاب من ملف CSV وتحويلهم إلى كائنات Student"""
        students = []
        if not os.path.exists(filename):
            return students # إذا الملف غير موجود نعود بقائمة فارغة

        try:
            with open(filename, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # تحويل نص الدرجات مرة أخرى إلى قائمة أرقام
                    grades = [float(g) for g in row['Grades'].split(',')] if row['Grades'] else []
                    new_student = Student(row['Name'], row['ID'], grades)
                    students.append(new_student)
            return students
        except Exception as e:
            print(f"Error loading data: {e}")
            return []

class Validator:
    
    @staticmethod
    def get_valid_score(prompt):
        """التأكد من أن المستخدم أدخل درجة صحيحة (رقم بين 0 و 100) أو -1 للتوقف"""
        while True:
            try:
                line = input(prompt).strip()
                if not line: # إذا ضغط المستخدم Enter بدون كتابة شيء
                    print("Please enter a number or -1 to finish.")
                    continue
                
                score = float(line)
                
                # السماح بـ -1 للخروج، أو التأكد أن الدرجة بين 0 و 100
                if score == -1 or 0 <= score <= 100:
                    return score
                else:
                    print("Score must be between 0 and 100 (or -1 to finish).")
            except ValueError:
                print("Invalid input! Please enter a number.")
        """التأكد من أن المستخدم أدخل درجة صحيحة (رقم بين 0 و 100)"""
        while True:
            try:
                score = float(input(prompt))
                if 0 <= score <= 100:
                    return score
                else:
                    print("Score must be between 0 and 100.")
            except ValueError:
                print("Invalid input! Please enter a number.")

    @staticmethod
    def get_non_empty_input(prompt):
        """التأكد من أن المستخدم لم يترك الحقل فارغاً"""
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print("This field cannot be empty.")
import sys
from models import Student, Classroom
from utils import DataHandler, Validator
from analytics import StudentAnalytics

def show_menu():
    print("\n" + "═"*35)
    print("  STUDENT PERFORMANCE ANALYZER")
    print("" + "═"*35)
    print("1. ➕ Add New Student")
    print("2. 📋 View All Students")
    print("3. 🔍 Search by ID")
    print("4. 🔎 Search by Name") # الخيار الجديد
    print("5. ❌ Remove Student")
    print("6. 📊 View Full Analytics & Ranking") # تحسين العرض
    print("7. 💾 Save and Exit")
    print("═"*35)

def main():
    my_classroom = Classroom()
    filename = 'data.csv'
    my_classroom.students = DataHandler.load_students(filename)

    while True:
        show_menu()
        choice = input("Select an option (1-7): ").strip()

        if choice == '1':
            name = Validator.get_non_empty_input("Enter Name: ")
            sid = Validator.get_non_empty_input("Enter ID: ")
            if my_classroom.search_student(sid):
                print("Error: ID already exists!")
                continue
            
            grades = []
            print("Enter grades (type -1 to finish):")
            while True:
                score = Validator.get_valid_score("Score: ")
                if score == -1: break
                grades.append(score)
            
            my_classroom.add_student(Student(name, sid, grades))

        elif choice == '2':
            if not my_classroom.students:
                print("No students registered.")
            for s in my_classroom.students:
                print(s)

        elif choice == '3':
            sid = input("Enter ID: ")
            s = my_classroom.search_student(sid)
            print(s if s else "Student not found.")

        elif choice == '4': # منطق البحث بالاسم
            name = input("Enter Name to search: ")
            results = my_classroom.search_student_by_name(name)
            if results:
                print(f"\nFound {len(results)} student(s):")
                for s in results: print(s)
            else:
                print("No student found with that name.")

        elif choice == '5':
            sid = input("Enter ID to remove: ")
            my_classroom.remove_student(sid)

        elif choice == '6': # عرض التحليلات والترتيب (Ranking)
            if not my_classroom.students:
                print("No data for analysis.")
                continue
            
            # 1. الإحصائيات العامة (Top/Lowest/Avg)
            top = StudentAnalytics.get_top_student(my_classroom.students)
            low = StudentAnalytics.get_lowest_student(my_classroom.students)
            dist = StudentAnalytics.get_grade_distribution(my_classroom.students)
            
            print("\n--- Quick Stats ---")
            print(f"Class Average: {my_classroom.calculate_classroom_average():.2f}")
            print(f"⭐ Top Student: {top.name} ({top.calculate_average():.2f})")
            print(f"📉 Lowest Student: {low.name} ({low.calculate_average():.2f})")
            print(f"📊 Distribution: {dist}")

            # 2. الترتيب (Ranking) - هذا هو المطلوب في المتطلبات
            print("\n--- Student Ranking (High to Low) ---")
            ranked = StudentAnalytics.rank_students(my_classroom.students)
            for i, s in enumerate(ranked, 1):
                print(f"{i}. {s.name} - Avg: {s.calculate_average():.2f} [{s.get_grade_category()}]")

        elif choice == '7':
            DataHandler.save_students(filename, my_classroom.students)
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
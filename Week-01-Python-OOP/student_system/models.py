class Student:
    def __init__(self, name, student_id, grades):
        self.name = name
        self.student_id = student_id
        # Encapsulation: نستخدم __ قبل الاسم لجعله خاصاً (Private)
        self.__grades = grades 

    # وظيفة لحساب المتوسط الخاص بالطالب
    def calculate_average(self):
        if not self.__grades:
            return 0
        return sum(self.__grades) / len(self.__grades)

    # وظيفة لتحديد التقدير (A, B, C...)
    def get_grade_category(self):
        avg = self.calculate_average()
        if avg >= 90: return "A"
        elif avg >= 80: return "B"
        elif avg >= 70: return "C"
        elif avg >= 60: return "D"
        else: return "F"

    # Getter: للسماح بقراءة الدرجات لأنها Private
    def get_grades(self):
        return self.__grades

    # @staticmethod: وظيفة مساعدة لا تعتمد على بيانات طالب معين
    @staticmethod
    def is_passing(average):
        return average >= 50

    # تمثيل الطالب كـ نص عند طباعته
    def __str__(self):
        return f"ID: {self.student_id} | Name: {self.name} | Average: {self.calculate_average():.2f}"
    

    @classmethod
    def from_dict(cls, data):
        """إنشاء كائن طالب من قاموس بيانات (مفيد عند القراءة من الملفات)"""
        return cls(data['Name'], data['ID'], data['Grades'])


class Classroom:
    def __init__(self):
        self.students = []

    def add_student(self, student):
        self.students.append(student)
        print(f"Student {student.name} added successfully.")

    def remove_student(self, student_id):
        # البحث عن الطالب وحذفه من القائمة
        original_count = len(self.students)
        self.students = [s for s in self.students if s.student_id != student_id]
        if len(self.students) < original_count:
            print(f"Student with ID {student_id} removed.")
        else:
            print("Student not found.")

    def search_student(self, student_id):
        for student in self.students:
            if student.student_id == student_id:
                return student
        return None

    def calculate_classroom_average(self):
        if not self.students:
            return 0
        total_avg = sum(s.calculate_average() for s in self.students)
        return total_avg / len(self.students)
    
    def search_student_by_name(self, name):
        """البحث عن الطلاب بناءً على الاسم (تجاهل حالة الأحرف)"""
        results = [s for s in self.students if name.lower() in s.name.lower()]
        return results
    

    
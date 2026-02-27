class StudentAnalytics:

    @staticmethod
    def get_top_student(students):
        """البحث عن الطالب صاحب أعلى معدل"""
        if not students:
            return None
        # نستخدم دالة max ونخبر Python أن تقارن بناءً على المعدل المحسوب
        return max(students, key=lambda s: s.calculate_average())

    @staticmethod
    def get_lowest_student(students):
        """البحث عن الطالب صاحب أقل معدل"""
        if not students:
            return None
        return min(students, key=lambda s: s.calculate_average())

    @staticmethod
    def rank_students(students):
        """ترتيب الطلاب من الأعلى معدلاً إلى الأقل"""
        # نستخدم sorted مع reverse=True للترتيب التنازلي
        return sorted(students, key=lambda s: s.calculate_average(), reverse=True)

    @staticmethod
    def get_grade_distribution(students):
        """حساب عدد الطلاب في كل فئة تقدير (A, B, C...)"""
        distribution = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
        for s in students:
            category = s.get_grade_category()
            if category in distribution:
                distribution[category] += 1
        return distribution
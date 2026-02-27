import csv
import re
import numpy as np
import pickle

# الخطوة 2: دالة تنظيف محتوى المقال
def clean_content(text):
    # تحويل النص لحروف صغيرة
    text = text.lower()
    # إزالة علامات الترقيم والأرقام باستخدام Regex
    text = re.sub(r'[^a-z\s]', '', text)
    # تقسيم النص إلى كلمات (Tokenization)
    return text.split()

# الخطوة 1: دالة قراءة ملف الـ CSV
def read_csv(file_path):
    articles = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            articles.append({
                'id': int(row['id']),
                'title': row['title'],
                'words': clean_content(row['content'])
            })
    return articles

# الخطوة 3: بناء القاموس الشامل (Unique words)
def build_global_vocabulary(articles):
    vocab = set()
    for art in articles:
        for word in art['words']:
            vocab.add(word)
    return sorted(list(vocab))

# الخطوة 4: بناء المتجهات (Vector Representation 0 or 1)
def build_article_vectors(articles, vocab):
    for art in articles:
        # إنشاء قائمة بها 1 إذا كانت الكلمة موجودة و 0 إذا لم تكن موجودة
        art['vector'] = [1 if word in art['words'] else 0 for word in vocab]
    return articles

# الخطوة 5: حساب مصفوفة التشابه باستخدام مكتبة Numpy
def calculate_cosine_similarity_matrix(articles):
    num_articles = len(articles)
    # إنشاء مصفوفة مربعة مليئة بالأصفار
    matrix = np.zeros((num_articles, num_articles))
    
    for i in range(num_articles):
        for j in range(num_articles):
            vec_a = np.array(articles[i]['vector'])
            vec_b = np.array(articles[j]['vector'])
            
            norm_a = np.linalg.norm(vec_a)
            norm_b = np.linalg.norm(vec_b)
            
            # حساب قانون جيب التمام للتشابه
            if norm_a == 0 or norm_b == 0:
                matrix[i][j] = 0.0
            else:
                matrix[i][j] = np.dot(vec_a, vec_b) / (norm_a * norm_b)
    return matrix

# الخطوة 6: حفظ المصفوفة في ملف Pickle
def save_matrix_to_pkl(matrix, filename):
    with open(filename, 'wb') as f:
        pickle.dump(matrix, f)

# الخطوة 7: دالة البحث عن أكثر 3 مقالات تشابهاً
def get_top_3_similar_articles(article_id, articles, matrix):
    # إيجاد مكان المقال في القائمة
    target_idx = -1
    for i, art in enumerate(articles):
        if art['id'] == article_id:
            target_idx = i
            break
            
    if target_idx == -1:
        return []

    # جلب قيم التشابه لهذا المقال مع استبعاد نفسه
    similarities = matrix[target_idx]
    scores = [(i, similarities[i]) for i in range(len(similarities)) if i != target_idx]

    # الترتيب من الأعلى تشابهاً إلى الأقل
    scores.sort(key=lambda x: x[1], reverse=True)

    # إرجاع عناوين أول 3 مقالات فقط
    return [articles[s[0]]['title'] for s in scores[:3]]
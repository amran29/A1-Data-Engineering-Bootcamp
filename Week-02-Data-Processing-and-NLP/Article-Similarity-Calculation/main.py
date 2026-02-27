import similarity # استيراد ملف الدوال الخاص بنا

def main():
    # إعداد أسماء الملفات
    input_file = 'articles.csv'
    output_pkl = 'similarities.pkl'

    print("--- Article Similarity Calculation Started ---")

    # 1 & 2. قراءة وتنظيف البيانات
    articles = similarity.read_csv(input_file)
    print(f"Successfully loaded {len(articles)} articles.")

    # 3. بناء القاموس العالمي
    vocabulary = similarity.build_global_vocabulary(articles)
    print(f"Global vocabulary size: {len(vocabulary)} words.")

    # 4. تحويل المقالات لمتجهات (0, 1)
    articles = similarity.build_article_vectors(articles, vocabulary)

    # 5. حساب مصفوفة التشابه (Numpy)
    sim_matrix = similarity.calculate_cosine_similarity_matrix(articles)
    print("Similarity matrix calculated successfully.")

    # 6. حفظ المخرجات في ملف PKL
    similarity.save_matrix_to_pkl(sim_matrix, output_pkl)
    print(f"Matrix saved to: {output_pkl}")

    # 7. تجربة البحث عن مقالات مشابهة للمقال رقم 1
    target_id = 1
    top_articles = similarity.get_top_3_similar_articles(target_id, articles, sim_matrix)

    print(f"\nTop 3 most similar articles to (Article ID {target_id}):")
    for title in top_articles:
        print(f"- {title}")

    print("\n--- Process Completed Successfully ---")

if __name__ == "__main__":
    main()
import pickle

# فتح الملف وقراءة محتواه
with open('similarities.pkl', 'rb') as file:
    data = pickle.load(file)

print("Contents of similarities.pkl:")
print(data)
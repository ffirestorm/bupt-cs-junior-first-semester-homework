import os

type_list = ["auto", "business", "cul", "edu", "fz", "house", "mil", "ny", "ty", "yl"]
data_dir = "./data/splice"

def count_words(text):
    words = text.split()
    return len(words)

def select_data():
    for t in type_list:
        dir_path = os.path.join(data_dir, t)
        print(t)
        count = 0
        os.makedirs("./data/select/"+t, exist_ok=True)  # 确保文件夹存在，如果不存在则创建
        for root, _, files in os.walk(dir_path):
            for f in files:
                
                file_path = os.path.join(root, f)
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                word_count = count_words(content)
                if word_count >= 150 and word_count <=500:
                    count += 1
                    out_path = os.path.join('./data/select/' + t, f)
                    with open(out_path, 'w', encoding='utf-8') as out:
                        out.write(content)
        print(count)

if __name__ == "__main__":
    select_data()
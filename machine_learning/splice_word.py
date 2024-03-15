import os
import jieba.posseg as pseg
import threading

def is_all_chinese(strs):
    for _char in strs:
        if not ('\u4e00' <= _char <= '\u9fa5'):
            return False
    return True

def process_text(doc, stop_words):
    words = pseg.cut(doc)
    word_str = ''
    first = True
    for word in words:
        now_word = str(word.word)
        # 判断词是否是名词，且不是人名，同时不在停用词表中
        if 'n' in word.flag and word.flag != 'nr' and is_all_chinese(now_word) and now_word not in stop_words:
            if first:
                first = False
            else:
                word_str += ' '
            word_str += word.word
    return word_str

def process_category(base_dir, category, stop_words):
    dir_path = os.path.join(base_dir, category)
    count = 0
    out_dir = "./data/splice/" + category
    os.makedirs(out_dir, exist_ok=True)  # 确保文件夹存在，如果不存在则创建
    for _, _, files in os.walk(dir_path):
        for f in files:
            out_path = os.path.join('./data/splice/' + category, f)
            if os.path.exists(out_path):
                print(f"文件 {out_path} 已存在，跳过处理。")
                continue

            file_path = os.path.join(dir_path, f)
            with open(file_path, 'rb') as file_obj:
                doc = file_obj.read()
                count += 1

            word_str = process_text(doc, stop_words)
            
            with open(out_path, 'w', encoding='utf-8') as out:
                out.write(word_str)
            if(count % 100 == 0):
                print("{} : {}".format(category, count))
    print(count)

if __name__ == "__main__":
    type_list = ["auto", "business", "cj", "cul", "edu", "fz", "house", "mil", "ny", "ty", "yl"]
    stop_word_path = "./data/stop/stop_words_ch.txt"
    
    # 读取停用词表
    with open(stop_word_path, 'r', encoding='gbk') as stop_word_file:
        stop_words = set(stop_word_file.read().split('\n'))

    base_dir = './data/news/'
    threads = []
    try:
        for category in type_list:
            thread = threading.Thread(target=process_category, args=[base_dir, category, stop_words])
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()
    except Exception as e:
        print("出现问题:{}".format(e))

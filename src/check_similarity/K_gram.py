def generateKgram(file, k):
    # kgram 中存放的是我们的文档的所有shingle的集合
    kgram = []
    for i in range(len(file)):
        if(i + k > len(file)):
            break
        shingle = file[i:i+k]
        kgram.append(shingle)
    return kgram

'''
k = 3
if __name__ == '__main__':
    with open("D:\\數據科學基礎/best-partner/test/test.txt", "r", encoding="utf-8") as f:
        data = f.readlines()
        print(data)
        file = data[0]
        kgram = generateKgram(file, k)
        print(kgram)
'''


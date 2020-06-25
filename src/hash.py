def generateHash(base, kgram, k):
    Hashlist = []
    for i in range(len(kgram)):
        hash = 0
        shingle = kgram[i]

        for j in range(k):
            hash += ord(shingle[j]) * (base ** (k - 1 - j))
        Hashlist.append(hash)

    return Hashlist

base = 5
k = 3
if __name__ == '__main__':
    kgram = ['yab', 'abb', 'bba', 'bad', 'ada', 'dab', 'abb', 'bba', 'bad', 'ado', 'doo']
    Hashlist = generateHash(base, kgram, k)
    print(Hashlist)

import string
import collections
import multiprocessing
import time

STOP_WORDS = None
TR = None
# read the stopwords file
with open('stopwords.txt', 'rt', encoding='utf8') as f:
    STOP_WORDS = set(f.read().split())
# create a translation table to remove punctuation
TR = str.maketrans(string.punctuation, ' ' * len(string.punctuation))

def words_in_file(fileName):
    output = []
    with open(fileName, 'rt', encoding="utf8") as f:
        for line in f:
            line = line.translate(TR) # Loại bỏ dấu câu
            for word in line.split():
                word = word.lower()
                if word.isalpha() and word not in STOP_WORDS:
                    output.append( (word, 1) )
        time.sleep(0.05)
    return output

if __name__ == '__main__':
    import glob
    input_files = glob.glob('data/*.txt')
    #Cache all input files to memory
    for file in input_files:
        with open(file, 'rt', encoding='utf8') as f:
            f.read()

    startTime = time.perf_counter()
    
    word_occurances = collections.defaultdict(list)
    for file in input_files:
        print(multiprocessing.current_process().name, 'reading', file)
        for k,v in words_in_file(file):
            word_occurances[k].append(v)
    #word_counts = [(k, sum(v)) for k,v in word_occurances.items()]
    word_counts = []
    for k,v in word_occurances.items():
        word_counts.append((k,sum(v)))
    word_counts.sort(key = lambda item: item[1], reverse=True)
    print('\n20 từ xuất hiện nhiều nhất\n')
    top20 = word_counts[:20]
    longest = max(len(word) for word, count in top20)
    for word, count in top20:
        print('%-*s: %5s' % (longest+1, word, count))

    endTime = time.perf_counter()
    print('\nTime taken: {:.2f} seconds'.format(endTime - startTime))
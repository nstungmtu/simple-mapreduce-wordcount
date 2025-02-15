import collections
import itertools
import multiprocessing
import multiprocessing.pool
import string
import time

STOP_WORDS = None
TR = None
# Đọc tập tin stopwords
with open('stopwords.txt', 'rt', encoding='utf8') as f:
    STOP_WORDS = set(f.read().split())
# tạo bảng dịch thuật để loại bỏ dấu câu (thay dấu câu bằng khoảng trắng)
TR = str.maketrans(string.punctuation, ' ' * len(string.punctuation))

class SimpleMapReduce(object):
    def __init__(self, map_func, reduce_func, num_workers=None):
        self.map_func = map_func
        self.reduce_func = reduce_func
        # Tạo số lượng worker tương ứng với số lượng CPU
        self.workers = multiprocessing.Pool(num_workers)
    
    def shuffle(self, mapped_values):
        partitioned_data = collections.defaultdict(list)
        for key, value in mapped_values:
            partitioned_data[key].append(value)
        return partitioned_data.items()
    
    def __call__(self, inputs):
        map_responses = self.workers.map(self.map_func, inputs, chunksize=1)
        shuffled_data = self.shuffle(itertools.chain(*map_responses))
        reduced_values = self.workers.map(self.reduce_func, shuffled_data)
        return reduced_values

def words_in_file(fileName):
    print(multiprocessing.current_process().name, 'reading', fileName)
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

def count_words(item):
    word, occurances = item
    return (word, sum(occurances))

if __name__ == '__main__':
    import glob
    input_files = glob.glob('data/*.txt')
    #Cache all input files to memory
    for file in input_files:
        with open(file, 'rt', encoding='utf8') as f:
            f.read()
    
    startTime = time.perf_counter()
    
    mapper = SimpleMapReduce(words_in_file, count_words)
    word_counts = mapper(input_files)
    word_counts.sort(key = lambda item: item[1], reverse=True)
    print('\nTOP 20 WORDS BY FREQUENCY\n')
    top20 = word_counts[:20]
    longest = max(len(word) for word, count in top20)
    for word, count in top20:
        print('%-*s: %5s' % (longest+1, word, count))

    endTime = time.perf_counter()
    print('\nTime taken: {:.2f} seconds'.format(endTime - startTime))
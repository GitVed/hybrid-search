from src.tokenizer import tokenize

class InvertedIndex:
    def __init__(self):
        self.postings = {}
        self.doc_lengths = {}

    def add_document(self, doc_id, text):
        tokens = tokenize(text)
        self.doc_lengths[doc_id] = len(tokens)

        for word in tokens:
            if word not in self.postings:
                self.postings[word] = {}

            if doc_id not in self.postings[word]:
                self.postings[word][doc_id] = 0
                
            self.postings[word][doc_id] += 1

            
    def get_postings(self, word):
        return self.postings.get(word, {})

    def num_docs(self):
        return len(self.doc_lengths)

    def avg_doc_length(self):
        total_length = 0
        total = len(self.doc_lengths)
        if not total:
            return 0
        for value in self.doc_lengths.values():
            total_length += value
        return total_length / total

    def search_and(self, query):
        tokens = tokenize(query)

        if not tokens:
            return set()
        
        posting_sets = []
        for word in tokens:
            if word in self.postings and self.postings[word] != {}:
                posting_sets.append(set(self.postings[word]))
            else:
                return set()
        if not posting_sets:
            return set()
        master_set = posting_sets.pop(0)
        for posting_set in posting_sets:
            master_set = master_set.intersection(posting_set)

        return master_set #should this be inside a set()?
        

    def search_or(self, query):
        pass        

from sentence_transformers import SentenceTransformer, util


class SimilarityCalculator:

    def __init__(self, sampled_queries) -> None:
        print("On downloading model...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.sampled_queries = sampled_queries
        print("On encode")
        self.sampled_queries_xd = [q['question'] for q in sampled_queries]
        self.embeddings = self.model.encode(self.sampled_queries_xd, normalize_embeddings=True)

    def sentence_vector(self, question, k):
        target_embedding = self.model.encode(question)

        similarities = []
        for i, (sentence, embedding) in enumerate(zip(self.sampled_queries_xd, self.embeddings)):
            similarities.append((util.pytorch_cos_sim(target_embedding, embedding), sentence, self.sampled_queries[i]['query']))

        similarities.sort(reverse=True)
        while similarities[0][0] > 0.998:
            similarities.pop(0)
        
        return similarities[:k]
"""


from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy
import numpy as np

nlp = spacy.load('en_core_web_sm')  # load the English model

def mask_nouns(text):
    doc = nlp(text)
    return ' '.join('[MASK]' if w.pos_ == 'NOUN' else w.text for w in doc)

def find_most_similar_k_items(question, question_list, k):
    # Masking nouns in the questions
    masked_question_list = [mask_nouns(q) for q in question_list]
    masked_question_input = mask_nouns(question)

    # Add the input question into the list for vectorization
    masked_question_list.append(masked_question_input)

    # Vectorization
    vectorizer = CountVectorizer().fit_transform(masked_question_list)
    vectors = vectorizer.toarray()

    # Cosine similarity
    csim = cosine_similarity(vectors)

    # Get similarity values for the input question compared to others
    similarity_values = csim[-1][:-1]  # Excluding last item because it's the input question itself

    # Get top k indices with highest similarity 
    k_most_similar_indices = np.argpartition(similarity_values, -k)[-k:]

    return [question_list[index] for index in k_most_similar_indices]



question_list = ["What is your name?", "Where do you live?", "What's your age?", "What do you do?"]
question = "Where do you work?" 

most_similar_questions = find_most_similar_k_items(question, question_list, 2)

"""
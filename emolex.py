import joblib
from nltk import stem 


# NRC emotion lexicons as dictionary format. Key: Emotion type, Value: List of words
emotion_lexicons = joblib.load( 'emotion_lexicons_dict.pkl')

emotion_types = ['anger', 'anticipation', 'disgust', 'fear', 'joy',
                     'negative', 'positive', 'sadness', 'surprise', 'trust']

# Get shortest and longest words length in the lexicon list
minl= 1000
maxl = -1
imdb_ids = []
segment_scores_list = []
plot_lengths = []

for k, v in emotion_lexicons.items():
    for word in v:
        if len(word) < minl:
            minl = len(word)
        if len(word) > maxl:
            maxl = len(word)

print(minl, maxl)

#getting emotional scores of a chunk

def get_chunks_of_emotional_scores(content, N=20):
    # TODO: STEMMING BASED
    segment_scores =[[0 for j in range(len(emotion_types))] for i in range(N)]

    # content = content.lower().split()
    segment_length = round(len(content) / N)
    for i in range(N):
        start_index = i * segment_length
        end_index   = (i+1) * segment_length
        for token in content[start_index:end_index]:
            if len(token)>= minl and len(token) <= maxl:
                for emo_idx in range(len(emotion_types)):
                    if token in  emotion_lexicons[emotion_types[emo_idx]]:
                        segment_scores[i][emo_idx] += 1
            
            

        total = sum(segment_scores[i])
        if total > 0:
            for j in range(len(segment_scores[i])):
                segment_scores[i][j] /= total
                segment_scores[i][j] *= 100

    return segment_scores


   # emotion_score_vectors_dict = {}
    #for imdb_id, clean_content in clean_text_dict.items():
    	#emotion_score_vectors_dict[imdb_id] = get_chunks_of_emotional_scores(clean_content, 20

import unidecode
import re

def unicode_to_ascii(s):
    return unidecode.unidecode(s)
  
# Lowercase, trim, and remove non-letter characters
def normalize_string(s):
    s = unicode_to_ascii(s.lower().strip())
    s = re.sub(r"([.!?])", r" \1", s)
    s = re.sub(r"[^a-zA-Z.!?]+", r" ", s)
    return s

f =open('beatles.txt' ).read().strip().split('\n')

lancaster=stem.LancasterStemmer()
nf = [normalize_string(x) for x in f]

mylist = []
for x in nf:
	x = x.split()
	mylist = mylist + x

mylist = [lancaster.stem(x) for x in mylist]
scores = get_chunks_of_emotional_scores(mylist, 5)
print(scores)





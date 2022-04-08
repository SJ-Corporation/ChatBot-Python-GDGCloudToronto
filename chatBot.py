import nltk
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('omw-1.4')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
import json
import random

from keras.models import load_model
model = load_model('chatbotModel.h5')
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl' , 'rb'))
classes = pickle.load(open('classes.pkl' , 'rb'))

def cleanUpSentence(sentence):
    sentenceWords = nltk.word_tokenize(sentence)
    sentenceWords = [lemmatizer.lemmatize(word.lower()) for word in sentenceWords]
    return sentenceWords

def bow(sentence , words , show_details=True):
    sentenceWords = cleanUpSentence(sentence)
    bag = [0] * len(words)
    for s in sentenceWords:
        for i , w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print("Found in bag: %s" %w)
    return(np.array(bag))

def predict_class(sentence , model):
    p = bow(sentence , words , show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list


def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = {
                "answer": random.choice(i['responses']), 
                "choices": i['choices']
            }
            break
    return result

def chatbot_response(text):
    ints = predict_class(text, model)
    res = getResponse(ints, intents)
    return res


# just simple changes
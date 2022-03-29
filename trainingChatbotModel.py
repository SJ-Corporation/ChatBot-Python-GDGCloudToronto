#Import necessary packages
# from operator import mod
# from pickletools import optimize
# from tabnanny import verbose
import nltk
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import json
import pickle

import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD
import random

words = []
classes = []
documents = []
ignoreWords = ['?' , '!']
file = open('intents.json' , 'r')
intents = json.load(file)


#Tokenize the sentence
for intent in intents['intents']:
    for pattern in intent['patterns']:
        # Tokenize the each word
        w = nltk.word_tokenize(pattern)
        words.extend(w)

        if intent['tag'] not in classes:
            classes.append(intent['tag'])

        #add documents in the corpus
        documents.append((w , intent['tag']))

#lemmatize, lower each word and remove duplicates
words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignoreWords]
words = sorted(list(set(words)))

#sort classes
classes = sorted(list(set(classes)))

#documents = pattens and intents
print(len(documents) , "documents")

#classes = intents
print(len(classes) , "classes" , classes)

#words = all words
print(len(words) , "unique words" , words)

pickle.dump(words , open('words.pkl' , 'wb'))
pickle.dump(classes , open('classes.pkl' , 'wb'))

# Let's create our training data
training = []

output = [0] * len(classes)

#training set, bag of words for each sentence
for doc in documents:
    bag = []
    wordPattern = doc[0]

    #lemmatize each word
    wordPattern = [lemmatizer.lemmatize(word.lower()) for word in wordPattern]

    for w in words:
        bag.append(1) if w in wordPattern else bag.append(0)

    output_row = list(output)
    output_row[classes.index(doc[1])] = 1

    training.append([bag , output_row])

#Shuffle our features and turn into np.array
random.shuffle(training)
training = np.array(training)

#train and test
x_train = list(training[ : , 0])
y_train = list(training[ : , 1])

print(x_train)
print(y_train)

#build the model
model = Sequential()
model.add(Dense(128 , input_shape=(len(x_train[0]) , ) , activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64 , activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(y_train[0]) , activation='softmax'))

#compile the model
sgd = SGD(lr = 0.01 , decay = 1e-6, momentum = 0.9 , nesterov = True)
model.compile(loss='categorical_crossentropy' , optimizer = sgd , metrics = ['accuracy'])

#fit and save the model
hist = model.fit(np.array(x_train) , np.array(y_train) , epochs = 200 , batch_size = 5 , verbose = 1)
model.save("chatbotModel.h5" , hist)

print("model created")






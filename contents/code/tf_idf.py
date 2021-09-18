# _____TF-IDF libraries_____
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

# _____helper Libraries_____
import pickle
import csv
import json
import timeit
import secrets, os
from pathlib import Path 
from dotenv import dotenv_values

# Initialise environment variables
ENV_FILE = Path(os.getcwd(), 'environments/.env.dev')
env = dotenv_values(ENV_FILE)

class Bot:
    def talk_to_cb_primary(self, test_set_sentence, minimum_score , json_file_path , tfidf_vectorizer_pikle_path ,tfidf_matrix_train_pikle_path):
    
    # json_file_path = "data/convertcsv.json"

    # tfidf_vectorizer_pikle_path = "data/tfidf_vectorizer.pickle"
    # tfidf_matrix_train_pikle_path ="data/tfidf_matrix_train.pickle"
        test_set = (test_set_sentence, "")

        try:
            # b = fghfhg
            ##--------------to use------------------#
            f = open(tfidf_vectorizer_pikle_path, 'rb')
            tfidf_vectorizer = pickle.load(f)
            f.close()

            f = open(tfidf_matrix_train_pikle_path, 'rb')
            tfidf_matrix_train = pickle.load(f)
            f.close()
            # ----------------------------------------#
        except:
            # ---------------to train------------------#
            tfidf_vectorizer , tfidf_matrix_train = self.train_chat(json_file_path , tfidf_vectorizer_pikle_path , tfidf_matrix_train_pikle_path)
            # -----------------------------------------#

        tfidf_matrix_test = tfidf_vectorizer.transform(test_set)

        cosine = cosine_similarity(tfidf_matrix_test, tfidf_matrix_train)

        cosine = np.delete(cosine, 0)
        max = cosine.max()
        response_index = 0
        if (max > minimum_score):
            new_max = max - 0.01
            list = np.where(cosine > new_max)
            response_index = secrets.choice(list[0])
        else :
            return "Apologies! I did not get you. Please bear with me I'm still learning. Alternatively you can call on Toll Free Number - (1800-419-8300)" , 0
            
    # else:
            #response_index = np.where(cosine == max)[0][0] + 2  # no offset at all +3
        

        j = 0

        with open(json_file_path, "r") as sentences_file:
            reader = json.load(sentences_file)
            for row in reader:
                j += 1  # we begin with 1 not 0 &    j is initialized by 0
                if j == response_index:

                    #if delimeter in row[1]:
                    #    # get newest suggestion
                    #    answer_row = row[1].split(delimeter)
                    #    row[1] = answer_row[1]

                    #else:  # add new suggestion
                    #    note = "just return old original suggestion"

                    return row["response"], max
                    break


    #def previous_chats(query):
    #    minimum_score = 0.7
    #    file = "data/previous_chats.json"
    #    tfidf_vectorizer_pikle_path = "data/previous_tfidf_vectorizer.pickle"
    #    tfidf_matrix_train_path = "data/previous_tfidf_matrix_train.pickle"
    #    query_response, score = talk_to_cb_primary(query , minimum_score , file , tfidf_vectorizer_pikle_path , tfidf_matrix_train_path)
    #    return query_response , score

    def train_chat(self, json_file_path, tfidf_vectorizer_pikle_path , tfidf_matrix_train_pikle_path):
        i = 0
        sentences = []
        # enter your test sentence
            # 3ashan yzabt el indexes
        sentences.append(" No you.")
        sentences.append(" No you.")

        start = timeit.default_timer()

        # enter jabberwakky sentence
        with open(json_file_path, "r") as sentences_file:
            reader = json.load(sentences_file)
            # reader.next()
            # reader.next()
            for row in reader:
                # if i==stop_at_sentence:
                #    break
                sentences.append(row["message"])
                i += 1

        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix_train = tfidf_vectorizer.fit_transform(sentences)  # finds the tfidf score with normalization
        # tfidf_matrix_test =tfidf_vectorizer.transform(test_set)
        stop = timeit.default_timer()

        f = open(tfidf_vectorizer_pikle_path, 'wb')
        pickle.dump(tfidf_vectorizer, f)
        f.close()

        f = open(tfidf_matrix_train_pikle_path, 'wb')
        pickle.dump(tfidf_matrix_train, f)
        f.close()

        return tfidf_vectorizer , tfidf_matrix_train
        # -----------------------------------------#


    def previous_chats(self, query):
        minimum_score = 0.5
        file = env['PSB_JSON_FILE']
        tfidf_vectorizer_pikle_path = "previous_tfidf_vectorizer.pickle"
        tfidf_matrix_train_path = "previous_tfidf_matrix_train.pickle"
        query_response, score = self.talk_to_cb_primary(query , minimum_score , file , tfidf_vectorizer_pikle_path , tfidf_matrix_train_path)
        return query_response
    
    # def runbot(self):
    #     while 1:
    #         sent = input("User : ")

    def runbot(self, msg):
        return (self.previous_chats(msg))

# bot = Bot()

# bot.previous_chats('hi')
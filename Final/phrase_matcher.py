import os,json
import gensim.models.word2vec as w2v
import pandas as pd
import math
import numpy as np
from nltk.corpus import stopwords
from phrase_vector import PhraseVector

class PhraseMatcher():
    tempdict = {"tweet_id" : None ,"text" : None ,"primary_geo" : None}
    seekers_suppliers_list = []
    potential_list = []
    seekerslist_json = {}
    supplierslist_json = {}

    path_name = r'C:\Users\Kushal\flask-tutorial\Final'
    threshold = 0.60
  
    def __init__(self, threshold=0.60,path_name=r'C:\Users\Kushal\flask-tutorial\Final',seekerslist_json={},supplierslist_json={}):
        self.threshold = threshold
        self.path_name = path_name
        self.seekerslist_json = seekerslist_json
        self.supplierslist_json = supplierslist_json

    def get_threshold(self):
        return self.threshold

    def set_threshold(self,threshold):
        self.threshold = threshold

    def set_seekers_suppliers_list(self,seekerslist_json={},supplierslist_json={}):
        if supplierslist_json: self.supplierslist_json = supplierslist_json
        if seekerslist_json: self.seekerslist_json = seekerslist_json
        i = 0
        # print(type(self.seekerslist_json),type(self.supplierslist_json))
        for seeker in self.seekerslist_json:
            seekers_suppliers = {}
            seekers_suppliers['tweet_id'] = seeker['tweet_id']
            seekers_suppliers['text'] = seeker['text']
            seekers_suppliers['primary_geo'] = seeker['features']['primary_geo']
            # self.potential_list = []
            # seekers_suppliers["potential_offers"] = self.potential_list
            seekers_suppliers["potential_offers"] = []
            for supplier in self.supplierslist_json:
                phraseVector1 = PhraseVector(seeker['text'])
                phraseVector2 = PhraseVector(supplier['text']) 
                similarityScore  = phraseVector1.CosineSimilarity(phraseVector2.vector)
                if similarityScore >= self.threshold:
                    similarityScore = float('%.2f' % (similarityScore * 100))
                    potential_offers = {"tweet_id" : None ,"text" : None ,"primary_geo" : None ,"smiliarity_score_in_percentage" : None}
                    potential_offers['tweet_id'] = supplier['tweet_id']
                    potential_offers['text'] =  supplier['text']
                    potential_offers['primary_geo'] =supplier['features']['primary_geo']
                    potential_offers['smiliarity_score_in_percentage'] = similarityScore
                    seekers_suppliers["potential_offers"].append(potential_offers) 
            self.seekers_suppliers_list.append(seekers_suppliers.copy())
            i = i+1;    

    def get_seekers_suppliers_list(self):
        return self.seekers_suppliers_list

    def match(self, path_name=r'C:\Users\Kushal\flask-tutorial\Final'):
        self.path_name = path_name
        #load the required json files for matching task
        # with open(self.path_name+'\seekerslist.json', 'r',encoding = 'utf8') as fseek:
        #     seekerslist_json = json.load(fseek)
        # with open(self.path_name+'\supplierslist.json', 'r',encoding = 'utf8') as fsupp:
        #     supplierslist_json = json.load(fsupp)
        if bool(self.seekerslist_json) == False:
            self.seekerslist_json = json.loads(open(self.path_name+'\seekerslist.json').read())
        if bool(self.supplierslist_json) == False:
            self.supplierslist_json = json.loads(open(self.path_name+'\supplierslist.json').read())
        self.set_seekers_suppliers_list()     
        # self.json.dumps(self.seekers_suppliers_list)
        with open('seekers_suppliers_list.json', 'w') as fpsk:
            json.dump(self.get_seekers_suppliers_list(), fpsk, indent=4)
        

    



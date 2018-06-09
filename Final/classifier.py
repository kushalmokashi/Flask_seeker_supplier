import json
#from calculate_classification import ClassificationCalculator
from sklearn.externals import joblib



class Classifier():
    # data,seekerslist,supplierslist,otherslist  = None,None,None,None
    seekerslist = []
    supplierslist = []
    otherslist = []
    data=None
    request_model = joblib.load(r'C:\Users\Kushal\flask-tutorial\Final\random_forest_request_other')
    request_model_CV = joblib.load(r'C:\Users\Kushal\flask-tutorial\Final\random_forest_request_other_tfidf') 
    offer_model = joblib.load(r'C:\Users\Kushal\flask-tutorial\Final\random_forest_offer_other')
    offer_model_CV = joblib.load(r'C:\Users\Kushal\flask-tutorial\Final\random_forest_offer_other_tfidf')
   
        
    def __init__(self,data={},seekerslist=[],supplierslist=[],otherslist=[]):
        self.data = data
        self.seekerslist = seekerslist
        self.supplierslist = supplierslist
        self.otherslist = otherslist
        
    
    def get_data(self):
        return self.data
    
    def set_data(self,data):
        self.data=data

    def get_seekerslist(self):
        return self.seekerslist

    def set_seekerslist(self,seekerslist):
        self.seekerslist = seekerslist

    def get_otherslist(self):
            return self.otherslist

    def set_otherslist(self,otherslist):
        self.otherslist = otherslist

    def get_supplierslist(self):
            return self.supplierslist

    def set_supplierslist(self,supplierslist):
        self.supplierslist = supplierslist
   

    def dump_data_to_file(self,seekerslist=None,supplierslist=None,otherslist=None):
        if seekerslist: self.seekerslist = seekerslist
        if supplierslist: self.supplierslist = supplierslist
        if otherslist: self.otherslist = otherslist
        with open('seekerslist.json', 'w') as fpot:
            json.dump(self.seekerslist, fpot, indent=4)
        with open('supplierslist.json', 'w') as fpsk:
            json.dump(self.supplierslist, fpsk, indent=4)
        with open('otherslist.json', 'w') as fpsp:
            json.dump(self.otherslist , fpsp, indent=4)
               
        


    def classify(self,data=None):
        if data: self.data = data
        # print(type(self.data))
        # for i in range(len(data['item'])):
        for item in self.data['items']:
            tweet = item['text']
            seeker_data = dict(tweet_id=None,text=None,features=dict(name=None,id=None,screen_name=None,location=None,primary_geo=[],geo_type=None))
            # {"tweet_id" : None ,"text" : None,"features" :
            #  {"name" : None,"id": None,"screen_name": None,"location": None,"primary_geo" : [],"geo_type":None}}
            self.calculate_Seeker_Supplier(item,tweet,seeker_data)
            # self.seekerslist,self.supplierslist,self.otherslist = calculated_value.seekerslist,calculated_value.supplierslist,calculated_value.otherslist
        self.dump_data_to_file()

    def calculate_Seeker_Supplier(self,item,tweet,seeker_data):
                tweetaslist=[tweet]
                seeker_data = self.get_locations_userinfo(item,seeker_data)
                tweetcv= self.request_model_CV.transform(tweetaslist)
                predictions = self.request_model.predict(tweetcv)
                # self.append_seeker_item(predictions,seeker_data.copy())
                if self.append_seeker_item(predictions,seeker_data.copy()) == False:
                    self.append_supplier_item(predictions,seeker_data.copy(),tweetaslist)

                       
               
                   
    def append_seeker_item(self,predictions,seeker_data):
        if predictions == 1:
             self.seekerslist.append(seeker_data.copy())
             return True
        if predictions != 1:
            return False
      
    
    def append_supplier_item(self,predictions,seeker_data,tweetaslist):
        tweetcvoffer=self.offer_model_CV.transform(tweetaslist)
        predictions_offer =self.offer_model.predict(tweetcvoffer)
        if predictions_offer == 1:
            self.supplierslist.append(seeker_data.copy())
            return True
        if predictions_offer != 1:
            self.append_others_item(seeker_data.copy())
            return False
    
        

    def append_others_item(self,seeker_data):
        self.otherslist.append(seeker_data.copy())


    def get_locations_userinfo(self,item,seeker_data):
        seeker_data['tweet_id'] = str(item['id'])
        seeker_data['features']['name'] = item['user']['name']
        seeker_data['features']['id'] = item['user']['id']
        seeker_data['features']['screen_name'] = item['user']['screen_name']
        seeker_data['text'] = item['text']
        
        if item['coordinates'] is not None:
                        seeker_data["features"]["primary_geo"].append(item['coordinates']['coordinates'][1])
                        seeker_data["features"]["primary_geo"].append(item['coordinates']['coordinates'][0])
                        seeker_data["features"]["geo_type"] = "Tweet coordinates"
                        return seeker_data
        elif item['place'] is not None:
                        seeker_data["features"]["primary_geo"] = item['place']['full_name'] + ", " + item['place']['country']
                        seeker_data["features"]["geo_type"] = "Tweet place"
                        return seeker_data
        else:
                        seeker_data["features"]["primary_geo"] = item['user']['location']
                        seeker_data["features"]["geo_type"] = "User location"
                        return seeker_data
    
   
from sklearn.externals import joblib

class ClassificationCalculator():
    seekerslist = []
    supplierslist = []
    otherslist = []
    request_model = joblib.load(r'C:\Users\Kushal\flask-tutorial\Final\random_forest_request_other')
    request_model_CV = joblib.load(r'C:\Users\Kushal\flask-tutorial\Final\random_forest_request_other_tfidf') 
    offer_model = joblib.load(r'C:\Users\Kushal\flask-tutorial\Final\random_forest_offer_other')
    offer_model_CV = joblib.load(r'C:\Users\Kushal\flask-tutorial\Final\random_forest_offer_other_tfidf')
   
        
    def __init__(self,item=None,tweet=None,seeker_data=None):
        self.calculate_Seeker_Supplier(item,tweet,seeker_data)
        
    # return  dict(seekerslist=seekerslist,supplierslist=supplierslist,otherslist=otherslist)

    def append_seeker_item(self,predictions,seeker_data):
         if predictions == 1:
             self.seekerslist.append(seeker_data.copy())
      
    
    def append_supplier_item(self,predictions,seeker_data,tweetaslist):
        if predictions != 1 :
            tweetcvoffer=self.offer_model_CV.transform(tweetaslist)
            predictions_offer =self.offer_model.predict(tweetcvoffer)
            if predictions_offer == 1:
                self.supplierslist.append(seeker_data.copy())
                return True
            if predictions_offer != 1:
                return False
        

    def append_others_item(self,peredication,item):
        return item

    def calculate_Seeker_Supplier(self,item,tweet,seeker_data):
                tweetaslist=[tweet]
                seeker_data = self.get_locations_userinfo(item,seeker_data)
                tweetcv= self.request_model_CV.transform(tweetaslist)
                predictions = self.request_model.predict(tweetcv)
                self.append_seeker_item(predictions,seeker_data.copy())
                if self.append_supplier_item(predictions,seeker_data.copy(),tweetaslist) == False:
                    self.append_others_item(predictions,seeker_data.copy())
               
                   
    def get_locations_userinfo(self,item,seeker_data):
        seeker_data['tweet_id'] = item['id']
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
   

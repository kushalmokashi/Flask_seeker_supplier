import googlemaps
import json


class GeoCoder():
    api_key ='AIzaSyB0wCBqqyAHZ8uWcK86zcxzz3PZ6pyP9m0'
    gm = googlemaps.Client(key=api_key)
    seekers_suppliers_list = {}
    def __init__(self, seekers_suppliers_list):
        self.seekers_suppliers_list = seekers_suppliers_list
  
    def geocode(self,seekers_suppliers_list = {}):
        print(type(self.seekers_suppliers_list))
        if seekers_suppliers_list: self.seekers_suppliers_list = seekers_suppliers_list
        if bool(self.seekers_suppliers_list) == False:
            print("taking file for geocode")
            self.seekers_suppliers_list = json.loads( open('seekers_suppliers_list.json').read())
        for i in range(len(self.seekers_suppliers_list)):
            if isinstance(self.seekers_suppliers_list[i]['primary_geo'],str):
                self.seekers_suppliers_list[i]['primary_latlng'] = []
                geocode_result =self.gm.geocode(self.seekers_suppliers_list[i]['primary_geo'])
                self.seekers_suppliers_list[i]["primary_latlng"].append(geocode_result[0]['geometry']['location']['lat'])
                self.seekers_suppliers_list[i]["primary_latlng"].append(geocode_result[0]['geometry']['location']['lng'])
                for j in range(len(self.seekers_suppliers_list[i]['potential_offers'])):
                    if isinstance(self.seekers_suppliers_list[i]['potential_offers'][j]['primary_geo'],str):
                        self.seekers_suppliers_list[i]['potential_offers'][j]['primary_latlng'] = []
                        geocode_result =self.gm.geocode(self.seekers_suppliers_list[i]['potential_offers'][j]['primary_geo'])
                        self.seekers_suppliers_list[i]['potential_offers'][j]["primary_latlng"].append(geocode_result[0]['geometry']['location']['lat'])
                        self.seekers_suppliers_list[i]['potential_offers'][j]["primary_latlng"].append(geocode_result[0]['geometry']['location']['lng'])
                    else:
                        reversegeocode_result=self.gm.reverse_geocode(self.seekers_suppliers_list[i]['potential_offers'][j]['primary_geo'])
                        self.seekers_suppliers_list[i]['potential_offers'][j]['primary_latlng'] = []
                        self.seekers_suppliers_list[i]['potential_offers'][j]['primary_latlng'].append(self.seekers_suppliers_list[i]['potential_offers'][j]['primary_geo'][0])
                        self.seekers_suppliers_list[i]['potential_offers'][j]['primary_latlng'].append(self.seekers_suppliers_list[i]['potential_offers'][j]['primary_geo'][1])
                        self.seekers_suppliers_list[i]['potential_offers'][j]['primary_geo'] = str(reversegeocode_result[0]['formatted_address'])

            else:
                reversegeocode_result=self.gm.reverse_geocode(self.seekers_suppliers_list[i]['primary_geo'])
                self.seekers_suppliers_list[i]['primary_latlng'] = []
                self.seekers_suppliers_list[i]["primary_latlng"].append(self.seekers_suppliers_list[i]['primary_geo'][0])
                self.seekers_suppliers_list[i]["primary_latlng"].append(self.seekers_suppliers_list[i]['primary_geo'][1])
                self.seekers_suppliers_list[i]['primary_geo'] = str(reversegeocode_result[0]['formatted_address'])
                for k in range(len(self.seekers_suppliers_list[i]['potential_offers'])):
                    if isinstance(self.seekers_suppliers_list[i]['potential_offers'][k]['primary_geo'],str):
                        self.seekers_suppliers_list[i]['potential_offers'][k]['primary_latlng'] = []
                        geocode_result =self.gm.geocode(self.seekers_suppliers_list[i]['potential_offers'][k]['primary_geo'])
                        self.seekers_suppliers_list[i]['potential_offers'][k]["primary_latlng"].append(geocode_result[0]['geometry']['location']['lat'])
                        self.seekers_suppliers_list[i]['potential_offers'][k]["primary_latlng"].append(geocode_result[0]['geometry']['location']['lng'])
                    else:
                        reversegeocode_result=self.gm.reverse_geocode(self.seekers_suppliers_list[i]['potential_offers'][k]['primary_geo'])
                        self.seekers_suppliers_list[i]['potential_offers'][k]['primary_latlng'] = []
                        self.seekers_suppliers_list[i]['potential_offers'][k]['primary_latlng'].append(self.seekers_suppliers_list[i]['potential_offers'][k]['primary_geo'][0])
                        self.seekers_suppliers_list[i]['potential_offers'][k]['primary_latlng'].append(self.seekers_suppliers_list[i]['potential_offers'][k]['primary_geo'][1])
                        self.seekers_suppliers_list[i]['potential_offers'][k]['primary_geo'] = str(reversegeocode_result[0]['formatted_address'])
        with open('seekers_suppliers_list.json', 'w') as fpsk:
            json.dump(self.seekers_suppliers_list, fpsk, indent=4)
        return self.seekers_suppliers_list
        

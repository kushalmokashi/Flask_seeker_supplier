from flask import Flask, render_template,request,jsonify
import sys,json,os
import googlemaps
import uuid
from classifier import Classifier
from phrase_matcher import PhraseMatcher
from geocoder import GeoCoder

UPLOAD_FOLDER =r'C:\Users\Kushal\flask-tutorial\Final\download'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=['GET' , 'POST'])
def homepage():
        if request.method == 'POST':
            f = request.files['file']
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
            data = json.loads(open(os.path.join(app.config['UPLOAD_FOLDER'], f.filename)).read())
            # print(data)
            # with open(os.path.join(app.config['UPLOAD_FOLDER'], f.filename)) as f1:
            #     data = json.load(f1)
            classifier = Classifier(data=data)
            classifier.classify()
            matcher = PhraseMatcher(seekerslist_json=classifier.seekerslist,supplierslist_json=classifier.supplierslist)
            matcher.match()
            # matching()
            seekers_suppliers_list = GeoCoder(seekers_suppliers_list=matcher.get_seekers_suppliers_list()).geocode()
            # seekers_suppliers_list = seekers_suppliers_list.geocode()
            # print(seekers_suppliers_list)

            # print(seekers_suppliers_list)seekers_suppliers_list
            return jsonify(seekers_suppliers_list)
            #return render_template('main.html',seekers_suppliers_list=json.dumps(seekers_suppliers_list))
        if request.method == 'GET':
            return render_template('main.html')

@app.template_filter('autoversion')
def autoversion_filter(filename):
  # determining fullpath might be project specific
  fullpath = filename[1:]
  try:
      timestamp = str(os.path.getmtime(fullpath))
  except OSError:
      return filename
  newfilename = "{0}?v={1}".format(filename, timestamp)
  return newfilename
    


if __name__ == "__main__":
      app.run(host='0.0.0.0', port=8000, debug=True)

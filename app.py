from flask import Flask, jsonify, render_template, url_for, request 
import spacy
from spacy import displacy
import es_core_news_sm

nlp = spacy.load('es_core_news_sm')

app = Flask(__name__)

@app.route('/')
def index():
	return "Spacy NLP API for LSB App"

@app.route('/process',methods=["POST"])
def analyze():  
    try: 
        sentence = request.get_json(force=True)
        try:
            doc = nlp(sentence["word"]) 

            tokens={"response":[]}
            for token in doc:
                string_tags=token.tag_.split("|") 
                tags = [{tag.split("=")[0]:tag.split("=")[1]} for tag in string_tags if len(tag.split("=")) >1 ]
                tokens["response"].append({
                                "lemma":token.lemma_,
                                "tag":token.pos_,
                                "tags":tags,"token":token.text})
            return tokens 
        except KeyError:
            return {"error":"Invalid Parameters"} , 400
    except ValueError:
        return {"error":"Invalid Parameters"} , 400

if __name__ == '__main__':
	app.run(debug=True)
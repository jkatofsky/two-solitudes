from flask import Flask, request
from flask_cors import CORS
from aitextgen import aitextgen
import traceback

app = Flask(__name__, static_folder='static', static_url_path='/')
CORS(app)

QC_model = aitextgen(model_folder='models/QC', \
        tokenizer_file='models/QC/aitextgen.tokenizer.json')
CA_model = aitextgen(model_folder='models/CA', \
        tokenizer_file='models/CA/aitextgen.tokenizer.json')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data: dict = request.json
        model = data.get('model')
        if not model or model not in ['CA', 'QC']:
            return {'error': 'invalid model'}, 400
        prompt = data.get('prompt', '')
        temperature = float(data.get('temperature', 0.6))
        gen_model = QC_model if model == 'QC' else CA_model
        text = gen_model.generate(prompt=prompt, return_as_list=True, temperature=temperature)[0]
        return {'text': text}
    except Exception as e:
        traceback.print_exc()
        return {'error': 'a server error occured'}, 500

@app.route('/')
def homepage():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
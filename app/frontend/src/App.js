import './App.css';
import { useState } from 'react';

let API_URL;
if (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1") {
  API_URL = "http://localhost:8080";
} else {
  API_URL = "https://two-solitudes.appspot.com";
}

async function generateAPICall(data) {
  const response = await fetch(`${API_URL}/generate`, {
    method: 'POST',
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data)
  });
  return response;
}

function App() {

  const [QCText, setQCText] = useState('');
  const [CAText, setCAText] = useState('');
  const [prompt, setPrompt] = useState('');

  const generateText = async (model) => {
    const setter = model === 'QC' ? setQCText : setCAText;
    setter('Loading...');
    const data = { model: model, prompt: prompt };
    console.log(data);
    const response = await generateAPICall(data);
    const responseData = await response.json();
    if (response.status !== 200) setter(responseData.error);
    else setter(responseData.text);
    console.log(QCText, CAText);
  }

  return (
    <div>
      <h1>Two Solitudes Text Genration (POLI 336)</h1>
      <h2><i>Josh Katofsky</i></h2>
      <hr />
      <textarea name="prompt" id="prompt" rows={1}
        placeholder="Write an (optional) start of a sentence that the models will attempt to continue"
        onChange={(event) => setPrompt(event.target.value)}
      />
      <h3>Quebec</h3>
      <button onClick={() => generateText('QC')}>Generate Text</button>
      <p>{QCText}</p>
      <h3>Rest of Canada</h3>
      <button onClick={() => generateText('CA')}>Generate Text</button>
      <p>{CAText}</p>
      <hr />
      <h2>About</h2>
      The Quebec and R.O.C. datasets are GPT-2 models fine-trained on about 100,000 reddit comments each.
    </div>
  );
}

export default App;

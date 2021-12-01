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
  const [temperature, setTemperature] = useState(0.6);

  const generateText = async (model) => {
    const setter = model === 'QC' ? setQCText : setCAText;
    setter('Loading...');
    const data = { model, prompt, temperature };
    const response = await generateAPICall(data);
    const responseData = await response.json();
    if (response.status !== 200) setter(responseData.error);
    else setter(`"${responseData.text}"`);
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
      <p>
        Temperature (between 0-1):
        <input type="number" id="temperature" name="temperature"
          min="0.1" max="1" defaultValue={temperature}
          onChange={(event) => setTemperature(event.target.value)} />
      </p>
      <h3>Quebec</h3>
      <button onClick={() => generateText('QC')}>Generate Text</button>
      <p>{QCText}</p>
      <h3>Rest of Canada</h3>
      <button onClick={() => generateText('CA')}>Generate Text</button>
      <p>{CAText}</p>
      <hr />
      <h2>About</h2>
      The models are GPT-2 instances fine-tuned on about 100,000 reddit comments each. All the code for that, as well as for this web app, can be found <a href="https://github.com/jkatofsky/two-solitudes" target='_blank' rel='noreferrer'>here</a>. The presentation associated with this project can be found <a href="https://mcgill-my.sharepoint.com/:p:/g/personal/joshua_katofsky_mail_mcgill_ca/EShwf6PLgWBHrpX2eB7fdkUBIC9g0bt4dcHhwnfZ3xaiCg?e=ZXgGHO" target='_blank' rel='noreferrer'>here</a>.
    </div>
  );
}

export default App;

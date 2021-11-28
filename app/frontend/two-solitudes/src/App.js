import './App.css';
import { useState } from 'react';

function App() {

  const [QCText, setQCText] = useState('');
  const [ROCText, setROCText] = useState('');

  const generateText = (model) => {
    const setter = model === 'QC' ? setQCText : setROCText;
    setter('Loading...');
    // TODO: call the Flask server and use setter again with the result and some "'s
  }

  return (
    <div>
      <h1>Two Solitudes Text Genration (POLI 336)</h1>
      <h2><i>Josh Katofsky</i></h2>
      <hr />
      <textarea name="prompt" id="prompt" rows={1} placeholder="Write an (optional) start of a sentence that the models will attempt to continue"/>
      <h3>Quebec</h3>
      <button onClick={() => generateText('QC')}>Generate Text</button>
      <p>{QCText}</p>
      <h3>Rest of Canada</h3>
      <button onClick={() => generateText('ROC')}>Generate Text</button>
      <p>{ROCText}</p>
      <hr />
      <h2>About the models</h2>
      <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed nec vestibulum velit. Maecenas molestie velit a posuere imperdiet. Integer leo tellus, pharetra eu sapien non, vestibulum dapibus est. Nam hendrerit posuere libero, sit amet accumsan magna iaculis eu. Donec nec arcu ac diam mattis condimentum. Sed at venenatis nulla. Vestibulum sit amet ullamcorper libero. Proin nibh metus, pellentesque in massa sed, tincidunt mollis ante. Praesent at dolor vel purus dictum dignissim. Nunc magna neque, sodales ac maximus ac, tincidunt nec enim. Ut ornare erat orci, vitae consequat dolor auctor sit amet. Sed aliquam dolor consequat, condimentum ligula a, convallis nisi.
      </p>
      <p>Morbi placerat in sem nec ornare. Nullam massa metus, pellentesque accumsan tincidunt sit amet, cursus varius eros. Etiam vitae arcu varius tellus feugiat tempor. Nam a metus ut ex scelerisque pulvinar at a quam. Quisque hendrerit risus quis posuere malesuada. Integer aliquet lacinia posuere. In auctor porttitor placerat. Suspendisse venenatis dui nisi, quis tempus tellus tincidunt eget. Sed convallis elementum congue. Maecenas luctus iaculis tempor. Vestibulum euismod, nunc eget efficitur cursus, lorem libero consectetur velit, id ullamcorper leo diam sed sapien. Maecenas a justo felis.</p>
    </div>
  );
}

export default App;

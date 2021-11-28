import './App.css';

function App() {
  return (
    <div>
      <h1>Two Solitudes - COMP 336 Final Project</h1>
      <textarea name="prompt" id="prompt" rows={1} placeholder="Write an (optional) start of a sentence to prompt the models"/>
      <button>
        Generate Text
      </button>
      <h3>Quebec:</h3>
      <p>[Generated text goes here]</p>
      <h3>Rest of Canada:</h3>
      <p>[Generated text goes here]</p>
    </div>
  );
}

export default App;

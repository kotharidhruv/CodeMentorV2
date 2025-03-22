import React, { useState } from 'react';
import CodeEditor from './components/CodeEditor';
import './App.css';

function App() {
  const [feedback, setFeedback] = useState(null); // Define setFeedback using useState

  const handleSubmitCode = (feedbackData) => {
    setFeedback(feedbackData); 
  };

  return (
    <div className="App-container">
      <header>
        <h1>CodeMentor</h1>
      </header>
      <p>Get feedback from your personal AI</p>
      <br/>
      <main>
        <CodeEditor onSubmitCode={handleSubmitCode} />
      </main>
    </div>
  );
}

export default App;

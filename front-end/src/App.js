import React, { useState } from 'react';
import CodeEditor from './components/CodeEditor';
import FeedbackPanel from './components/FeedbackPanel';
import './App.css';

function App() {
  const [feedback, setFeedback] = useState(null);

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

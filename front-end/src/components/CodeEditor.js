import React, { useState } from 'react';
import { loader, Editor } from '@monaco-editor/react';
import FeedbackPanel from './FeedbackPanel';

loader.config({
  paths: {
    vs: 'https://cdn.jsdelivr.net/npm/monaco-editor@0.40.0/min/vs',
  },
});

const CodeEditor = () => {
  const [code, setCode] = useState('// Write your code here...');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);
    setResponse('');
    try {
      const res = await fetch('http://localhost:5000/api/analyze_code', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code: code }),
      });

      const data = await res.json();

      if (data.response) {
        setResponse(data.response);
      } else if (data.error) {
        setResponse(`Error: ${data.error}`);
      }
    } catch (error) {
      setResponse(`Error: ${error.message}`);
    }
    setLoading(false);
  };

  return (
    <div className="CodeEditor-container">
      <h2 className="text-lg font-bold mb-4">Code Editor</h2>
      <Editor
        height="500px"
        width="100%"
        defaultLanguage="python"
        theme="vs-dark"
        value={code}
        onChange={(value) => setCode(value || '')}
        onMount={(editor, monaco) => {
          console.log('Monaco Editor loaded successfully.');
        }}
        onError={(error) => {
          console.error('Monaco initialization error:', error);
        }}
      />
      <button
        onClick={handleSubmit}
        className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-700"
        disabled={loading}
      >
        {loading ? <div className="loader"></div> : 'Submit Code'}
      </button>

      <FeedbackPanel feedback={response} />
    </div>
  );
};

export default CodeEditor;

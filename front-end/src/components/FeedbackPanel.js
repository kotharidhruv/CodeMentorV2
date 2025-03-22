import React from 'react';
import ReactMarkdown from 'react-markdown';

const FeedbackPanel = ({ feedback }) => {
  return (
    <div className="FeedbackPanel">
      <h2>AI Feedback</h2>
      <div className="feedback-content">
        <ReactMarkdown>{feedback}</ReactMarkdown>
      </div>
    </div>
  );
};

export default FeedbackPanel;

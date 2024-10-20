import React, { useState } from 'react';
import LandingPage from './LandingPage';

const App: React.FC = () => {
  const [userInput, setUserInput] = useState<string>('');
  const [response, setResponse] = useState<string | null>(null);

  // Handle input changes
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setUserInput(e.target.value);
  };

  // Handle form submit and send data to Flask backend
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();  // Prevent form from refreshing the page
    try {
      const res = await fetch(`http://127.0.0.1:5000/data/${userInput}`);
      const data = await res.json();
      setResponse(data.Output);  // Update the response state with the output from the backend
    } catch (error) {
      console.error('Error: ', error);
    }
  };

  return (
    <div>
      {/* Pass the form handling logic to the LandingPage */}
      <LandingPage
        userInput={userInput}
        handleInputChange={handleInputChange}
        handleSubmit={handleSubmit}
      />

      {/* Display response from the backend */}
      {response && (
        <div className="container has-text-centered">
          <h2 className="title">Response:</h2>
          <p>{response}</p>
        </div>
      )}
    </div>
  );
};

export default App;




import React, { useState } from "react";
import './App.css';

function App() {
  const [message, setMessage] = useState('');

  const [inputValue, setInputValue] = useState('');

  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };

  const handleClick = async () => {
    try {
      const response = await fetch('/data/' + inputValue);
      const data = await response.json();
      setMessage(data.Output);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className='App'>
      <header className='App-header'>
          <input
            type="text"
            value={inputValue}
            onChange={handleInputChange}
            placeholder="Enter text here"
          />
          <button onClick={handleClick}>Submit</button>
          <p>{ message }</p>
        </header>
    </div>
  );
}

export default App;

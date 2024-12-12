//Move React code (App.tsx, LandingPage.tsx, etc.) into popup.js.
//Update the fetch request in App.tsx to make sure it works in the extension:
//const res = await fetch(`http://127.0.0.1:5000/data/${userInput}`);

const { useState } = React;

// LandingPage Component (extracted from LandingPage.tsx)
const LandingPage = ({ userInput, handleInputChange, handleSubmit }) => (
  <section className="hero is-info is-fullheight">
    <div className="hero-body">
      <div className="container has-text-centered">
        <h1 className="title">Welcome to AutoQuote</h1>
        <h2 className="subtitle">Generate pop culture quotes in seconds!</h2>
        <div className="box">
          <form onSubmit={handleSubmit}>
            <div className="field is-grouped">
              <p className="control is-expanded">
                <input
                  className="input"
                  type="text"
                  placeholder="Enter your message"
                  value={userInput}
                  onChange={handleInputChange}
                  required
                />
              </p>
              <p className="control">
                <button className="button is-info" type="submit">
                  Generate Quote
                </button>
              </p>
            </div>
          </form>
        </div>
      </div>
    </div>
  </section>
);

// Main App Component (extracted from App.tsx)
const App = () => {
  const [userInput, setUserInput] = useState('');
  const [response, setResponse] = useState(null);

  const handleInputChange = (e) => {
    setUserInput(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await fetch(`http://127.0.0.1:5000/data/${userInput}`);
      const data = await res.json();
      setResponse(data.Output);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div>
      <LandingPage
        userInput={userInput}
        handleInputChange={handleInputChange}
        handleSubmit={handleSubmit}
      />
      {response && (
        <div className="container has-text-centered">
          <h2 className="title">Response:</h2>
          <p>{response}</p>
        </div>
      )}
    </div>
  );
};

// Render the app into the root element
ReactDOM.render(<App />, document.getElementById('root'));

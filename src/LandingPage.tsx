import React from 'react';
import 'bulma/css/bulma.min.css';
import '@fortawesome/fontawesome-free/css/all.min.css';

interface LandingPageProps {
  userInput: string;
  handleInputChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  handleSubmit: (e: React.FormEvent) => void;
}

const LandingPage: React.FC<LandingPageProps> = ({ userInput, handleInputChange, handleSubmit }) => {
  return (
    <section className="hero is-info is-fullheight">
      <div className="hero-body">
        <div className="container has-text-centered">
          <h1 className="title">Welcome to Autoquote</h1>
          <h2 className="subtitle">Generate pop culture quotes in seconds!</h2>
          <div className="box">
            {/* Form handles input and submission */}
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
};

export default LandingPage;




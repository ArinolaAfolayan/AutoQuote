document.getElementById('generateQuoteButton').addEventListener('click', async () => {
    console.log('Generate Quote button clicked'); // Log when button is clicked

    // Get the selected text
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    chrome.scripting.executeScript(
        {
            target: { tabId: tab.id },
            function: getSelectedText,
        },
        async (injectionResults) => {
            const selectedText = injectionResults[0].result;
            console.log('Selected text:', selectedText); // Log selected text

            if (selectedText) {
                try {
                    // Call the Flask backend to get the quote and GIF URL
                    const response = await fetch('http://localhost:5000/data/' + selectedText, {
                        method: 'GET',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                    });

                    console.log('Response status:', response.status); // Log response status

                    if (response.ok) {
                        const data = await response.json();
                        console.log('Received quote:', data.Output); // Log received quote
                        document.getElementById('quoteText').innerText = data.Output;
                        document.getElementById('quoteContainer').style.display = 'block';
                        const gifElement = document.createElement('img');
                        gifElement.src = data.gif_url;
                        gifElement.id = 'quoteGIF';
                        document.getElementById('quoteContainer').appendChild(gifElement);

                        // Add copy GIF button
                        const copyGIFButton = document.createElement('button');
                        copyGIFButton.innerText = 'Copy GIF';
                        copyGIFButton.className = 'copy-button';
                        copyGIFButton.id = 'copyGIFButton';
                        document.getElementById('quoteContainer').appendChild(copyGIFButton);

                        // Add event listener for copying GIF
                        document.getElementById('copyGIFButton').addEventListener('click', async () => {
                            try {
                                const response = await fetch(data.gif_url);
                                const blob = await response.blob();
                                const clipboardItem = new ClipboardItem({ 'image/gif': blob });
                                await navigator.clipboard.write([clipboardItem]);
                                alert('GIF copied to clipboard!');
                            } catch (err) {
                                console.error('Could not copy GIF: ', err);
                                alert('Failed to copy GIF.');
                            }
                        });

                    } else {
                        alert('Error generating quote. Please try again.');
                    }
                } catch (error) {
                    console.error('Error fetching quote:', error);
                    alert('An error occurred while generating the quote. Please try again.');
                }
            } else {
                alert('Please highlight some text first.');
            }
        }
    );
});

// Function to retrieve the selected text on the webpage
function getSelectedText() {
    return window.getSelection().toString();
}

// Copy quote to clipboard
document.getElementById('copyQuoteButton').addEventListener('click', () => {
    const quoteText = document.getElementById('quoteText').innerText;
    if (quoteText && quoteText !== "Your quote will appear here...") {
        navigator.clipboard.writeText(quoteText)
            .then(() => {
                alert('Quote copied to clipboard!');
            })
            .catch(err => {
                console.error('Could not copy text: ', err);
            });
    } else {
        alert('No quote to copy!');
    }
});






// //Move React code (App.tsx, LandingPage.tsx, etc.) into popup.js.
// //Update the fetch request in App.tsx to make sure it works in the extension:
// //const res = await fetch(`http://127.0.0.1:5000/data/${userInput}`);
// const { useState } = React;

// // LandingPage Component (extracted from LandingPage.tsx)
// const LandingPage = ({ userInput, handleInputChange, handleSubmit }) => (
//   <section className="hero is-info is-fullheight">
//     <div className="hero-body">
//       <div className="container has-text-centered">
//         <h1 className="title">Welcome to AutoQuote</h1>
//         <h2 className="subtitle">Generate pop culture quotes in seconds!</h2>
//         <div className="box">
//           <form onSubmit={handleSubmit}>
//             <div className="field is-grouped">
//               <p className="control is-expanded">
//                 <input
//                   className="input"
//                   type="text"
//                   placeholder="Enter your message"
//                   value={userInput}
//                   onChange={handleInputChange}
//                   required
//                 />
//               </p>
//               <p className="control">
//                 <button className="button is-info" type="submit">
//                   Generate Quote
//                 </button>
//               </p>
//             </div>
//           </form>
//         </div>
//       </div>
//     </div>
//   </section>
// );

// // Main App Component (extracted from App.tsx)
// const App = () => {
//   const [userInput, setUserInput] = useState('');
//   const [response, setResponse] = useState(null);

//   const handleInputChange = (e) => {
//     setUserInput(e.target.value);
//   };

//   const handleSubmit = async (e) => {
//     e.preventDefault();

//     try {
//       const res = await fetch(`http://127.0.0.1:5000/data/${userInput}`);
//       const data = await res.json();
//       setResponse(data.Output);
//     } catch (error) {
//       console.error('Error:', error);
//     }
//   };
// // 
//   return (
//     <div>
//       <LandingPage
//         userInput={userInput}
//         handleInputChange={handleInputChange}
//         handleSubmit={handleSubmit}
//       />
//       {response && (
//         <div className="container has-text-centered">
//           <h2 className="title">Response:</h2>
//           <p>{response}</p>
//         </div>
//       )}
//     </div>
//   );
// };

// // Render the app into the root element
// ReactDOM.render(<App />, document.getElementById('root'));

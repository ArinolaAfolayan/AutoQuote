document.getElementById('generateQuoteButton').addEventListener('click', async () => {
    const generateButton = document.getElementById('generateQuoteButton');
    const quoteContainer = document.getElementById('quoteContainer');
    const quoteTextElement = document.getElementById('quoteText');
    const gifElement = document.getElementById('quoteGIF');
    const copyQuoteButton = document.getElementById('copyQuoteButton');

    // Clear the previous result immediately
    quoteTextElement.innerText = '';
    gifElement.src = '';
    quoteContainer.style.display = 'none';

    // Update button text to indicate loading state
    generateButton.innerText = 'Loading...';

    // Get selected text from the active tab
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    chrome.scripting.executeScript(
        {
            target: { tabId: tab.id },
            function: () => window.getSelection().toString(),
        },
        async (results) => {
            const selectedText = results[0]?.result;
            if (!selectedText) {
                alert('Please select some text on the page or navigate to supported webpage.');
                console.error('No text selected.');
                generateButton.innerText = 'Get Quote & GIF'; // Reset button text
                return;
            }

            try {
                // Fetch quote and GIF from backend
                const response = await fetch(`http://localhost:8000/data/${selectedText}`);
                if (!response.ok) throw new Error('Error fetching quote data');

                const data = await response.json();

                // Update quote and GIF
                quoteTextElement.innerText = data.Output;
                gifElement.src = data.gif_url;
                quoteContainer.style.display = 'block';

                // Add copy functionality for quote only
                copyQuoteButton.onclick = () => {
                    navigator.clipboard.writeText(data.Output).catch((err) => console.error('Error copying quote:', err));
                };

                // Update button text to allow fetching a new result
                generateButton.innerText = 'Get New Quote & GIF';

            } catch (error) {
                console.error('Error processing request:', error);
                quoteTextElement.innerText = 'Failed to fetch quote. Please try again.';
                quoteContainer.style.display = 'block';
                generateButton.innerText = 'Get Quote & GIF'; // Reset button text
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

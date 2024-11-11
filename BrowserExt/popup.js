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
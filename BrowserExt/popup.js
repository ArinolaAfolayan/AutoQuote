// Declaring global variables, to be used in the copy quote fxn
// Give em a default value
let g_fontSize = '16px';
let g_fontType = 'Arial';

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
            function: () => {
                // Retrieving element where text is selected: https://stackoverflow.com/questions/1335252/how-can-i-get-the-dom-element-which-contains-the-current-selection/1335347
                // Example of using window.getComputedStyle(element): https://www.w3schools.com/jsref/jsref_getcomputedstyle.asp

                const selectedText = window.getSelection().toString();
                
                const textElement = window.getSelection().getRangeAt(0).startContainer.parentNode;
                const styleElement = window.getComputedStyle(textElement);
                
                
                const fontType = styleElement.getPropertyValue("font-family");
                const fontSize = styleElement.getPropertyValue("font-size");
                window.getSelection().removeAllRanges();

                return {
                    selectedText,
                    fontType,
                    fontSize  
                };
            },
        },
        async (results) => {
            console.log(results);
            // console.log(results[0]?.result);
            const { fontSize, fontType, selectedText } = results[0]?.result;
            // console.log(selectedText);
            // console.log(fontSize);
            // console.log(fontType);
            if (!selectedText) {
                console.error('No text selected.');
                generateButton.innerText = 'Get Quote & GIF'; // Reset button text
                return;
            }

            // Set font size and font type
            g_fontSize = fontSize;
            g_fontType = fontType;

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
// Source -- Copy rich text: https://stackoverflow.com/questions/74838274/copy-html-rich-text-using-js-navigator-clipboard
document.getElementById('copyQuoteButton').addEventListener('click', () => {
    const quoteText = document.getElementById('quoteText').innerText.trim();
    const content = `<span style="font-size: ${g_fontSize}; font-family: ${g_fontType}">${quoteText}</span>`
    const blobHtml = new Blob([content], { type: "text/html" });
    const blobText = new Blob([quoteText], { type: "text/plain" });
    const data = [new ClipboardItem({
        ["text/plain"]: blobText,
        ["text/html"]: blobHtml,
    })];

    if (quoteText && quoteText !== "Your quote will appear here...") {
        navigator.clipboard.write(data)
            .then(() => {
                // alert('Quote copied to clipboard!');
                const buttonElement = document.getElementById('copyQuoteButton');
                const buttonText = buttonElement.innerHTML;
                buttonElement.innerHTML = 'Copied &#x2714;';

                // Revert button text after some time
                setTimeout(() => {
                    buttonElement.innerHTML = buttonText;
                }, 1500);
            })
            .catch(err => {
                console.error('Could not copy text: ', err);
            });
    } else {
        alert('No quote to copy!');
    }
});

// The content script is injected into web pages and can interact with DOM elements to read the text displayed on the page.

// Function to extract text from a webpage (simple version)
function extractText() {
    // Get the text content from the body of the webpage
    let pageText = document.body.innerText;
    return pageText;
  }
  
  // Send extracted text to the background script
  chrome.runtime.sendMessage({ text: extractText() }, function(response) {
    console.log("Relevant Quote:", response.quote);
  });
  
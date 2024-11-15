chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "getQuote",
    title: "Spice Up Your Messages",
    contexts: ["selection"]
  });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "getQuote" && info.selectionText) {
    chrome.storage.local.set({ selectedText: info.selectionText }, () => {
      chrome.action.openPopup();
    });
  }
});

// PDF Upload functionality
document.getElementById("fileUpload").addEventListener("change", async function() {
    const file = this.files[0];
    if (!file) return;
    if (file.type !== "application/pdf") {
        alert("Please upload a PDF file.");
        return;
    }
    // Check the checkbox when a file is uploaded
    const pdfCheckbox = document.getElementById("usePdfCheckbox");
    if (pdfCheckbox) pdfCheckbox.checked = true;

    const formData = new FormData();
    formData.append("file", file);
    const outputDiv = document.getElementById("output");
    outputDiv.innerHTML += `<p><b>You uploaded:</b> ${file.name}</p>`;
    try {
        const response = await fetch("/upload_pdf", {
            method: "POST",
            body: formData
        });
        const data = await response.json();
        if (data.success) {
            // Only show that PDF was uploaded, not its content
            outputDiv.innerHTML += `<p style='color:green;'><b>PDF uploaded and ready for questions.</b></p>`;
        } else if (data.error) {
            outputDiv.innerHTML += `<p style='color:red;'><b>Error:</b> ${data.error}</p>`;
        }
        outputDiv.scrollTop = outputDiv.scrollHeight;
    } catch (err) {
        outputDiv.innerHTML += `<p style='color:red;'><b>Error uploading PDF.</b></p>`;
    }
});
document.getElementById("sendBtn").addEventListener("click", () => sendCommand())
document.getElementById("micBtn").addEventListener("click", toggleMic);

async function sendCommand(input = null, speak = false) {
    const inputBox = document.getElementById("commandInput");
    const text = input || inputBox.value;
    const usePdf = document.getElementById("usePdfCheckbox")?.checked;

    if (!text.trim()) return;

    const response = await fetch("/process", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({command: text, use_pdf: usePdf})
    });

    const data = await response.json();
    const outputDiv = document.getElementById("output");

    // Add user message (right)
    outputDiv.innerHTML += `
      <div class="chat-message user">
        <div class="bubble user"><b>You:</b> ${text}</div>
      </div>
    `;
    // Add AI message (left, structured)
    outputDiv.innerHTML += `
      <div class="chat-message ai">
        <div class="bubble ai"><pre>${data.response}</pre></div>
      </div>
    `;
    console.log(data.response);
    outputDiv.scrollTop = outputDiv.scrollHeight;

    if (speak) {
        speakResponse(data.response);
    }

    inputBox.value = "";

}

// 🎤 Microphone Functionality
let recognition;
function toggleMic() {
    console.log("Button clicked");
    if (!('webkitSpeechRecognition' in window)) {
        alert("Your browser doesn't support speech recognition.");
        return;
    }

    if (!recognition) {
        recognition = new webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = "en-US";

        recognition.onstart = () => {
            console.log("Speech recognition started");
            document.getElementById("micBtn").classList.add("listening");
        };

        recognition.onend = () => {
            console.log("Speech recognition ended");
            document.getElementById("micBtn").classList.remove("listening");
        };

        recognition.onerror = (event) => {
        console.error("Speech recognition error:", event.error);
        };

        recognition.onresult = (event) => {
        console.log("onresult event fired");
        const transcript = event.results[0][0].transcript;
        console.log(transcript);
        sendCommand(transcript, true);
};
    }

    recognition.start();
}

// 🗣️ Voice output
function speakResponse(text) {
    if ("speechSynthesis" in window) {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = "en-US";
        speechSynthesis.speak(utterance);
    }
}

import React, { useState } from "react";

function App() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);

  const sendMessage = async () => {
    if (!input) return;

    const userMessage = { role: "user", content: input };
    setMessages([...messages, userMessage]);

    try {
      const response = await fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: input }),
      });

      const data = await response.json();
      const aiMessage = { role: "ai", content: data.response };

      setMessages([...messages, userMessage, aiMessage]);
      setInput("");
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h1>AI Chatbot</h1>
      <div
        style={{
          border: "1px solid black",
          padding: "10px",
          width: "300px",
          margin: "auto",
          height: "400px",
          overflowY: "auto",
        }}
      >
        {messages.map((msg, index) => (
          <p key={index} style={{ textAlign: msg.role === "user" ? "right" : "left" }}>
            <strong>{msg.role === "user" ? "You" : "AI"}:</strong> {msg.content}
          </p>
        ))}
      </div>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Type a message..."
        style={{ marginTop: "10px", padding: "5px" }}
      />
      <button onClick={sendMessage} style={{ marginLeft: "10px", padding: "5px" }}>
        Send
      </button>
    </div>
  );
}

export default App;

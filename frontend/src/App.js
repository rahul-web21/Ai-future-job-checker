import { useState } from "react";
import "./App.css";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = {
      role: "user",
      content: input,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: userMessage.content,
          history: [],
        }),
      });

      const data = await response.json();

      const botMessage = {
        role: "assistant",
        content: data.answer,
        sources: data.sources,
        score: data.future_score,
        evaluation: data.evaluation,
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "⚠️ Backend not reachable" },
      ]);
    }

    setLoading(false);
  };

  return (
    <div className="app">
      <h2>🤖 AI Career Chatbot</h2>

      <div className="chat-box">
        {messages.map((msg, i) => (
          <div key={i} className={`msg ${msg.role}`}>
            <p>{msg.content}</p>

            {msg.score !== undefined && (
              <p className="score">Future Safety Score: {msg.score}/100</p>
            )}

            {msg.sources && (
              <ul>
                {msg.sources.map((s, idx) => (
                  <li key={idx}>{s}</li>
                ))}
              </ul>
            )}
          </div>
        ))}

        {loading && <p>AI is thinking...</p>}
      </div>

      <div className="input-box">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about future of a job..."
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
}

export default App;
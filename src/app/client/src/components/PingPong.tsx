import { useState } from "react";

const PingPong = () => {
  const [response, setResponse] = useState<string>("");

  const handlePing = async () => {
    try {
      const res = await fetch("http://localhost:3000/ping");
      const data = await res.json();
      setResponse(data.message);
    } catch (error) {
      console.error("Error fetching ping:", error);
      setResponse("Error");
    }
  };

  return (
    <div>
      <button onClick={handlePing}>Ping</button>
      <p>Response: {response}</p>
    </div>
  );
};

export default PingPong;

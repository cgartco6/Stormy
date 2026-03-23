import React, { useState, useEffect } from 'react';
import { io } from 'socket.io-client';
import Chat from './components/Chat';
import MusicPlayer from './components/MusicPlayer';
import Settings from './components/Settings';

function App() {
  const [socket, setSocket] = useState(null);
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    const newSocket = io(process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000');
    setSocket(newSocket);
    newSocket.on('response', (data) => {
      setMessages(prev => [...prev, { from: 'stormy', text: data.reply }]);
    });
    return () => newSocket.close();
  }, []);

  const sendMessage = (text) => {
    setMessages(prev => [...prev, { from: 'user', text }]);
    socket.emit('message', { message: text });
  };

  return (
    <div>
      <Chat messages={messages} onSend={sendMessage} />
      <MusicPlayer />
      <Settings />
    </div>
  );
}

export default App;

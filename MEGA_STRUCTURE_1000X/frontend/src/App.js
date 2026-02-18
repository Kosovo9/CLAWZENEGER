import React, { useState, useEffect, useRef } from 'react';
import './App.css';

function App() {
    const [messages, setMessages] = useState([]);
    const [inputText, setInputText] = useState('');
    const [isConnected, setIsConnected] = useState(false);
    const [isListening, setIsListening] = useState(false);
    const [isTyping, setIsTyping] = useState(false);
    const [currentVoice, setCurrentVoice] = useState('joanna_co');
    const wsRef = useRef(null);
    const mediaRecorderRef = useRef(null);
    const audioChunksRef = useRef([]);
    const reconnectAttemptsRef = useRef(0);
    const scrollRef = useRef();

    useEffect(() => {
        connectWebSocket();
        // Auto-scroll
        scrollRef.current?.scrollIntoView({ behavior: 'smooth' });

        return () => {
            if (wsRef.current) wsRef.current.close();
        };
    }, [messages]);

    const connectWebSocket = () => {
        const wsUrl = `ws://${window.location.hostname}:9300/ws/voice`;
        wsRef.current = new WebSocket(wsUrl);

        wsRef.current.onopen = () => {
            console.log('✅ CONECTADO AL BUNKER');
            setIsConnected(true);
            reconnectAttemptsRef.current = 0;
            setMessages([{
                role: 'assistant',
                content: '🇨🇴 ¡Hola socio! Soy Joanna, tu ejecutiva personal. El búnker está operativo al 3000%. ¿Qué orden tienes para mí?',
                timestamp: new Date().toLocaleTimeString()
            }]);
        };

        wsRef.current.onclose = () => {
            setIsConnected(false);
            const delay = Math.min(1000 * Math.pow(2, reconnectAttemptsRef.current), 10000);
            console.log(`❌ Conexión perdida. Reintentando en ${delay}ms...`);
            setTimeout(() => {
                reconnectAttemptsRef.current++;
                connectWebSocket();
            }, delay);
        };

        wsRef.current.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);

                if (data.type === 'partial_response') {
                    setIsTyping(false);
                    setMessages(prev => {
                        const lastMsg = prev[prev.length - 1];
                        if (lastMsg && lastMsg.role === 'assistant' && !lastMsg.isFinal) {
                            const newMsgs = [...prev];
                            newMsgs[newMsgs.length - 1].content += data.text;
                            return newMsgs;
                        } else {
                            return [...prev, { role: 'assistant', content: data.text, isFinal: false }];
                        }
                    });
                }
                else if (data.type === 'response') {
                    setIsTyping(false);
                    setMessages(prev => {
                        const lastMsg = prev[prev.length - 1];
                        const finalMsg = {
                            role: 'assistant',
                            content: data.text,
                            isFinal: true,
                            timestamp: new Date().toLocaleTimeString()
                        };
                        if (lastMsg && lastMsg.role === 'assistant' && !lastMsg.isFinal) {
                            const newMsgs = [...prev];
                            newMsgs[newMsgs.length - 1] = finalMsg;
                            return newMsgs;
                        }
                        return [...prev, finalMsg];
                    });
                }
                else if (data.type === 'audio') {
                    const audio = new Audio("data:audio/wav;base64," + data.data);
                    audio.play().catch(e => console.error("Error audio:", e));
                }
                else if (data.type === 'status') {
                    if (data.text.includes("Pensando")) setIsTyping(true);
                    if (data.text.includes("Transcribiendo")) setIsListening(true);
                }
                else if (data.type === 'transcribed') {
                    setIsListening(false);
                    setMessages(prev => [...prev, { role: 'system', content: data.content }]);
                }
            } catch (e) {
                // Manejar chunks de audio binario si es necesario
            }
        };
    };

    const startRecording = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorderRef.current = new MediaRecorder(stream);
            audioChunksRef.current = [];

            mediaRecorderRef.current.ondataavailable = (e) => {
                if (e.data.size > 0) audioChunksRef.current.push(e.data);
            };

            mediaRecorderRef.current.onstop = () => {
                const blob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
                const reader = new FileReader();
                reader.onloadend = () => {
                    const base64 = reader.result.split(',')[1];
                    wsRef.current.send(JSON.stringify({ type: 'audio', data: base64 }));
                };
                reader.readAsDataURL(blob);
            };

            mediaRecorderRef.current.start();
            setIsListening(true);
        } catch (err) {
            alert("Error acceso micrófono");
        }
    };

    const stopRecording = () => {
        if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
            mediaRecorderRef.current.stop();
            setIsListening(false);
        }
    };

    const sendMessage = () => {
        if (!inputText.trim() || !isConnected) return;
        setMessages(prev => [...prev, { role: 'user', content: inputText, timestamp: new Date().toLocaleTimeString() }]);
        wsRef.current.send(JSON.stringify({ type: 'text', content: inputText }));
        setInputText('');
        setIsTyping(true);
    };

    return (
        <div className="app-container">
            <header className="glass-header">
                <div className="logo-section">
                    <span className="pulsing-dot"></span>
                    <h1>JOANNA 3000%</h1>
                </div>
                <div className={`connection-badge ${isConnected ? 'online' : 'offline'}`}>
                    {isConnected ? 'SISTEMA ONLINE' : 'RECONECTANDO BRAIN...'}
                </div>
            </header>

            <main className="chat-area">
                <div className="messages-list">
                    {messages.map((m, i) => (
                        <div key={i} className={`message-wrapper ${m.role}`}>
                            <div className="message-bubble">
                                <p>{m.content}</p>
                                <span className="msg-time">{m.timestamp}</span>
                            </div>
                        </div>
                    ))}
                    <div ref={scrollRef}></div>
                </div>

                {isTyping && <div className="typing-indicator">Joanna está analizando...</div>}
                {isListening && <div className="listening-indicator">Te escucho, socio...</div>}
            </main>

            <footer className="input-section">
                <div className="input-bar">
                    <button
                        className={`mic-btn ${isListening ? 'active' : ''}`}
                        onMouseDown={startRecording}
                        onMouseUp={stopRecording}
                        onMouseLeave={stopRecording}
                    >
                        🎤
                    </button>
                    <input
                        type="text"
                        placeholder="Ordenes tácticas..."
                        value={inputText}
                        onChange={(e) => setInputText(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                    />
                    <button className="send-btn" onClick={sendMessage}>🚀</button>
                </div>
            </footer>
        </div>
    );
}

export default App;

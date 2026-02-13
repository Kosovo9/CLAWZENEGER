import React, { useState, useEffect, useRef } from 'react';

function App() {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [ws, setWs] = useState(null);
    const [recording, setRecording] = useState(false);
    const [audioQueue, setAudioQueue] = useState([]);
    const mediaRecorderRef = useRef(null);
    const chunksRef = useRef([]);
    const messagesEndRef = useRef(null);
    const audioRef = useRef(null);

    useEffect(() => {
        const socket = new WebSocket(`ws://${window.location.hostname}:9300/ws/neilmaster`);

        socket.onmessage = (event) => {
            if (event.data instanceof Blob) {
                // Es audio
                const url = URL.createObjectURL(event.data);
                setAudioQueue(prev => [...prev, url]);
            } else {
                // Es JSON
                const data = JSON.parse(event.data);
                if (data.type === 'response') {
                    setMessages(prev => [...prev, {
                        role: 'neil',
                        text: data.text,
                        timestamp: new Date().toLocaleTimeString()
                    }]);
                }
            }
        };

        socket.onopen = () => {
            setMessages([{
                role: 'neil',
                text: '🦁 ¡Hola socio! Soy NeilZenneger, tu asistente personal. ¿En qué puedo ayudarte?',
                timestamp: new Date().toLocaleTimeString()
            }]);
        };

        setWs(socket);

        return () => socket.close();
    }, []);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    useEffect(() => {
        if (audioQueue.length > 0 && audioRef.current) {
            audioRef.current.src = audioQueue[0];
            audioRef.current.play();
            audioRef.current.onended = () => {
                setAudioQueue(prev => prev.slice(1));
            };
        }
    }, [audioQueue]);

    const sendMessage = () => {
        if (!input.trim() || !ws) return;

        setMessages(prev => [...prev, {
            role: 'user',
            text: input,
            timestamp: new Date().toLocaleTimeString()
        }]);

        ws.send(JSON.stringify({ type: 'text', content: input }));
        setInput('');
    };

    const startRecording = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorderRef.current = new MediaRecorder(stream);
            chunksRef.current = [];

            mediaRecorderRef.current.ondataavailable = (e) => {
                chunksRef.current.push(e.data);
            };

            mediaRecorderRef.current.onstop = () => {
                const audioBlob = new Blob(chunksRef.current, { type: 'audio/webm' });
                const reader = new FileReader();
                reader.onload = () => {
                    const base64 = reader.result.split(',')[1];
                    ws.send(JSON.stringify({ type: 'audio', data: base64 }));
                };
                reader.readAsDataURL(audioBlob);
                stream.getTracks().forEach(track => track.stop());
            };

            mediaRecorderRef.current.start();
            setRecording(true);
        } catch (error) {
            console.error('Error accessing microphone:', error);
        }
    };

    const stopRecording = () => {
        if (mediaRecorderRef.current && recording) {
            mediaRecorderRef.current.stop();
            setRecording(false);
        }
    };

    return (
        <div style={{
            display: 'flex',
            flexDirection: 'column',
            height: '100vh',
            backgroundColor: '#111827',
            color: 'white',
            fontFamily: 'system-ui, -apple-system, sans-serif'
        }}>
            {/* Header */}
            <div style={{
                background: 'linear-gradient(to right, #6b21a8, #1e3a8a)',
                padding: '16px 24px'
            }}>
                <h1 style={{ fontSize: '24px', fontWeight: 'bold', margin: 0 }}>
                    🤖 NeilZenneger - Tu Asistente Personal
                </h1>
                <p style={{ margin: '4px 0 0', opacity: 0.8 }}>
                    Háblame como a un amigo, te entiendo y ejecuto
                </p>
            </div>

            {/* Chat area */}
            <div style={{
                flex: 1,
                overflowY: 'auto',
                padding: '20px',
                display: 'flex',
                flexDirection: 'column',
                gap: '16px'
            }}>
                {messages.map((msg, i) => (
                    <div key={i} style={{
                        display: 'flex',
                        justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start'
                    }}>
                        <div style={{
                            maxWidth: '70%',
                            backgroundColor: msg.role === 'user' ? '#2563eb' : '#1f2937',
                            borderRadius: '12px',
                            padding: '12px 16px'
                        }}>
                            <p style={{ margin: 0 }}>{msg.text}</p>
                            <p style={{
                                fontSize: '10px',
                                opacity: 0.5,
                                margin: '4px 0 0',
                                textAlign: 'right'
                            }}>{msg.timestamp}</p>
                        </div>
                    </div>
                ))}
                <div ref={messagesEndRef} />
            </div>

            {/* Input area */}
            <div style={{
                borderTop: '1px solid #374151',
                padding: '16px',
                backgroundColor: '#1f2937'
            }}>
                <div style={{ display: 'flex', gap: '8px' }}>
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                        placeholder="Escribe o usa el micrófono..."
                        style={{
                            flex: 1,
                            backgroundColor: '#374151',
                            border: 'none',
                            borderRadius: '8px',
                            padding: '8px 16px',
                            color: 'white',
                            fontSize: '16px'
                        }}
                    />
                    <button
                        onClick={sendMessage}
                        style={{
                            backgroundColor: '#6b21a8',
                            color: 'white',
                            border: 'none',
                            borderRadius: '8px',
                            padding: '8px 16px',
                            cursor: 'pointer'
                        }}
                    >
                        Enviar
                    </button>
                    <button
                        onClick={recording ? stopRecording : startRecording}
                        style={{
                            backgroundColor: recording ? '#dc2626' : '#16a34a',
                            color: 'white',
                            border: 'none',
                            borderRadius: '8px',
                            padding: '8px 16px',
                            cursor: 'pointer'
                        }}
                    >
                        {recording ? '⏹️' : '🎤'}
                    </button>
                </div>
            </div>

            {/* Audio player oculto */}
            <audio ref={audioRef} style={{ display: 'none' }} />
        </div>
    );
}

export default App;

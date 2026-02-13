import React, { useState, useEffect, useRef } from 'react';
import { Mic, Square, Send, User, Bot, Zap } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export default function ChatInterface({ userId = "master" }) {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [ws, setWs] = useState(null);
    const [isRecording, setIsRecording] = useState(false);
    const [isProcessing, setIsProcessing] = useState(false);
    const messagesEndRef = useRef(null);
    const mediaRecorderRef = useRef(null);
    const chunksRef = useRef([]);

    useEffect(() => {
        const socket = new WebSocket(`ws://${window.location.hostname}:9300/ws/${userId}`);

        socket.onopen = () => console.log("✅ NeilChat Central Link Established");

        socket.onmessage = (event) => {
            const data = JSON.parse(event.data);

            if (data.type === 'history') {
                setMessages(data.data);
            } else if (data.type === 'response') {
                setMessages(prev => [...prev, {
                    role: 'neil',
                    text: data.text,
                    timestamp: new Date().toISOString(),
                    acciones: data.acciones
                }]);
                setIsProcessing(false);
            } else if (data.type === 'audio') {
                playAudio(data.data);
            } else if (data.type === 'transcription') {
                setMessages(prev => [...prev, {
                    role: 'user',
                    text: data.text,
                    timestamp: new Date().toISOString()
                }]);
            }
        };

        setWs(socket);
        return () => socket.close();
    }, [userId]);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    const playAudio = (base64) => {
        const audio = new Audio(`data:audio/wav;base64,${base64}`);
        audio.play();
    };

    const sendMessage = () => {
        if (!input.trim()) return;
        setMessages(prev => [...prev, {
            role: 'user',
            text: input,
            timestamp: new Date().toISOString()
        }]);
        ws.send(JSON.stringify({ type: 'text', content: input }));
        setInput('');
        setIsProcessing(true);
    };

    const startRecording = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorderRef.current = new MediaRecorder(stream);
            chunksRef.current = [];

            mediaRecorderRef.current.ondataavailable = (e) => chunksRef.current.push(e.data);

            mediaRecorderRef.current.onstop = () => {
                const audioBlob = new Blob(chunksRef.current, { type: 'audio/wav' });
                const reader = new FileReader();
                reader.onload = () => {
                    const base64 = reader.result.split(',')[1];
                    ws.send(JSON.stringify({ type: 'audio', data: base64 }));
                };
                reader.readAsDataURL(audioBlob);
                stream.getTracks().forEach(track => track.stop());
                setIsProcessing(true);
            };

            mediaRecorderRef.current.start();
            setIsRecording(true);
        } catch (error) {
            console.error('Error Mic:', error);
        }
    };

    const stopRecording = () => {
        if (mediaRecorderRef.current && isRecording) {
            mediaRecorderRef.current.stop();
            setIsRecording(false);
        }
    };

    return (
        <div className="flex flex-col h-screen bg-[#0a0b0e] text-gray-100 font-sans">
            {/* Header Premium */}
            <header className="px-6 py-4 bg-[#12141a] border-b border-gray-800 flex justify-between items-center shadow-2xl">
                <div className="flex items-center space-x-3">
                    <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-orange-500 to-red-600 flex items-center justify-center shadow-lg shadow-red-500/20">
                        <Bot size={24} className="text-white" />
                    </div>
                    <div>
                        <h1 className="text-xl font-bold tracking-tight text-white">NEILZENNEGER <span className="text-xs text-orange-500 font-mono">10000X</span></h1>
                        <p className="text-[10px] uppercase tracking-widest text-gray-500 flex items-center">
                            <span className="w-1.5 h-1.5 bg-green-500 rounded-full mr-2 animate-pulse"></span>
                            Soberanía Digital Activa
                        </p>
                    </div>
                </div>
            </header>

            {/* Area de Mensajes */}
            <main className="flex-1 overflow-y-auto px-6 py-8 space-y-6 scrollbar-hide">
                <AnimatePresence>
                    {messages.map((msg, i) => (
                        <motion.div
                            key={i}
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                        >
                            <div className={`flex max-w-[80%] space-x-3 ${msg.role === 'user' ? 'flex-row-reverse space-x-reverse' : ''}`}>
                                <div className={`mt-1 flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${msg.role === 'user' ? 'bg-blue-600' : 'bg-gray-800 border border-gray-700'
                                    }`}>
                                    {msg.role === 'user' ? <User size={16} /> : <Zap size={16} className="text-orange-500" />}
                                </div>

                                <div className={`p-4 rounded-2xl shadow-xl ${msg.role === 'user'
                                        ? 'bg-blue-600 text-white rounded-tr-none'
                                        : 'bg-[#1a1d24] text-gray-200 border border-gray-800 rounded-tl-none'
                                    }`}>
                                    <p className="text-[15px] leading-relaxed">{msg.text}</p>

                                    {msg.acciones && msg.acciones.length > 0 && (
                                        <div className="mt-3 pt-3 border-t border-gray-700/50 space-y-2">
                                            <p className="text-[10px] font-bold text-orange-500 uppercase tracking-tighter">Acciones Desencadenadas:</p>
                                            {msg.acciones.map((acc, j) => (
                                                <div key={j} className="flex items-center space-x-2 text-[12px] bg-black/20 p-2 rounded-lg border border-white/5">
                                                    <Zap size={10} className="text-yellow-500" />
                                                    <span className="font-mono">{acc.agente}</span>
                                                    <span className="text-gray-500">→</span>
                                                    <span className="text-blue-400">{acc.comando}</span>
                                                </div>
                                            ))}
                                        </div>
                                    )}

                                    <div className="mt-2 text-[9px] opacity-40 text-right">
                                        {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                    </div>
                                </div>
                            </div>
                        </motion.div>
                    ))}
                    {isProcessing && (
                        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex justify-start">
                            <div className="bg-[#1a1d24] p-4 rounded-2xl flex space-x-2">
                                <div className="w-2 h-2 bg-orange-500 rounded-full animate-bounce"></div>
                                <div className="w-2 h-2 bg-orange-500 rounded-full animate-bounce [animation-delay:-.3s]"></div>
                                <div className="w-2 h-2 bg-orange-500 rounded-full animate-bounce [animation-delay:-.5s]"></div>
                            </div>
                        </motion.div>
                    )}
                </AnimatePresence>
                <div ref={messagesEndRef} />
            </main>

            {/* Input de Control */}
            <footer className="p-6 bg-[#0a0b0e] border-t border-gray-900">
                <div className="max-w-4xl mx-auto flex items-center space-x-4 bg-[#1a1d24] p-2 rounded-2xl border border-gray-800 focus-within:border-orange-500/50 transition-all shadow-inner">
                    <button
                        onMouseDown={startRecording}
                        onMouseUp={stopRecording}
                        className={`p-4 rounded-xl transition-all ${isRecording ? 'bg-red-600 animate-pulse shadow-lg shadow-red-600/40' : 'bg-gray-800 hover:bg-gray-700 text-gray-400'
                            }`}
                    >
                        {isRecording ? <Square size={20} className="text-white" /> : <Mic size={20} />}
                    </button>

                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
                        placeholder="Comanda tus ideas..."
                        className="flex-1 bg-transparent border-none focus:ring-0 text-gray-100 placeholder-gray-600 py-3 px-2 font-medium"
                    />

                    <button
                        onClick={sendMessage}
                        className="p-4 bg-orange-600 text-white rounded-xl hover:bg-orange-700 transition-all shadow-lg shadow-orange-600/20"
                    >
                        <Send size={20} />
                    </button>
                </div>
                <p className="text-[10px] text-center mt-4 text-gray-600 font-mono italic">
                    Tip: NeilZenneger te escucha y traduce tus intenciones a comandos para los agentes.
                </p>
            </footer>
        </div>
    );
}

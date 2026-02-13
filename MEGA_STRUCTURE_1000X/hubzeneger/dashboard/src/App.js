import React, { useState, useEffect, useRef } from 'react';
import { BrowserRouter } from 'react-router-dom';

// === CONFIGURACIÓN ===
const WS_JOANNA = "ws://localhost:9300/ws/user_1000x";
const API_BASE = "http://localhost:54321/api/v1";

const SidebarItem = ({ icon, label, active, onClick, badge }) => (
  <button
    onClick={onClick}
    className={`w-full flex items-center justify-between gap-3 px-4 py-3 rounded-xl transition-all duration-300 group ${active
      ? 'bg-gradient-to-r from-red-900/40 to-transparent border-l-2 border-red-500 text-white'
      : 'text-gray-500 hover:text-gray-300 hover:bg-white/5'
      }`}
  >
    <div className="flex items-center gap-3">
      <div className={`${active ? 'text-red-500' : 'text-gray-500 group-hover:text-gray-300'}`}>
        {icon}
      </div>
      <span className="font-bold text-xs tracking-wider uppercase">{label}</span>
    </div>
    {badge && <span className="px-2 py-0.5 bg-red-600 text-white text-[10px] font-bold rounded-full">{badge}</span>}
  </button>
);

const StatCard = ({ icon, label, value, trend, color = "cyan" }) => (
  <div className="bg-[#0a0a0a] border border-white/5 rounded-2xl p-6 hover:border-red-500/30 transition-all">
    <div className="flex items-start justify-between mb-4">
      <div className={`w-12 h-12 rounded-xl bg-${color}-950/30 flex items-center justify-center text-${color}-400`}>
        {icon}
      </div>
      {trend && <span className={`text-xs font-bold ${trend > 0 ? 'text-green-500' : 'text-red-500'}`}>
        {trend > 0 ? '↑' : '↓'} {Math.abs(trend)}%
      </span>}
    </div>
    <div className="text-3xl font-black text-white mb-1">{value}</div>
    <div className="text-xs font-bold text-gray-500 uppercase tracking-wider">{label}</div>
  </div>
);

const AgentCard = ({ agent }) => (
  <div className="bg-[#0a0a0a] border border-white/5 rounded-xl p-4 hover:border-red-500/30 transition-all">
    <div className="flex items-center justify-between mb-3">
      <div className="flex items-center gap-3">
        <div className={`w-2 h-2 rounded-full ${agent.status === 'active' ? 'bg-green-500 animate-pulse' : 'bg-gray-600'}`}></div>
        <span className="font-bold text-sm text-white">{agent.name}</span>
      </div>
      <span className="text-xs text-gray-500">{agent.lastRun}</span>
    </div>
    <div className="flex items-center justify-between">
      <span className="text-xs text-gray-600">Tasks Completed</span>
      <span className="text-sm font-bold text-cyan-400">{agent.tasks.toLocaleString()}</span>
    </div>
  </div>
);

const ChatMessage = ({ text, isUser, timestamp, acciones }) => (
  <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-6 animate-in fade-in slide-in-from-bottom-2 duration-500`}>
    <div className="flex gap-4 max-w-[80%]">
      {!isUser && (
        <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-red-600 to-black border border-red-500/20 flex items-center justify-center shrink-0 text-lg">
          🔥
        </div>
      )}
      <div className="min-w-0">
        <div className="flex items-center gap-2 mb-1">
          <span className={`text-[10px] font-bold uppercase ${isUser ? 'text-red-500 text-right w-full' : 'text-gray-400'}`}>
            {isUser ? 'YOU' : 'JOANNA AI'} <span className="text-gray-700 mx-1">{timestamp}</span>
          </span>
        </div>
        <div className={`p-4 rounded-2xl text-sm font-medium leading-relaxed shadow-2xl ${isUser
          ? 'bg-red-950/20 border border-red-500/20 text-red-100'
          : 'bg-[#111] border border-white/5 text-gray-300'
          }`}>
          <div className="whitespace-pre-wrap">{text}</div>

          {/* RENDERIZADO DE ACCIONES TÁCTICAS */}
          {!isUser && acciones && acciones.length > 0 && (
            <div className="mt-4 space-y-2 border-t border-white/5 pt-4">
              <div className="flex items-center gap-2 mb-3">
                <div className="w-1.5 h-1.5 bg-red-500 rounded-full animate-pulse"></div>
                <div className="text-[10px] font-black text-red-500 uppercase tracking-widest">Protocolos de Acción Propuestos</div>
              </div>
              {acciones.map((action, idx) => (
                <div key={idx} className="bg-black/40 border border-white/5 rounded-xl p-3 flex items-center justify-between group hover:border-red-500/30 transition-all backdrop-blur-sm">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-lg bg-red-950/20 border border-red-500/10 flex items-center justify-center text-xl shadow-inner">
                      {action.type === 'run_agent' ? '🕵️‍♂️' : action.type === 'create_cron' ? '⏰' : '🔧'}
                    </div>
                    <div>
                      <div className="text-[10px] font-black text-white uppercase tracking-tighter">
                        {action.type === 'run_agent' ? `Desplegar ${action.agent}` :
                          action.type === 'create_cron' ? `Agendar: ${action.data?.name}` :
                            `Misión: ${action.description || 'Reparación Proyectada'}`}
                      </div>
                      <div className="text-[11px] text-gray-500 font-mono">
                        {action.params?.target || action.data?.schedule || `Etapa ${action.etapa || 'Beta'}`}
                      </div>
                    </div>
                  </div>
                  <button className="px-3 py-1.5 bg-red-600/10 border border-red-500/30 rounded-lg text-[9px] font-black text-red-500 uppercase hover:bg-red-600 hover:text-white hover:border-red-600 transition-all shadow-lg active:scale-95">
                    Autorizar
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
      {isUser && (
        <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-cyan-600 to-blue-900 border border-cyan-500/20 flex items-center justify-center shrink-0 text-lg">
          🌊
        </div>
      )}
    </div>
  </div>
);

// === VISTAS ===
const ChatView = ({ messages, isProcessing, onSendMessage, scrollRef, volume, setVolume }) => {
  const [input, setInput] = useState("");
  const [recording, setRecording] = useState(false);
  const [audioLevel, setAudioLevel] = useState(0);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const audioContextRef = useRef(null);
  const analyserRef = useRef(null);
  const animationFrameRef = useRef(null);

  const handleSend = () => {
    if (!input.trim()) return;
    onSendMessage(input);
    setInput("");
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      audioChunksRef.current = [];

      // Configurar analizador de audio para visualización
      audioContextRef.current = new (window.AudioContext || window.webkitAudioContext)();
      analyserRef.current = audioContextRef.current.createAnalyser();
      const source = audioContextRef.current.createMediaStreamSource(stream);
      source.connect(analyserRef.current);
      analyserRef.current.fftSize = 256;

      const bufferLength = analyserRef.current.frequencyBinCount;
      const dataArray = new Uint8Array(bufferLength);

      const updateLevel = () => {
        analyserRef.current.getByteFrequencyData(dataArray);
        const average = dataArray.reduce((a, b) => a + b) / bufferLength;
        setAudioLevel(Math.min(100, (average / 255) * 100));
        animationFrameRef.current = requestAnimationFrame(updateLevel);
      };
      updateLevel();

      mediaRecorderRef.current.ondataavailable = (e) => {
        audioChunksRef.current.push(e.data);
      };

      mediaRecorderRef.current.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        const reader = new FileReader();
        reader.onload = () => {
          const base64 = reader.result.split(',')[1];
          // ENVIAR AUDIO REAL AL BACKEND
          onSendMessage(base64, 'audio');
        };
        reader.readAsDataURL(audioBlob);
        stream.getTracks().forEach(track => track.stop());
        if (animationFrameRef.current) {
          cancelAnimationFrame(animationFrameRef.current);
        }
        setAudioLevel(0);
      };

      mediaRecorderRef.current.start();
      setRecording(true);
    } catch (error) {
      console.error('Error accessing microphone:', error);
      alert('No se pudo acceder al micrófono. Verifica los permisos.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && recording) {
      mediaRecorderRef.current.stop();
      setRecording(false);
    }
  };

  return (
    <div className="flex flex-col h-full">
      <div className="p-6 border-b border-white/5 bg-[#050505]/50 backdrop-blur-md">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-bold text-white">CHAT</h2>
            <div className="text-[10px] text-gray-500 font-mono">GATEWAY ACTIVE SESSION • ID: 8X-2991</div>
          </div>
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2 bg-[#0a0a0a] border border-white/10 rounded-lg px-3 py-2">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="text-gray-500">
                <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5" />
                <path d="M15.54 8.46a5 5 0 0 1 0 7.07" />
              </svg>
              <input
                type="range"
                min="0"
                max="100"
                value={volume}
                onChange={(e) => setVolume(e.target.value)}
                className="w-20 h-1 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-red-500"
              />
              <span className="text-xs font-mono text-gray-400 w-8">{volume}%</span>
            </div>
          </div>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-8 space-y-6">
        {messages.map((msg, idx) => <ChatMessage key={idx} {...msg} />)}
        {isProcessing && (
          <div className="flex justify-start">
            <div className="flex gap-4 items-center">
              <div className="w-8 h-8 rounded-lg bg-red-600/10 border border-red-500/20 flex items-center justify-center">
                <div className="w-1 h-4 bg-red-500 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
                <div className="w-1 h-4 bg-red-500 rounded-full animate-bounce [animation-delay:-0.15s] mx-1"></div>
                <div className="w-1 h-4 bg-red-500 rounded-full animate-bounce"></div>
              </div>
              <span className="text-[10px] text-red-500 font-bold uppercase tracking-[0.2em] animate-pulse">JOANNA ANALIZANDO ESTRATEGIA...</span>
            </div>
          </div>
        )}
        <div ref={scrollRef} />
      </div>

      <div className="p-6 bg-[#050505] border-t border-white/5 space-y-3">
        {/* Visualizador de audio cuando está grabando */}
        {recording && (
          <div className="bg-red-950/20 border border-red-500/30 rounded-xl p-4">
            <div className="flex items-center gap-3 mb-2">
              <div className="w-3 h-3 bg-red-500 rounded-full animate-pulse"></div>
              <span className="text-xs font-bold text-red-400 uppercase tracking-wider">Recording...</span>
            </div>
            <div className="flex items-center gap-1 h-8">
              {[...Array(40)].map((_, i) => (
                <div
                  key={i}
                  className="flex-1 bg-red-500/30 rounded-full transition-all duration-75"
                  style={{
                    height: `${Math.max(4, (audioLevel / 100) * 32 * (0.5 + Math.random() * 0.5))}px`
                  }}
                ></div>
              ))}
            </div>
          </div>
        )}

        <div className="flex items-center gap-3">
          <div className="flex-1 flex items-center gap-3 p-2 bg-[#0a0a0a] border border-white/10 rounded-2xl focus-within:border-red-500/50 transition-all">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && handleSend()}
              className="flex-1 bg-transparent text-sm font-medium text-white placeholder:text-gray-700 outline-none px-4"
              placeholder="Message (⏎ to send, Shift+⏎ for line breaks)"
              disabled={recording}
            />
            <button
              onClick={handleSend}
              disabled={recording}
              className="px-6 py-2 bg-red-600 hover:bg-red-500 disabled:bg-gray-700 disabled:cursor-not-allowed text-white text-xs font-bold rounded-lg transition-all"
            >
              Send →
            </button>
          </div>

          {/* Controles de audio */}
          <div className="flex items-center gap-2">
            {!recording ? (
              <button
                onClick={startRecording}
                className="w-12 h-12 bg-gradient-to-br from-red-600 to-red-700 hover:from-red-500 hover:to-red-600 rounded-xl flex items-center justify-center transition-all hover:scale-105 active:scale-95 shadow-lg shadow-red-500/20"
                title="Start Recording"
              >
                <svg width="20" height="20" viewBox="0 0 24 24" fill="white">
                  <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z" />
                  <path d="M19 10v2a7 7 0 0 1-14 0v-2" stroke="white" strokeWidth="2" fill="none" />
                  <line x1="12" y1="19" x2="12" y2="23" stroke="white" strokeWidth="2" />
                  <line x1="8" y1="23" x2="16" y2="23" stroke="white" strokeWidth="2" />
                </svg>
              </button>
            ) : (
              <button
                onClick={stopRecording}
                className="w-12 h-12 bg-gradient-to-br from-gray-700 to-gray-800 hover:from-gray-600 hover:to-gray-700 rounded-xl flex items-center justify-center transition-all hover:scale-105 active:scale-95 shadow-lg"
                title="Stop Recording"
              >
                <div className="w-4 h-4 bg-white rounded-sm"></div>
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

const OverviewView = ({ agents, sessions, skills }) => {
  const [memStats, setMemStats] = useState({ docs: 0, status: 'offline' });

  useEffect(() => {
    fetch("http://localhost:9300/api/memory/stats").then(r => r.json()).then(setMemStats);
  }, []);

  return (
    <div className="p-8 space-y-8 overflow-y-auto h-full scrollbar-hide">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-black text-white tracking-tighter italic">COMMAND CENTER <span className="text-red-500">1000X</span></h2>
          <p className="text-xs text-gray-500 font-mono mt-1">Status: Operational Swarm // Socio: Neil Ortega</p>
        </div>
        <div className="flex gap-2">
          <div className="px-4 py-2 bg-red-600/10 border border-red-500/20 rounded-xl flex items-center gap-2">
            <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></div>
            <span className="text-[10px] font-black text-red-500 uppercase tracking-widest">Live Link</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard icon={<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" /></svg>} label="Network Entities" value={agents.length} trend={+180} color="red" />
        <StatCard icon={<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M21 12V7H5a2 2 0 0 1 0-4h14v4" /><path d="M3 5v14a2 2 0 0 0 2 2h16v-5" /><path d="M18 12a2 2 0 0 0 0 4h4v-4Z" /></svg>} label="Neural Knowledge" value={memStats.docs} trend={5} color="cyan" />
        <StatCard icon={<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="10" /><polyline points="12 6 12 12 16 14" /></svg>} label="Uptime Guardian" value="1000%" trend={0} color="blue" />
        <StatCard icon={<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><line x1="12" y1="1" x2="12" y2="23" /><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" /></svg>} label="Operational Skills" value={skills.length} trend={+20} color="green" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-6">
          <h3 className="text-lg font-black text-white flex items-center gap-2 italic uppercase">
            <div className="w-1.5 h-6 bg-red-600"></div>
            Tactical Swarm Divisions
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {['LEADS SNIPER', 'SCRAPER ULTRA', 'BLUE OCEANS', 'MICRO SAAS GEN', 'CODER 10000X', 'MECHANIC 24/7'].map(cat => (
              <div key={cat} className="bg-[#0a0a0a] border border-white/5 rounded-2xl p-4 flex items-center justify-between hover:border-red-500/20 transition-all group cursor-pointer">
                <div>
                  <div className="text-[10px] font-black text-gray-500 group-hover:text-red-500 transition-colors uppercase tracking-[0.2em]">{cat}</div>
                  <div className="text-lg font-black text-white italic">30 Sub-Entidades</div>
                </div>
                <div className="w-8 h-8 rounded-full border border-white/5 flex items-center justify-center text-xs group-hover:border-red-500/30 transition-all">→</div>
              </div>
            ))}
          </div>
        </div>

        <div className="space-y-6">
          <h3 className="text-lg font-black text-white flex items-center gap-2 italic uppercase">
            <div className="w-1.5 h-6 bg-cyan-500"></div>
            Recent Mission Logs
          </h3>
          <div className="space-y-3">
            {sessions.slice(0, 4).map(s => (
              <div key={s.id} className="bg-black/50 border-l-2 border-cyan-500 rounded-r-xl p-4 hover:bg-cyan-500/5 transition-all">
                <div className="text-[9px] font-mono text-cyan-500 mb-1 uppercase italic">{new Date(s.timestamp).toLocaleTimeString()}</div>
                <div className="text-xs text-gray-400 font-medium line-clamp-1 italic">"{s.preview}"</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

const SkillsView = ({ skills }) => (
  <div className="p-8 overflow-y-auto h-full">
    <h2 className="text-2xl font-black text-white mb-6">Master Skills Repository</h2>
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {skills.map((skill, idx) => (
        <div key={idx} className="bg-[#0a0a0a] border border-white/5 rounded-2xl p-5 hover:border-red-500/30 transition-all group backdrop-blur-md">
          <div className="flex items-center justify-between mb-3">
            <span className="font-black text-sm text-white group-hover:text-red-500 transition-colors uppercase italic">{skill.name}</span>
            <div className={`px-2 py-0.5 rounded text-[8px] font-black ${skill.active ? 'bg-green-500/10 text-green-500 border border-green-500/20' : 'bg-gray-800 text-gray-500'}`}>
              {skill.active ? 'ENABLED' : 'LOCKED'}
            </div>
          </div>
          <p className="text-[10px] text-gray-500 font-mono tracking-widest">{skill.category}</p>
        </div>
      ))}
    </div>
  </div>
);

const CronView = ({ cronJobs }) => (
  <div className="p-8 overflow-y-auto h-full">
    <h2 className="text-2xl font-black text-white mb-6">Global Scheduler (The Bunker)</h2>
    <div className="space-y-4">
      {cronJobs.map(job => (
        <div key={job.id} className="bg-[#0a0a0a] border border-white/5 rounded-2xl p-5 flex items-center justify-between hover:border-cyan-500/30 transition-all group">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-xl bg-cyan-950/20 border border-cyan-500/10 flex items-center justify-center text-xl">⏰</div>
            <div>
              <div className="font-black text-white group-hover:text-cyan-400 transition-colors">{job.name}</div>
              <div className="text-[10px] text-gray-500 font-mono uppercase tracking-widest">{job.schedule}</div>
            </div>
          </div>
          <div className="text-right">
            <div className="text-[10px] text-gray-400 font-bold mb-1 italic">NEXT: {job.nextRun}</div>
            <span className={`px-3 py-1 rounded-lg text-[9px] font-black ${job.status === 'active' ? 'bg-green-500/10 text-green-500 border border-green-500/20' : 'bg-gray-800 text-gray-500 border border-white/5'}`}>
              {job.status.toUpperCase()}
            </span>
          </div>
        </div>
      ))}
    </div>
  </div>
);

const AgentsSwarmView = ({ agents }) => {
  const [filter, setFilter] = useState('');
  const [category, setCategory] = useState('ALL');

  const categories = ['ALL', ...new Set(agents.map(a => a.category))];
  const filtered = agents.filter(a =>
    (category === 'ALL' || a.category === category) &&
    (a.name.toLowerCase().includes(filter.toLowerCase()) || a.description.toLowerCase().includes(filter.toLowerCase()))
  );

  return (
    <div className="p-8 overflow-y-auto h-full space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-black text-white italic tracking-tighter uppercase">The Swarm <span className="text-red-500">(180 Agents)</span></h2>
          <p className="text-[10px] text-gray-500 font-mono uppercase">Unidad Especial de Operaciones Autónomas</p>
        </div>
        <div className="flex gap-2">
          <input
            type="text"
            placeholder="Search Signal..."
            className="bg-black border border-white/10 rounded-xl px-4 py-2 text-xs focus:border-red-500 outline-none transition-all w-64"
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
          />
          <select
            className="bg-black border border-white/10 rounded-xl px-4 py-2 text-xs focus:border-red-500 outline-none transition-all"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
          >
            {categories.map(c => <option key={c} value={c}>{c}</option>)}
          </select>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filtered.map((agent, idx) => (
          <div key={idx} className="bg-[#0a0a0a] border border-white/5 rounded-2xl p-5 hover:border-red-500/30 transition-all group backdrop-blur-md relative overflow-hidden">
            <div className="absolute top-0 right-0 w-24 h-24 bg-red-500/5 blur-3xl -mr-12 -mt-12"></div>
            <div className="flex items-center justify-between mb-4 relative z-10">
              <div className="flex items-center gap-3">
                <div className={`w-2.5 h-2.5 rounded-full ${agent.status === 'active' ? 'bg-green-500 animate-pulse' : 'bg-red-900/40 border border-red-500/20'}`}></div>
                <span className="font-black text-sm text-white group-hover:text-red-500 transition-colors uppercase italic tracking-tighter">{agent.name}</span>
              </div>
              <span className="text-[9px] font-black text-gray-600 uppercase tracking-widest">{agent.category}</span>
            </div>
            <p className="text-xs text-gray-500 mb-6 leading-relaxed relative z-10">{agent.description}</p>
            <div className="flex items-center justify-between pt-4 border-t border-white/5 relative z-10">
              <div className="flex flex-col">
                <span className="text-[8px] text-gray-700 font-black uppercase">Last Pulse</span>
                <span className="text-[10px] text-gray-400 font-mono">{agent.lastRun}</span>
              </div>
              <button className="bg-red-600/10 border border-red-500/30 rounded-lg px-3 py-1 text-[9px] font-black text-red-500 hover:bg-red-500 hover:text-white transition-all">DELEGATE</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

const SessionsView = ({ sessions }) => (
  <div className="p-8 overflow-y-auto h-full">
    <h2 className="text-2xl font-black text-white mb-6">Tactical Mission Logs (Sessions)</h2>
    <div className="space-y-3">
      {sessions.length === 0 ? (
        <div className="text-gray-600 italic">No hay registros de misiones aún, socio. Iniciando Swarm...</div>
      ) : (
        sessions.map(s => (
          <div key={s.id} className="bg-[#0a0a0a] border border-white/5 rounded-xl p-4 hover:border-red-500/30 transition-all cursor-pointer group">
            <div className="flex justify-between items-center mb-2">
              <span className="text-[10px] font-mono text-gray-500 uppercase tracking-widest">{new Date(s.timestamp).toLocaleString()}</span>
              <div className="w-1.5 h-1.5 bg-red-500 rounded-full group-hover:animate-ping"></div>
            </div>
            <p className="text-sm text-gray-300 line-clamp-2 italic">"{s.preview}"</p>
          </div>
        ))
      )}
    </div>
  </div>
);

const RevenueView = ({ revenue }) => (
  <div className="p-8 overflow-y-auto h-full scrollbar-hide">
    <div className="flex items-center justify-between mb-8">
      <div>
        <h2 className="text-3xl font-black text-white tracking-tighter italic">MONEY MACHINE <span className="text-green-500">1000X</span></h2>
        <p className="text-xs text-gray-500 font-mono mt-1 uppercase tracking-widest">Automatic Revenue Agency (AAA) Mode</p>
      </div>
      <div className="flex gap-4">
        <div className="bg-green-950/20 border border-green-500/20 rounded-2xl p-4 flex items-center gap-4">
          <div className="text-2xl font-black text-green-500 italic">${revenue.total_revenue?.toLocaleString()}</div>
          <div className="text-[10px] font-black text-gray-500 uppercase">Gross Profit</div>
        </div>
      </div>
    </div>

    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <StatCard icon={<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" /></svg>} label="Monthly Recurring (MRR)" value={`$${revenue.monthly_recurring?.toLocaleString()}`} trend={+15} color="green" />
      <StatCard icon={<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" /><circle cx="9" cy="7" r="4" /><path d="M22 21v-2a4 4 0 0 0-3-3.87" /><path d="M16 3.13a4 4 0 0 1 0 7.75" /></svg>} label="Clients Closed" value={revenue.leads_closed} trend={+8} color="cyan" />
      <StatCard icon={<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18" /><polyline points="17 6 23 6 23 12" /></svg>} label="Conv. Rate" value={revenue.conversion_rate} trend={+2} color="red" />
    </div>

    <div className="bg-[#0a0a0a] border border-white/5 rounded-3xl p-8 backdrop-blur-xl">
      <h3 className="text-lg font-black text-white mb-6 italic uppercase flex items-center gap-3">
        <div className="w-1.5 h-6 bg-green-500 shadow-[0_0_15px_rgba(34,197,94,0.5)]"></div>
        Automatic ROI Stream
      </h3>
      <div className="h-64 flex items-end gap-2 px-2">
        {revenue.history?.map((val, i) => (
          <div key={i} className="flex-1 bg-gradient-to-t from-green-900/40 to-green-500/20 border-t border-green-500/30 rounded-t-lg group relative" style={{ height: `${(val / 8000) * 100}%` }}>
            <div className="absolute -top-8 left-1/2 -translate-x-1/2 bg-black border border-green-500/50 text-[10px] font-black text-green-500 px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity">
              ${val.toLocaleString()}
            </div>
          </div>
        ))}
      </div>
      <div className="flex justify-between mt-4 text-[10px] font-black text-gray-700 uppercase tracking-widest px-2">
        <span>Aug</span><span>Sep</span><span>Oct</span><span>Nov</span><span>Dec</span><span>Jan</span>
      </div>
    </div>
  </div>
);

const ServiceCard = ({ name, port, status, description, metrics }) => (
  <div className="bg-[#0a0a0a] border border-white/5 rounded-2xl p-6 hover:border-red-500/30 transition-all">
    <div className="flex items-start justify-between mb-4">
      <div className="flex items-center gap-3">
        <div className={`w-3 h-3 rounded-full ${status === 'online' ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`}></div>
        <div>
          <h3 className="font-bold text-lg text-white">{name}</h3>
          <p className="text-xs text-gray-500 font-mono">Port: {port}</p>
        </div>
      </div>
      <span className={`px-3 py-1 rounded-full text-[10px] font-bold ${status === 'online' ? 'bg-green-950/30 text-green-500' : 'bg-red-950/30 text-red-500'}`}>
        {status.toUpperCase()}
      </span>
    </div>
    <p className="text-sm text-gray-400 mb-4">{description}</p>
    {metrics && (
      <div className="grid grid-cols-2 gap-3">
        {Object.entries(metrics).map(([key, value]) => (
          <div key={key} className="bg-black/30 rounded-lg p-3">
            <div className="text-xs text-gray-500 uppercase tracking-wider mb-1">{key}</div>
            <div className="text-lg font-bold text-white">{value}</div>
          </div>
        ))}
      </div>
    )}
  </div>
);

const ServicesView = ({ sessions }) => {
  const [systemStats, setSystemStats] = React.useState({
    cpu: "0%", memory: "0%", disk: "0%", uptime: "0", status: "offline"
  });

  React.useEffect(() => {
    const fetchStats = async () => {
      try {
        const resp = await fetch("http://localhost:9300/api/system/stats");
        if (resp.ok) {
          const data = await resp.json();
          setSystemStats(data);
        }
      } catch (e) {
        console.error("Error fetching stats:", e);
      }
    };
    fetchStats();
    const interval = setInterval(fetchStats, 5000);
    return () => clearInterval(interval);
  }, []);

  const [services, setServices] = React.useState([
    {
      name: "🧠 Ollama (Cerebro Local)",
      port: "11434",
      status: "online",
      description: "Motor de inferencia para Qwen, DeepSeek y Coder. Procesa el razonamiento táctico.",
      metrics: { "Models": "4 Active", "Latency": "15ms" }
    },
    {
      name: "🛡️ HF-Proxy (LiteLLM)",
      port: "4000",
      status: "online",
      description: "Puerta de enlace inteligente y seguridad de modelos.",
      metrics: { "Throughput": "85 req/s", "Auth": "Master Key" }
    },
    {
      name: "🚀 NeilChat Backend",
      port: "9300",
      status: "online",
      description: "Núcleo de Joanna. Gestiona el Swarm, RAG y orquestación multicanal.",
      metrics: { "Sessions": sessions.length, "Uptime": "1000%" }
    },
    {
      name: "️ Redis (Memoria Flash)",
      port: "6379",
      status: "online",
      description: "Caché de alta velocidad para estados de agentes y colas de tareas.",
      metrics: { "System": "Redis 7.0", "Persistence": "AOF" }
    },
    {
      name: "👁️ ChromaDB (Memoria RAG)",
      port: "8000",
      status: "online",
      description: "Base de datos vectorial. Conocimiento de largo plazo y contexto semántico.",
      metrics: { "Documents": "10K+", "Accuracy": "99%" }
    },
    {
      name: "📱 Evolution API (WhatsApp)",
      port: "8080",
      status: "online",
      description: "Puente de comunicación con el socio Neil Ortega.",
      metrics: { "Instances": "1", "Status": "Connected" }
    }
  ]);

  React.useEffect(() => {
    setServices(prev => prev.map(s => {
      if (s.name.includes("NeilChat Backend")) return { ...s, status: systemStats.status, metrics: { "CPU": systemStats.cpu, "RAM": systemStats.memory, "Sessions": sessions.length } };
      if (s.name.includes("ChromaDB")) return { ...s, metrics: { "Storage": systemStats.disk, "Collection": "joanna_brain" } };
      return s;
    }));
  }, [systemStats, sessions]);

  return (
    <div className="p-8 space-y-8">
      <div>
        <h2 className="text-2xl font-black text-white mb-2">Services Monitor</h2>
        <p className="text-sm text-gray-500">Estado en tiempo real de todos los servicios del sistema</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {services.map((service, idx) => (
          <ServiceCard key={idx} {...service} />
        ))}
      </div>

      <div className="bg-[#0a0a0a] border border-white/5 rounded-2xl p-6">
        <h3 className="text-lg font-black text-white mb-4">System Health</h3>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="text-center">
            <div className="text-3xl font-black text-green-500 mb-1">100%</div>
            <div className="text-xs text-gray-500 uppercase tracking-wider">Services Online</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-black text-cyan-400 mb-1">2.1K</div>
            <div className="text-xs text-gray-500 uppercase tracking-wider">Total Requests</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-black text-blue-400 mb-1">45ms</div>
            <div className="text-xs text-gray-500 uppercase tracking-wider">Avg Response</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-black text-purple-400 mb-1">99.9%</div>
            <div className="text-xs text-gray-500 uppercase tracking-wider">Uptime</div>
          </div>
        </div>
      </div>
    </div>
  );
};

// === APP PRINCIPAL ===
export default function App() {
  const [activeTab, setActiveTab] = useState('Overview');
  const [messages, setMessages] = useState([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [socket, setSocket] = useState(null);
  const [agentes, setAgentes] = useState([]);
  const [skills, setSkills] = useState([]);
  const [cronJobs, setCronJobs] = useState([]);
  const [sessions, setSessions] = useState([]);
  const [revenue, setRevenue] = useState({});
  const scrollRef = useRef();

  useEffect(() => {
    // Cargar datos reales
    const refreshData = () => {
      fetch("http://localhost:9300/api/agents").then(r => r.json()).then(d => setAgentes(d.agents || []));
      fetch("http://localhost:9300/api/skills").then(r => r.json()).then(d => setSkills(d.skills || []));
      fetch("http://localhost:9300/api/cron").then(r => r.json()).then(d => setCronJobs(d.jobs || []));
      fetch("http://localhost:9300/api/sessions").then(r => r.json()).then(d => setSessions(d.sessions || []));
      fetch("http://localhost:9300/api/revenue").then(r => r.json()).then(d => setRevenue(d || {}));
    };

    refreshData();
    const interval = setInterval(refreshData, 10000); // Auto-refresh cada 10s

    const ws = new WebSocket(WS_JOANNA);
    ws.onopen = () => {
      console.log('🔴 GATEWAY CONNECTED');
      setMessages(prev => [...prev, { text: "🔥 ¡Hola socio! Soy Joanna, tu ejecutiva personal. Conectando con los sistemas de ClawZeneger... 🚀", isUser: false, timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) }]);
    };
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        if (data.type === 'partial_response') {
          // STREAMING: Actualizar el último mensaje si es de Joanna
          setIsProcessing(false);
          setMessages(prev => {
            const lastMsg = prev[prev.length - 1];
            if (lastMsg && !lastMsg.isUser && !lastMsg.isFinal) {
              const newMessages = [...prev];
              newMessages[newMessages.length - 1] = {
                ...lastMsg,
                text: lastMsg.text + data.text
              };
              return newMessages;
            } else {
              return [...prev, {
                text: data.text,
                isUser: false,
                isFinal: false,
                timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
              }];
            }
          });
        }
        else if (data.type === 'response') {
          setIsProcessing(false);
          setMessages(prev => {
            // Reemplazar el mensaje parcial con el final si existe, o añadir nuevo
            const lastMsg = prev[prev.length - 1];
            const updatedMsg = {
              text: data.text,
              isUser: false,
              isFinal: true,
              acciones: data.acciones || [],
              timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
            };

            if (lastMsg && !lastMsg.isUser && !lastMsg.isFinal) {
              const newMessages = [...prev];
              newMessages[newMessages.length - 1] = updatedMsg;
              return newMessages;
            }
            return [...prev, updatedMsg];
          });

          // REPRODUCIR AUDIO SI VIENE INCLUIDO
          if (data.audio) {
            const audio = new Audio("data:audio/wav;base64," + data.audio);
            audio.volume = window.currentVolume / 100 || 0.8;
            audio.play().catch(e => console.error("Error playing response audio:", e));
          }

          if (data.acciones && data.acciones.length > 0) {
            console.log("🔥 Joanna ha solicitado misiones tácticas:", data.acciones);
          }
        }
        else if (data.type === 'audio') {
          // REPRODUCIR AUDIO REIBIDO
          const audio = new Audio("data:audio/wav;base64," + data.data);
          // Obtener el volumen actual desde el estado (necesitamos acceder al valor actual)
          // Usaremos una referencia para el volumen para que el callback del socket lo vea siempre actualizado
          audio.volume = window.currentVolume / 100 || 0.8;
          audio.play().catch(e => console.error("Error playing audio:", e));
        }
      } catch (e) {
        console.error('Error parsing message:', e);
      }
    };
    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      setIsProcessing(false);
    };
    setSocket(ws);
    return () => ws.close();
  }, []);

  // Referencia para el volumen para que el closure del useEffect lo vea
  const [volume, setVolume] = useState(80);
  useEffect(() => {
    window.currentVolume = volume;
  }, [volume]);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = (content, type = 'text') => {
    if (!socket || socket.readyState !== WebSocket.OPEN) {
      setMessages(prev => [...prev, {
        text: "⚠️ Conexión perdida. Recargando...",
        isUser: false,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }]);
      return;
    }

    if (type === 'text') {
      setMessages(prev => [...prev, {
        text: content,
        isUser: true,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }]);
      socket.send(JSON.stringify({ type: 'text', content }));
    } else if (type === 'audio') {
      // No agregamos el audio al chat visual aún o usamos un placeholder
      setMessages(prev => [...prev, {
        text: "🎤 [Audio message]",
        isUser: true,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }]);
      socket.send(JSON.stringify({ type: 'audio', data: content }));
    }

    setIsProcessing(true);
  };

  return (
    <BrowserRouter>
      <div className="flex h-screen bg-[#020202] text-white font-sans overflow-hidden">

        <aside className="w-64 bg-[#050505] border-r border-white/5 flex flex-col">
          <div className="p-6 flex items-center gap-3 mb-4">
            <div className="w-10 h-10 bg-gradient-to-br from-red-600 to-black rounded-xl flex items-center justify-center">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="white"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" /></svg>
            </div>
            <div>
              <h1 className="font-black text-sm tracking-tighter text-white">CLAWBOT</h1>
              <div className="text-[9px] font-bold text-gray-600 uppercase">Gateway Dashboard</div>
            </div>
          </div>

          <div className="flex-1 overflow-y-auto px-3">
            <div className="px-4 mt-2 mb-2 text-[10px] font-black text-gray-700 uppercase">CHAT</div>
            <SidebarItem icon={<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" /></svg>} label="Chat" active={activeTab === 'Chat'} onClick={() => setActiveTab('Chat')} />
            <SidebarItem icon={<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 20h9M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z" /></svg>} label="Sessions history" active={activeTab === 'Sessions'} onClick={() => setActiveTab('Sessions')} badge={sessions.length} />

            <div className="px-4 mt-6 mb-2 text-[10px] font-black text-gray-700 uppercase">WEALTH</div>
            <SidebarItem icon={<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><line x1="12" y1="1" x2="12" y2="23" /><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" /></svg>} label="Money Machine" active={activeTab === 'Money'} onClick={() => setActiveTab('Money')} badge={`$${(revenue.total_revenue / 1000).toFixed(1)}k`} />

            <div className="px-4 mt-6 mb-2 text-[10px] font-black text-gray-700 uppercase">CONTROL</div>
            <SidebarItem icon={<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M3 3v18h18" /><path d="M18.7 8l-5.1 5.2-2.8-2.7L7 14.3" /></svg>} label="Overview Hub" active={activeTab === 'Overview'} onClick={() => setActiveTab('Overview')} />
            <SidebarItem icon={<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" /></svg>} label="The Swarm (180)" active={activeTab === 'Swarm'} onClick={() => setActiveTab('Swarm')} badge={agentes.length} />
            <SidebarItem icon={<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" /></svg>} label="Services" active={activeTab === 'Services'} onClick={() => setActiveTab('Services')} badge="4" />
            <SidebarItem icon={<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="10" /><polyline points="12 6 12 12 16 14" /></svg>} label="Cron Jobs" active={activeTab === 'Cron Jobs'} onClick={() => setActiveTab('Cron Jobs')} badge={cronJobs.length} />

            <div className="px-4 mt-6 mb-2 text-[10px] font-black text-gray-700 uppercase">AGENT</div>
            <SidebarItem icon={<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" /></svg>} label="Skills" active={activeTab === 'Skills'} onClick={() => setActiveTab('Skills')} badge={skills.length} />
          </div>

          <div className="p-4 border-t border-white/5">
            <div className="flex items-center gap-3 p-2 rounded-xl hover:bg-white/5 cursor-pointer">
              <div className="w-8 h-8 rounded-full bg-red-600 flex items-center justify-center font-bold text-xs">A</div>
              <div>
                <div className="text-xs font-bold text-white">The Architect</div>
                <div className="text-[10px] text-gray-500">Super Admin</div>
              </div>
            </div>
          </div>
        </aside>

        <main className="flex-1 overflow-hidden relative flex flex-col">
          <div className="flex-1 overflow-y-auto">
            {activeTab === 'Chat' && <ChatView messages={messages} isProcessing={isProcessing} scrollRef={scrollRef} onSendMessage={handleSendMessage} volume={volume} setVolume={setVolume} />}
            {activeTab === 'Overview' && <OverviewView agents={agentes} sessions={sessions} skills={skills} />}
            {activeTab === 'Sessions' && <SessionsView sessions={sessions} />}
            {activeTab === 'Swarm' && <AgentsSwarmView agents={agentes} />}
            {activeTab === 'Money' && <RevenueView revenue={revenue} />}
            {activeTab === 'Services' && <ServicesView sessions={sessions} />}
            {activeTab === 'Skills' && <SkillsView skills={skills} />}
            {activeTab === 'Cron Jobs' && <CronView cronJobs={cronJobs} />}
          </div>
        </main>
      </div>
    </BrowserRouter>
  );
}

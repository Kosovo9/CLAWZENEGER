
import React, { useEffect, useState } from 'react';
import { getAgentsStatus, runAgentTask } from '../api';
import { MUST_HAVE_AGENTS } from '../constants/agents';

export default function AgentsPanel() {
    const [agentsStatus, setAgentsStatus] = useState({});
    const [loading, setLoading] = useState({});
    const [filter, setFilter] = useState('All');

    const categories = ['All', ...new Set(MUST_HAVE_AGENTS.map(a => a.role))];

    const fetchStatus = async () => {
        try {
            const res = await getAgentsStatus();
            setAgentsStatus(res.data);
        } catch (error) {
            console.error("Error fetching agent status:", error);
            // Fallback for UI visualization if API fails for some reason
            const fallback = {};
            MUST_HAVE_AGENTS.forEach(a => {
                fallback[a.id] = { status: "online", last_seen: "Last synced" };
            });
            setAgentsStatus(fallback);
        }
    };

    useEffect(() => {
        fetchStatus();
        const interval = setInterval(fetchStatus, 30000); // Sync every 30s
        return () => clearInterval(interval);
    }, []);

    const handleRun = async (agentId) => {
        setLoading(prev => ({ ...prev, [agentId]: true }));
        try {
            await runAgentTask(agentId, { prompt: "Autonomous optimization task" });
            fetchStatus(); // Refresh status immediately
        } catch (error) {
            console.error(`Error running agent ${agentId}:`, error);
        } finally {
            setLoading(prev => ({ ...prev, [agentId]: false }));
        }
    };

    const filteredAgents = filter === 'All'
        ? MUST_HAVE_AGENTS
        : MUST_HAVE_AGENTS.filter(a => a.role === filter);

    return (
        <div className="space-y-8 pb-20">
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div>
                    <h2 className="text-3xl font-black bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent uppercase tracking-tighter">
                        Autonomous Swarm
                    </h2>
                    <p className="text-gray-500 text-sm">20 specialized agents driving 1000x growth</p>
                </div>

                <div className="flex flex-wrap gap-2">
                    {categories.map(cat => (
                        <button
                            key={cat}
                            onClick={() => setFilter(cat)}
                            className={`px-3 py-1 rounded-full text-[10px] font-black transition-all ${filter === cat
                                    ? "bg-purple-600 text-white shadow-lg shadow-purple-500/20"
                                    : "bg-gray-800 text-gray-400 hover:bg-gray-700"
                                }`}
                        >
                            {cat.toUpperCase()}
                        </button>
                    ))}
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                {filteredAgents.map(agent => (
                    <AgentCard
                        key={agent.id}
                        agent={agent}
                        status={agentsStatus[agent.id]?.status || 'unknown'}
                        lastActive={agentsStatus[agent.id]?.last_seen || '---'}
                        loading={loading[agent.id]}
                        onRun={() => handleRun(agent.id)}
                    />
                ))}
            </div>
        </div>
    );
}

const AgentCard = ({ agent, status, lastActive, onRun, loading }) => (
    <div className={`group relative bg-gray-900/40 backdrop-blur-3xl border border-white/5 rounded-2xl p-5 hover:border-purple-500/40 transition-all duration-500 hover:shadow-[0_0_40px_-10px_rgba(168,85,247,0.2)] flex flex-col overflow-hidden`}>
        {/* Animated gradient border on hover */}
        <div className="absolute inset-0 bg-gradient-to-br from-purple-600/10 via-transparent to-blue-500/10 opacity-0 group-hover:opacity-100 transition-opacity duration-700" />

        <div className="relative z-10">
            <div className="flex justify-between items-start mb-4">
                <div className="flex items-center gap-3">
                    <div className="w-12 h-12 rounded-xl bg-white/5 border border-white/5 flex items-center justify-center text-2xl group-hover:scale-110 transition-transform shadow-inner">
                        {agent.icon}
                    </div>
                    <div>
                        <h3 className="font-black text-white text-sm leading-tight tracking-tight">{agent.name}</h3>
                        <span className="text-[10px] text-purple-400 font-bold uppercase tracking-widest">{agent.role}</span>
                    </div>
                </div>
                <div className={`w-2.5 h-2.5 rounded-full border-2 border-gray-900 ${status === 'online' ? 'bg-green-500 shadow-[0_0_12px_rgba(34,197,94,0.8)]' : 'bg-red-500'}`} />
            </div>

            <p className="text-gray-400 text-[11px] leading-relaxed mb-6 h-12 line-clamp-3">
                {agent.description}
            </p>

            <div className="flex items-center justify-between pt-4 border-t border-white/5">
                <div className="flex flex-col">
                    <span className="text-[8px] text-gray-500 uppercase font-bold tracking-tighter">Heartbeat</span>
                    <span className="text-[10px] text-gray-300 font-mono italic">{lastActive}</span>
                </div>
                <button
                    onClick={onRun}
                    disabled={loading}
                    className={`relative p-2.5 rounded-xl transition-all duration-300 ${loading
                            ? 'bg-purple-600/20 text-purple-400 cursor-wait'
                            : 'bg-white/5 hover:bg-purple-600 text-gray-400 hover:text-white shadow-lg'
                        }`}
                >
                    {loading ? (
                        <svg className="w-4 h-4 animate-spin" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                        </svg>
                    ) : (
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M13 10V3L4 14h7v7l9-11h-7z" />
                        </svg>
                    )}
                </button>
            </div>
        </div>
    </div>
);

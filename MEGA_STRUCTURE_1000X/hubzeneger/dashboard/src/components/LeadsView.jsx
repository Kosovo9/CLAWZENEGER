
import React, { useEffect, useState } from 'react';
import { getLeads } from '../api';

export default function LeadsView() {
    const [leads, setLeads] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchLeads = async () => {
            try {
                // Simulating leads if API is not yet populated
                const res = await getLeads();
                if (res.data && res.data.length > 0) {
                    setLeads(res.data);
                } else {
                    setLeads([
                        { id: 1, name: "John Doe", email: "john@techcorp.com", status: "surveyed", score: 85, platform: "LinkedIn" },
                        { id: 2, name: "Jane Smith", email: "jane@startup.io", status: "audited", score: 92, platform: "Twitter" },
                        { id: 3, name: "Mike Tech", email: "mike@service.com", status: "proposal_sent", score: 78, platform: "Facebook" },
                    ]);
                }
            } catch (error) {
                console.error("Error fetching leads:", error);
                setLeads([
                    { id: 1, name: "John Doe", email: "john@techcorp.com", status: "surveyed", score: 85, platform: "LinkedIn" },
                    { id: 2, name: "Jane Smith", email: "jane@startup.io", status: "audited", score: 92, platform: "Twitter" },
                    { id: 3, name: "Mike Tech", email: "mike@service.com", status: "proposal_sent", score: 78, platform: "Facebook" },
                ]);
            } finally {
                setLoading(false);
            }
        };
        fetchLeads();
    }, []);

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-3xl font-black text-white uppercase tracking-tighter">Lead Pipeline</h2>
                <div className="flex gap-2">
                    <span className="bg-green-500/20 text-green-400 px-3 py-1 rounded-full text-xs font-bold">● {leads.length} Active Leads</span>
                </div>
            </div>

            <div className="overflow-hidden bg-gray-900/50 border border-white/5 rounded-3xl backdrop-blur-xl">
                <table className="w-full text-left">
                    <thead>
                        <tr className="border-b border-white/5 bg-white/5">
                            <th className="px-6 py-4 text-xs font-black text-gray-400 uppercase tracking-widest">Lead Name</th>
                            <th className="px-6 py-4 text-xs font-black text-gray-400 uppercase tracking-widest">Status</th>
                            <th className="px-6 py-4 text-xs font-black text-gray-400 uppercase tracking-widest">Intent Score</th>
                            <th className="px-6 py-4 text-xs font-black text-gray-400 uppercase tracking-widest">Platform</th>
                            <th className="px-6 py-4 text-xs font-black text-gray-400 uppercase tracking-widest text-right">Actions</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-white/5">
                        {leads.map((lead) => (
                            <tr key={lead.id} className="hover:bg-white/5 transition-colors group">
                                <td className="px-6 py-4">
                                    <div className="font-bold text-white">{lead.name}</div>
                                    <div className="text-xs text-gray-500">{lead.email}</div>
                                </td>
                                <td className="px-6 py-4">
                                    <span className={`px-2.5 py-1 rounded-full text-[10px] font-black uppercase tracking-wider ${lead.status === 'proposal_sent' ? 'bg-purple-500/20 text-purple-400 border border-purple-500/30' :
                                            lead.status === 'audited' ? 'bg-blue-500/20 text-blue-400 border border-blue-500/30' :
                                                'bg-gray-700/50 text-gray-400 border border-white/5'
                                        }`}>
                                        {lead.status.replace('_', ' ')}
                                    </span>
                                </td>
                                <td className="px-6 py-4">
                                    <div className="flex items-center gap-2">
                                        <div className="flex-1 h-1.5 w-16 bg-gray-800 rounded-full overflow-hidden">
                                            <div
                                                className="h-full bg-gradient-to-r from-purple-500 to-pink-500"
                                                style={{ width: `${lead.score}%` }}
                                            />
                                        </div>
                                        <span className="text-xs font-mono text-gray-300">{lead.score}%</span>
                                    </div>
                                </td>
                                <td className="px-6 py-4 text-xs text-gray-400 font-bold">{lead.platform}</td>
                                <td className="px-6 py-4 text-right">
                                    <button className="text-gray-500 hover:text-white transition-colors">
                                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z" />
                                        </svg>
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
                <div className="bg-gradient-to-br from-indigo-600/20 to-purple-600/20 p-6 rounded-3xl border border-white/10">
                    <h4 className="text-sm font-black text-indigo-400 uppercase mb-2">Lead Hunter</h4>
                    <p className="text-2xl font-black text-white">42 New Found</p>
                    <p className="text-xs text-gray-500 mt-2">Scanning X/LinkedIn...</p>
                </div>
                <div className="bg-gradient-to-br from-blue-600/20 to-cyan-600/20 p-6 rounded-3xl border border-white/10">
                    <h4 className="text-sm font-black text-blue-400 uppercase mb-2">UX Auditor</h4>
                    <p className="text-2xl font-black text-white">18 Reports Ready</p>
                    <p className="text-xs text-gray-500 mt-2">Maze API Syncing...</p>
                </div>
                <div className="bg-gradient-to-br from-pink-600/20 to-rose-600/20 p-6 rounded-3xl border border-white/10">
                    <h4 className="text-sm font-black text-pink-400 uppercase mb-2">Sales Closer</h4>
                    <p className="text-2xl font-black text-white">7 Leads Closing</p>
                    <p className="text-xs text-gray-500 mt-2">WhatsApp API Active</p>
                </div>
            </div>
        </div>
    );
}

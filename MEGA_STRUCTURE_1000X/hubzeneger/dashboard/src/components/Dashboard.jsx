
import React, { useEffect, useState } from 'react';
import { getStats } from '../api';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function Dashboard() {
    const [stats, setStats] = useState({
        revenue_mtd: 0,
        active_funnels: 0,
        leads_today: 0,
        agents_active: 0
    });

    useEffect(() => {
        // Simular carga o conectar real
        // getStats().then(res => setStats(res.data)).catch(console.error);

        // Datos dummy para visualización inmediata
        setStats({
            revenue_mtd: 12450,
            active_funnels: 5,
            leads_today: 42,
            agents_active: 4
        });
    }, []);

    const chartData = [
        { name: 'Mon', leads: 40 },
        { name: 'Tue', leads: 30 },
        { name: 'Wed', leads: 55 },
        { name: 'Thu', leads: 80 },
        { name: 'Fri', leads: 65 },
        { name: 'Sat', leads: 90 },
        { name: 'Sun', leads: 120 },
    ];

    return (
        <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <StatCard title="Revenue MTD" value={`$${stats.revenue_mtd.toLocaleString()}`} change="+12%" color="text-green-400" />
                <StatCard title="Active Leads Today" value={stats.leads_today} change="+24%" color="text-blue-400" />
                <StatCard title="Active Funnels" value={stats.active_funnels} change="Stable" color="text-purple-400" />
                <StatCard title="Agents Online" value={`${stats.agents_active}/4`} change="100% Uptime" color="text-yellow-400" />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="bg-gray-800 p-6 rounded-xl border border-gray-700">
                    <h3 className="text-lg font-medium mb-4">Lead Growth</h3>
                    <div className="h-64 w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <LineChart data={chartData}>
                                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                                <XAxis dataKey="name" stroke="#9CA3AF" />
                                <YAxis stroke="#9CA3AF" />
                                <Tooltip contentStyle={{ backgroundColor: '#1F2937', border: 'none' }} />
                                <Line type="monotone" dataKey="leads" stroke="#8B5CF6" strokeWidth={3} dot={{ r: 4 }} />
                            </LineChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                <div className="bg-gray-800 p-6 rounded-xl border border-gray-700">
                    <h3 className="text-lg font-medium mb-4">Recent Activity</h3>
                    <div className="space-y-4">
                        <ActivityItem icon="💰" text="New sale from 'Webinar Funnel'" time="2m ago" />
                        <ActivityItem icon="🤖" text="Agent 'Market Researcher' finished daily scan" time="15m ago" />
                        <ActivityItem icon="📩" text="Lead 'John Doe' opened email #3" time="1h ago" />
                        <ActivityItem icon="🔧" text="Mechanic optimized Redis cache" time="2h ago" />
                    </div>
                </div>
            </div>
        </div>
    );
}

const StatCard = ({ title, value, change, color }) => (
    <div className="bg-gray-800 p-6 rounded-xl border border-gray-700">
        <p className="text-gray-400 text-sm">{title}</p>
        <div className="flex items-baseline justify-between mt-2">
            <h3 className="text-3xl font-bold">{value}</h3>
            <span className={`text-sm ${color}`}>{change}</span>
        </div>
    </div>
);

const ActivityItem = ({ icon, text, time }) => (
    <div className="flex items-center justify-between border-b border-gray-700 pb-3 last:border-0 last:pb-0">
        <div className="flex items-center space-x-3">
            <div className="w-8 h-8 rounded-full bg-gray-700 flex items-center justify-center text-lg">{icon}</div>
            <p className="text-gray-300 text-sm">{text}</p>
        </div>
        <span className="text-xs text-gray-500">{time}</span>
    </div>
);

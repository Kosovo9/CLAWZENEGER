import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
    Users,
    DollarSign,
    TrendingUp,
    Clock,
    Copy,
    ChevronRight,
    LogOut,
    Wallet
} from 'lucide-react';
import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    Tooltip,
    ResponsiveContainer,
    CartesianGrid
} from 'recharts';
import toast, { Toaster } from 'react-hot-toast';

const API_URL = "http://localhost:9200/api/v1";

export default function AffiliateDashboard() {
    const [stats, setStats] = useState({
        referrals_count: 0,
        conversions: 0,
        total_earned: 0,
        available_balance: 0,
        pending_balance: 0,
        referral_link: ""
    });
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchStats();
    }, []);

    const fetchStats = async () => {
        try {
            // En una implementación real, aquí va el token
            const res = await axios.get(`${API_URL}/affiliates/stats`);
            setStats(res.data);
        } catch (err) {
            console.error(err);
            toast.error("Error cargando estadísticas");
        } finally {
            setLoading(false);
        }
    };

    const copyLink = () => {
        navigator.clipboard.writeText(stats.referral_link);
        toast.success("Enlace copiado!");
    };

    if (loading) return <div className="h-screen flex items-center justify-center bg-[#0a0f1d] text-white">Cargando Sistema de Afiliados...</div>;

    return (
        <div className="min-h-screen bg-[#0a0f1d] text-white font-sans p-4 md:p-8">
            <Toaster />

            {/* Header */}
            <div className="flex justify-between items-center mb-12">
                <div>
                    <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
                        Clawzeneger Affiliates
                    </h1>
                    <p className="text-gray-400 mt-1">Gana el 30% por cada referido exitoso</p>
                </div>
                <button className="flex items-center gap-2 bg-gray-800/50 px-4 py-2 rounded-lg border border-gray-700 hover:bg-gray-700 transition">
                    <LogOut size={18} /> Salir
                </button>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">

                {/* Main Stats */}
                <div className="lg:col-span-2 space-y-8">

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <StatCard title="Ganancias Totales" value={`$${stats.total_earned}`} icon={<DollarSign className="text-green-400" />} />
                        <StatCard title="Referidos" value={stats.referrals_count} icon={<Users className="text-blue-400" />} />
                        <StatCard title="Conversiones" value={stats.conversions} icon={<TrendingUp className="text-purple-400" />} />
                    </div>

                    <div className="bg-gray-900/50 p-6 rounded-2xl border border-gray-800 backdrop-blur-xl">
                        <h2 className="text-xl font-semibold mb-6">Rendimiento Histórico</h2>
                        <div className="h-[300px]">
                            <ResponsiveContainer width="100%" height="100%">
                                <LineChart data={mockChartData}>
                                    <CartesianGrid strokeDasharray="3 3" stroke="#2d3748" vertical={false} />
                                    <XAxis dataKey="name" stroke="#718096" />
                                    <YAxis stroke="#718096" />
                                    <Tooltip
                                        contentStyle={{ backgroundColor: '#1a202c', border: 'none', borderRadius: '8px' }}
                                        itemStyle={{ color: '#fff' }}
                                    />
                                    <Line type="monotone" dataKey="clics" stroke="#3182ce" strokeWidth={3} dot={false} />
                                    <Line type="monotone" dataKey="ventas" stroke="#805ad5" strokeWidth={3} dot={false} />
                                </LineChart>
                            </ResponsiveContainer>
                        </div>
                    </div>
                </div>

                {/* Sidebar */}
                <div className="space-y-8">

                    {/* Referral Link */}
                    <div className="bg-gradient-to-br from-blue-600/20 to-purple-600/20 p-6 rounded-2xl border border-blue-500/30">
                        <h3 className="text-lg font-bold mb-4">Tu Enlace de Socio</h3>
                        <div className="flex gap-2 bg-[#0a0f1d] p-3 rounded-xl border border-gray-700">
                            <input
                                type="text"
                                readOnly
                                value={stats.referral_link}
                                className="bg-transparent text-sm w-full outline-none text-gray-300"
                            />
                            <button onClick={copyLink} className="text-blue-400 hover:text-blue-300 transition">
                                <Copy size={20} />
                            </button>
                        </div>
                    </div>

                    {/* Wallet */}
                    <div className="bg-gray-900/50 p-6 rounded-2xl border border-gray-800">
                        <div className="flex items-center justify-between mb-6">
                            <h3 className="text-lg font-bold">Billetera</h3>
                            <Wallet className="text-gray-500" />
                        </div>

                        <div className="space-y-4">
                            <div className="flex justify-between items-center text-sm">
                                <span className="text-gray-400">Disponible</span>
                                <span className="font-bold text-green-400">${stats.available_balance}</span>
                            </div>
                            <div className="flex justify-between items-center text-sm">
                                <span className="text-gray-400">En espera</span>
                                <span className="font-bold text-orange-400">${stats.pending_balance}</span>
                            </div>
                            <hr className="border-gray-800" />
                            <button
                                className="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-3 rounded-xl transition shadow-lg shadow-blue-600/20 flex items-center justify-center gap-2"
                                onClick={() => toast("Opción de retiro disponible pronto")}
                            >
                                Retirar Fondos <ChevronRight size={18} />
                            </button>
                        </div>
                    </div>

                </div>

            </div>
        </div>
    );
}

function StatCard({ title, value, icon }) {
    return (
        <div className="bg-gray-900/50 p-6 rounded-2xl border border-gray-800 hover:border-gray-700 transition group">
            <div className="flex items-center gap-4">
                <div className="p-3 bg-gray-800 rounded-xl group-hover:scale-110 transition-transform">
                    {icon}
                </div>
                <div>
                    <p className="text-gray-400 text-sm font-medium">{title}</p>
                    <p className="text-2xl font-bold">{value}</p>
                </div>
            </div>
        </div>
    );
}

const mockChartData = [
    { name: 'Lun', clics: 40, ventas: 24 },
    { name: 'Mar', clics: 30, ventas: 13 },
    { name: 'Mie', clics: 20, ventas: 98 },
    { name: 'Jue', clics: 27, ventas: 39 },
    { name: 'Vie', clics: 18, ventas: 48 },
    { name: 'Sab', clics: 23, ventas: 38 },
    { name: 'Dom', clics: 34, ventas: 43 },
];

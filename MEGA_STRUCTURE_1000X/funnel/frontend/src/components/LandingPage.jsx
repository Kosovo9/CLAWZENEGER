
import React, { useState } from 'react';

const LandingPage = () => {
    const [email, setEmail] = useState('');
    const [isSubmitted, setIsSubmitted] = useState(false);

    const handleSubmit = (e) => {
        e.preventDefault();
        // Here you would connect to backend API
        console.log("Lead captured:", email);
        setIsSubmitted(true);
        setTimeout(() => setIsSubmitted(false), 3000);
    };

    return (
        <div className="min-h-screen bg-[#0f172a] text-white font-['Outfit'] overflow-hidden relative">

            {/* Background Gradients */}
            <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] bg-purple-600/30 rounded-full blur-[120px] pointer-events-none"></div>
            <div className="absolute bottom-[-20%] right-[-10%] w-[50%] h-[50%] bg-blue-600/30 rounded-full blur-[120px] pointer-events-none"></div>

            {/* Header */}
            <nav className="relative z-10 flex justify-between items-center px-10 py-6 glass sticky top-0">
                <div className="text-2xl font-bold tracking-tighter">
                    CLAW<span className="text-purple-500">ZENEGER</span>
                </div>
                <div className="hidden md:flex space-x-8">
                    <a href="#features" className="hover:text-purple-400 transition">Features</a>
                    <a href="#demo" className="hover:text-purple-400 transition">Live Demo</a>
                    <a href="#pricing" className="hover:text-purple-400 transition">Pricing</a>
                </div>
                <button className="bg-white/10 hover:bg-white/20 border border-white/20 px-6 py-2 rounded-full transition">
                    Login
                </button>
            </nav>

            {/* Hero Section */}
            <header className="relative z-10 container mx-auto px-6 py-20 flex flex-col md:flex-row items-center">
                <div className="md:w-1/2 text-center md:text-left mb-16 md:mb-0">
                    <div className="inline-block px-4 py-1 mb-6 rounded-full bg-purple-500/10 border border-purple-500/50 text-purple-400 text-sm font-semibold tracking-wide">
                        🚀 AI SALES AUTOMATION V2.0
                    </div>
                    <h1 className="text-5xl md:text-7xl font-bold leading-tight mb-6">
                        Turn Leads Into <br />
                        <span className="text-gradient">Revenue on Autopilot</span>
                    </h1>
                    <p className="text-xl text-gray-300 mb-8 max-w-lg mx-auto md:mx-0">
                        The world's first AI-powered funnel builder that clones your best sales rep and works 24/7. No coding required.
                    </p>

                    <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-4 max-w-md mx-auto md:mx-0">
                        <input
                            type="email"
                            placeholder="Enter your work email"
                            className="flex-1 px-6 py-4 rounded-xl bg-white/5 border border-white/10 focus:border-purple-500 focus:outline-none focus:ring-2 focus:ring-purple-500/50 transition"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                        <button type="submit" className="btn-primary px-8 py-4 rounded-xl font-bold text-lg whitespace-nowrap">
                            {isSubmitted ? "Access Granted ✅" : "Start Free Trial"}
                        </button>
                    </form>
                    <p className="mt-4 text-sm text-gray-500">No credit card required • 14-day free trial</p>
                </div>

                <div className="md:w-1/2 relative">
                    <div className="glass-card p-6 rounded-3xl animate-float">
                        <div className="flex items-center justify-between mb-6 border-b border-white/10 pb-4">
                            <div className="flex gap-2">
                                <div className="w-3 h-3 rounded-full bg-red-500"></div>
                                <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
                                <div className="w-3 h-3 rounded-full bg-green-500"></div>
                            </div>
                            <div className="text-sm text-gray-400">Nexovbot Automation Dashboard</div>
                        </div>
                        <div className="space-y-4">
                            <div className="flex items-center gap-4 p-4 rounded-xl bg-white/5 border border-white/5 hover:border-purple-500/50 transition cursor-pointer">
                                <div className="w-12 h-12 rounded-full bg-blue-500/20 flex items-center justify-center text-blue-400 text-xl">🤖</div>
                                <div>
                                    <h3 className="font-semibold">Lead Qualified: John Doe</h3>
                                    <p className="text-xs text-green-400">Score: 98/100 • Ready to Buy</p>
                                </div>
                                <div className="ml-auto text-sm text-gray-400">Just now</div>
                            </div>
                            <div className="flex items-center gap-4 p-4 rounded-xl bg-white/5 border border-white/5 hover:border-purple-500/50 transition cursor-pointer">
                                <div className="w-12 h-12 rounded-full bg-purple-500/20 flex items-center justify-center text-purple-400 text-xl">💬</div>
                                <div>
                                    <h3 className="font-semibold">WhatsApp Auto-Reply Sent</h3>
                                    <p className="text-xs text-gray-400">Offer: Premium Package (20% OFF)</p>
                                </div>
                                <div className="ml-auto text-sm text-gray-400">2m ago</div>
                            </div>
                            <div className="flex items-center gap-4 p-4 rounded-xl bg-white/5 border border-white/5 hover:border-purple-500/50 transition cursor-pointer">
                                <div className="w-12 h-12 rounded-full bg-green-500/20 flex items-center justify-center text-green-400 text-xl">💰</div>
                                <div>
                                    <h3 className="font-semibold">Payment Received: $997.00</h3>
                                    <p className="text-xs text-gray-400">Stripe • Recurring Subscription</p>
                                </div>
                                <div className="ml-auto text-sm text-gray-400">15m ago</div>
                            </div>
                        </div>
                    </div>

                    {/* Stats Floating Card */}
                    <div className="absolute -bottom-10 -left-10 glass p-6 rounded-2xl animate-pulse">
                        <div className="text-sm text-gray-400 mb-1">Today's Revenue</div>
                        <div className="text-3xl font-bold text-green-400">$4,250.00</div>
                        <div className="text-xs text-green-500 mt-1">▲ 12% vs yesterday</div>
                    </div>
                </div>
            </header>

            {/* Features Grid */}
            <section id="features" className="py-20 bg-black/20">
                <div className="container mx-auto px-6">
                    <div className="text-center mb-16">
                        <h2 className="text-3xl md:text-5xl font-bold mb-4">God Mode Features</h2>
                        <p className="text-gray-400 max-w-2xl mx-auto">Everything you need to dominate your market, built into one powerful dashboard.</p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                        {[
                            { icon: "🧠", title: "Autonomous AI Agents", desc: "Agents that research, sell, and support 24/7 without sleep." },
                            { icon: "🌪️", title: "Smart Funnels", desc: "Drag-and-drop builder that predicts user behavior and optimizes conversion." },
                            { icon: "🕵️", title: "Deep Market Scraping", desc: "Find blue ocean niches and trends before your competitors do." }
                        ].map((feature, idx) => (
                            <div key={idx} className="glass p-8 rounded-3xl hover:bg-white/5 transition duration-300">
                                <div className="text-4xl mb-6">{feature.icon}</div>
                                <h3 className="text-2xl font-bold mb-3">{feature.title}</h3>
                                <p className="text-gray-400 leading-relaxed">{feature.desc}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* Footer */}
            <footer className="py-10 border-t border-white/10 text-center text-gray-500 text-sm">
                <p>&copy; 2026 Clawzeneger Inc. All rights reserved.</p>
            </footer>
        </div>
    );
};

export default LandingPage;

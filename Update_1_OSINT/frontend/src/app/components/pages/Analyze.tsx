import { useState } from 'react';
import { Search, Download, FileText, AlertTriangle, Shield, TrendingUp, Sparkles } from 'lucide-react';
import { PieChart, Pie, Cell, ResponsiveContainer } from 'recharts';

const mockAnalysisResult = {
    ip: '192.168.1.100',
    threatLevel: 'High',
    threatScore: 78,
    threatType: 'Malicious Activity Detected',
    recommendation: 'Block this IP address immediately and investigate associated traffic for potential compromise.',
    details: {
        country: 'Russia',
        isp: 'Example ISP',
        asn: 'AS12345',
        openPorts: [
            { port: 22, service: 'SSH', risk: 'High' },
            { port: 80, service: 'HTTP', risk: 'Medium' },
            { port: 443, service: 'HTTPS', risk: 'Medium' },
            { port: 3389, service: 'RDP', risk: 'Critical' },
        ],
    },
};

const scoreData = [
    { name: 'Threat', value: 78, color: '#ef4444' },
    { name: 'Safe', value: 22, color: '#1e293b' },
];

export function Analyze() {
    const [searchValue, setSearchValue] = useState('');
    const [showResult, setShowResult] = useState(false);

    const handleAnalyze = () => {
        if (searchValue) {
            setShowResult(true);
        }
    };

    const getThreatColor = (level: string) => {
        switch (level) {
            case 'High':
            case 'Critical':
                return 'cyber-red';
            case 'Medium':
                return 'cyber-orange';
            case 'Low':
                return 'cyber-green';
            default:
                return 'cyber-blue';
        }
    };

    return (
        <div className="space-y-6">
            {/* Page Title */}
            <div>
                <h1 className="text-3xl bg-gradient-to-r from-[var(--cyber-blue)] to-[var(--cyber-purple)] bg-clip-text text-transparent">
                    IP & Domain Analysis
                </h1>
                <p className="text-muted-foreground mt-1">Analyze IP addresses and domains for threat intelligence</p>
            </div>

            {/* Search Bar */}
            <div className="glass-card rounded-xl p-6">
                <div className="flex gap-3">
                    <div className="flex-1 relative">
                        <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
                        <input
                            type="text"
                            placeholder="Enter IP address or domain (e.g., 192.168.1.100 or example.com)"
                            value={searchValue}
                            onChange={(e) => setSearchValue(e.target.value)}
                            onKeyDown={(e) => e.key === 'Enter' && handleAnalyze()}
                            className="w-full pl-12 pr-4 py-3 bg-white/5 border border-border/50 rounded-lg text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-[var(--cyber-blue)] focus:border-transparent"
                        />
                    </div>
                    <button
                        onClick={handleAnalyze}
                        className="px-6 py-3 bg-gradient-to-r from-[var(--cyber-blue)] to-[var(--cyber-purple)] text-white rounded-lg hover:shadow-lg hover:shadow-[var(--cyber-blue)]/50 transition-all"
                    >
                        Analyze
                    </button>
                </div>
            </div>

            {/* Results */}
            {showResult && (
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    {/* Left Column - Analysis Result */}
                    <div className="lg:col-span-2 space-y-6">
                        {/* Main Result Card */}
                        <div className="glass-card rounded-xl p-6 border border-border/50">
                            <div className="flex items-start justify-between mb-6">
                                <div>
                                    <h2 className="text-xl text-foreground mb-2">Analysis Result</h2>
                                    <p className="text-sm text-muted-foreground">{mockAnalysisResult.ip}</p>
                                </div>
                                <div className="flex gap-2">
                                    <button className="p-2 hover:bg-white/5 rounded-lg transition-colors" title="Export PDF">
                                        <FileText className="w-5 h-5 text-muted-foreground" />
                                    </button>
                                    <button className="p-2 hover:bg-white/5 rounded-lg transition-colors" title="Export Excel">
                                        <Download className="w-5 h-5 text-muted-foreground" />
                                    </button>
                                </div>
                            </div>

                            {/* Threat Level Badge */}
                            <div className="flex items-center gap-3 mb-6">
                                <div className={`px-4 py-2 rounded-lg bg-[var(--${getThreatColor(mockAnalysisResult.threatLevel)})]/20 border border-[var(--${getThreatColor(mockAnalysisResult.threatLevel)})]/50 flex items-center gap-2`}>
                                    <AlertTriangle className={`w-5 h-5 text-[var(--${getThreatColor(mockAnalysisResult.threatLevel)})]`} />
                                    <span className={`text-[var(--${getThreatColor(mockAnalysisResult.threatLevel)})]`}>
                                        {mockAnalysisResult.threatLevel} Risk
                                    </span>
                                </div>
                                <div className="px-4 py-2 rounded-lg bg-white/5 border border-border/30">
                                    <span className="text-foreground">{mockAnalysisResult.threatType}</span>
                                </div>
                            </div>

                            {/* Recommendation */}
                            <div className="p-4 bg-[var(--cyber-orange)]/10 border border-[var(--cyber-orange)]/30 rounded-lg mb-6">
                                <div className="flex items-start gap-2">
                                    <Shield className="w-5 h-5 text-[var(--cyber-orange)] mt-0.5" />
                                    <div>
                                        <h4 className="text-sm text-[var(--cyber-orange)] mb-1">Recommendation</h4>
                                        <p className="text-sm text-foreground">{mockAnalysisResult.recommendation}</p>
                                    </div>
                                </div>
                            </div>

                            {/* IP Details */}
                            <div className="grid grid-cols-2 gap-4">
                                <div className="p-4 bg-white/5 rounded-lg">
                                    <p className="text-xs text-muted-foreground mb-1">Country</p>
                                    <p className="text-foreground">{mockAnalysisResult.details.country}</p>
                                </div>
                                <div className="p-4 bg-white/5 rounded-lg">
                                    <p className="text-xs text-muted-foreground mb-1">ISP</p>
                                    <p className="text-foreground">{mockAnalysisResult.details.isp}</p>
                                </div>
                                <div className="p-4 bg-white/5 rounded-lg">
                                    <p className="text-xs text-muted-foreground mb-1">ASN</p>
                                    <p className="text-foreground">{mockAnalysisResult.details.asn}</p>
                                </div>
                                <div className="p-4 bg-white/5 rounded-lg">
                                    <p className="text-xs text-muted-foreground mb-1">Open Ports</p>
                                    <p className="text-foreground">{mockAnalysisResult.details.openPorts.length}</p>
                                </div>
                            </div>
                        </div>

                        {/* Open Ports Risk Table */}
                        <div className="glass-card rounded-xl p-6">
                            <h3 className="mb-4 text-foreground">Open Ports Risk Analysis</h3>
                            <div className="overflow-x-auto">
                                <table className="w-full">
                                    <thead>
                                        <tr className="border-b border-border/30">
                                            <th className="text-left py-3 px-4 text-sm text-muted-foreground">Port</th>
                                            <th className="text-left py-3 px-4 text-sm text-muted-foreground">Service</th>
                                            <th className="text-left py-3 px-4 text-sm text-muted-foreground">Risk Level</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {mockAnalysisResult.details.openPorts.map((port, index) => (
                                            <tr key={index} className="border-b border-border/10 hover:bg-white/5 transition-colors">
                                                <td className="py-3 px-4 text-foreground">{port.port}</td>
                                                <td className="py-3 px-4 text-foreground">{port.service}</td>
                                                <td className="py-3 px-4">
                                                    <span className={`px-3 py-1 text-xs rounded-full ${port.risk === 'Critical'
                                                            ? 'bg-[var(--cyber-red)]/20 text-[var(--cyber-red)]'
                                                            : port.risk === 'High'
                                                                ? 'bg-[var(--cyber-orange)]/20 text-[var(--cyber-orange)]'
                                                                : 'bg-[var(--cyber-yellow)]/20 text-[var(--cyber-yellow)]'
                                                        }`}>
                                                        {port.risk}
                                                    </span>
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        </div>

                        {/* AI Threat Explanation */}
                        <div className="glass-card rounded-xl p-6 border border-[var(--cyber-purple)]/50 bg-gradient-to-br from-[var(--cyber-purple)]/5 to-transparent">
                            <div className="flex items-start gap-3">
                                <div className="p-2 bg-[var(--cyber-purple)]/20 rounded-lg">
                                    <Sparkles className="w-5 h-5 text-[var(--cyber-purple)]" />
                                </div>
                                <div className="flex-1">
                                    <h4 className="text-foreground mb-2">AI Threat Explanation</h4>
                                    <p className="text-sm text-muted-foreground leading-relaxed">
                                        This IP address has been flagged for multiple malicious activities including brute-force login attempts,
                                        port scanning, and suspicious C2 (Command & Control) communications. The IP originates from a known
                                        threat actor infrastructure and has been associated with APT campaigns targeting financial institutions.
                                        Immediate action is recommended to prevent potential data exfiltration or lateral movement within your network.
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Right Column - Threat Score */}
                    <div className="space-y-6">
                        <div className="glass-card rounded-xl p-6">
                            <h3 className="mb-4 text-foreground">Threat Score</h3>
                            <div className="h-48 flex items-center justify-center">
                                <ResponsiveContainer width="100%" height="100%">
                                    <PieChart>
                                        <Pie
                                            data={scoreData}
                                            cx="50%"
                                            cy="50%"
                                            innerRadius={50}
                                            outerRadius={70}
                                            startAngle={90}
                                            endAngle={-270}
                                            dataKey="value"
                                        >
                                            {scoreData.map((entry, index) => (
                                                <Cell key={`cell-${index}`} fill={entry.color} />
                                            ))}
                                        </Pie>
                                    </PieChart>
                                </ResponsiveContainer>
                                <div className="absolute">
                                    <div className="text-center">
                                        <div className="text-4xl text-[var(--cyber-red)]">{mockAnalysisResult.threatScore}</div>
                                        <div className="text-xs text-muted-foreground mt-1">/ 100</div>
                                    </div>
                                </div>
                            </div>
                            <div className="mt-6 p-4 bg-white/5 rounded-lg">
                                <div className="flex items-center gap-2 mb-2">
                                    <TrendingUp className="w-4 h-4 text-[var(--cyber-red)]" />
                                    <span className="text-sm text-foreground">Risk Assessment</span>
                                </div>
                                <p className="text-xs text-muted-foreground">
                                    This score indicates a high probability of malicious intent. Take immediate action.
                                </p>
                            </div>
                        </div>

                        {/* Quick Actions */}
                        <div className="glass-card rounded-xl p-6">
                            <h3 className="mb-4 text-foreground">Quick Actions</h3>
                            <div className="space-y-2">
                                <button className="w-full px-4 py-3 bg-[var(--cyber-red)]/20 border border-[var(--cyber-red)]/50 text-[var(--cyber-red)] rounded-lg hover:bg-[var(--cyber-red)]/30 transition-colors">
                                    Block IP Address
                                </button>
                                <button className="w-full px-4 py-3 bg-white/5 border border-border/30 text-foreground rounded-lg hover:bg-white/10 transition-colors">
                                    Add to Watchlist
                                </button>
                                <button className="w-full px-4 py-3 bg-white/5 border border-border/30 text-foreground rounded-lg hover:bg-white/10 transition-colors">
                                    Generate Report
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {/* Empty State */}
            {!showResult && (
                <div className="glass-card rounded-xl p-12 text-center">
                    <div className="w-16 h-16 bg-[var(--cyber-blue)]/10 rounded-full flex items-center justify-center mx-auto mb-4">
                        <Search className="w-8 h-8 text-[var(--cyber-blue)]" />
                    </div>
                    <h3 className="text-xl text-foreground mb-2">Start Your Analysis</h3>
                    <p className="text-muted-foreground">
                        Enter an IP address or domain above to begin threat intelligence analysis
                    </p>
                </div>
            )}
        </div>
    );
}

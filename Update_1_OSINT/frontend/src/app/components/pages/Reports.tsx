import { FileText, Calendar, TrendingUp, Upload, Eye, FileDown, FileSpreadsheet } from 'lucide-react';
import { useState } from 'react';

const summaryData = [
    { label: 'Total Reports', value: '47', icon: FileText, color: 'cyber-blue' },
    { label: 'This Month', value: '12', icon: Calendar, color: 'cyber-purple' },
    { label: 'Critical Findings', value: '23', icon: TrendingUp, color: 'cyber-red' },
];

const reportsData = [
    {
        id: 1,
        title: 'Weekly Threat Intelligence Summary',
        type: 'Weekly Summary',
        date: 'Jan 29, 2026',
        time: '14:30',
        size: '2.4 MB',
        threats: 145,
        status: 'Ready',
    },
    {
        id: 2,
        title: 'Q1 2026 Security Analysis Report',
        type: 'Quarterly Report',
        date: 'Jan 28, 2026',
        time: '09:15',
        size: '5.8 MB',
        threats: 423,
        status: 'Ready',
    },
    {
        id: 3,
        title: 'Incident Response - Malware Campaign',
        type: 'Incident Report',
        date: 'Jan 27, 2026',
        time: '16:45',
        size: '3.2 MB',
        threats: 67,
        status: 'Ready',
    },
    {
        id: 4,
        title: 'Vulnerability Assessment - Jan 2026',
        type: 'Assessment',
        date: 'Jan 26, 2026',
        time: '11:20',
        size: '4.1 MB',
        threats: 89,
        status: 'Ready',
    },
    {
        id: 5,
        title: 'APT29 Campaign Analysis',
        type: 'Threat Actor Report',
        date: 'Jan 25, 2026',
        time: '13:00',
        size: '1.9 MB',
        threats: 34,
        status: 'Ready',
    },
    {
        id: 6,
        title: 'Monthly IOC Summary - December',
        type: 'Monthly IOC',
        date: 'Jan 24, 2026',
        time: '10:30',
        size: '2.7 MB',
        threats: 178,
        status: 'Ready',
    },
];

export function Reports() {
    const [selectedReport, setSelectedReport] = useState<number | null>(null);

    const getTypeColor = (type: string) => {
        if (type.includes('Incident')) return 'bg-[var(--cyber-red)]/20 text-[var(--cyber-red)]';
        if (type.includes('Quarterly')) return 'bg-[var(--cyber-purple)]/20 text-[var(--cyber-purple)]';
        if (type.includes('Weekly')) return 'bg-[var(--cyber-blue)]/20 text-[var(--cyber-blue)]';
        if (type.includes('Threat Actor')) return 'bg-[var(--cyber-orange)]/20 text-[var(--cyber-orange)]';
        return 'bg-[var(--cyber-cyan)]/20 text-[var(--cyber-cyan)]';
    };

    return (
        <div className="space-y-6">
            {/* Page Title */}
            <div>
                <h1 className="text-3xl bg-gradient-to-r from-[var(--cyber-blue)] to-[var(--cyber-purple)] bg-clip-text text-transparent">
                    Reports
                </h1>
                <p className="text-muted-foreground mt-1">Generate and download threat intelligence reports</p>
            </div>

            {/* Summary Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {summaryData.map((item, index) => {
                    const Icon = item.icon;
                    return (
                        <div key={index} className="glass-card rounded-xl p-6 hover:shadow-lg hover:shadow-[var(--cyber-blue)]/10 transition-all">
                            <div className="flex items-center justify-between mb-3">
                                <span className="text-sm text-muted-foreground">{item.label}</span>
                                <div className={`p-2 rounded-lg bg-[var(--${item.color})]/10`}>
                                    <Icon className={`w-5 h-5 text-[var(--${item.color})]`} />
                                </div>
                            </div>
                            <div className="text-3xl text-foreground">{item.value}</div>
                        </div>
                    );
                })}
            </div>

            {/* Generate New Report */}
            <div className="glass-card rounded-xl p-6">
                <div className="flex items-center justify-between">
                    <div>
                        <h3 className="text-foreground mb-1">Generate New Report</h3>
                        <p className="text-sm text-muted-foreground">Create a custom threat intelligence report</p>
                    </div>
                    <button className="px-6 py-3 bg-gradient-to-r from-[var(--cyber-blue)] to-[var(--cyber-purple)] text-white rounded-lg hover:shadow-lg hover:shadow-[var(--cyber-blue)]/50 transition-all">
                        Generate Report
                    </button>
                </div>
            </div>

            {/* Reports List */}
            <div className="glass-card rounded-xl p-6">
                <div className="flex items-center justify-between mb-6">
                    <h3 className="text-foreground">Available Reports</h3>
                    <p className="text-sm text-muted-foreground">
                        {selectedReport ? `Selected: Report #${selectedReport}` : 'No report selected'}
                    </p>
                </div>
                <div className="space-y-4">
                    {reportsData.map((report) => (
                        <div
                            key={report.id}
                            onClick={() => setSelectedReport(report.id)}
                            className={`p-4 bg-white/5 rounded-lg border cursor-pointer transition-all group ${selectedReport === report.id
                                ? 'border-[var(--cyber-blue)] bg-[var(--cyber-blue)]/10 shadow-lg shadow-[var(--cyber-blue)]/20'
                                : 'border-border/30 hover:border-[var(--cyber-blue)]/50'
                                }`}
                        >
                            <div className="flex items-start justify-between gap-4">
                                <div className="flex-1">
                                    <div className="flex items-center gap-3 mb-2">
                                        <div className={`p-2 rounded-lg transition-all ${selectedReport === report.id
                                            ? 'bg-[var(--cyber-blue)]/20'
                                            : 'bg-white/5'
                                            }`}>
                                            <FileText className={`w-5 h-5 ${selectedReport === report.id
                                                ? 'text-[var(--cyber-blue)]'
                                                : 'text-muted-foreground'
                                                }`} />
                                        </div>
                                        <h4 className="text-foreground">{report.title}</h4>
                                    </div>
                                    <div className="flex flex-wrap items-center gap-4 text-sm text-muted-foreground">
                                        <span className={`px-3 py-1 rounded-full text-xs ${getTypeColor(report.type)}`}>
                                            {report.type}
                                        </span>
                                        <span className="flex items-center gap-1">
                                            <Calendar className="w-4 h-4" />
                                            {report.date} at {report.time}
                                        </span>
                                        <span>Size: {report.size}</span>
                                        <span>Threats: {report.threats}</span>
                                    </div>
                                </div>
                                {selectedReport === report.id && (
                                    <div className="flex items-center gap-2 px-3 py-1.5 bg-[var(--cyber-blue)]/20 rounded-lg border border-[var(--cyber-blue)]/30">
                                        <div className="w-2 h-2 bg-[var(--cyber-blue)] rounded-full animate-pulse"></div>
                                        <span className="text-xs text-[var(--cyber-blue)]">Selected</span>
                                    </div>
                                )}
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* Report Actions - Conditional Buttons */}
            <div className="glass-card rounded-xl p-6">
                <div className="mb-4">
                    <h3 className="text-foreground mb-2">Report Actions</h3>
                    <p className="text-sm text-muted-foreground">
                        {selectedReport
                            ? 'Report selected. Choose an action below.'
                            : 'Please select a report from the list above to enable actions.'}
                    </p>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                    {/* View Report Button */}
                    <button
                        disabled={!selectedReport}
                        className={`p-5 rounded-lg border transition-all flex flex-col items-center gap-3 ${selectedReport
                            ? 'bg-white/5 border-[var(--cyber-blue)]/30 hover:border-[var(--cyber-blue)] hover:bg-[var(--cyber-blue)]/10 hover:shadow-lg hover:shadow-[var(--cyber-blue)]/20 cursor-pointer'
                            : 'bg-white/5 border-border/20 opacity-40 cursor-not-allowed'
                            }`}
                    >
                        <div className={`p-3 rounded-lg ${selectedReport
                            ? 'bg-[var(--cyber-blue)]/20'
                            : 'bg-white/5'
                            }`}>
                            <Eye className={`w-6 h-6 ${selectedReport
                                ? 'text-[var(--cyber-blue)]'
                                : 'text-muted-foreground'
                                }`} />
                        </div>
                        <div className="text-center">
                            <div className={`text-sm mb-1 ${selectedReport
                                ? 'text-foreground'
                                : 'text-muted-foreground'
                                }`}>
                                View Report
                            </div>
                            <div className="text-xs text-muted-foreground">
                                Preview in browser
                            </div>
                        </div>
                    </button>

                    {/* Download Report Button */}
                    <button
                        disabled={!selectedReport}
                        className={`p-5 rounded-lg border transition-all flex flex-col items-center gap-3 ${selectedReport
                            ? 'bg-white/5 border-[var(--cyber-purple)]/30 hover:border-[var(--cyber-purple)] hover:bg-[var(--cyber-purple)]/10 hover:shadow-lg hover:shadow-[var(--cyber-purple)]/20 cursor-pointer'
                            : 'bg-white/5 border-border/20 opacity-40 cursor-not-allowed'
                            }`}
                    >
                        <div className={`p-3 rounded-lg ${selectedReport
                            ? 'bg-[var(--cyber-purple)]/20'
                            : 'bg-white/5'
                            }`}>
                            <FileDown className={`w-6 h-6 ${selectedReport
                                ? 'text-[var(--cyber-purple)]'
                                : 'text-muted-foreground'
                                }`} />
                        </div>
                        <div className="text-center">
                            <div className={`text-sm mb-1 ${selectedReport
                                ? 'text-foreground'
                                : 'text-muted-foreground'
                                }`}>
                                Download Report
                            </div>
                            <div className="text-xs text-muted-foreground">
                                Save as PDF
                            </div>
                        </div>
                    </button>

                    {/* Export Report Button */}
                    <button
                        disabled={!selectedReport}
                        className={`p-5 rounded-lg border transition-all flex flex-col items-center gap-3 ${selectedReport
                            ? 'bg-white/5 border-[var(--cyber-cyan)]/30 hover:border-[var(--cyber-cyan)] hover:bg-[var(--cyber-cyan)]/10 hover:shadow-lg hover:shadow-[var(--cyber-cyan)]/20 cursor-pointer'
                            : 'bg-white/5 border-border/20 opacity-40 cursor-not-allowed'
                            }`}
                    >
                        <div className={`p-3 rounded-lg ${selectedReport
                            ? 'bg-[var(--cyber-cyan)]/20'
                            : 'bg-white/5'
                            }`}>
                            <FileSpreadsheet className={`w-6 h-6 ${selectedReport
                                ? 'text-[var(--cyber-cyan)]'
                                : 'text-muted-foreground'
                                }`} />
                        </div>
                        <div className="text-center">
                            <div className={`text-sm mb-1 ${selectedReport
                                ? 'text-foreground'
                                : 'text-muted-foreground'
                                }`}>
                                Export Report
                            </div>
                            <div className="text-xs text-muted-foreground">
                                Export as Excel/CSV
                            </div>
                        </div>
                    </button>
                </div>

                {/* Action Hint */}
                {!selectedReport && (
                    <div className="mt-4 p-4 bg-[var(--cyber-blue)]/5 border border-[var(--cyber-blue)]/20 rounded-lg">
                        <div className="flex items-start gap-3">
                            <div className="p-2 bg-[var(--cyber-blue)]/10 rounded mt-0.5">
                                <Upload className="w-4 h-4 text-[var(--cyber-blue)]" />
                            </div>
                            <div>
                                <h4 className="text-sm text-foreground mb-1">No Report Selected</h4>
                                <p className="text-xs text-muted-foreground leading-relaxed">
                                    Click on any report from the list above to select it. The action buttons will become enabled,
                                    allowing you to view, download, or export the selected report.
                                </p>
                            </div>
                        </div>
                    </div>
                )}
            </div>

            {/* Export Options */}
            <div className="glass-card rounded-xl p-6">
                <h3 className="mb-4 text-foreground">Export All Reports</h3>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                    <button className="p-4 bg-white/5 border border-border/30 rounded-lg hover:border-[var(--cyber-blue)]/50 hover:bg-white/10 transition-all text-center">
                        <FileText className="w-6 h-6 text-[var(--cyber-blue)] mx-auto mb-2" />
                        <span className="text-sm text-foreground">Export as PDF</span>
                    </button>
                    <button className="p-4 bg-white/5 border border-border/30 rounded-lg hover:border-[var(--cyber-green)]/50 hover:bg-white/10 transition-all text-center">
                        <FileText className="w-6 h-6 text-[var(--cyber-green)] mx-auto mb-2" />
                        <span className="text-sm text-foreground">Export as Excel</span>
                    </button>
                    <button className="p-4 bg-white/5 border border-border/30 rounded-lg hover:border-[var(--cyber-purple)]/50 hover:bg-white/10 transition-all text-center">
                        <FileText className="w-6 h-6 text-[var(--cyber-purple)] mx-auto mb-2" />
                        <span className="text-sm text-foreground">Export as CSV</span>
                    </button>
                </div>
            </div>
        </div>
    );
}

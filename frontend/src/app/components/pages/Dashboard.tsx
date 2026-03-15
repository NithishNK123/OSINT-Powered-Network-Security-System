import { TrendingUp, AlertTriangle, Shield, Activity } from 'lucide-react';
import { PieChart, Pie, BarChart, Bar, LineChart, Line, Cell, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

// Mock data
const kpiData = [
  { label: 'Total Scans', value: '1,247', icon: Activity, color: 'cyber-blue' },
  { label: 'High Risk IPs', value: '38', icon: AlertTriangle, color: 'cyber-red' },
  { label: 'Medium Risk', value: '142', icon: TrendingUp, color: 'cyber-orange' },
  { label: 'Low Risk', value: '1,067', icon: Shield, color: 'cyber-green' },
];

const statusData = [
  { name: 'Critical', value: 38, color: '#ef4444' },
  { name: 'High', value: 65, color: '#f59e0b' },
  { name: 'Medium', value: 142, color: '#eab308' },
  { name: 'Low', value: 1067, color: '#10b981' },
];

const countryData = [
  { country: 'China', hosts: 450 },
  { country: 'Russia', hosts: 320 },
  { country: 'USA', hosts: 180 },
  { country: 'Iran', hosts: 95 },
  { country: 'Brazil', hosts: 70 },
];

const severeIssues = [
  { issue: 'CVE-2024-1234: RCE Vulnerability', severity: 'Critical', ip: '192.168.1.100' },
  { issue: 'SQL Injection Detected', severity: 'Critical', ip: '10.0.0.45' },
  { issue: 'Unauthorized Access Attempt', severity: 'High', ip: '172.16.0.33' },
  { issue: 'Malware C2 Communication', severity: 'Critical', ip: '203.0.113.8' },
  { issue: 'DDoS Traffic Pattern', severity: 'High', ip: '198.51.100.22' },
];

const newsData = [
  { title: 'APT29 Targets Government Agencies', time: '2 hours ago' },
  { title: 'New Ransomware Strain Discovered', time: '5 hours ago' },
  { title: 'Zero-Day in Popular CMS', time: '1 day ago' },
  { title: 'Phishing Campaign Using AI', time: '1 day ago' },
];

const reportsData = [
  { title: 'Weekly Threat Summary', date: 'Jan 29, 2026' },
  { title: 'Q1 Security Analysis', date: 'Jan 28, 2026' },
  { title: 'Incident Response Report', date: 'Jan 27, 2026' },
  { title: 'Vulnerability Assessment', date: 'Jan 26, 2026' },
];

const severityTrendData = [
  { month: 'Jul', high: 45, medium: 120, low: 890 },
  { month: 'Aug', high: 52, medium: 135, low: 950 },
  { month: 'Sep', high: 48, medium: 128, low: 920 },
  { month: 'Oct', high: 55, medium: 142, low: 980 },
  { month: 'Nov', high: 42, medium: 138, low: 1010 },
  { month: 'Dec', high: 50, medium: 145, low: 1045 },
  { month: 'Jan', high: 38, medium: 142, low: 1067 },
];

const threatActors = [
  { name: 'APT29 (Cozy Bear)', activity: 'High', campaigns: 12 },
  { name: 'Lazarus Group', activity: 'High', campaigns: 8 },
  { name: 'APT28 (Fancy Bear)', activity: 'Medium', campaigns: 6 },
  { name: 'Carbanak', activity: 'Medium', campaigns: 4 },
];

const ttpsData = [
  { tactic: 'Initial Access - Phishing', occurrences: 145 },
  { tactic: 'Execution - PowerShell', occurrences: 98 },
  { tactic: 'Persistence - Registry', occurrences: 76 },
  { tactic: 'Lateral Movement - RDP', occurrences: 54 },
];

export function Dashboard() {
  return (
    <div className="space-y-6">
      {/* Page Title */}
      <div>
        <h1 className="text-3xl bg-gradient-to-r from-[var(--cyber-blue)] to-[var(--cyber-purple)] bg-clip-text text-transparent">
          Dashboard
        </h1>
        <p className="text-muted-foreground mt-1">Real-time threat intelligence overview</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {kpiData.map((kpi, index) => {
          const Icon = kpi.icon;
          return (
            <div key={index} className="glass-card rounded-xl p-6 hover:shadow-lg hover:shadow-[var(--cyber-blue)]/10 transition-all">
              <div className="flex items-center justify-between mb-3">
                <span className="text-sm text-muted-foreground">{kpi.label}</span>
                <div className={`p-2 rounded-lg bg-[var(--${kpi.color})]/10`}>
                  <Icon className={`w-5 h-5 text-[var(--${kpi.color})]`} />
                </div>
              </div>
              <div className="text-3xl text-foreground">{kpi.value}</div>
            </div>
          );
        })}
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Issues by Status - Donut Chart */}
        <div className="glass-card rounded-xl p-6">
          <h3 className="mb-4 text-foreground">Issues by Status</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={statusData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={80}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {statusData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{
                    backgroundColor: 'rgba(15, 23, 42, 0.95)',
                    border: '1px solid rgba(148, 163, 184, 0.2)',
                    borderRadius: '8px',
                    color: '#e5e7eb',
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="grid grid-cols-2 gap-2 mt-4">
            {statusData.map((item, index) => (
              <div key={index} className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full" style={{ backgroundColor: item.color }}></div>
                <span className="text-sm text-muted-foreground">{item.name}: {item.value}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Hosts by Country - Bar Chart */}
        <div className="glass-card rounded-xl p-6">
          <h3 className="mb-4 text-foreground">Hosts by Country</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={countryData}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(148, 163, 184, 0.1)" />
                <XAxis dataKey="country" stroke="#94a3b8" />
                <YAxis stroke="#94a3b8" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: 'rgba(15, 23, 42, 0.95)',
                    border: '1px solid rgba(148, 163, 184, 0.2)',
                    borderRadius: '8px',
                    color: '#e5e7eb',
                  }}
                />
                <Bar dataKey="hosts" fill="url(#colorGradient)" radius={[8, 8, 0, 0]} />
                <defs>
                  <linearGradient id="colorGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#3b82f6" stopOpacity={0.8} />
                    <stop offset="100%" stopColor="#8b5cf6" stopOpacity={0.8} />
                  </linearGradient>
                </defs>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Most Severe Issues */}
        <div className="glass-card rounded-xl p-6">
          <h3 className="mb-4 text-foreground">Most Severe Issues</h3>
          <div className="space-y-3">
            {severeIssues.map((issue, index) => (
              <div key={index} className="p-3 bg-white/5 rounded-lg border border-border/30 hover:border-[var(--cyber-red)]/50 transition-colors">
                <div className="flex items-start justify-between gap-2">
                  <div className="flex-1">
                    <p className="text-sm text-foreground">{issue.issue}</p>
                    <p className="text-xs text-muted-foreground mt-1">{issue.ip}</p>
                  </div>
                  <span className={`px-2 py-1 text-xs rounded ${
                    issue.severity === 'Critical' 
                      ? 'bg-[var(--cyber-red)]/20 text-[var(--cyber-red)]' 
                      : 'bg-[var(--cyber-orange)]/20 text-[var(--cyber-orange)]'
                  }`}>
                    {issue.severity}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* News Analysis */}
        <div className="glass-card rounded-xl p-6">
          <h3 className="mb-4 text-foreground">Threat News Analysis</h3>
          <div className="space-y-3">
            {newsData.map((news, index) => (
              <div key={index} className="p-3 bg-white/5 rounded-lg border border-border/30 hover:border-[var(--cyber-blue)]/50 transition-colors cursor-pointer">
                <p className="text-sm text-foreground">{news.title}</p>
                <p className="text-xs text-muted-foreground mt-1">{news.time}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Latest Reports */}
        <div className="glass-card rounded-xl p-6">
          <h3 className="mb-4 text-foreground">Latest Reports</h3>
          <div className="space-y-3">
            {reportsData.map((report, index) => (
              <div key={index} className="p-3 bg-white/5 rounded-lg border border-border/30 hover:border-[var(--cyber-purple)]/50 transition-colors cursor-pointer">
                <p className="text-sm text-foreground">{report.title}</p>
                <p className="text-xs text-muted-foreground mt-1">{report.date}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Issues Based on Severity - Line Chart */}
        <div className="glass-card rounded-xl p-6">
          <h3 className="mb-4 text-foreground">Issues Based on Severity</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={severityTrendData}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(148, 163, 184, 0.1)" />
                <XAxis dataKey="month" stroke="#94a3b8" />
                <YAxis stroke="#94a3b8" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: 'rgba(15, 23, 42, 0.95)',
                    border: '1px solid rgba(148, 163, 184, 0.2)',
                    borderRadius: '8px',
                    color: '#e5e7eb',
                  }}
                />
                <Line type="monotone" dataKey="high" stroke="#ef4444" strokeWidth={2} dot={{ fill: '#ef4444' }} />
                <Line type="monotone" dataKey="medium" stroke="#f59e0b" strokeWidth={2} dot={{ fill: '#f59e0b' }} />
                <Line type="monotone" dataKey="low" stroke="#10b981" strokeWidth={2} dot={{ fill: '#10b981' }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* My Top Threats - Actors */}
        <div className="glass-card rounded-xl p-6">
          <h3 className="mb-4 text-foreground">My Top Threats – Actors</h3>
          <div className="space-y-3">
            {threatActors.map((actor, index) => (
              <div key={index} className="p-3 bg-white/5 rounded-lg border border-border/30">
                <div className="flex items-center justify-between mb-1">
                  <p className="text-sm text-foreground">{actor.name}</p>
                  <span className={`px-2 py-1 text-xs rounded ${
                    actor.activity === 'High' 
                      ? 'bg-[var(--cyber-red)]/20 text-[var(--cyber-red)]' 
                      : 'bg-[var(--cyber-orange)]/20 text-[var(--cyber-orange)]'
                  }`}>
                    {actor.activity}
                  </span>
                </div>
                <p className="text-xs text-muted-foreground">{actor.campaigns} active campaigns</p>
              </div>
            ))}
          </div>
        </div>

        {/* My Top Threats - TTPs */}
        <div className="glass-card rounded-xl p-6">
          <h3 className="mb-4 text-foreground">My Top Threats – TTPs</h3>
          <div className="space-y-3">
            {ttpsData.map((ttp, index) => (
              <div key={index} className="p-3 bg-white/5 rounded-lg border border-border/30">
                <div className="flex items-center justify-between mb-2">
                  <p className="text-sm text-foreground">{ttp.tactic}</p>
                  <span className="text-xs text-[var(--cyber-cyan)]">{ttp.occurrences}</span>
                </div>
                <div className="w-full bg-white/10 rounded-full h-2">
                  <div 
                    className="bg-gradient-to-r from-[var(--cyber-blue)] to-[var(--cyber-purple)] h-2 rounded-full"
                    style={{ width: `${(ttp.occurrences / 145) * 100}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

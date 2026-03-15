import { useState } from 'react';
import { Search, Filter } from 'lucide-react';

const historyData = [
  { id: 1, target: '192.168.1.100', type: 'IP', risk: 'High', date: 'Jan 31, 2026 14:23', threats: 8 },
  { id: 2, target: 'malicious-site.com', type: 'Domain', risk: 'Critical', date: 'Jan 31, 2026 13:15', threats: 12 },
  { id: 3, target: '10.0.0.45', type: 'IP', risk: 'Medium', date: 'Jan 31, 2026 11:47', threats: 3 },
  { id: 4, target: '172.16.0.33', type: 'IP', risk: 'Low', date: 'Jan 31, 2026 10:22', threats: 1 },
  { id: 5, target: 'suspicious-domain.net', type: 'Domain', risk: 'High', date: 'Jan 30, 2026 16:55', threats: 6 },
  { id: 6, target: '203.0.113.8', type: 'IP', risk: 'Critical', date: 'Jan 30, 2026 15:30', threats: 15 },
  { id: 7, target: '198.51.100.22', type: 'IP', risk: 'Medium', date: 'Jan 30, 2026 14:12', threats: 4 },
  { id: 8, target: 'phishing-example.org', type: 'Domain', risk: 'High', date: 'Jan 30, 2026 12:05', threats: 7 },
  { id: 9, target: '192.0.2.146', type: 'IP', risk: 'Low', date: 'Jan 30, 2026 09:38', threats: 2 },
  { id: 10, target: '172.31.255.1', type: 'IP', risk: 'Medium', date: 'Jan 29, 2026 18:20', threats: 5 },
];

export function History() {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterRisk, setFilterRisk] = useState('All');

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'Critical':
        return 'bg-[var(--cyber-red)]/20 text-[var(--cyber-red)] border-[var(--cyber-red)]/50';
      case 'High':
        return 'bg-[var(--cyber-orange)]/20 text-[var(--cyber-orange)] border-[var(--cyber-orange)]/50';
      case 'Medium':
        return 'bg-[var(--cyber-yellow)]/20 text-[var(--cyber-yellow)] border-[var(--cyber-yellow)]/50';
      case 'Low':
        return 'bg-[var(--cyber-green)]/20 text-[var(--cyber-green)] border-[var(--cyber-green)]/50';
      default:
        return 'bg-white/5 text-muted-foreground border-border/30';
    }
  };

  const filteredData = historyData.filter((item) => {
    const matchesSearch = item.target.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filterRisk === 'All' || item.risk === filterRisk;
    return matchesSearch && matchesFilter;
  });

  return (
    <div className="space-y-6">
      {/* Page Title */}
      <div>
        <h1 className="text-3xl bg-gradient-to-r from-[var(--cyber-blue)] to-[var(--cyber-purple)] bg-clip-text text-transparent">
          Scan History
        </h1>
        <p className="text-muted-foreground mt-1">View all previous threat intelligence scans</p>
      </div>

      {/* Filters */}
      <div className="glass-card rounded-xl p-6">
        <div className="flex flex-col sm:flex-row gap-4">
          {/* Search */}
          <div className="flex-1 relative">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
            <input
              type="text"
              placeholder="Search by IP or domain..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-12 pr-4 py-3 bg-white/5 border border-border/50 rounded-lg text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-[var(--cyber-blue)] focus:border-transparent"
            />
          </div>

          {/* Risk Level Filter */}
          <div className="relative">
            <Filter className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground pointer-events-none" />
            <select
              value={filterRisk}
              onChange={(e) => setFilterRisk(e.target.value)}
              style={{
                color: 'var(--foreground)',
                backgroundColor: 'var(--input-background)',
              }}
              className="pl-12 pr-8 py-3 border border-border/50 rounded-lg focus:outline-none focus:ring-2 focus:ring-[var(--cyber-blue)] focus:border-transparent appearance-none cursor-pointer transition-all hover:border-[var(--cyber-blue)]/50"
            >
              <option value="All" style={{ backgroundColor: 'var(--input-background)', color: 'var(--foreground)' }}>All Risks</option>
              <option value="Critical" style={{ backgroundColor: 'var(--input-background)', color: 'var(--foreground)' }}>Critical</option>
              <option value="High" style={{ backgroundColor: 'var(--input-background)', color: 'var(--foreground)' }}>High</option>
              <option value="Medium" style={{ backgroundColor: 'var(--input-background)', color: 'var(--foreground)' }}>Medium</option>
              <option value="Low" style={{ backgroundColor: 'var(--input-background)', color: 'var(--foreground)' }}>Low</option>
            </select>
            {/* Custom dropdown arrow */}
            <div className="absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none">
              <svg className="w-4 h-4 text-muted-foreground" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            </div>
          </div>
        </div>
      </div>

      {/* History Table */}
      <div className="glass-card rounded-xl overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-white/5 border-b border-border/30">
              <tr>
                <th className="text-left py-4 px-6 text-sm text-muted-foreground">Target</th>
                <th className="text-left py-4 px-6 text-sm text-muted-foreground">Type</th>
                <th className="text-left py-4 px-6 text-sm text-muted-foreground">Risk Level</th>
                <th className="text-left py-4 px-6 text-sm text-muted-foreground">Threats Found</th>
                <th className="text-left py-4 px-6 text-sm text-muted-foreground">Scan Date</th>
                <th className="text-left py-4 px-6 text-sm text-muted-foreground">Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredData.map((item) => (
                <tr key={item.id} className="border-b border-border/10 hover:bg-white/5 transition-colors">
                  <td className="py-4 px-6 text-foreground">{item.target}</td>
                  <td className="py-4 px-6">
                    <span className="px-3 py-1 text-xs rounded-full bg-white/10 text-muted-foreground">
                      {item.type}
                    </span>
                  </td>
                  <td className="py-4 px-6">
                    <span className={`px-3 py-1 text-xs rounded-full border ${getRiskColor(item.risk)}`}>
                      {item.risk}
                    </span>
                  </td>
                  <td className="py-4 px-6 text-foreground">{item.threats}</td>
                  <td className="py-4 px-6 text-muted-foreground text-sm">{item.date}</td>
                  <td className="py-4 px-6">
                    <button className="px-4 py-1.5 text-sm bg-[var(--cyber-blue)]/20 text-[var(--cyber-blue)] rounded-lg hover:bg-[var(--cyber-blue)]/30 transition-colors">
                      View Details
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        <div className="p-4 border-t border-border/30 flex items-center justify-between">
          <p className="text-sm text-muted-foreground">
            Showing {filteredData.length} of {historyData.length} scans
          </p>
          <div className="flex gap-2">
            <button className="px-4 py-2 bg-white/5 text-foreground rounded-lg hover:bg-white/10 transition-colors">
              Previous
            </button>
            <button className="px-4 py-2 bg-[var(--cyber-blue)]/20 text-[var(--cyber-blue)] rounded-lg">
              1
            </button>
            <button className="px-4 py-2 bg-white/5 text-foreground rounded-lg hover:bg-white/10 transition-colors">
              2
            </button>
            <button className="px-4 py-2 bg-white/5 text-foreground rounded-lg hover:bg-white/10 transition-colors">
              Next
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

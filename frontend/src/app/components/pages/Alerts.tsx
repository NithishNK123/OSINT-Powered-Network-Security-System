import { AlertTriangle, Bell, Clock, MapPin } from 'lucide-react';

const alertsData = [
  {
    id: 1,
    target: '192.168.1.100',
    type: 'IP',
    risk: 'Critical',
    title: 'Malicious C2 Communication Detected',
    description: 'Multiple connections to known command and control server',
    timestamp: '2 minutes ago',
    location: 'Russia',
  },
  {
    id: 2,
    target: 'phishing-site.com',
    type: 'Domain',
    risk: 'High',
    title: 'Phishing Campaign Active',
    description: 'Domain associated with credential harvesting campaign',
    timestamp: '15 minutes ago',
    location: 'China',
  },
  {
    id: 3,
    target: '203.0.113.8',
    type: 'IP',
    risk: 'Critical',
    title: 'Brute Force Attack Attempt',
    description: 'Multiple failed authentication attempts detected',
    timestamp: '1 hour ago',
    location: 'Unknown',
  },
  {
    id: 4,
    target: '10.0.0.45',
    type: 'IP',
    risk: 'High',
    title: 'Suspicious Port Scanning Activity',
    description: 'Sequential port scanning behavior observed',
    timestamp: '2 hours ago',
    location: 'Iran',
  },
  {
    id: 5,
    target: 'malware-cdn.net',
    type: 'Domain',
    risk: 'Critical',
    title: 'Malware Distribution Site',
    description: 'Domain serving known ransomware payloads',
    timestamp: '3 hours ago',
    location: 'Brazil',
  },
];

export function Alerts() {
  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'Critical':
        return {
          bg: 'bg-[var(--cyber-red)]/10',
          border: 'border-[var(--cyber-red)]/50',
          text: 'text-[var(--cyber-red)]',
          icon: 'text-[var(--cyber-red)]',
        };
      case 'High':
        return {
          bg: 'bg-[var(--cyber-orange)]/10',
          border: 'border-[var(--cyber-orange)]/50',
          text: 'text-[var(--cyber-orange)]',
          icon: 'text-[var(--cyber-orange)]',
        };
      case 'Medium':
        return {
          bg: 'bg-[var(--cyber-yellow)]/10',
          border: 'border-[var(--cyber-yellow)]/50',
          text: 'text-[var(--cyber-yellow)]',
          icon: 'text-[var(--cyber-yellow)]',
        };
      default:
        return {
          bg: 'bg-[var(--cyber-green)]/10',
          border: 'border-[var(--cyber-green)]/50',
          text: 'text-[var(--cyber-green)]',
          icon: 'text-[var(--cyber-green)]',
        };
    }
  };

  return (
    <div className="space-y-6">
      {/* Page Title */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl bg-gradient-to-r from-[var(--cyber-blue)] to-[var(--cyber-purple)] bg-clip-text text-transparent">
            Threat Alerts
          </h1>
          <p className="text-muted-foreground mt-1">Real-time security threat notifications</p>
        </div>
        <div className="flex items-center gap-3 glass-card px-4 py-2 rounded-lg">
          <div className="relative">
            <Bell className="w-5 h-5 text-[var(--cyber-blue)]" />
            <span className="absolute -top-1 -right-1 w-3 h-3 bg-[var(--cyber-red)] rounded-full animate-pulse"></span>
          </div>
          <span className="text-foreground">{alertsData.length} Active Alerts</span>
        </div>
      </div>

      {/* Alert Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="glass-card rounded-xl p-6 border-l-4 border-[var(--cyber-red)]">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground mb-1">Critical Alerts</p>
              <p className="text-3xl text-foreground">3</p>
            </div>
            <div className="p-3 bg-[var(--cyber-red)]/10 rounded-lg">
              <AlertTriangle className="w-6 h-6 text-[var(--cyber-red)]" />
            </div>
          </div>
        </div>

        <div className="glass-card rounded-xl p-6 border-l-4 border-[var(--cyber-orange)]">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground mb-1">High Priority</p>
              <p className="text-3xl text-foreground">2</p>
            </div>
            <div className="p-3 bg-[var(--cyber-orange)]/10 rounded-lg">
              <AlertTriangle className="w-6 h-6 text-[var(--cyber-orange)]" />
            </div>
          </div>
        </div>

        <div className="glass-card rounded-xl p-6 border-l-4 border-[var(--cyber-blue)]">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground mb-1">Last 24 Hours</p>
              <p className="text-3xl text-foreground">12</p>
            </div>
            <div className="p-3 bg-[var(--cyber-blue)]/10 rounded-lg">
              <Clock className="w-6 h-6 text-[var(--cyber-blue)]" />
            </div>
          </div>
        </div>
      </div>

      {/* Alerts List */}
      <div className="space-y-4">
        {alertsData.map((alert) => {
          const colors = getRiskColor(alert.risk);
          return (
            <div
              key={alert.id}
              className={`glass-card rounded-xl p-6 border-l-4 ${colors.border} hover:shadow-lg transition-all`}
            >
              <div className="flex items-start gap-4">
                {/* Alert Icon */}
                <div className={`p-3 ${colors.bg} rounded-lg mt-1`}>
                  <AlertTriangle className={`w-6 h-6 ${colors.icon}`} />
                </div>

                {/* Alert Content */}
                <div className="flex-1">
                  <div className="flex items-start justify-between gap-4 mb-3">
                    <div>
                      <h3 className="text-lg text-foreground mb-1">{alert.title}</h3>
                      <p className="text-sm text-muted-foreground">{alert.description}</p>
                    </div>
                    <span className={`px-3 py-1 text-xs rounded-full border ${colors.bg} ${colors.border} ${colors.text} whitespace-nowrap`}>
                      {alert.risk}
                    </span>
                  </div>

                  {/* Alert Details */}
                  <div className="flex flex-wrap items-center gap-4 text-sm text-muted-foreground">
                    <div className="flex items-center gap-2">
                      <span className="px-2 py-1 bg-white/5 rounded text-xs text-foreground">
                        {alert.type}
                      </span>
                      <span className="text-foreground">{alert.target}</span>
                    </div>
                    <div className="flex items-center gap-1">
                      <MapPin className="w-4 h-4" />
                      <span>{alert.location}</span>
                    </div>
                    <div className="flex items-center gap-1">
                      <Clock className="w-4 h-4" />
                      <span>{alert.timestamp}</span>
                    </div>
                  </div>

                  {/* Actions */}
                  <div className="flex gap-2 mt-4">
                    <button className="px-4 py-2 bg-[var(--cyber-blue)]/20 text-[var(--cyber-blue)] rounded-lg hover:bg-[var(--cyber-blue)]/30 transition-colors text-sm">
                      Investigate
                    </button>
                    <button className="px-4 py-2 bg-[var(--cyber-red)]/20 text-[var(--cyber-red)] rounded-lg hover:bg-[var(--cyber-red)]/30 transition-colors text-sm">
                      Block IP
                    </button>
                    <button className="px-4 py-2 bg-white/5 text-foreground rounded-lg hover:bg-white/10 transition-colors text-sm">
                      Dismiss
                    </button>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Empty State (shown when no alerts) */}
      {alertsData.length === 0 && (
        <div className="glass-card rounded-xl p-12 text-center">
          <div className="w-16 h-16 bg-[var(--cyber-green)]/10 rounded-full flex items-center justify-center mx-auto mb-4">
            <Bell className="w-8 h-8 text-[var(--cyber-green)]" />
          </div>
          <h3 className="text-xl text-foreground mb-2">No Active Alerts</h3>
          <p className="text-muted-foreground">
            Your system is secure. No threats detected at this time.
          </p>
        </div>
      )}
    </div>
  );
}

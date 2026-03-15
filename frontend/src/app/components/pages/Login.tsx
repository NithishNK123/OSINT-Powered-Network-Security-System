import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Shield, User, Lock, ChevronDown } from 'lucide-react';
import { useAuth, UserRole } from '@/app/context/AuthContext';

export function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState<UserRole>('analyst');
  const [error, setError] = useState('');
  const [showRoleDropdown, setShowRoleDropdown] = useState(false);
  
  const { login } = useAuth();
  const navigate = useNavigate();

  const roles = [
    { 
      value: 'viewer' as UserRole, 
      label: 'Viewer', 
      description: 'View-only access to dashboard',
      color: 'cyber-green'
    },
    { 
      value: 'analyst' as UserRole, 
      label: 'SOC Analyst', 
      description: 'Full analysis and reporting access',
      color: 'cyber-blue'
    },
    { 
      value: 'admin' as UserRole, 
      label: 'Administrator', 
      description: 'Complete system access and control',
      color: 'cyber-purple'
    },
  ];

  const selectedRole = roles.find(r => r.value === role);

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    if (!username || !password) {
      setError('Please enter username and password');
      return;
    }
    
    // In a real app, validation would happen here or in the auth context
    // For this demo, we'll just proceed with the login function
    const success = login(username, password, role);
    if (success) {
      navigate('/');
    } else {
      setError('Invalid credentials');
    }
  };

  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-4 relative overflow-hidden">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-0 left-0 w-96 h-96 bg-[var(--cyber-blue)]/20 rounded-full blur-[120px] animate-pulse"></div>
        <div className="absolute bottom-0 right-0 w-96 h-96 bg-[var(--cyber-purple)]/20 rounded-full blur-[120px] animate-pulse" style={{ animationDelay: '1s' }}></div>
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-[var(--cyber-cyan)]/10 rounded-full blur-[100px] animate-pulse" style={{ animationDelay: '2s' }}></div>
      </div>

      {/* Login Card */}
      <div className="glass-card rounded-2xl p-8 w-full max-w-md relative z-10 border-2 border-border/30">
        {/* Header */}
        <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center p-4 bg-gradient-to-br from-[var(--cyber-blue)] to-[var(--cyber-purple)] rounded-2xl mb-4 shadow-lg shadow-[var(--cyber-blue)]/50">
            <Shield className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-[var(--cyber-blue)] to-[var(--cyber-purple)] bg-clip-text text-transparent mb-2">
            OSINT ADVANTAGE
          </h1>
          <p className="text-muted-foreground text-sm">Threat Intelligence Platform</p>
        </div>

        {/* Login Form */}
        <form onSubmit={handleLogin} className="space-y-5">
            {/* Role Selection */}
            <div className="relative">
            <label className="block text-sm font-medium text-muted-foreground mb-2">
              Select Role
            </label>
            <button
                type="button"
                onClick={() => setShowRoleDropdown(!showRoleDropdown)}
                className="w-full px-4 py-3 bg-white/5 border border-border/50 rounded-lg text-foreground focus:outline-none focus:ring-2 focus:ring-[var(--cyber-blue)] focus:border-transparent transition-all hover:border-[var(--cyber-blue)]/50 flex items-center justify-between"
            >
                <div className="flex items-center gap-3">
                <div className={`w-2 h-2 rounded-full bg-[var(--${selectedRole?.color})]`}></div>
                <span>{selectedRole?.label}</span>
                </div>
                <ChevronDown className={`w-4 h-4 text-muted-foreground transition-transform ${showRoleDropdown ? 'rotate-180' : ''}`} />
            </button>

            {/* Dropdown Menu */}
            {showRoleDropdown && (
                <div className="absolute top-full left-0 right-0 mt-2 bg-background border border-border/50 rounded-lg shadow-xl overflow-hidden z-50">
                {roles.map((r) => (
                    <button
                    key={r.value}
                    type="button"
                    onClick={() => {
                        setRole(r.value);
                        setShowRoleDropdown(false);
                    }}
                    className={`w-full px-4 py-3 text-left transition-all hover:bg-white/10 flex flex-col items-start gap-1 border-l-2 ${
                        role === r.value
                        ? `border-[var(--${r.color})] bg-white/5`
                        : 'border-transparent'
                    }`}
                    >
                    <div className="flex items-center gap-2">
                        <div className={`w-2 h-2 rounded-full bg-[var(--${r.color})]`}></div>
                        <span className="text-foreground font-medium">{r.label}</span>
                    </div>
                    <span className="text-xs text-muted-foreground ml-4">{r.description}</span>
                    </button>
                ))}
                </div>
            )}
            </div>

          {/* Username Input */}
          <div>
            <label className="block text-sm font-medium text-muted-foreground mb-2">
              Username
            </label>
            <div className="relative">
              <User className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Enter your username"
                className="w-full pl-12 pr-4 py-3 bg-white/5 border border-border/50 rounded-lg text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-[var(--cyber-blue)] focus:border-transparent transition-all"
              />
            </div>
          </div>

          {/* Password Input */}
          <div>
            <label className="block text-sm font-medium text-muted-foreground mb-2">
              Password
            </label>
            <div className="relative">
              <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter your password"
                className="w-full pl-12 pr-4 py-3 bg-white/5 border border-border/50 rounded-lg text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-[var(--cyber-blue)] focus:border-transparent transition-all"
              />
            </div>
          </div>

          {/* Error Message */}
          {error && (
            <div className="p-3 bg-[var(--cyber-red)]/10 border border-[var(--cyber-red)]/30 rounded-lg text-center">
              <p className="text-sm text-[var(--cyber-red)] font-medium">{error}</p>
            </div>
          )}

          {/* Login Button */}
          <button
            type="submit"
            className="w-full px-6 py-3 bg-gradient-to-r from-[var(--cyber-blue)] to-[var(--cyber-purple)] text-white font-medium rounded-lg hover:shadow-lg hover:shadow-[var(--cyber-blue)]/50 transition-all transform hover:scale-[1.02] active:scale-[0.98]"
          >
            Login to Dashboard
          </button>
        </form>

        {/* Info Section */}
        <div className="mt-8 pt-6 border-t border-border/30">
          <div className="p-4 bg-[var(--cyber-blue)]/5 border border-[var(--cyber-blue)]/20 rounded-lg">
            <p className="text-xs text-muted-foreground text-center leading-relaxed">
              <span className="text-[var(--cyber-blue)] font-medium">Demo Credentials:</span> Use any username and password to login with selected role
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

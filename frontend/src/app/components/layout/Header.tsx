import { LogOut, User } from 'lucide-react';
import { useAuth } from '@/app/context/AuthContext';
import { useNavigate } from 'react-router-dom';

export function Header() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const getRoleDisplay = (role: string) => {
    switch (role) {
      case 'viewer':
        return { label: 'Viewer', color: 'cyber-green' };
      case 'analyst':
        return { label: 'SOC Analyst', color: 'cyber-blue' };
      case 'admin':
        return { label: 'Administrator', color: 'cyber-purple' };
      default:
        return { label: 'User', color: 'cyber-blue' };
    }
  };

  const roleDisplay = user ? getRoleDisplay(user.role) : null;

  return (
    <header className="fixed top-0 left-0 right-0 h-16 glass-card border-b border-border/50 z-50 flex items-center justify-between px-6">
      {/* Left - Empty (logo and branding removed) */}
      <div className="flex-1"></div>

      {/* Center - Title */}
      <div className="absolute left-1/2 -translate-x-1/2">
        <h1 className="text-lg text-muted-foreground">Threat Intelligence Platform</h1>
      </div>

      {/* Right - User Profile and Role Badge */}
      <div className="flex items-center gap-3">
        {/* User Profile with Role Badge */}
        <div className="flex items-center gap-3 px-4 py-2 glass-card rounded-lg border border-border/30">
          <div className={`w-8 h-8 bg-gradient-to-br from-[var(--${roleDisplay?.color})] to-[var(--cyber-blue)] rounded-full flex items-center justify-center shadow-lg shadow-[var(--${roleDisplay?.color})]/30`}>
            <User className="w-4 h-4 text-white" />
          </div>
          <div className="flex flex-col">
            <span className="text-sm text-foreground">{user?.username || 'User'}</span>
            <span className={`text-xs text-[var(--${roleDisplay?.color})]`}>
              {roleDisplay?.label}
            </span>
          </div>
        </div>

        {/* Logout Button */}
        <button
          onClick={handleLogout}
          className="p-2 hover:bg-[var(--cyber-red)]/10 rounded-lg transition-all group"
          title="Logout"
        >
          <LogOut className="w-5 h-5 text-muted-foreground group-hover:text-[var(--cyber-red)] transition-colors" />
        </button>
      </div>
    </header>
  );
}

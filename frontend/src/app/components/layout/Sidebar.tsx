import { LayoutDashboard, Search, History, FileText, Settings, Bell } from 'lucide-react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '@/app/context/AuthContext';

const menuItems = [
  { icon: LayoutDashboard, label: 'Dashboard', path: '/', roles: ['viewer', 'analyst', 'admin'] },
  { icon: Search, label: 'Analyze', path: '/analyze', roles: ['analyst', 'admin'] },
  { icon: History, label: 'History', path: '/history', roles: ['analyst', 'admin'] },
  { icon: FileText, label: 'Reports', path: '/reports', roles: ['analyst', 'admin'] },
  { icon: Bell, label: 'Alerts', path: '/alerts', roles: ['analyst', 'admin'] },
  { icon: Settings, label: 'Settings', path: '/settings', roles: ['admin'] },
];

export function Sidebar() {
  const location = useLocation();
  const { user } = useAuth();

  // Filter menu items based on user role
  const visibleMenuItems = menuItems.filter(item => 
    user && item.roles.includes(user.role)
  );

  return (
    <aside className="fixed left-0 top-16 bottom-0 w-64 glass-card border-r border-border/50 p-4">
      {/* Navigation */}
      <nav className="space-y-2">
        {visibleMenuItems.map((item) => {
          const isActive = location.pathname === item.path;
          const Icon = item.icon;

          return (
            <Link
              key={item.path}
              to={item.path}
              className={`
                flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all
                ${
                  isActive
                    ? 'bg-gradient-to-r from-[var(--cyber-blue)]/20 to-[var(--cyber-purple)]/20 text-[var(--cyber-blue)] border border-[var(--cyber-blue)]/30 shadow-lg shadow-[var(--cyber-blue)]/20'
                    : 'text-muted-foreground hover:bg-white/5 hover:text-foreground'
                }
              `}
            >
              <Icon className="w-5 h-5" />
              <span>{item.label}</span>
            </Link>
          );
        })}
      </nav>

      {/* Role Info at Bottom */}
      <div className="absolute bottom-4 left-4 right-4">
        <div className="p-3 bg-white/5 rounded-lg border border-border/30">
          <p className="text-xs text-muted-foreground mb-1">Access Level</p>
          <div className="flex items-center gap-2">
            <div className={`w-2 h-2 rounded-full ${
              user?.role === 'admin' ? 'bg-[var(--cyber-purple)]' :
              user?.role === 'analyst' ? 'bg-[var(--cyber-blue)]' :
              'bg-[var(--cyber-green)]'
            }`}></div>
            <span className="text-sm text-foreground">
              {user?.role === 'admin' ? 'Full Access' :
               user?.role === 'analyst' ? 'Analysis Access' :
               'View Only'}
            </span>
          </div>
        </div>
      </div>
    </aside>
  );
}

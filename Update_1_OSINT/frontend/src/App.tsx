import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider } from '@/app/context/ThemeContext';
import { AuthProvider, useAuth } from '@/app/context/AuthContext';
import { ProtectedRoute } from '@/app/components/auth/ProtectedRoute';
import { Header } from '@/app/components/layout/Header';
import { AppSidebar } from '@/app/components/layout/Sidebar';
import { Dashboard } from '@/app/components/pages/Dashboard';
import { Analyze } from '@/app/components/pages/Analyze';
import { History } from '@/app/components/pages/History';
import { Reports } from '@/app/components/pages/Reports';
import { Alerts } from '@/app/components/pages/Alerts';
import { Settings } from '@/app/components/pages/Settings';
import { Login } from '@/app/components/pages/Login';

function AppContent() {
  const { isAuthenticated } = useAuth();

  return (
    <div className="min-h-screen bg-background transition-colors duration-300">
      {isAuthenticated && (
        <>
          {/* Header */}
          <Header />

          {/* Sidebar */}
          <AppSidebar />
        </>
      )}

      {/* Main Content */}
      <main className={isAuthenticated ? "ml-64 mt-16 p-8" : ""}>
        <Routes>
          {/* Login Route */}
          <Route path="/login" element={<Login />} />

          {/* Protected Routes */}
          <Route
            path="/"
            element={
              <ProtectedRoute allowedRoles={['viewer', 'analyst', 'admin']}>
                <Dashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="/analyze"
            element={
              <ProtectedRoute allowedRoles={['analyst', 'admin']}>
                <Analyze />
              </ProtectedRoute>
            }
          />
          <Route
            path="/history"
            element={
              <ProtectedRoute allowedRoles={['analyst', 'admin']}>
                <History />
              </ProtectedRoute>
            }
          />
          <Route
            path="/reports"
            element={
              <ProtectedRoute allowedRoles={['analyst', 'admin']}>
                <Reports />
              </ProtectedRoute>
            }
          />
          <Route
            path="/alerts"
            element={
              <ProtectedRoute allowedRoles={['analyst', 'admin']}>
                <Alerts />
              </ProtectedRoute>
            }
          />
          <Route
            path="/settings"
            element={
              <ProtectedRoute allowedRoles={['admin']}>
                <Settings />
              </ProtectedRoute>
            }
          />

          {/* Redirect to login if no other route matches */}
          <Route path="*" element={<Navigate to={isAuthenticated ? "/" : "/login"} replace />} />
        </Routes>
      </main>
    </div>
  );
}

export default function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <Router>
          <AppContent />
        </Router>
      </AuthProvider>
    </ThemeProvider>
  );
}

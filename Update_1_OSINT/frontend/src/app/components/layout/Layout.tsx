import { type FC } from 'react';
import { Outlet } from 'react-router-dom';
import { Header } from './Header';
import { AppSidebar } from './Sidebar';

const Layout: FC = () => {
    return (
        <div className="min-h-screen bg-background text-foreground transition-colors duration-300 font-sans selection:bg-primary/20">
            <Header />
            <AppSidebar />
            <main className="pt-20 pl-64 p-6 min-h-screen transition-all duration-300">
                <div className="max-w-7xl mx-auto space-y-6">
                    <Outlet />
                </div>
            </main>
        </div>
    );
};

export default Layout;

import { createContext, useContext, useEffect, useState, type ReactNode } from 'react';

type Theme = 'dark' | 'light';

interface ThemeContextType {
    theme: Theme;
    toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export function ThemeProvider({ children }: { children: ReactNode }) {
    const [theme, setTheme] = useState<Theme>('dark');
    const [isTransitioning, setIsTransitioning] = useState(false);

    useEffect(() => {
        // Apply theme class to html element
        const root = document.documentElement;
        if (theme === 'dark') {
            root.classList.add('dark');
        } else {
            root.classList.remove('dark');
        }
    }, [theme]);

    const toggleTheme = () => {
        if (isTransitioning) return;

        setIsTransitioning(true);
        const newTheme = theme === 'dark' ? 'light' : 'dark';

        // Create transition overlay container
        const overlay = document.createElement('div');
        overlay.className = 'theme-transition-overlay';

        // Create the wave element
        const wave = document.createElement('div');
        wave.className = `theme-transition-wave to-${newTheme}`;
        overlay.appendChild(wave);

        document.body.appendChild(overlay);

        // Change theme at optimal point for seamless water wave reveal
        setTimeout(() => {
            setTheme(newTheme);
        }, 500);

        // Remove overlay after animation completes
        setTimeout(() => {
            if (document.body.contains(overlay)) {
                document.body.removeChild(overlay);
            }
            setIsTransitioning(false);
        }, 1700);
    };

    return (
        <ThemeContext.Provider value={{ theme, toggleTheme }}>
            {children}
        </ThemeContext.Provider>
    );
}

export function useTheme() {
    const context = useContext(ThemeContext);
    if (context === undefined) {
        throw new Error('useTheme must be used within a ThemeProvider');
    }
    return context;
}

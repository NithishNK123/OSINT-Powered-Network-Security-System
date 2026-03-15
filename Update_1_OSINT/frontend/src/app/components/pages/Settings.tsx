import { useState } from 'react';
import { Save, Shield, Database, Bell, Sun, Moon } from 'lucide-react';
import { useTheme } from '@/app/context/ThemeContext';

export function Settings() {
    const { theme, toggleTheme } = useTheme();

    const [thresholds, setThresholds] = useState({
        low: 30,
        medium: 60,
        high: 80,
    });

    const [integrations, setIntegrations] = useState({
        virusTotal: true,
        abuseIPDB: true,
        shodan: false,
    });

    const [notifications, setNotifications] = useState({
        emailAlerts: true,
        criticalOnly: false,
        weeklyReport: true,
    });

    const handleSave = () => {
        // Mock save action
        alert('Settings saved successfully!');
    };

    return (
        <div className="space-y-6">
            {/* Page Title */}
            <div>
                <h1 className="text-3xl bg-gradient-to-r from-[var(--cyber-blue)] to-[var(--cyber-purple)] bg-clip-text text-transparent">
                    Settings
                </h1>
                <p className="text-muted-foreground mt-1">Configure your threat intelligence platform</p>
            </div>

            {/* Appearance Settings */}
            <div className="glass-card rounded-xl p-6">
                <div className="flex items-center gap-3 mb-6">
                    <div className="p-2 bg-[var(--cyber-purple)]/10 rounded-lg">
                        {theme === 'dark' ? (
                            <Moon className="w-5 h-5 text-[var(--cyber-purple)]" />
                        ) : (
                            <Sun className="w-5 h-5 text-[var(--cyber-purple)]" />
                        )}
                    </div>
                    <div>
                        <h3 className="text-foreground">Appearance</h3>
                        <p className="text-sm text-muted-foreground">Customize the visual theme with animated transitions</p>
                    </div>
                </div>

                <div className="p-5 bg-gradient-to-br from-[var(--cyber-blue)]/5 to-[var(--cyber-purple)]/5 rounded-lg border border-border/30 hover:border-border/60 transition-all">
                    <div className="flex items-center justify-between">
                        <div className="flex-1">
                            <div className="flex items-center gap-2 mb-2">
                                <h4 className="text-foreground">Theme Mode</h4>
                                <span className="px-2 py-0.5 text-xs rounded-full bg-[var(--cyber-purple)]/20 text-[var(--cyber-purple)] border border-[var(--cyber-purple)]/30">
                                    {theme === 'dark' ? 'Dark' : 'Light'}
                                </span>
                            </div>
                            <p className="text-sm text-muted-foreground mb-1">
                                {theme === 'dark'
                                    ? 'Dark mode - Reduced eye strain in low light environments'
                                    : 'Light mode - Enhanced visibility in bright environments'}
                            </p>
                            <p className="text-xs text-[var(--cyber-cyan)] flex items-center gap-1">
                                <span className="inline-block w-1 h-1 bg-[var(--cyber-cyan)] rounded-full animate-pulse"></span>
                                Features diagonal wave transition animation
                            </p>
                        </div>
                        <button
                            onClick={toggleTheme}
                            className={`relative inline-flex items-center h-9 w-20 rounded-full transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-offset-2 shadow-lg ml-6 ${theme === 'dark'
                                    ? 'bg-gradient-to-r from-[var(--cyber-blue)] to-[var(--cyber-purple)] focus:ring-[var(--cyber-blue)] shadow-[var(--cyber-blue)]/50'
                                    : 'bg-gradient-to-r from-[var(--cyber-purple)] to-[var(--cyber-pink)] focus:ring-[var(--cyber-purple)] shadow-[var(--cyber-purple)]/50'
                                }`}
                            title="Toggle theme with diagonal wave animation"
                        >
                            <span
                                className={`inline-flex items-center justify-center w-7 h-7 transform rounded-full bg-white shadow-lg transition-all duration-300 ${theme === 'dark' ? 'translate-x-11' : 'translate-x-1'
                                    }`}
                            >
                                {theme === 'dark' ? (
                                    <Moon className="w-4 h-4 text-[var(--cyber-blue)]" />
                                ) : (
                                    <Sun className="w-4 h-4 text-[var(--cyber-purple)]" />
                                )}
                            </span>
                        </button>
                    </div>
                </div>

                {/* Theme Preview Info */}
                <div className="mt-4 p-4 bg-white/5 dark:bg-white/5 rounded-lg border border-border/20">
                    <div className="flex items-start gap-3">
                        <div className="p-2 bg-[var(--cyber-blue)]/10 rounded mt-0.5">
                            <svg className="w-4 h-4 text-[var(--cyber-blue)]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                        </div>
                        <div className="flex-1">
                            <h4 className="text-sm text-foreground mb-1">Fluid Water Wave Transition</h4>
                            <p className="text-xs text-muted-foreground leading-relaxed">
                                When you toggle the theme, a fluid water wave animation with organic curves will flow from the top-left
                                to bottom-right corner. The wave uses radial gradients and multiple shimmer layers to create a natural,
                                liquid-like reveal effect across all interface elements.
                            </p>
                        </div>
                    </div>
                </div>
            </div>

            {/* Threat Level Thresholds */}
            <div className="glass-card rounded-xl p-6">
                <div className="flex items-center gap-3 mb-6">
                    <div className="p-2 bg-[var(--cyber-blue)]/10 rounded-lg">
                        <Shield className="w-5 h-5 text-[var(--cyber-blue)]" />
                    </div>
                    <div>
                        <h3 className="text-foreground">Threat Level Thresholds</h3>
                        <p className="text-sm text-muted-foreground">Configure risk score boundaries</p>
                    </div>
                </div>

                <div className="space-y-6">
                    {/* Low Threshold */}
                    <div>
                        <div className="flex items-center justify-between mb-3">
                            <label className="text-sm text-foreground">Low Risk Threshold</label>
                            <span className="text-sm text-[var(--cyber-green)]">{thresholds.low}</span>
                        </div>
                        <input
                            type="range"
                            min="0"
                            max="100"
                            value={thresholds.low}
                            onChange={(e) => setThresholds({ ...thresholds, low: parseInt(e.target.value) })}
                            className="w-full h-2 bg-white/10 rounded-lg appearance-none cursor-pointer accent-[var(--cyber-green)]"
                        />
                        <div className="flex justify-between text-xs text-muted-foreground mt-1">
                            <span>0</span>
                            <span>100</span>
                        </div>
                    </div>

                    {/* Medium Threshold */}
                    <div>
                        <div className="flex items-center justify-between mb-3">
                            <label className="text-sm text-foreground">Medium Risk Threshold</label>
                            <span className="text-sm text-[var(--cyber-orange)]">{thresholds.medium}</span>
                        </div>
                        <input
                            type="range"
                            min="0"
                            max="100"
                            value={thresholds.medium}
                            onChange={(e) => setThresholds({ ...thresholds, medium: parseInt(e.target.value) })}
                            className="w-full h-2 bg-white/10 rounded-lg appearance-none cursor-pointer accent-[var(--cyber-orange)]"
                        />
                        <div className="flex justify-between text-xs text-muted-foreground mt-1">
                            <span>0</span>
                            <span>100</span>
                        </div>
                    </div>

                    {/* High Threshold */}
                    <div>
                        <div className="flex items-center justify-between mb-3">
                            <label className="text-sm text-foreground">High Risk Threshold</label>
                            <span className="text-sm text-[var(--cyber-red)]">{thresholds.high}</span>
                        </div>
                        <input
                            type="range"
                            min="0"
                            max="100"
                            value={thresholds.high}
                            onChange={(e) => setThresholds({ ...thresholds, high: parseInt(e.target.value) })}
                            className="w-full h-2 bg-white/10 rounded-lg appearance-none cursor-pointer accent-[var(--cyber-red)]"
                        />
                        <div className="flex justify-between text-xs text-muted-foreground mt-1">
                            <span>0</span>
                            <span>100</span>
                        </div>
                    </div>
                </div>
            </div>

            {/* API Integrations */}
            <div className="glass-card rounded-xl p-6">
                <div className="flex items-center gap-3 mb-6">
                    <div className="p-2 bg-[var(--cyber-cyan)]/10 rounded-lg">
                        <Database className="w-5 h-5 text-[var(--cyber-cyan)]" />
                    </div>
                    <div>
                        <h3 className="text-foreground">API Integrations</h3>
                        <p className="text-sm text-muted-foreground">Enable or disable threat intelligence sources</p>
                    </div>
                </div>

                <div className="space-y-4">
                    {/* VirusTotal */}
                    <div className="p-4 bg-white/5 dark:bg-white/5 rounded-lg border border-border/30">
                        <div className="flex items-center justify-between">
                            <div>
                                <h4 className="text-foreground mb-1">VirusTotal</h4>
                                <p className="text-xs text-muted-foreground">Malware and threat detection database</p>
                            </div>
                            <label className="relative inline-flex items-center cursor-pointer">
                                <input
                                    type="checkbox"
                                    checked={integrations.virusTotal}
                                    onChange={(e) => setIntegrations({ ...integrations, virusTotal: e.target.checked })}
                                    className="sr-only peer"
                                />
                                <div className="w-11 h-6 bg-white/10 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-[var(--cyber-blue)] rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[var(--cyber-blue)]"></div>
                            </label>
                        </div>
                    </div>

                    {/* AbuseIPDB */}
                    <div className="p-4 bg-white/5 dark:bg-white/5 rounded-lg border border-border/30">
                        <div className="flex items-center justify-between">
                            <div>
                                <h4 className="text-foreground mb-1">AbuseIPDB</h4>
                                <p className="text-xs text-muted-foreground">IP address abuse and threat intelligence</p>
                            </div>
                            <label className="relative inline-flex items-center cursor-pointer">
                                <input
                                    type="checkbox"
                                    checked={integrations.abuseIPDB}
                                    onChange={(e) => setIntegrations({ ...integrations, abuseIPDB: e.target.checked })}
                                    className="sr-only peer"
                                />
                                <div className="w-11 h-6 bg-white/10 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-[var(--cyber-blue)] rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[var(--cyber-blue)]"></div>
                            </label>
                        </div>
                    </div>

                    {/* Shodan */}
                    <div className="p-4 bg-white/5 dark:bg-white/5 rounded-lg border border-border/30">
                        <div className="flex items-center justify-between">
                            <div>
                                <h4 className="text-foreground mb-1">Shodan</h4>
                                <p className="text-xs text-muted-foreground">Internet-connected devices search engine</p>
                            </div>
                            <label className="relative inline-flex items-center cursor-pointer">
                                <input
                                    type="checkbox"
                                    checked={integrations.shodan}
                                    onChange={(e) => setIntegrations({ ...integrations, shodan: e.target.checked })}
                                    className="sr-only peer"
                                />
                                <div className="w-11 h-6 bg-white/10 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-[var(--cyber-blue)] rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[var(--cyber-blue)]"></div>
                            </label>
                        </div>
                    </div>
                </div>
            </div>

            {/* Notification Settings */}
            <div className="glass-card rounded-xl p-6">
                <div className="flex items-center gap-3 mb-6">
                    <div className="p-2 bg-[var(--cyber-orange)]/10 rounded-lg">
                        <Bell className="w-5 h-5 text-[var(--cyber-orange)]" />
                    </div>
                    <div>
                        <h3 className="text-foreground">Notifications</h3>
                        <p className="text-sm text-muted-foreground">Configure alert preferences</p>
                    </div>
                </div>

                <div className="space-y-4">
                    {/* Email Alerts */}
                    <div className="p-4 bg-white/5 dark:bg-white/5 rounded-lg border border-border/30">
                        <div className="flex items-center justify-between">
                            <div>
                                <h4 className="text-foreground mb-1">Email Alerts</h4>
                                <p className="text-xs text-muted-foreground">Receive threat alerts via email</p>
                            </div>
                            <label className="relative inline-flex items-center cursor-pointer">
                                <input
                                    type="checkbox"
                                    checked={notifications.emailAlerts}
                                    onChange={(e) => setNotifications({ ...notifications, emailAlerts: e.target.checked })}
                                    className="sr-only peer"
                                />
                                <div className="w-11 h-6 bg-white/10 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-[var(--cyber-blue)] rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[var(--cyber-blue)]"></div>
                            </label>
                        </div>
                    </div>

                    {/* Critical Only */}
                    <div className="p-4 bg-white/5 dark:bg-white/5 rounded-lg border border-border/30">
                        <div className="flex items-center justify-between">
                            <div>
                                <h4 className="text-foreground mb-1">Critical Alerts Only</h4>
                                <p className="text-xs text-muted-foreground">Only notify for critical threats</p>
                            </div>
                            <label className="relative inline-flex items-center cursor-pointer">
                                <input
                                    type="checkbox"
                                    checked={notifications.criticalOnly}
                                    onChange={(e) => setNotifications({ ...notifications, criticalOnly: e.target.checked })}
                                    className="sr-only peer"
                                />
                                <div className="w-11 h-6 bg-white/10 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-[var(--cyber-blue)] rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[var(--cyber-blue)]"></div>
                            </label>
                        </div>
                    </div>

                    {/* Weekly Report */}
                    <div className="p-4 bg-white/5 dark:bg-white/5 rounded-lg border border-border/30">
                        <div className="flex items-center justify-between">
                            <div>
                                <h4 className="text-foreground mb-1">Weekly Summary Report</h4>
                                <p className="text-xs text-muted-foreground">Receive weekly threat summary</p>
                            </div>
                            <label className="relative inline-flex items-center cursor-pointer">
                                <input
                                    type="checkbox"
                                    checked={notifications.weeklyReport}
                                    onChange={(e) => setNotifications({ ...notifications, weeklyReport: e.target.checked })}
                                    className="sr-only peer"
                                />
                                <div className="w-11 h-6 bg-white/10 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-[var(--cyber-blue)] rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[var(--cyber-blue)]"></div>
                            </label>
                        </div>
                    </div>
                </div>
            </div>

            {/* Save Button */}
            <div className="flex justify-end">
                <button
                    onClick={handleSave}
                    className="px-6 py-3 bg-gradient-to-r from-[var(--cyber-blue)] to-[var(--cyber-purple)] text-white rounded-lg hover:shadow-lg hover:shadow-[var(--cyber-blue)]/50 transition-all flex items-center gap-2"
                >
                    <Save className="w-5 h-5" />
                    Save Settings
                </button>
            </div>
        </div>
    );
}

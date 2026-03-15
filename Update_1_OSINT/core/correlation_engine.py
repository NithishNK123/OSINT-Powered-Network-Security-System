"""
Threat Intelligence Correlation Engine
========================================
Correlates OSINT signals to enhance threat classification accuracy.

Features:
- Pattern detection (multiple malicious hits)
- Abuse reputation analysis
- Attack surface exposure scoring
- Confidence scoring
- Signal weighting
"""

from typing import Dict, List, Tuple


# ===============================
# SIGNAL WEIGHTS & THRESHOLDS
# ===============================

SIGNAL_WEIGHTS = {
    "virustotal_multiple_hits": 0.35,      # 3+ detection engines
    "virustotal_critical_engine": 0.25,    # Blocked by major AV vendor
    "abuse_reputation_spike": 0.30,        # Score > 50
    "abuse_previous_reports": 0.20,        # History of abuse
    "exposed_critical_ports": 0.25,        # 21, 23, 3389, 5900
    "exposed_service_ports": 0.20,         # Common service ports
    "exposed_port_count": 0.15,            # Total open ports
    "dns_reputation": 0.15,                # Domain reputation
    "asn_blacklist": 0.20,                 # Known malicious ASN
}


# ===============================
# CRITICAL SECURITY PORTS
# ===============================

CRITICAL_PORTS = [
    21,     # FTP
    23,     # Telnet
    3389,   # RDP
    5900,   # VNC
]

COMMON_SERVICE_PORTS = [
    22,     # SSH
    25,     # SMTP
    53,     # DNS
    80,     # HTTP
    443,    # HTTPS
    3306,   # MySQL
    5432,   # PostgreSQL
    6379,   # Redis
    27017,  # MongoDB
    9200,   # Elasticsearch
]


# ===============================
# CORRELATION ENGINE
# ===============================

class ThreatCorrelationEngine:
    """
    Correlates multiple OSINT signals to enhance threat assessment.
    """
    
    def __init__(self):
        self.signals = {}
        self.correlation_score = 0.0
        self.confidence = 0.0
    
    def correlate(self, vt_data: dict, abuse_data: dict, 
                 shodan_data: dict) -> dict:
        """
        Correlate all OSINT signals for comprehensive threat assessment.
        
        Args:
            vt_data: VirusTotal API response
            abuse_data: AbuseIPDB API response
            shodan_data: Shodan API response
        
        Returns:
            {
                'correlation_score': float (0-1),
                'confidence': float (0-1),
                'signals': dict of detected signals,
                'patterns': list of detected patterns,
                'risk_multiplier': float (1.0-2.0)
            }
        """
        self.signals = {}
        
        # Analyze each signal
        self._analyze_virustotal(vt_data)
        self._analyze_abuse(abuse_data)
        self._analyze_shodan(shodan_data)
        
        # Calculate correlation score
        self.correlation_score = self._calculate_correlation_score()
        
        # Detect patterns
        patterns = self._detect_patterns()
        
        # Calculate confidence
        self.confidence = self._calculate_confidence()
        
        # Calculate risk multiplier
        risk_multiplier = self._calculate_risk_multiplier(patterns)
        
        return {
            'correlation_score': round(self.correlation_score, 3),
            'confidence': round(self.confidence, 3),
            'signals': self.signals,
            'patterns': patterns,
            'risk_multiplier': round(risk_multiplier, 2)
        }
    
    # ========================
    # SIGNAL ANALYSIS
    # ========================
    
    def _analyze_virustotal(self, vt_data: dict):
        """
        Analyze VirusTotal signals.
        """
        if not vt_data:
            return
        
        malicious_count = vt_data.get("malicious", 0)
        
        # Signal 1: Multiple engine detections
        if malicious_count >= 3:
            self.signals["vt_multiple_hits"] = {
                "weight": SIGNAL_WEIGHTS["virustotal_multiple_hits"],
                "value": malicious_count,
                "description": f"Detected by {malicious_count} security engines"
            }
        
        # Signal 2: Critical engine detection
        critical_engines = vt_data.get("critical_engines", [])
        if critical_engines:
            self.signals["vt_critical_engine"] = {
                "weight": SIGNAL_WEIGHTS["virustotal_critical_engine"],
                "value": len(critical_engines),
                "description": f"Blocked by critical engines: {', '.join(critical_engines)}"
            }
    
    def _analyze_abuse(self, abuse_data: dict):
        """
        Analyze AbuseIPDB signals.
        """
        if not abuse_data:
            return
        
        score = abuse_data.get("score", 0)
        reports = abuse_data.get("reports", 0)
        
        # Signal 1: High abuse reputation score
        if score >= 50:
            self.signals["abuse_reputation_spike"] = {
                "weight": SIGNAL_WEIGHTS["abuse_reputation_spike"],
                "value": score,
                "description": f"High abuse reputation score: {score}%"
            }
        
        # Signal 2: Previous abuse reports
        if reports > 0:
            self.signals["abuse_previous_reports"] = {
                "weight": SIGNAL_WEIGHTS["abuse_previous_reports"],
                "value": reports,
                "description": f"Reported for abuse {reports} times"
            }
    
    def _analyze_shodan(self, shodan_data: dict):
        """
        Analyze Shodan signals (attack surface).
        """
        if not shodan_data:
            return
        
        open_ports = shodan_data.get("open_ports", [])
        
        if not open_ports:
            return
        
        # Signal 1: Critical ports exposed
        critical_exposed = [p for p in open_ports if p in CRITICAL_PORTS]
        if critical_exposed:
            self.signals["exposed_critical_ports"] = {
                "weight": SIGNAL_WEIGHTS["exposed_critical_ports"],
                "value": len(critical_exposed),
                "description": f"Critical ports exposed: {critical_exposed}"
            }
        
        # Signal 2: Common service ports exposed
        service_exposed = [p for p in open_ports if p in COMMON_SERVICE_PORTS]
        if service_exposed:
            self.signals["exposed_service_ports"] = {
                "weight": SIGNAL_WEIGHTS["exposed_service_ports"],
                "value": len(service_exposed),
                "description": f"Service ports exposed: {service_exposed}"
            }
        
        # Signal 3: Total port count
        port_count = len(open_ports)
        if port_count > 5:
            self.signals["exposed_port_count"] = {
                "weight": SIGNAL_WEIGHTS["exposed_port_count"],
                "value": port_count,
                "description": f"Large attack surface: {port_count} open ports"
            }
    
    # ========================
    # CORRELATION CALCULATION
    # ========================
    
    def _calculate_correlation_score(self) -> float:
        """
        Calculate overall correlation score (0-1).
        Higher = more signals detected.
        """
        if not self.signals:
            return 0.0
        
        total_weight = sum(sig["weight"] for sig in self.signals.values())
        return min(total_weight, 1.0)
    
    def _detect_patterns(self) -> list:
        """
        Detect suspicious patterns from correlated signals.
        """
        patterns = []
        
        # Pattern 1: Multi-vector attack infrastructure
        if (self.signals.get("vt_multiple_hits") and 
            self.signals.get("abuse_reputation_spike")):
            patterns.append({
                "name": "Multi-Vector Attack Infrastructure",
                "confidence": 0.95,
                "description": "IP shows both malware detections and abuse reputation"
            })
        
        # Pattern 2: Exposed infrastructure with malicious history
        if (self.signals.get("exposed_critical_ports") and 
            self.signals.get("vt_multiple_hits")):
            patterns.append({
                "name": "Compromised Attack Platform",
                "confidence": 0.90,
                "description": "Exposed critical services with malware history"
            })
        
        # Pattern 3: High-exposure botnet node
        if (self.signals.get("exposed_port_count") and 
            self.signals.get("abuse_previous_reports")):
            patterns.append({
                "name": "Botnet Node Candidate",
                "confidence": 0.80,
                "description": "High port exposure with abuse history"
            })
        
        # Pattern 4: C2 Infrastructure
        if (self.signals.get("vt_critical_engine") and 
            self.signals.get("abuse_reputation_spike") and
            self.signals.get("exposed_service_ports")):
            patterns.append({
                "name": "C2 Infrastructure Indicators",
                "confidence": 0.85,
                "description": "Multiple indicators of command & control infrastructure"
            })
        
        return patterns
    
    def _calculate_confidence(self) -> float:
        """
        Calculate confidence score based on signal diversity.
        """
        signal_types = {
            'virustotal': sum(1 for s in self.signals if s.startswith('vt_')),
            'abuse': sum(1 for s in self.signals if s.startswith('abuse_')),
            'shodan': sum(1 for s in self.signals if s.startswith('exposed_'))
        }
        
        # Confidence increases with diverse signals
        confidence = 0.0
        if signal_types['virustotal'] > 0:
            confidence += 0.3
        if signal_types['abuse'] > 0:
            confidence += 0.3
        if signal_types['shodan'] > 0:
            confidence += 0.4
        
        return min(confidence, 1.0)
    
    def _calculate_risk_multiplier(self, patterns: list) -> float:
        """
        Calculate risk multiplier based on detected patterns.
        
        Returns:
            float: 1.0 (no multiplier) to 2.0 (maximum multiplier)
        """
        if not patterns:
            return 1.0
        
        # Average confidence of patterns
        avg_confidence = sum(p["confidence"] for p in patterns) / len(patterns)
        
        # Multiplier: 1.0 + (confidence - 1.0) = confidence
        # Clamped between 1.0 and 2.0
        multiplier = 1.0 + (avg_confidence * 1.0)
        return min(multiplier, 2.0)
    
    # ========================
    # EXPLANATION GENERATION
    # ========================
    
    def get_correlation_explanation(self) -> str:
        """
        Generate human-readable explanation of correlation analysis.
        """
        if not self.signals:
            return "No concerning signals detected in correlation analysis."
        
        explanation = f"Threat Intelligence Correlation Analysis:\n\n"
        
        # List detected signals
        explanation += f"Detected Signals ({len(self.signals)}):\n"
        for signal_name, signal_data in self.signals.items():
            explanation += f"  • {signal_data['description']}\n"
        
        # List detected patterns
        if self.signals:
            patterns = self._detect_patterns()
            if patterns:
                explanation += f"\nDetected Patterns ({len(patterns)}):\n"
                for pattern in patterns:
                    explanation += f"  • {pattern['name']} ({pattern['confidence']:.0%} confidence)\n"
        
        explanation += f"\nCorrelation Score: {self.correlation_score:.1%}\n"
        explanation += f"Analysis Confidence: {self.confidence:.1%}\n"
        
        return explanation

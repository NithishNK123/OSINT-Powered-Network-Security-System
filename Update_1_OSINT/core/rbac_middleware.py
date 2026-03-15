"""
RBAC Middleware - Role-Based Access Control
=============================================
Enforces permissions for Admin, Analyst, and Viewer roles.

Usage:
    @app.before_request
    def check_rbac():
        enforce_rbac()

    In routes:
    @require_role(['Admin'])
    def settings():
        ...
"""

from functools import wraps
from flask import session, redirect, url_for, abort

# ===============================
# ROLE DEFINITIONS & PERMISSIONS
# ===============================

ROLE_PERMISSIONS = {
    "Admin": {
        "analyze": True,
        "view_dashboard": True,
        "view_alerts": True,
        "view_history": True,
        "export_reports": True,
        "modify_settings": True,
        "enable_engines": True,
        "modify_thresholds": True,
        "view_reports": True,
    },
    "Analyst": {
        "analyze": True,
        "view_dashboard": True,
        "view_alerts": True,
        "view_history": True,
        "export_reports": True,
        "modify_settings": False,
        "enable_engines": False,
        "modify_thresholds": False,
        "view_reports": True,
    },
    "Viewer": {
        "analyze": False,
        "view_dashboard": True,
        "view_alerts": True,
        "view_history": True,
        "export_reports": False,
        "modify_settings": False,
        "enable_engines": False,
        "modify_thresholds": False,
        "view_reports": True,
    }
}


# ===============================
# ROUTE DECORATOR
# ===============================

def require_role(*allowed_roles):
    """
    Decorator to restrict routes by role.
    
    Example:
        @app.route("/settings")
        @require_role("admin")
        def settings():
            return render_template("settings.html")
        
        @app.route("/analyze")
        @require_role("analyst", "admin")
        def analyze():
            return render_template("analyze.html")
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = session.get("user")
            
            if not user:
                return redirect(url_for("login"))
            
            # Normalize role to lowercase for comparison
            user_role = user.get("role", "").lower()
            allowed_roles_lower = [r.lower() for r in allowed_roles]
            
            if user_role not in allowed_roles_lower:
                abort(403)  # Forbidden
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator


def require_permission(permission: str):
    """
    Decorator to restrict routes by permission.
    
    Example:
        @app.route("/export")
        @require_permission("export_reports")
        def export():
            return send_file(...)
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = session.get("user")
            
            if not user:
                return redirect(url_for("login"))
            
            role = user.get("role", "Viewer")
            permissions = ROLE_PERMISSIONS.get(role, {})
            
            if not permissions.get(permission, False):
                abort(403)  # Forbidden
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator


# ===============================
# PERMISSION CHECKERS (For Templates)
# ===============================

def user_has_permission(permission: str) -> bool:
    """
    Check if current user has a specific permission.
    Use in templates: {% if user_has_permission('export_reports') %}
    """
    user = session.get("user")
    if not user:
        return False
    
    role = user.get("role", "Viewer")
    permissions = ROLE_PERMISSIONS.get(role, {})
    
    return permissions.get(permission, False)


def user_has_role(role: str) -> bool:
    """
    Check if current user is a specific role.
    Use in templates: {% if user_has_role('Admin') %}
    """
    user = session.get("user")
    if not user:
        return False
    
    return user.get("role") == role


# ===============================
# ENFORCE RBAC MIDDLEWARE
# ===============================

def enforce_rbac(app):
    """
    Register RBAC middleware globally on the Flask app.
    
    Usage in app.py:
        from core.rbac_middleware import enforce_rbac
        enforce_rbac(app)
    """
    @app.before_request
    def check_user_session():
        # Ensure user is in session
        if "user" not in session:
            session["user"] = {
                "name": "SOC Analyst",
                "role": "Analyst"  # Default role
            }
        
        # Make permissions available to templates
        user_role = session["user"].get("role", "Viewer")
        return None  # Continue to route


# ===============================
# TEMPLATE CONTEXT INJECTION
# ===============================

def inject_rbac_context():
    """
    Inject RBAC helpers into all templates.
    
    Usage in app.py:
        @app.context_processor
        def inject_rbac():
            return {
                'user_has_permission': user_has_permission,
                'user_has_role': user_has_role,
                'ROLE_PERMISSIONS': ROLE_PERMISSIONS
            }
    """
    return {
        'user_has_permission': user_has_permission,
        'user_has_role': user_has_role,
        'ROLE_PERMISSIONS': ROLE_PERMISSIONS
    }

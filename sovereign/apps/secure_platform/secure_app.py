import hashlib, hmac, secrets, json
from datetime import datetime

class SecurePrivatePlatform:
    '''Privacy-First RBAC, Session Management & Data Security Engine.'''
    def __init__(self, secret_key=None):
        self.secret_key = secret_key or secrets.token_hex(32)
        self.sessions = {}

    def hash_password(self, password, salt=None):
        salt = salt or secrets.token_hex(16)
        hashed = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
        return salt, hashed.hex()

    def create_session(self, user_id, role="ANALYST"):
        token = secrets.token_urlsafe(32)
        self.sessions[token] = {
            "user_id": user_id,
            "role": role,
            "created_at": datetime.now().isoformat()
        }
        return token

    def verify_permission(self, session_token, required_role="ADMIN"):
        sess = self.sessions.get(session_token)
        if not sess: return False, "SESSION_EXPIRED_OR_INVALID"
        
        role_hierarchy = {"GUEST": 0, "ANALYST": 1, "MANAGER": 2, "ADMIN": 3}
        user_level = role_hierarchy.get(sess["role"], 0)
        req_level = role_hierarchy.get(required_role, 3)
        
        if user_level >= req_level:
            return True, "AUTHORIZED"
        return False, "FORBIDDEN_INSUFFICIENT_PRIVILEGES"

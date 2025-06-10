import random
import json
import time

from app.core.redis.redis_client import redis_client

class OTPService:
    OTP_TTL_SECONDS = 300  

    @staticmethod
    def generate_otp():
        return str(random.randint(100000, 999999))

    @staticmethod
    def set_otp(identity, role, otp):
        redis_key = f"reset_otp:{role}:{identity}"
        data = {
            "otp": otp,
            "created_at": int(time.time())
        }
        redis_client.setex(redis_key, OTPService.OTP_TTL_SECONDS, json.dumps(data))

    @staticmethod
    def get_otp(identity, role):
        redis_key = f"reset_otp:{role}:{identity}"
        data = redis_client.get(redis_key)
        if not data:
            return None
        return json.loads(data)

    @staticmethod
    def delete_otp(identity, role):
        redis_key = f"reset_otp:{role}:{identity}"
        redis_client.delete(redis_key)

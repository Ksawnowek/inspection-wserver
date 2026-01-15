from typing import Any

from app.models.models import Uzytkownik
from app.repositories.users_repo import UserRepo
import bcrypt
from app.core.config import settings
from datetime import datetime, timezone, timedelta
from jose import JWTError, jwt

class AuthService:
    def __init__(self, repo: UserRepo):
        self.repo = repo
    
    def auth_user(self, login, pwd):
        user = self.repo.get_by_login(login)
        if user is None:
            return None
        hashed_from_db_bytes = user.UZT_pwd.strip().encode('utf-8')
        password_attempt_bytes = pwd.encode('utf-8')
        if bcrypt.checkpw(password_attempt_bytes, hashed_from_db_bytes):
            token_data = {"sub": user.UZT_Login}
            token = self._create_access_token(data=token_data)
            return token
        else:
            return None

    def create_access_token_by_login(self, login: str):
        return self._create_access_token(
            data={"sub": login} )

    def _create_access_token(self, data: dict):
        data["type"] = "access"
        to_encode = data.copy()

        expire = datetime.now(timezone.utc) + timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.TOKEN_ALGORITHM)
        return encoded_jwt



    def register_user(self, login, imie, nazwisko, pwd, rola):
        from sqlalchemy.exc import IntegrityError

        # 1. WALIDACJA: Sprawdź czy login już istnieje
        existing_user = self.repo.get_by_login(login)
        if existing_user:
            raise ValueError(f"Użytkownik o loginie '{login}' już istnieje w systemie")

        # 2. Hash hasła i utwórz użytkownika
        passwordHash = self.hash_pwd(pwd)
        user = Uzytkownik(
            UZT_Imie=imie,
            UZT_Nazwisko=nazwisko,
            UZT_Login=login,
            UZT_pwd=passwordHash,
            UZT_ROL_Id=rola
        )

        # 3. Zapisz do bazy z obsługą błędów
        try:
            result = self.repo.add_user(user)
            return result
        except IntegrityError as e:
            # Backup na wypadek race condition (dwóch użytkowników dodaje tego samego loginu jednocześnie)
            error_msg = str(e.orig) if hasattr(e, 'orig') else str(e)

            if 'UZT_Login' in error_msg or 'UNIQUE' in error_msg or 'unique constraint' in error_msg.lower():
                raise ValueError(f"Użytkownik o loginie '{login}' już istnieje w systemie")
            else:
                # Inny błąd integrity (np. FK violation)
                raise ValueError(f"Błąd podczas tworzenia użytkownika: Naruszenie integralności danych")

    def validate_and_decode_token(self, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.TOKEN_ALGORITHM)
            username: str = payload.get("sub")
            if username is None:
                return None
        except JWTError:
            return None
        user = self.repo.get_by_login(username)
        if user is None:
            return None

        return user

    # def get_role(self, role_id):
    #     return self.repo.get_role_name(role_id)

    def create_refresh_token(self, login: str):
        data: dict[str, Any] = {
            "login": login,
            "type": "refresh"
        }
        to_encode = data.copy()

        expire = datetime.now(timezone.utc) + timedelta(minutes=int(settings.REFRESH_TOKEN_EXPIRE_DAYS) * 24 * 60)
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, settings.REFRESH_SECRET_KEY, algorithm=settings.TOKEN_ALGORITHM)
        return encoded_jwt

    def hash_pwd(self, password):
        return  bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
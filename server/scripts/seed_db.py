import os
import sys
from uuid import uuid4
from sqlalchemy.orm import Session

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.core.db import SessionLocal, engine, Base
from app.core.security import hash_password
from app.models import User


def add_initial_user():
    print("Verificando/criando tabelas no banco de dados...")
    Base.metadata.create_all(bind=engine) 

    db: Session = SessionLocal()
    try:
        existing_user = db.query(User).filter(User.email == "teste@planit.ai").first()

        if existing_user:
            print(f"Usuário 'teste@planit.ai' já existe com ID: {existing_user.uuid}. Nenhuma ação necessária.")
            return existing_user.uuid

        user_uuid = str(uuid4())
        print(f"\nGerando um novo usuário de teste com ID: {user_uuid}")

        new_user = User(
            uuid=user_uuid,
            name="Usuário de Teste Planit",
            nickname="Testador",
            email="teste@planit.ai",
            hashed_password=hash_password("senhaforte123"),
            is_active=True
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        print(f"Usuário '{new_user.name}' ({new_user.email}) adicionado com sucesso ao DB local!")
        print(f"UUID do Usuário de Teste: {new_user.uuid}\n")
        return new_user.uuid
    except Exception as e:
        db.rollback()
        print(f"Erro ao adicionar usuário de teste: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    add_initial_user()

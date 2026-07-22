# backend/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Definição do caminho e nome do banco de dados SQLite
# O banco será criado na raiz do diretório backend como 'controltask.db'
# e pode ser sobrescrito por uma variável de ambiente para testes.
DATABASE_URL = os.getenv(
    "CONTROLTASK_DATABASE_URL",
    os.getenv("DATABASE_URL", "sqlite:///./backend/controltask.db"),
)

# 2. Criação do Engine de Conexão
# O argumento 'check_same_thread=False' é uma boa prática mandatória para o SQLite 
# funcionar corretamente com o ecossistema assíncrono do FastAPI.
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# 3. Configuração do Criador de Sessões (Session Factory)
# autoflush=False: evita que o SQLAlchemy envie alterações parciais ao banco antes do commit manual
# autocommit=False: garante o controle transacional (nós decidimos quando salvar com db.commit())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Classe Base para o Mapeamento Objeto-Relacional (ORM)
# Todos os nossos modelos (User, Task) herdarão desta classe Base para serem mapeados nas tabelas
Base = declarative_base()

# 5. Função de Injeção de Dependência (Dependency Injection)
# Esta função será utilizada pelo FastAPI para fornecer uma sessão de banco limpa
# para cada requisição HTTP e fechá-la automaticamente ao final.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# backend/models.py

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

# Ajustado: Importando a Base utilizando o caminho absoluto do pacote backend
from backend.database import Base

class User(Base):
    """
    Modelo ORM para a tabela de Usuários (users).
    Armazena as credenciais de acesso e informações de perfil.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # Relacionamento: Permite acessar as tarefas do usuário via 'user.tasks'
    # 'cascade="all, delete-orphan"' garante que se o usuário for deletado, 
    # todas as suas tarefas serão apagadas automaticamente do banco.
    tasks = relationship("Task", back_populates="owner", cascade="all, delete-orphan")

class Task(Base):
    """
    Modelo ORM para a tabela de Tarefas (tasks).
    Armazena os dados das tarefas vinculadas a cada usuário.
    """
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True) # Pode ser nulo até a IA ou o usuário preencher
    priority = Column(String(10), nullable=False) # 'LOW', 'MEDIUM', 'HIGH'
    status = Column(String(20), nullable=False, default="PENDING") # 'PENDING', 'IN_PROGRESS', 'COMPLETED'
    created_at = Column(DateTime, server_default=func.now())

    # Relacionamento: Permite saber quem é o dono da tarefa via 'task.owner'
    owner = relationship("User", back_populates="tasks")

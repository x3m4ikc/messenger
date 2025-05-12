import enum
from sqlalchemy import Column, String, TIMESTAMP, func, select, update, delete, Integer, Enum, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import mapped_column, Mapped, relationship

from messenger.database.engine import Base, metadata


class ChatTypes(enum.Enum):
    PRIVATE = 'PRIVATE'
    GROUP = 'GROUP'


class BaseModel(Base):
    __abstract__ = True
    __metadata__ = metadata


class Users(BaseModel):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)

    created_groups = relationship("Group", back_populates="creator")
    messages = relationship("Message", back_populates="sender")
    chat_memberships = relationship("ChatMember", back_populates="user")


class Chats(BaseModel):
    __tablename__ = 'chats'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    type: Mapped[ChatTypes] = mapped_column(Enum(ChatTypes), default=ChatTypes.PRIVATE)

    messages = relationship("Message", back_populates="chat")
    members = relationship("ChatMember", back_populates="chat")
    group_info = relationship("Group", back_populates="chat", uselist=False)


class Groups(BaseModel):
    __tablename__ = 'groups'

    id: Mapped[int] = mapped_column(ForeignKey('chats.id'), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    creator_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    chat = relationship("Chat", back_populates="group_info")
    creator = relationship("User", back_populates="created_groups")


# Добавил от себя таблицу chat_members для более удобного управления участниками групповых чатов
class ChatMembers(BaseModel):
    __tablename__ = 'chat_members'

    chat_id: Mapped[int] = mapped_column(ForeignKey('chats.id'), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)

    chat = relationship("Chat", back_populates="members")
    user = relationship("User", back_populates="chat_memberships")


class Messages(BaseModel):
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey('chats.id'))
    sender_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    text: Mapped[str] = mapped_column(String(1000), nullable=False)
    timestamp: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, server_default=func.now())
    is_read: Mapped[bool] = mapped_column(default=False)

    chat = relationship("Chat", back_populates="messages")
    sender = relationship("User", back_populates="messages")

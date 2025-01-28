# from app.core.database import Base
# from sqlalchemy import String, Text
# from sqlalchemy.orm import Mapped, mapped_column
# from .mixins import UserRelationShipMixins


# class Task(UserRelationShipMixins, Base):
#     _user_back_populates = 'task'

#     title: Mapped[str] = mapped_column(String(100), index=True)
#     body: Mapped[str] = mapped_column(Text, default="", server_default="")

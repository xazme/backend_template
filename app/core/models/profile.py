# from typing import TYPE_CHECKING
# from app.core.database import Base
# from sqlalchemy.orm import Mapped, mapped_column
# from sqlalchemy import String, ForeignKey
# from .mixins import UserRelationShipMixins

# # if TYPE_CHECKING:
# from .user import User


# class Profile(Base, UserRelationShipMixins):

#     _user_back_populates = 'profile'

#     name: Mapped['User'] = mapped_column(ForeignKey('user.name'))
#     first_name: Mapped[str | None] = mapped_column(String(30))
#     second_name: Mapped[str | None] = mapped_column(String(30))
#     bio: Mapped[str | None] = mapped_column(String(300))

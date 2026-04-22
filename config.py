"""

If you have a shared config for your settings, then you can import it here.
Otherwise, uncomment and set up values of the snippet below.
Alternatively, you can set it up on your docker-compose.

"""

from pydantic_settings import BaseSettings
# from shared_lib.shared_config import shared_settings
# settings = shared_settings



class DBSettings(BaseSettings):
    DB_USER: str = "user"
    DB_PASSWORD: str = "password"
    DB_HOST: str = "mysql"
    DB_PORT: int = 3306
    DB_NAME: str = "my_db"
    DB_CHARSET: str = 'utf8mb4'
    DB_COLLATE: str = 'utf8mb4_general_ci'

    #Setting this to true will drop and reset your whole database
    RESET_DB: bool = False

    def create_db_base_url(self) -> str:
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}?charset={self.DB_CHARSET}&collation={self.DB_COLLATE}"

    def create_db_url(self) -> str:
        return f"mysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?charset={self.DB_CHARSET}&collation={self.DB_COLLATE}"

settings = DBSettings()

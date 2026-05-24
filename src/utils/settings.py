from pydantic_settings import SettingsConfigDict,BaseSettings

class Settings(BaseSettings): 
    model_config=SettingsConfigDict(env_file='.env',extra='ignore')

    connection_string: str
    EXP_TIME: int
    ALGORITHM: str
    SECRET_KEY:str
    

    
settings = Settings()
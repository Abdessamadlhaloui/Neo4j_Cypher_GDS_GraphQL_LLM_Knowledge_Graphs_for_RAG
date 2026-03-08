from dotenv import load_dotenv 
import os 


load_dotenv()

class Settings : 
    
    def __init__(self) : 
        self.xai_api_key = os.getenv("XAI_API_KEY","")
        self.neo4j_uri = os.getenv("NEO4J_URI","bolt://localhost:7687")
        self.neo4j_user = os.getenv("NEO4J_USER","neo4j")
        self.neo4j_password = os.getenv("NEO4J_PASSWORD","")
        self.xai_model = os.getenv("XAI_MODEL","grok-beta")
        self.max_tokens = int(os.getenv("MAX_TOKENS","1000"))
        
    def validate(self) : 
        if not self.xai_api_key : raise ValueError("XAI API KEY missing !!")
        if not self.neo4j_password : raise ValueError("PASSWORD missing")
        

settings = Settings() 
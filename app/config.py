

class Config:
    MODEL_NAME:str = None
    PIPELINE:str = None
    
    MODEL:any = None
    TOKENIZER:any = None

    def __str__(self) -> str:
        return f"Config( MODEL:{self.MODEL} | PIPELINE: {self.PIPELINE})"

CONFIG = Config()
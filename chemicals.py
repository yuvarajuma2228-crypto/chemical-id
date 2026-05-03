from pydantic import BaseModel

class item(BaseModel):
    sno: int
    name: str
    formula: str
    mw: float
    bp: float

    

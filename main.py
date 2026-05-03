from fastapi import Depends,FastAPI
from chemicals import item
from database import session ,engine
import dbmodels
from sqlalchemy.orm import Session


dbmodels.Base.metadata.create_all(bind=engine)

app = FastAPI()

chemi = [
    item(sno=1,name="water",formula="H2O",mw=18.015,bp=373.12),
    item(sno=2,name="hydrogen",formula="H",mw=1,bp=100),
    item(sno=3,name="oxygen",formula="O",mw=16,bp=109),
    item(sno=4,name="carbon dioxide",formula="CO2",mw=44.01,bp=194.67),
    item(sno=5,name="methane",formula="CH4",mw=16.04,bp=111.66),
    item(sno=6,name="ethanol",formula="C2H5OH",mw=46.07,bp=351.44),
    item(sno=7,name="sodium chloride",formula="NaCl",mw=58.44,bp=1413)

]

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db = session()
    count = db.query(dbmodels.CHEMICAL).count()
    if count == 0:
        for item in chemi:
            db.add(dbmodels.CHEMICAL(**item.model_dump()))  
        db.commit()


init_db()

@app.get('/chemicals')
def getchemicals(db: Session = Depends(get_db)):
    db_chemicals = db.query(dbmodels.CHEMICAL).all()
    return db_chemicals

@app.get('/chemical/{sno}')
def getchemical(sno: int, db: Session = Depends(get_db)):
    chemical: dbmodels.CHEMICAL | None = db.query(dbmodels.CHEMICAL).filter(dbmodels.CHEMICAL.sno == sno).first()
    if chemical:
         return chemical
    return {"error": "Chemical not found"}


@app.post('/chemical')
def addchemical(chemical: item,db: Session = Depends(get_db)):
    db.add(dbmodels.CHEMICAL(**chemical.model_dump()))
    db.commit()
    return chemical

@app.put('/chemical')
def updatechemical(sno: int, updated_chemical: item, db: Session = Depends(get_db)):
    chemical: dbmodels.CHEMICAL | None = db.query(dbmodels.CHEMICAL).filter(dbmodels.CHEMICAL.sno == sno).first()
    if chemical:
        chemical.name = updated_chemical.name
        chemical.formula = updated_chemical.formula
        chemical.mw = updated_chemical.mw
        chemical.bp = updated_chemical.bp
        db.commit()
        return chemical
    else:
        return {"error": "Chemical not found"}

@app.delete('/chemical')
def deletechemical(sno: int, db: Session = Depends(get_db)):
    chemical: dbmodels.CHEMICAL | None = db.query(dbmodels.CHEMICAL).filter(dbmodels.CHEMICAL.sno == sno).first()
    if chemical:
        db.delete(chemical)
        db.commit()
        return {"message": "Chemical deleted"}
    
    else:  
        return {"error": "Chemical not found"}



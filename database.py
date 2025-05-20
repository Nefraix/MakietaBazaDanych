from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from models import Base, IQRF, Group, Command, Situation, Intersection

DATABASE_URL = "sqlite:///./items.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

@event.listens_for(engine, "connect")
def enable_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

''' Listy IQRFów i Grup, stan domyślny bazy: '''

groups = [
    #Group(id=0, description="Nie istnieje"),
    #Group(id=1, description="Nie istnieje"),
    #Group(id=2, description="Nie istnieje"),
    #Group(id=3, description="Nie istnieje"),
    #Group(id=4, description="Nie istnieje"),
    #Group(id=5, description="Nie istnieje"),
    #Group(id=6, description="Nie istnieje"),
    #Group(id=7, description="Nie istnieje"),
    #Group(id=8, description="Nie istnieje"),
    #Group(id=9, description="Nie istnieje"),
    Group(id=99, description="Nie istnieje"),
]

commands = [
    Command(id=0, name="Automatyczna jazda w prawo", code="0001"),
    Command(id=1, name="Automatyczna jazda w lewo", code="0002"),
    Command(id=2, name="Blokada poruszania się w prawo", code="0003"), 
    Command(id=3, name="Blokada poruszania się w lewo", code="0004"),
    Command(id=4, name="Ustaw prędkość na", code="0005"),
    Command(id=5, name="Zmień prędkość o", code="0006"),
    Command(id=6, name="Stopniowe zatrzymanie się", code="0007"),
    Command(id=7, name="Nagłe zatrzymanie się", code="0008"),
    Command(id=8, name="Blokada parkowania", code="0009"),
]

situations = [
    Situation(id=0, name="Ostrzeżenie", code="0000"),
    Situation(id=1, name="Droga prosta", code="0001"),
    Situation(id=2, name="Łuk", code="0002"),
    # Skrzyżowanie potrójne
    Situation(id=3, name="Skrzyzowanie potrojne Zjazd nr.1 ", code="0003"),
    Situation(id=4, name="Skrzyzowanie potrojne Zjazd nr.2", code="0004"),
    Situation(id=5, name="Skrzyzowanie potrojne Zjazd nr.3", code="0005"),
    Situation(id=6, name="Skrzyzowanie potrojne Zjazd nr.4", code="0006"),
    # Skrzyżowanie poczwórne
    Situation(id=7, name="Skrzyzowanie poczworne Zjazd nr.1", code="0007"),
    Situation(id=8, name="Skrzyzowanie poczworne Zjazd nr.2", code="0008"),
    Situation(id=9, name="Skrzyzowanie poczworne Zjazd nr.3", code="0009"),
    Situation(id=10, name="Skrzyzowanie poczworne Zjazd nr.4", code="000A"),
    # Miejsca parkingowe
    Situation(id=11, name="Miejsce parkingowe 1", code="000B"),
    Situation(id=12, name="Miejsce parkingowe 2", code="000C"),
    Situation(id=13, name="Miejsce parkingowe 3", code="000D"),
    Situation(id=14, name="Miejsce parkingowe 4", code="000E"),
    Situation(id=15, name="Miejsce parkingowe 5", code="000F"),
    Situation(id=16, name="Miejsce parkingowe 6", code="0010"),
    Situation(id=17, name="Miejsce parkingowe 7", code="0011"),
    Situation(id=18, name="Miejsce parkingowe 8", code="0012"),
    Situation(id=19, name="Miejsce parkingowe 9", code="0013"),
    Situation(id=20, name="Miejsce parkingowe 10", code="0014"),
    # Rondo potrójne
    Situation(id=21, name="Rondo potrojne Zjazd nr.1", code="0015"),
    Situation(id=22, name="Rondo potrojne Zjazd nr.2", code="0016"),
    Situation(id=23, name="Rondo potrojne Zjazd nr.3", code="0017"),
    Situation(id=24, name="Rondo potrojne Zjazd nr.4", code="0018"),
    # Rondo poczwórne
    Situation(id=25, name="Rondo poczworne Zjazd nr.1", code="0019"),
    Situation(id=26, name="Rondo poczworne Zjazd nr.2", code="001A"),
    Situation(id=27, name="Rondo poczworne Zjazd nr.3", code="001B"),
    Situation(id=28, name="Rondo poczworne Zjazd nr.4", code="001C"),
]

intersections = [
    Intersection(id = 0, name="Skrzyzowanie potrojne"),
    Intersection(id = 1, name="Skrzyzowanie poczworne"),
    Intersection(id = 2, name="Rondo potrojne"),
    Intersection(id = 3, name="Rondo poczworne"),
    Intersection(id = 99, name="TEST testowy"),
]


iqrfs = [
    IQRF(id=9999, group=99,intersection=99,priority=1,lights=0, description="Nie istnieje, rekord testowy"),
    IQRF(id=9998, group=99,intersection=99, priority=5,lights=0, description="Nie istnieje, rekord testowy"),

]

def init_db():
    
    "Uncomment to generate DB from 0 using above cells"
    #Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    


    if not db.query(Group).first():
        db.add_all(groups)

    if not db.query(Intersection).first():
        db.add_all(intersections)
        
    if not db.query(Command).first():
        db.add_all(commands)
    
    if not db.query(Situation).first():
        db.add_all(situations)
        
    if not db.query(IQRF).first():
        db.add_all(iqrfs)
        
    db.commit()
    db.close()

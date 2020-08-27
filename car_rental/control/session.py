from sqlalchemy.orm import sessionmaker


def create_session(db):
    session = sessionmaker(bind=db.engine)
    return session()

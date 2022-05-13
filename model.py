from enum import unique
from operator import index
import psycopg2
from sqlalchemy import column, create_engine, Column, Integer, String, PrimaryKeyConstraint, ForeignKey, true
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative  import declarative_base

engine = create_engine('postgresql://postgres:res101992@localhost:5432/owl_control')

db_session  = scoped_session(sessionmaker(autocommit = False,
                                            bind = engine))

Base = declarative_base()
Base.query = db_session.query_property()

class Master(Base):
    __tablename__ = 'master'
    id = Column(Integer, primary_key = True)
    master = Column(String(40), index = True)
    login = Column(String(40), index = True)
    senha = Column(String(40), index = True)

    def __repr__(self):
        return '<Master {}'.format(self.id)
    
    def save(self):
        db_session.add(self)
        db_session.commit()
    
    def delete(self):
        db_session.delete(self)
        db_session.commit()
        

class Supervisor(Base):
    __tablename__ = 'supervisor'
    id = Column(Integer, primary_key = True)
    supervisor = Column(String(40), index = True)
    login = Column(String(40), index = True)
    senha = Column(String(40), index = True)

    def __repr__(self):
        return '<Supervisor {}'.format(self.id)
    
    def save(self):
        db_session.add(self)
        db_session.commit()
    
    def delete(self):
        db_session.delete(self)
        db_session.commit()


class Usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key = True)
    usuario = Column(String(40), index = True)
    login = Column(String(40), index = True)
    senha = Column(String(40), index = True)

    def __repr__(self):
        return '<Usuario {}'.format(self.id)
    
    def save(self):
        db_session.add(self)
        db_session.commit()
    
    def delete(self):
        db_session.delete(self)
        db_session.commit()


class Read(Base):
    __tablename__ = 'read'
    id = Column(Integer, primary_key = True)
    id_firebase = Column(String(6), index = True,unique = True)
    comando_front = Column(String(10), index = True)
    running_fw = Column(Integer, index = True)
    update_to = Column(Integer, index = True)
    vibra_sensivity = Column(Integer, index = True)
    
    def save(self):
        db_session.add(self)
        db_session.commit()
    
    def delete(self):
        db_session.delete(self)
        db_session.commit()



class Senha(Base):
    __tablename__ = 'senha'
    id = Column(Integer, primary_key = True)
    id_firebase = Column(String(6), index = True,unique = True)
    senha_1 = Column(String(30), index = True)
    
    def save(self):
        db_session.add(self)
        db_session.commit()
    
    def delete(self):
        db_session.delete(self)
        db_session.commit()


class Status(Base):
    __tablename__ = 'status'
    id = Column(Integer, primary_key = True)
    id_firebase = Column(String(6), index = True,unique = True)
    status = Column(Integer, index = True)
    
    def save(self):
        db_session.add(self)
        db_session.commit()
    
    def delete(self):
        db_session.delete(self)
        db_session.commit()

class Write(Base):
    __tablename__ = 'write'
    id = Column(Integer, primary_key = True)
    id_firebase = Column(String(6), index = True,unique = True)
    senha_1 = Column(String(30), index = True)
    value = Column(String(100), index = True)
    
    def save(self):
        db_session.add(self)
        db_session.commit()
    
    def delete(self):
        db_session.delete(self)
        db_session.commit()



def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    init_db()
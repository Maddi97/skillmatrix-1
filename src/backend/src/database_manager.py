import parentdir
from flask import Flask, json, request, redirect
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Momomomo2@localhost/sm1'
api = Api(app)
db = SQLAlchemy(app)

def handle_query(self, query):
    #Accepts the query from REST-API and hands it to database_handler, returns JSON
    results = database_handler.search(self,query)
    if(results is None):
         raise ValueError
    return json.dumps(results)
    

class database_handler:
    '''Class to handle everything about table-manipulation'''
    def add_skill(self, skill1, level1):
        '''Adds skill to database.'''
        object_name = skill(name = skill1, level = level1)
        db.session.add(object_name)
        db.session.commit()

    def add_user(self, username1):
        '''Adds user to database. #Place is optional and is NULL if not given.'''
        #works
        object_name = users(username = username1)
        db.session.add(object_name)
        db.session.commit()

    #def change_user(self, username1, surname1, forename1, place1= None):
        #'''Changes a colum of the users-table, based on the username (the username is ad-given and can not be changed here).'''
        #works
        #update_this = users.query.filter_by(username = username1).first()
        #update_this.surname = surname1
        #update_this.forename = forename1
        #if place1 != NULL:
        #    update_this.place = place1
        #db.session.commit()

    
    def clear_database(self):
        '''Destroys the whole tablestructure and builds a new one with empty colums. For professionals only'''
        #works
        db.drop_all()
        db.create_all()

    def delete_user(self, username1):
        '''Deletes a colum of the users-table, based on the given username.'''
        #works
        delete_this = users.query.filter_by(username = username1).first()
        db.session.delete(delete_this)
        db.session.commit()

    def search(self, query):
        alistlevel = []
        #lsite aller level
        alistname = []
        #liste aller usernamen
        data = skill.query.filter_by(name = query).all()
        for skill1 in data:
            alistlevel.append(skill1.give_level())
            for users1 in skill1.has_user:
                alistname.append(users1.give_name())

        name_skilllevel = zip(alistname, alistlevel)
        name_skilllevel_dict = dict(name_skilllevel)
        #dict von Usernames in Verbindung mit Skilllevel
        big_dict = dict(skill= query,result= name_skilllevel_dict)
        #print(big_dict)
        return big_dict
        



class Association(db.Model):
    __tablename__ = 'association'
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'), primary_key=True)
    level = db.Column(db.Integer, nullable=False)
    time_id = db.Column(db.Integer, db.ForeignKey('time.id'), nullable=False)
    milestone_id = db.Column(db.Integer, db.ForeignKey('milestone.id'), nullable=True)
    users_assoc = db.relationship("Users", back_populates="users_association")
    skill_assoc = db.relationship("Skill", back_populates="skill_association")
    time_assoc = db.relationship("Time", back_populates="time_association")
    milestone_assoc = db.relationship("Milestone", back_populates="milestone_association")
    #parent = relationship("Parent", back_populates="children")

user_skill = db.Table('user_skill',
    db.Column('Users_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('Skill_id', db.Integer, db.ForeignKey('skill.id')))

class Time(db.Model):
    '''SQL-Alchemy object time.'''
    __tablename__ = 'time'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, nullable=True, default=datetime.datetime.utcnow())
    time_association = db.relationship("Association", back_populates="time_assoc")
    #z.B. '9999-12-12 22:58:58'

class Milestone(db.Model):
    '''SQL-Alchemy object milestone.'''
    __tablename__ = 'milestone'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    time = db.Column(db.DateTime, nullable=True, default=datetime.datetime.utcnow())
    milestone_association = db.relationship("Association", back_populates="milestone_assoc")
    #z.B. '9999-12-12 22:58:58'
    description = db.Column(db.Text, nullable=True)

class Users(db.Model):
    '''SQL-Alchemy object users. Has an autoincremented id, an username, a surname, a forename and a place which can be NULL'''
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), nullable=False)
    #surname = db.Column(db.String(45), nullable=False)
    #forename = db.Column(db.String(45), nullable=False)
    #place = db.Column(db.String(45), nullable=True)
    #has_skill = db.relationship('Skill', secondary=user_skill, backref=db.backref('has_user', lazy = 'dynamic'))
    users_association = db.relationship("Association", back_populates="users_assoc")

    def give_name(self):
        return self.username

    def __repr__(self):
        return '<id = {0} und username = {1}>'.format(self.id, self.username)



class Skill(db.Model):
    __tablename__ = 'skill'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(127), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    skill_association = db.relationship("Association", back_populates="skill_assoc")
    #description = db.Column(db.Text, nullable=True)
    
    def give_level(self):
        return self.level

    def __repr__(self):
        return '<name {0} und level {1}>'.format(self.name, self.level) 

class Session(db.Model):
    __tablename__ = 'session'
    id = db.Column(db.Integer, primary_key=True)
    val = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<id {0}>'.format(self.id) 


class HelloWorld(Resource):
    dbh = database_handler()
    dbh.clear_database()
    Valdemar = Users(username='Valdemar-Forsberg')
    Karl = Users(username='Karl.Kalagin')
    Isaac = Users(username='Isaac.Hunt')
    Ozoemena = Users(username='Ozoemena.Somayina')
    Yvonne = Users(username='Yvonne.Thompsome')
    
    db.session.add(Valdemar)
    db.session.add(Karl)
    db.session.add(Isaac)
    db.session.add(Ozoemena)
    db.session.add(Yvonne)
    java1 = Skill(name = 'Java', level = 5)
    java2 = Skill(name = 'Java', level = 2)
    java3 = Skill(name = 'Java', level = 3)
    python1 = Skill(name = 'Python', level = 4)
    python2 = Skill(name = 'Python', level = 3)
    js1 = Skill(name = 'JavaScript', level = 4)
    js2 = Skill(name = 'JavaScript', level = 2)
    js3 = Skill(name = 'JavaScript', level = 1)
    db.session.add(java1)
    db.session.add(java2)
    db.session.add(java3)
    db.session.add(python1)
    db.session.add(python2)
    db.session.add(js1)
    db.session.add(js2)
    db.session.add(js3)
    
    time1 = Time()
    db.session.add(time1)
    milestone1 = Milestone(name = 'hackaton', description = 'war ganz nice. die Jungs von der Uni hatten aber keine Ahnung')
    milestone2 = Milestone(name = 'profie.de.com testingcup', time = '9999-12-12 22:58:58', description = 'mit testen hatte das nichts zu tun. braten war aber nice')
    db.session.add(milestone1)
    db.session.add(milestone2)
    a = Association(level = 9001)

    a.skill_assoc= js3
    a.time_assoc= time1
    a.milestone_assoc= milestone2
    Valdemar.users_association.append(a)

    db.session.commit()

    #data = users.query.filter_by(username = 'willy1').all()
    data = Users.query.all()
    #data = dbh.search('schnell_laufen')

    def get(self):
        sotr = ''.join(str(e) for e in self.data)
        return {'results' : sotr}, 201

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run()
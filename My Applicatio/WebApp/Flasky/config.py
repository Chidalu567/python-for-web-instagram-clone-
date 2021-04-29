import os

basedir=os.path.abspath(os.path.dirname(__file__)); #get the absolute path of file

class Config: #class definition
    SECRET_KEY='This is well encrypted';
    SQLALCHEMY_TRACK_MODIFICATIONS=False;
    FLASKY_POST_PER_PAGE=4;

    @staticmethod
    def init_app(app): #function definition
        pass;

class DevelopmentConfig(Config): #chilf class definitin
    Debug=True;
    SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir,'data-devss');

class ProductionConfig(Config): #child class definition
    SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir,'pro-data');


config={'development':DevelopmentConfig,'production':ProductionConfig,'default':DevelopmentConfig};

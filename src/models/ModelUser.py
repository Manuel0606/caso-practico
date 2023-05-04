from .entities.User import User

from flask import flash

class ModelUser():
    
    @classmethod
    def login(self, db, user):
        try:
            cursor = db.cursor()
            sql = """SELECT id, email, password FROM users
                        WHERE email = '{}'""".format(user.email)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                user = User(row[0], row[1], User.check_password(row[2], user.password), 0)
                return user
            else: 
                return None
        except Exception as ex:
            flash('Error: ', ex)
            raise Exception(ex)
    
    @classmethod
    def get_by_id(self, db, id):
        try:
            cursor = db.cursor()
            sql = """SELECT id, email, nombre FROM users
                        WHERE id = {}""".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return User(row[0], row[1], None, row[2])
            else: 
                return None
        except Exception as ex:
            flash('Error: ', ex)
            raise Exception(ex)
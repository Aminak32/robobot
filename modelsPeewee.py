import peewee
from peewee import *

db = peewee.SqliteDatabase('robobot.db')


# class BaseModel(peewee.Model):
#     class Meta:
#         database = db

########################################################################
class Profile(peewee.Model):
    """
    ORM model of the profile table
    """
    id = peewee.PrimaryKeyField()
    name = peewee.TextField()
    selected_location = peewee.TextField()
    selected_sub_location = peewee.TextField()
    selected_post_url = peewee.TextField()
    active = peewee.IntegerField()

    # def __str__(self):
    #     return "({0})".format(self.id)
    class Meta:
        database = db


########################################################################
class ProfilePicker(peewee.Model):
    """
    ORM model of the profilepicker table
    """
    id = peewee.PrimaryKeyField()
    profile_id = peewee.ForeignKeyField(Profile)
    order = peewee.IntegerField()
    url = peewee.TextField()
    selected_value = peewee.TextField()

    # def __str__(self):
    #     return "({0})".format(self.id)
    class Meta:
        database = db


########################################################################
class Proxy(peewee.Model):
    """
    ORM model of the proxy table
    """
    id = peewee.PrimaryKeyField()
    ip = peewee.TextField()
    port = peewee.TextField()
    type = peewee.TextField()
    active = peewee.IntegerField()

    # def __str__(self):
    #     return "({0})".format(self.id)
    class Meta:
        database = db


########################################################################
class Location(peewee.Model):
    """
    ORM model of the location table
    """
    id = peewee.PrimaryKeyField()
    location = peewee.TextField()
    sub_location = peewee.TextField()
    active = peewee.IntegerField()

    # def __str__(self):
    #     return "({0})".format(self.id)
    class Meta:
        database = db


if __name__ == "__main__":
    Profile.create_table()
    ProfilePicker.create_table()
    Proxy.create_table()
    Location.create_table()

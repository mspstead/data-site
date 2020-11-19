from app import db

class MapPhotos(db.Model):

    __tablename__ = 'MapPhotos'
    MapPhotoID = db.Column(db.Integer, primary_key=True)
    PhotoURL = db.Column(db.String(), unique=True, nullable=False)
    DateTaken = db.Column(db.String())
    Latitude = db.Column(db.Float, nullable=False)
    Longitude = db.Column(db.Float, nullable=False)

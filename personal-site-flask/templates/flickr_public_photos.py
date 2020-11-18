import requests as req
import time

class Flickr_Grabber:

    def __init__(self, flickr_api_key, flickr_user_id):

        self.flickr_api_key = flickr_api_key
        self.flickr_user_id = flickr_user_id

    def get_public_user_photos(self):
        """
        Returns all a user's public photos and the photo location data.
        :return: [{url:url,lat:lat,lon:lon}]
        :return: [] on failure
        """

        flickr_public_photos_url = "https://www.flickr.com/services/rest/?method=flickr.people.getPublicPhotos&api_key="\
                           +self.flickr_api_key\
                           +"&user_id="+\
                            self.flickr_user_id\
                           +"&format=json&nojsoncallback=1"
        try:

            public_photos = req.get(flickr_public_photos_url).json().get('photos')
            num_pages = public_photos.get('pages')
            photos = []

            if num_pages<=1:

                photo_list = public_photos.get('photo')

                for photo in photo_list:
                    id = str(photo.get('id'))
                    secret = str(photo.get('secret'))
                    server = str(photo.get('server'))
                    farm = str(photo.get('farm'))
                    photo_url = self.__photoUrlBuilder(id,server,farm,secret)
                    photo_dict = self.__get_photo_location(id,secret)
                    photo_dict['url'] = photo_url
                    photos.append(photo_dict)

            return photos

        except:
            return []


    def __get_photo_location(self,photo_id,photo_secret):
        """
        Method to grab a photos location data using the flickr get.info API
        :return: str(URL)
        """
        flickr_info_url = "https://www.flickr.com/services/rest/?method=flickr.photos.getInfo&"\
                              +"api_key="+self.flickr_api_key\
                              +"&photo_id="+photo_id\
                              +"&secret="+photo_secret\
                              +"&format=json&nojsoncallback=1"
        try:
            photo_location = req.get(flickr_info_url).json().get('photo').get('location')
            return {'lat':photo_location.get('latitude'), 'lon':photo_location.get('longitude')}
        except:
            return {'lat':None,'lon':None}

    def __photoUrlBuilder(self,id,server,farm,secret):
        """
        Method to construct and return the url string for a particular photo.
        :return: str(URL)
        """
        photo_url = "https://farm" + farm + ".staticflickr.com/" + server + "/" + id + "_" + secret + ".jpg"  # compile url
        return photo_url
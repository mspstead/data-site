import requests as req
import sys


class Flickr_Grabber:

    def __init__(self, flickr_api_key, flickr_user_id):

        self.flickr_api_key = flickr_api_key
        self.flickr_user_id = flickr_user_id

    def get_public_user_photos(self):
        """
        Returns all a user's public photos and the photo location data.
        :return: [{url:str,lat:float/None,lon:float/None, dateTaken:float/None}]
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

            if num_pages==1:

                photo_list = public_photos.get('photo')

                for photo in photo_list:
                    photos.append(self.__photo_details(photo))

            else:

                for i in range(1,num_pages+1):

                    page_number = "&page="+str(i)
                    public_photos = req.get(flickr_public_photos_url+page_number).json().get('photos')

                    photo_list = public_photos.get('photo')

                    for photo in photo_list:
                        photos.append(self.__photo_details(photo))

            return photos

        except AttributeError as e:
            print(e)
            print('API KEY or User Key incorrect.')
            return []


    def __photo_details(self,photo):
        """
        Get individual details for each photo
        :return: Dict Object format {url:str,lat:float/None,lon:float/None,dateTaken:str/None}
        """

        id = str(photo.get('id'))
        secret = str(photo.get('secret'))
        server = str(photo.get('server'))
        farm = str(photo.get('farm'))
        photo_url = self.__photoUrlBuilder(id, server, farm, secret)
        photo_dict = self.__get_photo_info(id, secret)
        photo_dict['url'] = photo_url

        return photo_dict

    def __get_photo_info(self,photo_id,photo_secret):
        """
        Method to grab a photos location data using the flickr get.info API
        :return: {lat:float,lon:float,dateTaken:str}
        """
        flickr_info_url = "https://www.flickr.com/services/rest/?method=flickr.photos.getInfo&"\
                              +"api_key="+self.flickr_api_key\
                              +"&photo_id="+photo_id\
                              +"&secret="+photo_secret\
                              +"&format=json&nojsoncallback=1"
        try:

            photo_info = req.get(flickr_info_url).json().get('photo')
            photo_location = photo_info.get('location')
            dateTaken = photo_info.get("dates").get("taken")

            return {'lat':float(photo_location.get('latitude')),
                    'lon':float(photo_location.get('longitude')),
                    'dateTaken':dateTaken}

        except AttributeError as e:
            print('Missing location or date for photoid: {}, photosecret: {}'.format(photo_id,photo_secret))
            return {'lat':None,'lon':None,'dateTaken':None}

    def __photoUrlBuilder(self,id,server,farm,secret):
        """
        Method to construct and return the url string for a particular photo.
        :return: URL:str
        """
        photo_url = "https://farm" + farm + ".staticflickr.com/" + server + "/" + id + "_" + secret + ".jpg"  # compile url
        return photo_url
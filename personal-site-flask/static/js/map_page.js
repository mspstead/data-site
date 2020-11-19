function createMap(photos) {

    var mymap = L.map('mapid').setView([22, 18], 2);
    L.tileLayer('https://tile.thunderforest.com/outdoors/{z}/{x}/{y}.png?apikey=5b73157d181c49b8b9ac3a6961d27e7b', {
    attribution: 'Maps &copy; <a href="https://www.thunderforest.com/">thunderforest</a> data &copy;, <a href="http://www.openstreetmap.org/copyright">OpenStreetMap Contributors</a>',
    maxZoom: 18,
    minZoom: 2,
    tileSize: 256
    }).addTo(mymap);

    var cameraIcon = L.divIcon({
        html: '<i class="fa fa-camera fa-3x"></i>'//, // size of the icon
        //iconAnchor:   [0, 0], // point of the icon which will correspond to marker's location
        //popupAnchor:  [0, 0] // point from which the popup should open relative to the iconAnchor
    });

    var markerClusters = L.markerClusterGroup();

    for (var i = 0; i < photos.length; i++) {

        var url = photos[i].URL;
        var lat = photos[i].Lat;
        var lon = photos[i].Lon;
        var date = photos[i].Date;

        var marker = L.marker([lat,lon],{icon: cameraIcon}).bindPopup('<img src='+ url +' height="80%" width="90%"/><h3>'+ date +'</h3>');
        markerClusters.addLayer(marker);

    }

    mymap.addLayer(markerClusters);
}

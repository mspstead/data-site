var mymap = L.map('mapid').setView([34.538238, 7.282901], 2);

L.tileLayer('https://tile.thunderforest.com/outdoors/{z}/{x}/{y}.png?apikey=5b73157d181c49b8b9ac3a6961d27e7b', {
    attribution: 'Maps &copy; <a href="https://www.thunderforest.com/">thunderforest</a> data &copy;, <a href="http://www.openstreetmap.org/copyright">OpenStreetMap Contributors</a>',
    maxZoom: 18,
    tileSize: 256
}).addTo(mymap);
var markerClusters = L.markerClusterGroup();
var marker1 = L.marker([51.5, -0.09]);
var marker2 = L.marker([51.5, -0.08]);
var marker3 = L.marker([60.41, -0.08]);
markerClusters.addLayer(marker1);
markerClusters.addLayer(marker2);
markerClusters.addLayer(marker3);
mymap.addLayer(markerClusters);
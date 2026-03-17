let map;

function initMap(){

map = new google.maps.Map(document.getElementById("map"),{
center:{lat:28.6139,lng:77.2090},
zoom:12
});

map.addListener("click",(e)=>{

document.getElementById("lat").value=e.latLng.lat();
document.getElementById("lng").value=e.latLng.lng();

new google.maps.Marker({
position:e.latLng,
map:map
});

});

}
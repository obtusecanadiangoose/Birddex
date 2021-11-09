alert("Custom Js Running!")
mapboxgl.accessToken = 'pk.eyJ1Ijoib2dpbHZpZWxpYW0iLCJhIjoiY2t0cWo5OTdyMHIwNjJ1cXN5dGdrc3UxbiJ9.pYwKqx5yeorTKH62sOrltA';
var map = new mapboxgl.Map({
  container: 'map',
  style: 'mapbox://styles/mapbox/streets-v11',
  center: [-122.486052, 37.830348],
  zoom: 14
});
map.on('style.load', function() {
  map.on('click', function(e) {
    var coordinates = e.lngLat;
    new mapboxgl.Popup()
      .setLngLat(coordinates)
      .setHTML('you clicked here: <br/>' + coordinates)
      .addTo(map);
  });
});
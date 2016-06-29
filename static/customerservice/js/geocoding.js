$(function(){
  $("#id_address_formated").geocomplete({
    map: ".map_canvas",
    details: "form",
    markerOptions: {
      draggable: true
    }
  });

  $("#id_address_formated").bind("geocode:dragged", function(event, latLng){
    $("input[name=latitude]").val(latLng.lat());
    $("input[name=longitude]").val(latLng.lng());
    $("#reset").show();
  });

  $("#reset").click(function(){
    $("#id_address_formated").geocomplete("resetMarker");
    $("#reset").hide();
    return false;
  });

  $("#find").click(function(){
    $("#id_address_formated").trigger("geocode");
  }).click();
});

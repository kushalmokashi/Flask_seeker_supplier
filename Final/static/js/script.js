

$(function(){

      loadGoogleMaps();

      var mdzn = new Dropzone("#mdzn",{
        'success':function(fileuploaded,seekers_suppliers_list){
          console.log(fileuploaded)
          console.log(seekers_suppliers_list)
          $("#upload-view").addClass('hidden')
          $("#file-view").removeClass('hidden')
          //console.log(seekers_suppliers_list)
          var options = {
            zoom:8,
            center:{lat:42.3601,lng:-71.0589}
          }
          map = new google.maps.Map(document.getElementById('map'), options);
          var infowindow = new google.maps.InfoWindow({maxWidth: 200});
          // list = {seekers_suppliers_list};
           list = seekers_suppliers_list;
           //console.log(typeof(list))
           var createMarker = function (position,content,iconImage) {
            var marker = new google.maps.Marker({
                position: position,
                content: content,
                icon: iconImage,
                map: map
          });
            google.maps.event.addListener(marker, 'click', function () {
            infowindow.setContent(content);
            infowindow.open(map, marker);
            });
          }
          for (var i = 0; i < list.length; i++) {
            //console.log(list)
            var position = {lat:list[i].primary_latlng[0],lng:list[i].primary_latlng[1]}
            var content = 'ID-->' + list[i].tweet_id + '---TWEET-->' +  list[i].text
            var iconImage = null
            createMarker(position,content,iconImage);
            for (var j = 0; j < list[i].potential_offers.length; j++) {
              var position = {lat:list[i].potential_offers[j].primary_latlng[0],lng:list[i].potential_offers[j].primary_latlng[1]}
              var content = 'ID-->' + list[i].potential_offers[j].tweet_id + '---TWEET-->' +  list[i].potential_offers[j].text
              var iconImage = 'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png'
              createMarker(position,content,iconImage);
            }
          }
          // $('#tree1').tree({data:list});
          $('#element').jsonView(JSON.stringify(seekers_suppliers_list, undefined, 2));
          // document.getElementById("disp").innerHTML = JSON.stringify(seekers_suppliers_list, undefined, 2);

            //  var createMarker = function (position,content,iconImage) {
            //       var marker = new google.maps.Marker({
            //           position: position,
            //           content: content,
            //           icon: iconImage,
            //           map: map
            //     });
      
              // google.maps.event.addListener(marker, 'click', function () {
              // infowindow.setContent(content);
              // infowindow.open(map, marker);
              // });
      
              //}
        }
       });
 
  // var infowindow = new google.maps.InfoWindow({maxWidth: 200});
});

$(document).ready(loadGoogleMaps)

var loadGoogleMaps = function () {
   
      
      if (document.querySelectorAll('#map').length > 0)
      {
        if (document.querySelector('html').lang)
          lang = document.querySelector('html').lang;
        else
          lang = 'en';

        var js_file = document.createElement('script');
        js_file.type = 'text/javascript';
        js_file.src = 'https://maps.googleapis.com/maps/api/js?callback=initMap&language=' + lang;
        document.getElementsByTagName('head')[0].appendChild(js_file);
      }
}


var initMap = function () {

    var options = {
          zoom:8,
          center:{lat:42.3601,lng:-71.0589}
        }
        // New map
     map = new google.maps.Map(document.getElementById('map'), options);
    // var infowindow = new google.maps.InfoWindow({maxWidth: 200});
    // // list = {seekers_suppliers_list};
    //  list = list;
    
    // for (var i = 0; i < list.length; i++) {
    //   console.log(list)
    //   var position = {lat:list[i].primary_latlng[0],lng:list[i].primary_latlng[1]}
    //   var content = 'ID-->' + list[i].tweet_id + '---TWEET-->' +  list[i].text
    //   var iconImage = null
    //   createMarker(position,content,iconImage);
    //   for (var j = 0; j < list[i].potential_offers.length; j++) {
    //     var position = {lat:list[i].potential_offers[j].primary_latlng[0],lng:list[i].potential_offers[j].primary_latlng[1]}
    //     var content = 'ID-->' + list[i].potential_offers[j].tweet_id + '---TWEET-->' +  list[i].potential_offers[j].text
    //     var iconImage = 'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png'
    //     createMarker(position,content,iconImage);
    //   }
    // }


    //    var createMarker = function (position,content,iconImage) {
    //         var marker = new google.maps.Marker({
    //             position: position,
    //             content: content,
    //             icon: iconImage,
    //             map: map
    //       });

    //     google.maps.event.addListener(marker, 'click', function () {
    //     infowindow.setContent(content);
    //     infowindow.open(map, marker);
    //     });

    //     }

   }
let xmlhttp = new XMLHttpRequest();
var ctx = document.getElementById("myChart").getContext('2d');
var reloadCnt = 0;
xmlhttp.onreadystatechange = function () {
  if (this.readyState == 4 && this.status == 200) {
    var timeinmilliseconds = 3000;
    let data1 = JSON.parse(this.responseText).feed.entry;
    if(data1 == undefined){setTimeout(function(){ window.location.reload(true) }, 3000)}

    let i;
    var osf = new Array(data1.length);
    var tt = new Array(data1.length);
    var xc = new Array(data1.length);
    var yc = new Array(data1.length);
    for (i = 0; i < data1.length; i++) {
      var OrderID = data1[i]["gsx$orderid"]["$t"];
      osf[i] = OrderID;
      let Item = data1[i]["gsx$item"]["$t"];
      let Priority = data1[i]["gsx$priority"]["$t"];
      let City = data1[i]["gsx$city"]["$t"];
      let Dispatched = data1[i]["gsx$dispatched"]["$t"];
      let Shipped = data1[i]["gsx$shipped"]["$t"];
      let OrderDateandTime = data1[i]["gsx$orderdateandtime"]["$t"];
      let DispatchDateandTime = data1[i]["gsx$dispatchdateandtime"]["$t"];
      let ShippingDateandTime = data1[i]["gsx$shippingdateandtime"]["$t"];
      let TimeTaken = data1[i]["gsx$timetaken"]["$t"];
      tt[i] = TimeTaken;
      let xcor = data1[i]["gsx$longitude"]["$t"];
      xc[i] = xcor;
      let ycor = data1[i]["gsx$latitude"]["$t"];
      yc[i] = ycor;
      document.getElementById("demo").innerHTML +=
        "<tr>" +
        "<td>" +
        OrderID +
        "</td>" +
        "<td>" +
        Item +
        "</td>" +
        "<td>" +
        Priority +
        "</td>" +
        "<td>" +
        City +
        "</td>" +
        "<td>" +
        Dispatched +
        "</td>" +
        "<td>" +
        Shipped +
        "</td>" +
        "<td>" +
        OrderDateandTime +
        "</td>" +
        "<td>" +
        DispatchDateandTime +
        "</td>" +
        "<td>" +
        ShippingDateandTime +
        "</td>" +
        "<td>" +
        TimeTaken +
        "</td>" +
        "</tr>";
    }
        // GPS Coordinates
        // for (var o = 0; o<xc.length;o++){
        //     xc[o] = parseFloat(xc[o]);
        //     yc[o] = parseFloat(yc[o]);
        // }
        
        var locations = [];
        for (var p = 0; p<data1.length; p++){locations[p] = new Array(2);}
        
        for (var r = 0;r<data1.length;r++){
          for (var c = 0;c<2;c++){
            if (!c){
              locations[r][c] = parseFloat(xc[r]);
            
            }
            else
              locations[r][c] = parseFloat(yc[r]);
          }
        }

        // console.log(locations)
        var map = L.map('map', {
            center: [18.7041, 87.1025],
            zoom: 4
        });


        L.tileLayer('https://api.maptiler.com/maps/streets/{z}/{x}/{y}.png?key=wxvvIbkL8U2EKwUTy3yI',{
            tileSize: 512,
            zoomOffset: -1,
            minZoom: 3,
            attribution: "\u003ca href=\"https://www.maptiler.com/copyright/\" target=\"_blank\"\u003e\u0026copy; MapTiler\u003c/a\u003e \u003ca href=\"https://www.openstreetmap.org/copyright\" target=\"_blank\"\u003e\u0026copy; OpenStreetMap contributors\u003c/a\u003e",
            crossOrigin: true
        }).addTo(map);
        
        for (var l = 0; l<locations.length;l++){
          marker = new L.marker([locations[l][0], locations[l][1]]).bindPopup(osf[l]).addTo(map);
        }


        // Chart Start
        var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: osf,
            datasets: [{
                data: tt,
                // backgroundColor: "rgb(255,218, 185)"
                backgroundColor: ["red", "blue", "green", "yellow", "grey","magenta","purple","indigo","orange"]
            }]
          },
        
        options: {
          legend: {
            display: false,
        },
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            xAxes:[{
              scaleLabel:{display:true,labelString:"Order IDs"}
            }],
            yAxes: [{
              scaleLabel:{display:true,labelString:"Time Taken"},
              ticks: {
                beginAtZero:true
              }
            }]
          }
        }
        }); 
        // Chart End

    console.log(osf[8])
    
    if(osf[8] == "1008"){
      clearTimeout(t);
      //window.stop();
    }
    else{
      var t = setTimeout(function(){ window.location.reload(true) }, timeinmilliseconds);
    }
    
  }
};


xmlhttp.open(
  "GET",
  "https://spreadsheets.google.com/feeds/list/1lStRXt0zWrFtgl89LziSmylPpJe-DfPQ4bPfMFeRvgk/5/public/values?alt=json",
  true
);
xmlhttp.send();



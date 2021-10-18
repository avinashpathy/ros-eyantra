let xmlhttp = new XMLHttpRequest();
var ctx = document.getElementById("myChart").getContext('2d');
xmlhttp.onreadystatechange = function () {
  if (this.readyState == 4 && this.status == 200) {
    let data1 = JSON.parse(this.responseText).feed.entry;
    let i;
    var osf = new Array(data1.length);
    var tt = new Array(data1.length);
    for (i = 0; i < data1.length; i++) {
      var OrderID = data1[i]["gsx$order"]["$t"];
      osf[i] = OrderID;
      console.log(OrderID[i]); 
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
        // console.log(osf)
        var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            // labels: ["M", "T", "W"],
            labels: osf,
            datasets: [{
                label:'Time taken',
                data: tt,
                backgroundColor: "rgb(255,218, 185)"
            }]
          },
        options: {
          scales: {
            yAxes: [{
              ticks: {
          beginAtZero:true
        }
      }]
    }
  }
        }); 
  }
};


xmlhttp.open(
  "GET",
  "https://spreadsheets.google.com/feeds/list/1Ajgey7xYF4PCG0Z1wJYv54XmC5ceTzF7AakaKg9Z8F0/1/public/values?alt=json",
  true
);
xmlhttp.send();

// var ctx = document.getElementById("myChart").getContext('2d');
// var myChart = new Chart(ctx, {
//   type: 'bar',
//   data: {
//     labels: ["M", "T", "W", "T", "F", "S", "S"],
//     datasets: [{
//       label:'Time taken',
//       data: [12, 19, 3, 17, 28, 24, 7],
//       backgroundColor: "rgb(255,218, 185)"
//     }]
//   }
// }); 

d3.csv('sunburst.csv', function(err, rows){

  function unpack(rows, key) {

  return rows.map(function(row) { return row[key]; });

}


var data = [

    {

      type: "sunburst",

      maxdepth: 3,

      ids: unpack(rows, 'ids'),

      labels: unpack(rows, 'labels'),

      parents:unpack(rows, 'parents'),

      values: unpack(rows, 'values'),

      branchvalues: "total"

    }

  ];


var layout = {

  margin: {l: 0, r: 0, b: 0, t:0},

  sunburstcolorway:[

    "#636efa","#EF553B","#00cc96","#ab63fa","#19d3f3",

    "#e763fa", "#FECB52","#FFA15A","#FF6692","#B6E880"

  ],

  extendsunburstcolorway: true

};



Plotly.newPlot('myDiv', data, layout, {showSendToCloud: true});

})

function change_page_graphe(){
  window.location.href = "../Graph/search_graph.html";
} 
function change_page_parallelCoord(){
  window.location.href = "../Parallel Coordinates/parallelCoord.html";
} 

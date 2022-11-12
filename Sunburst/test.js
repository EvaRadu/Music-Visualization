

d3.json('sunburst_hierarchy.json', 
function(error, root) {

  
  console.log(d3.hierarchy(root))

var g = svg.selectAll("g")
        .data(partition.nodes(root))
        .enter().append("g");

    var color = d3.scale.ordinal();

    var path = g.append("path")
        .attr("d", arc)
        //.style("fill", function(d) { return colors((d.children ? d :     d.parent).name); })
        .style("fill", function(d) { return color(d.color); })
        .on("click", click);
});




/*

function(err, rows){

  function unpack(rows, key) {

  return rows.map(function(row) { return row[key]; });

}
var data = [

    {

      type: "sunburst",

      maxdepth: 3,

      ids: unpack(rows, '_id'),

      labels: unpack(rows, 'name'),

      parents:unpack(rows, 'genre_cluster')

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
*/
function checkCheckbox() {
  //aucun filtre n'est coché
 // if (!(document.getElementById("displayUnknown").checked) && 
  //!(document.getElementById("displayUnknownYears").checked)) {
    document.getElementById("myDiv").innerHTML = "";  
    createSunburst("sunburst.csv");
}

function filters(year, data){

  for( var i = 0; i < data[0].ids.length; i++){ 
    

    if ( data[0].ids[i].includes(year+'')
    ||  data[0].ids[i] == year 
    || data[0].parents[i]== year
    || data[0].parents[i].includes(year+ '') ){ 
      delete data[0].ids[i]; 
      delete data[0].labels[i];
      delete data[0].parents[i];
      delete data[0].values[i];
    }

  };
  data[0].ids = data[0].ids.filter(element => {
    return element !== null;
  });
  data[0].labels = data[0].labels.filter(element => {
    return element !== null;
  });
  data[0].parents = data[0].parents.filter(element => {
    return element !== null;
  });
  data[0].values = data[0].values.filter(element => {
    return element !== null;
  });

}

function createSunburst(path) {

d3.csv(path, function(err, rows){

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

      values: unpack(rows, 'values')

      //branchvalues: "total"

    }

  ];

if (!document.getElementById("displayYear1970").checked) {
  filters(1970, data);
};
if (!document.getElementById("displayYear1980").checked) {
  filters(1980, data);
};
if (!document.getElementById("displayYear1990").checked) {
  filters(1990, data);
};
if (!document.getElementById("displayYear2000").checked) {
  filters(2000, data);
};
if (!document.getElementById("displayYear2010").checked) {
  filters(2010, data);
};

var layout = {

  margin: {l: 0, r: 0, b: 0, t:0},

  sunburstcolorway:[
    
    "#636efa","#EF553B","#00cc96","#ab63fa","#19d3f3",

    "#e763fa", "#FECB52","#FFA15A","#FF6692","#B6E880", 

  ],

  extendsunburstcolorway: true

};



  Plotly.newPlot('myDiv', data, layout, { showSendToCloud: true });

})};

function change_page_graphe(){
  window.location.href = "../Graph/search_graph.html";
} 
function change_page_parallelCoord(){
  window.location.href = "../Parallel Coordinates/parallelCoord.html";
} 

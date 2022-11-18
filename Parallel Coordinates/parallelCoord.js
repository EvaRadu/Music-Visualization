// Fonction qui permet l'affichage de la visualisation
//     data = les données à afficher
//     titles = liste des titres des chansons
//     rangeColors = liste des couleurs à utiliser
//     displayColomns = liste des colonnes à afficher
function loadVisualization(data, titles, rangeColors,displayColomns){  
    var margin = {top: 30, right: 0, bottom: 10, left: 0},
    width = 780 - margin.left - margin.right,
    height = 700 - margin.top - margin.bottom;
  
  var x = d3.scale.ordinal().rangePoints([0, width], 1),
      y = {},
      dragging = {};
  
  var line = d3.svg.line(),
      axis = d3.svg.axis().orient("left"),
      background,
      foreground;
  
  // Suppression de la visualisation précédente
  var clear = d3.select("svg").remove();  
  
  // Création de la nouvelle visualisation
  var svg = d3.select("#my_dataviz")
  .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .call(d3.behavior.zoom().on("zoom", function () {
      svg.attr("transform", "translate(" + d3.event.translate + ")" + " scale(" + d3.event.scale + ")")
    }))
   .append("g")
   .attr("transform",
         "translate(" + margin.left + "," + margin.top + ")");
   
    
  
    
    var color = d3.scale.ordinal()
      .domain(titles)
      .range(rangeColors)
      
    // Extract the list of dimensions and create a scale for each.
    x.domain(dimensions = d3.keys(data[0]).filter(function(d) {
        
        
        if(d==="Nom artist"){ return;}
  
        if(d==="Titre" || d === "Genre" || d==="Genre inféré" || d==="Nom Album" || d==="Langue") {
          
          if(displayColomns.includes(d) ||d==="Titre"){
            y[d] = d3.scale.ordinal()
              .domain(data.map(function(p) { return p[d]; }))
              .rangePoints([height, 0]);
   
        }
        else{
          return;
        }}
       
        else {
            y[d] = d3.scale.linear()
              .domain(d3.extent(data, function(p) { return +p[d]; }))
              .range([height, 0]);
        }

        
  
        return true;
    }));
  
  
  
  
    // Add grey background lines for context.
    background = svg.append("svg:g")
        .attr("class", "background")
      .selectAll("path")
        .data(data)
      .enter().append("svg:path")
        .attr("d", path);
  
    // Add blue foreground lines for focus.
    foreground = svg.append("svg:g")
        .attr("class", "foreground")
      .selectAll("path")
        .data(data)
      .enter().append("svg:path")
        .attr("d", path);
  
    // Add a group element for each dimension.
    var g = svg.selectAll(".dimension")
        .data(dimensions)
      .enter().append("svg:g")
        .attr("class", "dimension")
        .attr("transform", function(d) { return "translate(" + x(d) + ")"; })
        .call(d3.behavior.drag()
          .on("dragstart", function(d) {
            dragging[d] = this.__origin__ = x(d);
            background.attr("visibility", "hidden");
          })
          .on("drag", function(d) {
            dragging[d] = Math.min(width, Math.max(0, this.__origin__ += d3.event.dx));
            foreground.attr("d", path);
            dimensions.sort(function(a, b) { return position(a) - position(b); });
            x.domain(dimensions);
            g.attr("transform", function(d) { return "translate(" + position(d) + ")"; })
          })
          .on("dragend", function(d) {
            delete this.__origin__;
            delete dragging[d];
            transition(d3.select(this)).attr("transform", "translate(" + x(d) + ")");
            transition(foreground)
                .attr("d", path);
            background
                .attr("d", path)
                .transition()
                .delay(500)
                .duration(0)
                .attr("visibility", null);
          }));;
          
  
    // Add an axis and title.
    g.append("svg:g")
        .attr("class", "axis")
        .each(function(d) { d3.select(this).call(axis.scale(y[d])); })
      .append("svg:text")
        .attr("text-anchor", "middle")
        .attr("y", -9)
        .text(String)
  
        
  
    // Add and store a brush for each axis.
    g.append("svg:g")
        .attr("class", "brush")
        .each(function(d) { d3.select(this).call(y[d].brush = d3.svg.brush().y(y[d]).on("brush", brush)); })
      .selectAll("rect")
        .attr("x", -8)
        .attr("width", 16);
  
  
  
  function position(d) {
    var v = dragging[d];
    return v == null ? x(d) : v;
  }
  
  function transition(g) {
    return g.transition().duration(500);
  }
  
  
  
  // Returns the path for a given data point.
  function path(d) {
    return line(dimensions.map(function(p) {
     return [position(p), y[p](d[p])]; }));
  }
  
  // Handles a brush event, toggling the display of foreground lines.
  function brush() {
    var actives = dimensions.filter(function(p) { return !y[p].brush.empty(); }),
        extents = actives.map(function(p) { return y[p].brush.extent(); });
    foreground.style("display", function(d) {
      return actives.every(function(p, i) {
        return extents[i][0] <= d[p] && d[p] <= extents[i][1];
      }) ? null : "none";
    });
  }
  
  svg
      .selectAll("myPath")
      .data(data)
      .enter()
      .append("path")
        .attr("class", function (d) { return "line " + d.Titre } ) // 2 class for each line: 'line' and the group name
        .attr("d",  path)
        .style("fill", "none" )
        .style("stroke", function(d){ return( color(d.Titre))} )
        .style("opacity", 0.5)
        .on("mouseover",  function (d) { 
          var toolTip = document.getElementById("tooltip");
          tooltip.innerHTML = "";
          tooltip.style.visibility = "visible";
          tooltip.innerHTML = "<h3>Details de la chanson : </h3>";
          toolTip.innerHTML += "<div><b>Titre : </b>" + d.Titre +"</div>";
          toolTip.innerHTML += "<div><b>Genre : </b>" + d.Genre + "</div>";
          toolTip.innerHTML += "<div><b>Genre inféré : </b>" + d['Genre inféré'] + "</div>";
          toolTip.innerHTML += "<div><b>Nom Album : </b>" + d['Nom Album'] + "</div>";
          toolTip.innerHTML += "<div><b>Langue : </b>" + d.Langue + "</div>";;
         })
  
  
        svg.selectAll("myAxis")
      // For each dimension of the dataset I add a 'g' element:
      .data(dimensions).enter()
      .append("g")
      .attr("class", "axis")
      // I translate this element to its right position on the x axis
      .attr("transform", function(d) { return "translate(" + x(d) + ")"; })
      // Add axis title
      .append("text")
        .style("text-anchor", "middle")
        .attr("y", -9)
        .text(function(d) { return d; })
        .style("fill", "black")   
        
        
  }
  

  // Fonction reliée au bouton confirmer qui permet de filtrer les données en fonction des choix de l’utilisateur
  function displayVisualisation(){
      readCsvArtist("../../DATA/artists.csv");
      readCsvSong();
  
  }
    

// Fonction qui permet de lire le fichier csv des artistes
function readCsvArtist(filename){
    getListOfArtists(filename);
  }
  
// Fonction qui permet d'obtenir les informations du fichier csv des artistes afin de remplir le menu déroulant
function getListOfArtists(file){
    d3.csv(file, function(data){
      var listArtist = [];
      for(i=0; i<data.length; i++){
        if(!(data[i]["name"].includes("http:"))){
        listArtist.push(data[i]["name"]);
        }
      }
      
      var sel1 = document.getElementById('artists-select');
      for (var i = 1; i <= listArtist.length; i++) {
      var opt = document.createElement('option');
      opt.text = listArtist[i];
      opt.value = listArtist[i];
      sel1.appendChild(opt);
    }
  
    })
  }
  
  // Fonction qui permet de lire le fichier csv des chansons
  // Cette fonction tient compte des filtres et crées les données à utilisées pour la visualisation
  // Elle appelle ensuite la fonction qui permet de créer la visualisation
  function readCsvSong(){
    var artist = document.getElementById("artists-select").value;
    artist = artist.replace("/","")
    artist = artist.replace('"',"")
    artist = artist.replace("*","")
    artist = artist.replace(">","")
    artist = artist.replace("'","")
    artist = artist.replace("<","")
    artist = artist.replace('\\',"")
    artist = artist.replace(':',"")
    artist = artist.replace("?","")
    artist = artist.replace('|',"")
    var path = "../../DATA/ParCoordCsv/"+artist+".csv" 
   
      d3.csv(path, function(data) {
  
        var songs = [];
        var titles = [];
        var genres = [];
        var genresInferes = [];
        var albums = [];
        var langues = [];
        var isUnknownType = document.getElementById("unknownType").checked;
        var isUnknownInferedType = document.getElementById("unknownInferedType").checked;
        var isUnknownLangue = document.getElementById("unknownLangue").checked;

       
      /* FILTRES SUR LES DONNEES : GESTION DE L'AFFICHAGE DES DONNEES INCONNUES */
  
        if(!isUnknownType){ // Si on ne veut pas les chansons dont le genre est inconnu
          if(!isUnknownLangue && isUnknownInferedType){ // Et qu'on ne veut pas les chansons dont la langue est inconnue
            for(i=0;i<data.length;i++){
              if(data[i]["Genre"]!="Unknown" && data[i]["Langue"]!="Unknown"){
              titles.push(data[i]["Titre"]);
              genres.push(data[i]["Genre"]);
              genresInferes.push(data[i]["Genre inféré"])
              albums.push(data[i]["Nom Album"])
              langues.push(data[i]["Langue"])
              songs.push(data[i]);
            }
            }
          
          }
          else if(!isUnknownInferedType && isUnknownLangue){ // Et qu'on ne veut pas les chansons dont le genre inféré est inconnue
            for(i=0;i<data.length;i++){
              if(data[i]["Genre"]!="Unknown" && data[i]["Genre inféré"]!="Unknown"){
              titles.push(data[i]["Titre"]);
              genres.push(data[i]["Genre"]);
              genresInferes.push(data[i]["Genre inféré"])
              albums.push(data[i]["Nom Album"])
              langues.push(data[i]["Langue"])
              songs.push(data[i]);
            }
            }
          }
          else if(!isUnknownInferedType && !isUnknownLangue){ // Et qu'on ne veut pas les chansons dont le genre inféré et la langue sont inconnus
            for(i=0;i<data.length;i++){
              if(data[i]["Genre inféré"]!="Unknown" && data[i]["Langue"]!="Unknown" && data[i]["Genre"]!="Unknown"){
              titles.push(data[i]["Titre"]);
              genres.push(data[i]["Genre"]);
              genresInferes.push(data[i]["Genre inféré"])
              albums.push(data[i]["Nom Album"])
              langues.push(data[i]["Langue"])
              songs.push(data[i]);
            }
            }
          }
          else{
            for(i=0; i<data.length;i++){
            if(data[i]["Genre"]!="Unknown"){
              titles.push(data[i]["Titre"]);
              genres.push(data[i]["Genre"]);
              genresInferes.push(data[i]["Genre inféré"])
              albums.push(data[i]["Nom Album"])
              langues.push(data[i]["Langue"])
              songs.push(data[i]);
            
          }
        }
          }
        }
        else if(!isUnknownInferedType){ // Si on ne veut pas les chansons dont le genre inféré est inconnu
          if(!isUnknownLangue && isUnknownType){ // Et qu'on ne veut pas les chansons dont la langue est inconnue
            console.log("infered + langue");
            for(i=0;i<data.length;i++){
              if(data[i]["Genre inféré"]!="Unknown" && data[i]["Langue"]!="Unknown"){
              titles.push(data[i]["Titre"]);
              genres.push(data[i]["Genre"]);
              genresInferes.push(data[i]["Genre inféré"])
              albums.push(data[i]["Nom Album"])
              langues.push(data[i]["Langue"])
              songs.push(data[i]);
            }
            }
          }
          else{
            console.log("infered");
            for(i=0; i<data.length;i++){
            if(data[i]["Genre inféré"]!="Unknown"){
              titles.push(data[i]["Titre"]);
              genres.push(data[i]["Genre"]);
              genresInferes.push(data[i]["Genre inféré"])
              albums.push(data[i]["Nom Album"])
              langues.push(data[i]["Langue"])
              songs.push(data[i]);
            
          }
        }
          }
        }
        else if(!isUnknownLangue){ // Si on ne veut pas les chansons dont la langue est inconnue
          for(i=0; i<data.length;i++){
          if(data[i]["Langue"]!="Unknown"){
              titles.push(data[i]["Titre"]);
              genres.push(data[i]["Genre"]);
              genresInferes.push(data[i]["Genre inféré"])
              albums.push(data[i]["Nom Album"])
              langues.push(data[i]["Langue"])
              songs.push(data[i]);
            
          }
        }
        }
        else{ // Si on veut toutes les chansons (même avec des données inconnues)
          for(i=0; i<data.length;i++){
            titles.push(data[i]["Titre"]);
            genres.push(data[i]["Genre"]);
            genresInferes.push(data[i]["Genre inféré"])
            albums.push(data[i]["Nom Album"])
            langues.push(data[i]["Langue"])
            songs.push(data[i]);
          }
        }
  
        
        
        /* GENERATION ALEATOIRE DE COULEUR POUR LES DONNEES */ 
        var colors = [];
        for(j=0; j<songs.length; j++){
          colors.push('#'+(Math.random() * 0xFFFFFF << 0).toString(16).padStart(6, '0'));
        } 
  
  
        /* REMPLISSAGE DES INFORMATIONS EN DESSOUS DE LA VISUALISATION */
        fillInfo("listSongs",titles,"Titres");
        fillInfo("listGenres",genres, "Genres");
        fillInfo("listGenresInferes",genresInferes,"Genres inférés");
        fillInfo("listAlbums",albums, "Noms albums");
        fillInfo("listLangues",langues, "Langues");
        
  
        /* CREATION DU GRAPHIQUE */
        if(songs.length==0){ // Si il n'y a pas de données -> message d'erreur
          alert("La recherche que vous avez lancé n'a pas de résultat associé. Veuillez réessayer avec un autre artiste et/ou d'autres filtres.");
        }
        else{ // Sinon : création de la visualisation
        loadVisualization(songs,titles,colors, getColomunFilter());
        }
    
        
      });
  }
  
  
  // Fonction pour remplire les infos en dessous de la visualisation
  function fillInfo(listeName, dataList,nom){
    let list = document.getElementById(listeName);
        list.innerHTML = "";
        list.innerHTML += "<h3 style='color: #553c9a;'>" + nom + "</h3>";
        uniqueList = dataList.filter(function(item, pos) {
        return dataList.indexOf(item) == pos;
        })
        uniqueList.forEach((item) => {
          let li = document.createElement("li");
          li.innerText += item;
          list.appendChild(li);
        });
  }
  
  // Filtrer les colonnes à afficher
  function getColomunFilter(){
    var filters = [];
    var displayGenre = document.getElementById("displayGenre").checked;
    var displayGenreInferes = document.getElementById("displayGenreInferes").checked;
    var displayAlbum = document.getElementById("displayAlbums").checked;
    var displayLangues = document.getElementById("displayLangues").checked;
    if(displayGenre){
      filters.push("Genre");
    }
    if(displayGenreInferes){
      filters.push("Genre inféré");
    }
    if(displayAlbum){
      filters.push("Nom Album");
    }
    if(displayLangues){
      filters.push("Langue");
    }
    return filters;
  
  }

  // Fonction qui permet de charger la visualisation du graphe
  function change_page_graphe(){
    window.location.href = "../Graph/search_graph.html";
  } 

  // Fonction qui permet de charger la visualisation du sunburst
  function change_page_Sunburst(){
    window.location.href = "../SunBurst/test_csv.html";
  } 

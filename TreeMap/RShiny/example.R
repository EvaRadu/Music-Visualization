  library(ECharts2Shiny)
  library("rjson")
  
  setwd("~/FAC/S9/Information Visualisation/Music-Visualization/TreeMap")
  
  if (interactive()) {
    library(shiny)
    library(ECharts2Shiny)
    fileName <- 'test2.txt'
    myData <- readChar(fileName, file.info(fileName)$size)
    print(myData)
    
    # Prepare sample data for plotting --------------------------
    dat <- "[{name: 'Artiste 1',
                value: 6,
                children: [
                    {
                    name: 'Genre 1',
                    value: 6,
                    children:[
                    {
                    name: 'Genre 1.1',
                    value: 6
                    },
                    {
                    name: 'Genre 1.2',
                    value: 2
                    }
                    ]
                    },
                    {
                    name: 'Genre 2',
                    value: 3
                    }
                ]
              },
              {
                name: 'Artiste 2',
                value: 6,
                children: [
                    {name : 'Genre 1',
                    value:10
                    },
                    {
                    name:'Genre 2',
                    value:2
                    }
                ]
              },
              {
                name: 'Artiste 3',
                value: 4,
                children: [
                    {name : 'Genre 1',
                    value:10
                    },
                    {
                    name:'Genre 2',
                    value:2
                    }
                ]
              }]"
    
    dat2 <- "[{name: 'Album 1',
                value: 6,
                children: [
                    {
                    name: 'Genre 1',
                    value: 6,
                    children:[
                    {
                    name: 'Genre 1.1',
                    value: 6
                    },
                    {
                    name: 'Genre 1.2',
                    value: 2
                    }
                    ]
                    },
                    {
                    name: 'Genre 2',
                    value: 3
                    }
                ]
              },
              {
                name: 'Album 2',
                value: 6,
                children: [
                    {name : 'Genre 1',
                    value:10
                    },
                    {
                    name:'Genre 2',
                    value:2
                    }
                ]
              },
              {
                name: 'Album 3',
                value: 4,
                children: [
                    {name : 'Genre 1',
                    value:10
                    },
                    {
                    name:'Genre 2',
                    value:2
                    }
                ]
              }]"
    
    # Server function -------------------------------------------
    server <- function(input, output) {
      # Call functions from ECharts2Shiny to render charts
      output$treePlot <- renderTreeMap(div_id = "test", data = dat, leafDepth=1, name="Visu1")
      
      observeEvent(input$typeVisu, 
        {print(input$typeVisu); 
          if(input$typeVisu=="genreAlbums"){
          output$treePlot <- renderTreeMap(div_id = "test", data = myData, leafDepth=1, name="Visu2")}
          else{
            output$treePlot <- renderTreeMap(div_id = "test", data = dat, leafDepth=1, name="Visu1")}
          },  ## handlerExpr
          
        ignoreInit = TRUE
      )
    }
    
    
    # UI layout -------------------------------------------------
    ui <- fluidPage(
      # We MUST load the ECharts javascript library in advance
      loadEChartsLibrary(),
      selectInput(inputId="typeVisu", label = h3("Type de visualisation :"),
                  choices = list("Afficher les genres des artistes" = "genreArtistes", 
                                 "Afficher les genres des musiques" = "genreMusiques", 
                                 "Afficher les genres des albums" = "genreAlbums",
                                 "Afficher les artistes les plus populaires d'un genre" = "artistePopulaires",
                                 "Afficher les genres d'un artiste" = "genreUnArtiste"), selected = "genreArtistes"),
      tags$div(id="test", style="width:100%;height:500px;"),
      deliverChart(div_id = "test")
    )
    
    # Run the application --------------------------------------
    shinyApp(ui = ui, server = server)
    
  }
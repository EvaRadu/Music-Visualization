if(interactive()) {
  library(shiny)
  library(parallelPlot)
  
  ui <- fluidPage(
    selectInput("categoricalCsSelect", "Type de visualisation :",
                choices = list("Afficher les genres des artistes" = "Category10", 
                               "Afficher les genres des musiques" = "Accent", 
                               "Afficher les genres des albums" = "Dark2",
                               "Afficher les artistes les plus populaires d'un genre" = "Paired",
                               "Afficher les genres d'un artiste" = "Set1"), selected = "Category10"),
    textInput("a","Text input : "," "),
    parallelPlotOutput("parPlot")
  )
  
  server <- function(input, output, session) {
    output$parPlot <- renderParallelPlot({
      parallelPlot(data = iris, refColumnDim = "Species")
    })
    
    observeEvent(input$categoricalCsSelect, {
      parallelPlot::setCategoricalColorScale("parPlot", input$categoricalCsSelect)
    })
  }
  
  shinyApp(ui, server)
}

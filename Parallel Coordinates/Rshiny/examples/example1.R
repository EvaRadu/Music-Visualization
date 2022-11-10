# Un 2eme exemple basique de coordonées parallèles implémenté avec Rshiny et d3js. 
# A noter : il faut avoir installé la librairie parallelPlot.

if(interactive()) {
  library(shiny)
  library(parallelPlot)
  
  # Le client : l'utilisateur choisi dans le menu le type de couleur qu'il veut
  ui <- fluidPage(
    selectInput("categoricalCsSelect", "Categorical Color Scale:",
                choices = list("Category10" = "Category10", "Accent" = "Accent", "Dark2" = "Dark2",
                               "Paired" = "Paired", "Set1" = "Set1"), selected = "Category10"),
    p("The selector controls the colors used when reference column is of type categorical"),
    parallelPlotOutput("parPlot")
  )
  
  # Le serveur : Affiche le graphique.
  server <- function(input, output, session) {
    output$parPlot <- renderParallelPlot({
      parallelPlot(data = iris, refColumnDim = "Species")
    })
    
    # Modifie la couleur si le client le demande.
    observeEvent(input$categoricalCsSelect, {
      parallelPlot::setCategoricalColorScale("parPlot", input$categoricalCsSelect)
    })
  }
  # Lien entre le client et le server.
  shinyApp(ui, server)
}

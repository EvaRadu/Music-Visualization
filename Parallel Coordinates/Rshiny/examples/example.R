# Un exemple basique de coordonées parallèles implémenté avec Rshiny et d3js. 
# A noter : il faut avoir installé la librairie parallelPlot.

if(interactive()) {
  library(shiny)
  library(parallelPlot)
  
  # Le client : l'utilisateur règle l'échelle pour changer la valeur de la première ligne.
  ui <- fluidPage(
    sliderInput("rowValueSlider", "Value for 'Sepal.Length' of first row:",
                min = 4, max = 8, step = 0.1, value = iris[["Sepal.Length"]][1]),
    p("The slider controls the new value to assign to the 'Sepal.Length' of the first row"),
    parallelPlotOutput("parPlot")
  )
  
  # Le serveur : Affiche le graphique.
  server <- function(input, output, session) {
    output$parPlot <- renderParallelPlot({
      parallelPlot(iris)
    })
    
    # Modifie la première ligne si le client le demande.
    observeEvent(input$rowValueSlider, {
      newValues <- iris[1,]
      newValues[["Sepal.Length"]] <- input$rowValueSlider
      parallelPlot::changeRow("parPlot", 1, newValues)
    })
  }
  
  # Lien entre le client et le server.
  shinyApp(ui, server)
}


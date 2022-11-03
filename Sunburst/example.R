temp<-structure(list(year = c(1397, 1398, 1399), v13 = c(2506, 1759, 
                                                         1754), per_v10 = c(20.11, 16.66, 19.44), per_v11 = c(65.13, 79.99, 
                                                                                                              75.43), per_v12 = c(14.76, 3.35, 5.13)), row.names = c(NA, -3L
                                                                                                              ), class = "data.frame")

# create a df
(df <- data.frame(
  ids = c("total", paste0("total - ", temp$year), paste0("total - ", rep(temp$year, each = 3), " - ", rep(c('per_v10', 'per_v11', 'per_v12'), 3))),
  labels = c("Total", as.character(temp$year), rep(c('per_v10', 'per_v11', 'per_v12'), 3)),
  parents = c("", "total", "total", "total", rep(paste0("total - ", temp$year), each =3)),
  values = c(rep(0, 4), c(t(temp[, 3:5])))
))

library(plotly)
library(shiny)
library(shiny)

ui <- fluidPage(
  plotlyOutput("myplot"),
  textOutput("percent")
)

server <- function(input, output, session) {
  output$myplot <- renderPlotly({
    plot_ly(
      data = df,
      ids = ~ids,
      labels = ~labels,
      parents = ~parents,
      type = 'sunburst',
      values = ~values,
      source = "myplot_source"
    )
  })
  output$percent <- renderPrint({
    clicked <- event_data(event = "plotly_click", source = "myplot_source", priority = "event")$pointNumber + 1
    req(clicked)
    if (clicked < 5) "You are not clicking on the children"
    else paste0("Clicked percentage is ", df$values[clicked])    
  })
}

shinyApp(ui, server)
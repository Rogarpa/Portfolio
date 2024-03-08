library(tidyverse)
library(skimr)
library(nortest)

# Cargar el archivo CSV
data <- read.csv("path/globalterrorismdb_0718dist.csv", sep=",", header = T, stringsAsFactors = F ,encoding = "ISO-8859-1")

# Seleccionar las columnas de inters (69 a 102)
#selected_data <- data[, 69:102]

# Funcion para analizar cada columna
analisis_exploratorio <- function(column) {
  result <- list()
  
  # Tipo de dato
  get_type <- function() {
    if (is.factor(column)) {
      return("Cualitativo")
    } else if (is.numeric(column)) {
      return("Cuantitativo")
    } else {
      return("Cualitativo")
    }
  }
  
  result$Type <- get_type()
  
  # Subtipo del datp
  get_subtype <- function() {
    if (is.numeric(column)) {
      if (all(!is.na(column) & column %% 1 == 0))  {
        return("Discreto")
      } else {
        return("Continuo")
      }
    } else if (is.character(column)) {
      return("Nominal")
    } else {
      return("Otro")
    }
  }
  
  result$SubType <- get_subtype()
  
  # Sacamos los niveles y frecuencia
  if (any(result$Type %in% c("Cualitativo", "factor", "character"))) {
    result$Levels <- levels(factor(column))
    result$Frequencies <- table(column)
  }
  
  # Numero de porcentaje de valores perdidos
  result$MissingPercentage <- sum(is.na(column) | column == "") / length(column) * 100
  
  # Sacamos los valores permitidos:
  get_allowed_values <- function() {
    if (is.numeric(column)) {
      if (all(!is.na(column) & column %% 1 == 0))  {
        return("Enteros")
      } else {
        return("Flotantes")
      }
    } else if (is.character(column)) {
      return("Cadenas")
    } else {
      return("Otro")
    }
  }
  result$AllowedValues = get_allowed_values()
  
  # Sacamos el min, max, media y desviacion estandar
  if (any(result$Type %in% c("Cuantitativo","integer", "numeric"))) {
    result$Min <- min(column, na.rm = TRUE)
    result$Max <- max(column, na.rm = TRUE)
    result$Mean <- mean(column, na.rm = TRUE)
    result$SD <- sd(column, na.rm = TRUE)
    
    # Evaluacion de la distribucion
    if (length(column[!is.na(column)]) > 2) {
      ad_test <- ad.test(column[!is.na(column)])
      result$Distribution <- ifelse(ad_test$p.value > 0.05, "Normal", "Non-Normal")
    } else {
      result$Distribution <- NA
    }
    
    # valores atipicos
    Q1 <- quantile(column, 0.25, na.rm = TRUE)
    Q3 <- quantile(column, 0.75, na.rm = TRUE)
    IQR <- Q3 - Q1
    result$Outliers <- sum(column < (Q1 - 1.5 * IQR) | column > (Q3 + 1.5 * IQR), na.rm = TRUE)
  }
  
  return(result)
}

# Aplicar la funcion a cada columna y almacenar los resultados
analysis_results <- lapply(data, analisis_exploratorio)

# Imprimir los resultados
#print(analysis_results)

# Guardar datos
output_text <- ""
for (col in names(analysis_results)) {
  output_text <- paste(output_text, "\n###################################################################\nColumna:", col, "\n", sep = "")
  output_text <- paste(output_text, paste(names(analysis_results[[col]]), analysis_results[[col]], sep = ": ", collapse = "\n"), sep = "\n")
}

# Guardar los resultados en un archivo de texto
write(output_text, file = "./analisis_exploratorio.txt")

library(ggplot2)
data = read.csv(file = "E:/Descargas/Repos/AMD-2024-1/globalterrorismdb_0718dist.csv", sep=",", header = T, stringsAsFactors = F)


#########################################################
###################Columnas 1-34###################
#########################################################



manejo <- function(tabla){
  ##### SELECCION DE ATRIBUTOS #####
  
  seleccion_de_atributos <- tabla
  
  ####### VALORES PERDIDOS #######
  
  valores_perdidos <- function(datos) {
    resultados <- matrix(nrow = ncol(datos), ncol = 2)
    
    for (i in seq_along(datos)) {
      nombre_columna <- names(datos)[i]
      cantidad_perdidos <- sum(is.na(datos[, i]) | datos[, i] == "")
      resultados[i, ] <- c(nombre_columna, cantidad_perdidos)
    }
    
    colnames(resultados) <- c("Columna", "Valores_Perdidos")
    return(resultados)
  }
  
  valores_perdidos_data <- valores_perdidos(seleccion_de_atributos)
  
  # Reemplazar NA en "latitude" por la media
  media_latitude <- mean(seleccion_de_atributos$latitude, na.rm = TRUE)
  seleccion_de_atributos$latitude[is.na(seleccion_de_atributos$latitude)] <- media_latitude
  
  # Reemplazar NA en "longitude" por la media
  media_longitude <- mean(seleccion_de_atributos$longitude, na.rm = TRUE)
  seleccion_de_atributos$longitude[is.na(seleccion_de_atributos$longitude)] <- media_longitude
  
  # Reemplazar los valores NA en la columna 'specificity' con 0
  seleccion_de_atributos$specificity[is.na(seleccion_de_atributos$specificity)] <- 0
  
  # Reemplazar NA en  por la moda
  moda_attacktype2 <- as.numeric(names(sort(table(seleccion_de_atributos$attacktype2), decreasing = TRUE)[1]))
  seleccion_de_atributos$attacktype2[is.na(seleccion_de_atributos$attacktype2)] <- moda_attacktype2
  moda_attacktype3 <- as.numeric(names(sort(table(seleccion_de_atributos$attacktype3), decreasing = TRUE)[1]))
  seleccion_de_atributos$attacktype3[is.na(seleccion_de_atributos$attacktype3)] <- moda_attacktype3
  
  # Reemplazar las cadenas vacías en las columnas "provstate", "city", "attacktype2" y "attacktype3"
  seleccion_de_atributos$provstate[seleccion_de_atributos$provstate == ""] <- "Desconocido"
  seleccion_de_atributos$city[seleccion_de_atributos$city == ""] <- "Desconocido"
  seleccion_de_atributos$attacktype2_txt[seleccion_de_atributos$attacktype2_txt == ""] <- "Armed Assault"
  seleccion_de_atributos$attacktype3_txt[seleccion_de_atributos$attacktype3_txt == ""] <- "Facility/Infrastructure Attack"
  
  ####### VALORES ATÍPICOS #######
  
  seleccion_de_atributos2 <- seleccion_de_atributos
  valores_perdidos_data <- valores_perdidos(seleccion_de_atributos2)
  
  attacktype_herarchy = c("Assassination", "Hijacking", "Hostage Taking (Kidnapping)", "Hostage Taking (Barricade Incident)"
                          , "Bombing/Explosion", "Armed Assault", "Unarmed Assault", "Facility/Infrastructure Attack", "Unknown")
  
  seleccion_de_atributos2$attacktype1_txt = as.numeric(factor(seleccion_de_atributos2$attacktype1_txt, levels=attacktype_herarchy))
  seleccion_de_atributos2$attacktype2_txt = as.numeric(factor(seleccion_de_atributos2$attacktype2_txt, levels=attacktype_herarchy))
  seleccion_de_atributos2$attacktype3_txt = as.numeric(factor(seleccion_de_atributos2$attacktype3_txt, levels=attacktype_herarchy))
  
  par(mfrow = c(4, 4), mar = c(2, 2, 2, 2))
  boxplot(seleccion_de_atributos2$country, ylab = "country")
  boxplot(seleccion_de_atributos2$latitude, ylab = "latitude")
  boxplot(seleccion_de_atributos2$longitude, ylab = "longitude")
  boxplot(seleccion_de_atributos2$specificity, ylab = "specificity")
  boxplot(seleccion_de_atributos2$attacktype1_txt, ylab = "attacktype1_txt")
  boxplot(seleccion_de_atributos2$attacktype2_txt, ylab = "attacktype2_txt")
  boxplot(seleccion_de_atributos2$attacktype3_txt, ylab = "attacktype3_txt")
  
  # Extracción de valores atípicos basado en criterios IQR 
  outliers_country <- boxplot.stats(seleccion_de_atributos2$country)$out
  outliers_latitude <- boxplot.stats(seleccion_de_atributos2$latitude)$out
  outliers_longitude <- boxplot.stats(seleccion_de_atributos2$longitude)$out
  outliers_specificity <- boxplot.stats(seleccion_de_atributos2$specificity)$out
  outliers_attacktype1_txt <- boxplot.stats(seleccion_de_atributos2$attacktype1_txt)$out
  outliers_attacktype2_txt <- boxplot.stats(seleccion_de_atributos2$attacktype2_txt)$out
  outliers_attacktype3_txt <- boxplot.stats(seleccion_de_atributos2$attacktype3_txt)$out
  
  # Identificación de numero de indices de columnas con valores atípicos
  outlier_indices_country <- which(seleccion_de_atributos2$country %in% outliers_country)
  outlier_indices_latitude <- which(seleccion_de_atributos2$latitude %in% outliers_latitude)
  outlier_indices_longitude <- which(seleccion_de_atributos2$longitude %in% outliers_longitude)
  outlier_indices_specificity <- which(seleccion_de_atributos2$specificity %in% outliers_specificity)
  outlier_indices_attacktype1_txt <- which(seleccion_de_atributos2$attacktype1_txt %in% outliers_attacktype1_txt)
  outlier_indices_attacktype2_txt <- which(seleccion_de_atributos2$attacktype2_txt %in% outliers_attacktype2_txt)
  outlier_indices_attacktype3_txt <- which(seleccion_de_atributos2$attacktype3_txt %in% outliers_attacktype3_txt)
  
  valores_atipicos_country <- seleccion_de_atributos2[outlier_indices_country, ]$country
  moda_country <- as.numeric(names(sort(table(seleccion_de_atributos2$country), decreasing = TRUE)[1]))
  seleccion_de_atributos2$country[seleccion_de_atributos2$country %in% valores_atipicos_country] <- moda_country
  
  valores_atipicos_latitude <- seleccion_de_atributos2[outlier_indices_latitude, ]$latitude
  seleccion_de_atributos2$latitude[seleccion_de_atributos2$latitude %in% valores_atipicos_latitude] <- media_latitude
  
  valores_atipicos_longitude <- seleccion_de_atributos2[outlier_indices_longitude, ]$longitude
  seleccion_de_atributos2$longitude[seleccion_de_atributos2$longitude %in% valores_atipicos_longitude] <- media_longitude
  
  valores_atipicos_specificity <- seleccion_de_atributos2[outlier_indices_specificity, ]$specificity
  moda_specificity <- as.numeric(names(sort(table(seleccion_de_atributos2$specificity), decreasing = TRUE)[1]))
  seleccion_de_atributos2$specificity[seleccion_de_atributos2$specificity %in% valores_atipicos_specificity] <- moda_specificity
  
  valores_atipicos_attacktype1_txt <- seleccion_de_atributos2[outlier_indices_attacktype1_txt, ]$attacktype1_txt
  moda_attacktype1_txt <- as.numeric(names(sort(table(seleccion_de_atributos2$attacktype1_txt), decreasing = TRUE)[1]))
  seleccion_de_atributos2$attacktype1_txt[seleccion_de_atributos2$attacktype1_txt %in% valores_atipicos_attacktype1_txt] <- moda_attacktype1_txt
  
  valores_atipicos_attacktype2_txt <- seleccion_de_atributos2[outlier_indices_attacktype2_txt, ]$attacktype2_txt
  moda_attacktype2_txt <- as.numeric(names(sort(table(seleccion_de_atributos2$attacktype2_txt), decreasing = TRUE)[1]))
  seleccion_de_atributos2$attacktype2_txt[seleccion_de_atributos2$attacktype2_txt %in% valores_atipicos_attacktype2_txt] <- moda_attacktype2_txt
  
  valores_atipicos_attacktype3_txt <- seleccion_de_atributos2[outlier_indices_attacktype3_txt, ]$attacktype3_txt
  moda_attacktype3_txt <- as.numeric(names(sort(table(seleccion_de_atributos2$attacktype3_txt), decreasing = TRUE)[1]))
  seleccion_de_atributos2$attacktype3_txt[seleccion_de_atributos2$attacktype3_txt %in% valores_atipicos_attacktype3_txt] <- moda_attacktype3_txt
  
  seleccion_de_atributos2$approxdate <- as.factor(seleccion_de_atributos2$approxdate)
  seleccion_de_atributos2$resolution  <- as.factor(seleccion_de_atributos2$resolution )
  seleccion_de_atributos2$country_txt <- as.factor(seleccion_de_atributos2$country_txt)
  seleccion_de_atributos2$region_txt <- as.factor(seleccion_de_atributos2$region_txt)
  seleccion_de_atributos2$provstate <- as.factor(seleccion_de_atributos2$provstate)
  seleccion_de_atributos2$city <- as.factor(seleccion_de_atributos2$city)
  seleccion_de_atributos2$location <- as.factor(seleccion_de_atributos2$location)
  seleccion_de_atributos2$summary <- NULL
  seleccion_de_atributos2$alternative_txt <- as.factor(seleccion_de_atributos2$alternative_txt)
  
  return(seleccion_de_atributos2)
}
  

  ### Manipulación de tabla
  data <- manejo(data)


  
library(ggplot2)
library(dplyr)
library(caret)
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


manejo2 <- function(tabla){
  #hacemos una tabla con el conteo de las categorias de 1 a 22
  tabla_frecuencia <- table(tabla$targtype1)
  print(tabla_frecuencia)


  # Frecuencia de valores en targtype1
  value_counts <- table(tabla$targtype1)

  # boxplot targtype1 para ver si tiene valores atipicos
  boxplot(tabla$targtype1, horizontal = TRUE, main = "Boxplot de targtype1")

  # Visualización de Frecuencia de targtype1
  barplot(value_counts, main = "Frecuencia de valores en targtype1", xlab = "targtype1", ylab = "Frecuencia")



  # Calcular el rango intercuartílico (IQR) para ver si targtype tiene valore
  Q1 <- quantile(tabla$targtype1, 0.25)
  Q3 <- quantile(tabla$targtype1, 0.75)
  IQR <- Q3 - Q1

  # Definir límites para identificar valores atípicos
  lower_limit <- Q1 - 1.5 * IQR
  upper_limit <- Q3 + 1.5 * IQR

  # Identificar valores atípicos
  outliers <- tabla$targtype1 < lower_limit | tabla$targtype1 > upper_limit

  # Mostrar valores atípicos
  outlier_values <- tabla$targtype1[outliers]
  cat("Valores atípicos en targtype1:", unique(outlier_values), "\n")

  tabla_frecuencia <- table(tabla$targtype1_txt)
  print(tabla_frecuencia)

  # Obtiene los niveles únicos en el orden en que aparecen los datos
  unique_levels <- unique(tabla$targtype1_txt)

  # Convierte a factor con niveles manuales
  tabla$targtype1_txt <- factor(tabla$targtype1_txt, levels = unique_levels)

  # Verifica que la columna haya sido convertida a factor con los niveles deseados
  str(tabla$targtype1_txt)

  #impime
  print(tabla$targtype1_txt)

  #resultado <- factor((Private Citizens & Property,Government (Diplomatic),Journalists & Media,Police,Utilities,Military,Government (General),Airports & Aircraft,Business,Educational Institution,Violent Political Party ,Religious Figures/Institutions,Unknown,Transportation,Tourists,NGO,Telecommunication,Food or Water Supply,Terrorists/Non-State Militia,Other,Maritime, Abortion Related),levels=c("Private Citizens & Property","Government (Diplomatic)","Journalists & Media","Police","Utilities","Military","Government (General)","Airports & Aircraft","Business","Educational Institution","Violent Political Party ","Religious Figures/Institutions","Unknown","Transportation","Tourists","NGO","Telecommunication","Food or Water Supply","Terrorists/Non-State Militia","Other","Maritime", "Abortion Related"))




  # Verificar la distribución de categorías
  tabla_frecuencia <- tabla %>%
    group_by(targtype1_txt) %>%
    summarise(frecuencia = n())

  # Imprimir la tabla de frecuencias
  print(tabla_frecuencia)

  # Visualizar la distribución con un gráfico de barras
  ggplot(tabla, aes(x = targtype1_txt)) +
    geom_bar() +
    labs(title = "Distribución de la Variable Categórica",
        x = "Categoría",
        y = "Frecuencia")

  # Identificar categorías poco frecuentes
  umbral_frecuencia <- 5  # Puedes ajustar este umbral según tus necesidades
  categorias_poco_frecuentes <- tabla_frecuencia %>%
    filter(frecuencia < umbral_frecuencia) %>%
    pull(targtype1_txt)

  # Imprimir categorías poco frecuentes
  if (length(categorias_poco_frecuentes) > 0) {
    cat("Categorías poco frecuentes:", paste(categorias_poco_frecuentes, collapse = ", "), "\n")
  } else {
    cat("No hay categorías poco frecuentes.\n")
  }
  #conteo de targsubtype1
  tabla_frecuencia <- table(tabla$targsubtype1)
  print(tabla_frecuencia)
  #valores perdidos

  # Contar valores perdidos
  valores_perdidos <- sum(is.na(tabla$targsubtype1))

  # Imprimir la cantidad de valores perdidos
  cat("Número de valores perdidos:", valores_perdidos, "\n")


  # Calcular la media de la variable
  media_targsubtype1 <- ceiling(mean(tabla$targsubtype1, na.rm = TRUE))

  # Imputar la media redondeada hacia arriba
  tabla$targsubtype1 <- ifelse(is.na(tabla$targsubtype1), media_targsubtype1, tabla$targsubtype1)


  # Frecuencia de valores en targtype1
  value_counts <- table(tabla$targsubtype1)

  # boxplot targtype1 para ver si tiene valores atipicos
  boxplot(tabla$targsubtype1, horizontal = TRUE, main = "Boxplot de targtype1")

  # Visualización de Frecuencia de targtype1
  barplot(value_counts, main = "Frecuencia de valores en targtype1", xlab = "targtype1", ylab = "Frecuencia")

  # Rellenar los valores vacíos
  tabla$targsubtype1_txt <- replace(tabla$targsubtype1_txt, tabla$targsubtype1_txt == "", "International Organization (peacekeeper, aid agency, compound)")


  tabla_frecuencia <- table(tabla$targsubtype1_txt)
  print(tabla_frecuencia)

  #tabla de frecuencias para corp1
  tabla_frecuencia <- table(tabla$corp1)
  print(tabla_frecuencia)



  # Calcular la frecuencia de cada categoría
  frecuencia_categorias <- tabla %>%
    group_by(corp1) %>%
    summarise(frecuencia = n())

  # Definir un umbral de frecuencia para categorías poco frecuentes
  umbral_frecuencia <- 10  # Puedes ajustar este umbral según tus necesidades

  # Identificar las categorías poco frecuentes
  categorias_poco_frecuentes <- frecuencia_categorias %>%
    filter(frecuencia < umbral_frecuencia) %>%
    pull(corp1)

  # Agrupar las categorías poco frecuentes bajo una etiqueta común
  tabla <- tabla %>%
    mutate(variable_texto_agrupada = ifelse(corp1 %in% categorias_poco_frecuentes, "Otras", corp1))




  # Verificar la distribución de categorías
  tabla_frecuencia <- tabla %>%
    group_by(corp1) %>%
    summarise(frecuencia = n())

  # Imprimir la tabla de frecuencias
  print(tabla_frecuencia)

  # Visualizar la distribución con un gráfico de barras
  #ggplot(tabla, aes(x = corp1)) +
  # geom_bar() +
    #labs(title = "Distribución de la Variable Categórica",
    #    x = "Categoría",
      #   y = "Frecuencia")

  # Identificar categorías poco frecuentes
  #umbral_frecuencia <- 5  # Puedes ajustar este umbral según tus necesidades
  #categorias_poco_frecuentes <- tabla_frecuencia %>%
  # filter(frecuencia < umbral_frecuencia) %>%
    #pull(corp1)

  # Imprimir categorías poco frecuentes
  #if (length(categorias_poco_frecuentes) > 0) {
  # cat("Categorías poco frecuentes:", paste(categorias_poco_frecuentes, collapse = ", "), "\n")
  #} else {
  # cat("No hay categorías poco frecuentes.\n")
  #}


  #tabla de frecuencias para corp1
  tabla_frecuencia <- table(tabla$target1)
  print(tabla_frecuencia)


  # Contar los valores perdidos (cadenas vacías)
  valores_perdidos_contados <- sum(is.na(tabla$target1) | tabla$target1 == "")

  # Imprimir el resultado
  cat("Número de valores perdidos (cadenas vacías):", valores_perdidos_contados, "\n")


  # Calcular la frecuencia de cada categoría
  frecuencia_categorias <- tabla %>%
    group_by(target1) %>%
    summarise(frecuencia = n())

  # Definir un umbral de frecuencia para categorías poco frecuentes
  umbral_frecuencia <- 10  # Puedes ajustar este umbral según tus necesidades

  # Identificar las categorías poco frecuentes
  categorias_poco_frecuentes <- frecuencia_categorias %>%
    filter(frecuencia < umbral_frecuencia) %>%
    pull(target1)

  # Agrupar las categorías poco frecuentes bajo una etiqueta común
  tabla <- tabla %>%
    mutate(variable_texto_agrupada = ifelse(target1 %in% categorias_poco_frecuentes, "Otras", target1))

  #hacemos una tabla con el conteo de las categorias de natlty1
  tabla_frecuencia <- table(tabla$natlty1)
  print(tabla_frecuencia)

  table(tabla$natlty1, useNA = "ifany")

  # Calcular la media de la variable cuantitativa
  media_natlty1 <- mean(tabla$natlty1, na.rm = TRUE)

  # Imputar los valores perdidos con el techo de la media
  tabla$natlty1 <- ifelse(is.na(tabla$natlty1), ceiling(media_natlty1), tabla$natlty1)








  # Calcular el rango intercuartílico (IQR) para ver si targtype tiene valore
  Q1 <- quantile(tabla$natlty1, 0.25)
  Q3 <- quantile(tabla$natlty1, 0.75)
  IQR <- Q3 - Q1

  # Definir límites para identificar valores atípicos
  lower_limit <- Q1 - 1.5 * IQR
  upper_limit <- Q3 + 1.5 * IQR

  # Identificar valores atípicos
  outliers <- tabla$natlty1 < lower_limit | tabla$natlty1 > upper_limit

  # Mostrar valores atípicos
  outlier_values <- tabla$natlty1[outliers]
  cat("Valores atípicos en natlty1:", unique(outlier_values), "\n")

  # Valores atípicos que deseas eliminar
  valores_atipicos <- c(422, 359, 999, 403, 362, 603, 604, 377, 605, 349, 520, 351, 334, 1001, 347, 1003, 1002, 1004)

  # Filtrar el dataframe para excluir filas con valores atípicos
  tabla <- tabla[!tabla$natlty1 %in% valores_atipicos, ]








  # Obtiene los niveles únicos en el orden en que aparecen los datos
  unique_levels <- unique(tabla$natlty1_txt)

  # Convierte a factor con niveles manuales
  tabla$natlty1_txt <- factor(tabla$natlty1_txt, levels = unique_levels)

  # Verifica que la columna haya sido convertida a factor con los niveles deseados
  str(tabla$natlty1_txt)

  # imprime 
  print(tabla$natlty1_txt)


  # Contar los valores perdidos (cadenas vacías)
  valores_perdidos_contados <- sum(is.na(tabla$natlty1_txt) | tabla$natlty1_txt == "")

  # Imprimir el resultado
  cat("Número de valores perdidos (cadenas vacías):", valores_perdidos_contados, "\n")







  #eliminamos targtype2 pues es imposible imputar datos

  tabla$targtype2 <- NULL



  #eliminamos targtype2_txt pues es imposible imputar datos

  tabla$targtype2_txt <- NULL



  #eliminamos targsubtype2 pues es imposible imputar datos

  tabla$targsubtype2 <- NULL

  #eliminamos targsubtype2_txt pues es imposible imputar datos

  tabla$targsubtype2_txt <- NULL


  #eliminamos corp2 pues es imposible imputar datos

  tabla$corp2 <- NULL

  #eliminamos target2 pues es imposible imputar datos

  tabla$target2 <- NULL

  #eliminamos natlty2 pues es imposible imputar datos

  tabla$natlty2 <- NULL

  #eliminamos natlty2_txt pues es imposible imputar datos

  tabla$natlty2_txt <- NULL


  #eliminamos targtype3 pues es imposible imputar datos

  tabla$targtype3 <- NULL



  #eliminamos targtype3_txt pues es imposible imputar datos

  tabla$targtype3_txt <- NULL



  #eliminamos targsubtype3 pues es imposible imputar datos

  tabla$targsubtype3 <- NULL

  #eliminamos targsubtype3_txt pues es imposible imputar datos

  tabla$targsubtype3_txt <- NULL

  #eliminamos corp3 pues es imposible imputar datos

  tabla$corp3 <- NULL

  #eliminamos target3 pues es imposible imputar datos

  tabla$target3 <- NULL

  #eliminamos natlty3 pues es imposible imputar datos

  tabla$natlty3 <- NULL

  #eliminamos natlty2_txt pues es imposible imputar datos

  tabla$natlty3_txt <- NULL

  # Contar los valores perdidos (cadenas vacías)
  valores_perdidos_contados <- sum(is.na(tabla$gname) | tabla$gname == "")

  # Imprimir el resultado
  cat("Número de valores perdidos (cadenas vacías):", valores_perdidos_contados, "\n")

  # Obtiene los niveles únicos en el orden en que aparecen los datos
  unique_levels <- unique(tabla$gname)

  # Convierte a factor con niveles manuales
  tabla$gname <- factor(tabla$gname, levels = unique_levels)

  # Verifica que la columna haya sido convertida a factor con los niveles deseados
  str(tabla$gname)


  #eliminamos gsubname pues es imposible imputar datos

  tabla$gsubname <- NULL

  #eliminamos gname2 pues es imposible imputar datos

  tabla$gname2 <- NULL

  #eliminamos gsubname2 pues es imposible imputar datos

  tabla$gsubname2 <- NULL

  #eliminamos gname3 pues es imposible imputar datos

  tabla$gname3 <- NULL

  #eliminamos gsubname3 pues es imposible imputar datos

  tabla$gsubname3 <- NULL

  #podemos guardar los motivos de algunos grupos antes de borrar la columna con 
  # write.csv(tabla$motive, file = "ruta/del/archivo.csv", row.names = FALSE)

  #eliminamos motive pues es imposible imputar datos

  tabla$motive <- NULL

  # checamos si guncertain1 tiene valores perdidos
  valores_perdidos <- sum(is.na(tabla$guncertain1))

  cat("Número de valores perdidos en guncertain1:", valores_perdidos, "\n")



  # imputacion de guncertain con el techo de la media
  media_guncertain1 <- mean(tabla$guncertain1, na.rm = TRUE)
  techo_media <- ceiling(media_guncertain1)

  # Imputar valores faltantes con el techo de la media
  tabla$guncertain1 <- ifelse(is.na(tabla$guncertain1), techo_media, tabla$guncertain1)


  #eliminamos guncertain2 pues es imposible imputar datos

  tabla$guncertain2 <- NULL


  #eliminamos guncertain3 pues es imposible imputar datos

  tabla$guncertain3 <- NULL
  




  # Obtiene los niveles únicos en el orden en que aparecen los datos
  unique_levels <- unique(tabla$corp1)

  # Convierte a factor con niveles manuales
  tabla$corp1 <- factor(tabla$corp1 , levels = unique_levels)

  # Verifica que la columna haya sido convertida a factor con los niveles deseados
  str(tabla$corp1)

  # Suponiendo que tu dataframe se llama "tabla"
  tabla <- tabla %>%
    mutate(corp1 = ifelse(corp1 == 1, 924, corp1))

  # Suponiendo que tu dataframe se llama "tabla"
  tabla$corp1 <- ifelse(is.na(tabla$corp1), 936, tabla$corp1)


  # Obtiene los niveles únicos en el orden en que aparecen los datos
  unique_levels <- unique(tabla$corp1)

  # Convierte a factor con niveles manuales
  tabla$corp1 <- factor(tabla$corp1 , levels = unique_levels)

  # Verifica que la columna haya sido convertida a factor con los niveles deseados
  str(tabla$corp1)



  # Obtiene los niveles únicos en el orden en que aparecen los datos
  unique_levels <- unique(tabla$targsubtype1_txt)

  # Convierte a factor con niveles manuales
  tabla$targsubtype1_txt <- factor(tabla$targsubtype1_txt , levels = unique_levels)

  # Verifica que la columna haya sido convertida a factor con los niveles deseados
  str(tabla$targsubtype1_txt)


  # cambiamos las cadenas vacias a la categoria Unnamed Civilian/Unspecified
  tabla <- tabla %>%
    mutate(targsubtype1_txt = ifelse(targsubtype1_txt == 13, 45, targsubtype1_txt))
  #regresamos a facotor targetsubtype1_txt
  # Obtiene los niveles únicos en el orden en que aparecen los datos
  unique_levels <- unique(tabla$targsubtype1_txt)

  # Convierte a factor con niveles manuales
  tabla$targsubtype1_txt <- factor(tabla$targsubtype1_txt , levels = unique_levels)

  # Verifica que la columna haya sido convertida a factor con los niveles deseados
  str(tabla$targsubtype1_txt)






  # Obtiene los niveles únicos en el orden en que aparecen los datos
  unique_levels <- unique(tabla$target1)

  # Convierte a factor con niveles manuales
  tabla$target1 <- factor(tabla$target1 , levels = unique_levels)

  # Verifica que la columna haya sido convertida a factor con los niveles deseados
  str(tabla$target1)



  # Suponiendo que tu dataframe se llama "tabla"
  tabla <- tabla %>%
    mutate(target1 = ifelse(is.na(target1), "Civilians", target1))


  # Obtiene los niveles únicos en el orden en que aparecen los datos
  unique_levels <- unique(tabla$target1)

  # Convierte a factor con niveles manuales
  tabla$target1 <- factor(tabla$target1 , levels = unique_levels)

  # Verifica que la columna haya sido convertida a factor con los niveles deseados
  str(tabla$target1)

  #Convierte a factor corrección
  tabla$targsubtype1_txt <- as.factor(tabla$targsubtype1_txt)
  tabla$corp1 <- as.factor(tabla$corp1)
  tabla$target1 <- as.factor(tabla$target1)

  return (tabla)
}

data <- manejo2(data)






manejo3 <- function(table){
  # Seleccionar atributos relevantes
  selected_data <- table %>% select(individual, nkill, nwound, weaptype1_txt, attacktype1_txt, targtype1_txt, gname, country_txt)

  # Definir limites de los valores
  calculate_bounds <- function(x) {
    Q1 <- quantile(x, 0.25, na.rm = TRUE)
    Q3 <- quantile(x, 0.75, na.rm = TRUE)
    IQR <- Q3 - Q1
    lower_bound <- Q1 - 1.5 * IQR
    upper_bound <- Q3 + 1.5 * IQR
    return(c(lower = lower_bound, upper = upper_bound))
  }

  # Definir funcion para eliminar o limitar valores atipicos
  limit_outliers <- function(x) {
    bounds <- calculate_bounds(x)
    x[x < bounds["lower"]] <- bounds["lower"]
    x[x > bounds["upper"]] <- bounds["upper"]
    return(x)
  }

  # Aplicar funcion de limites de valores atipicos
  selected_data$nkill <- limit_outliers(selected_data$nkill)
  selected_data$nwound <- limit_outliers(selected_data$nwound)
  selected_data$individual <- limit_outliers(selected_data$individual)

  # Imputacion de valores perdidos para variables numericas
  selected_data <- selected_data %>% mutate(
    nkill = ifelse(is.na(nkill), median(nkill, na.rm = TRUE), nkill),
    nwound = ifelse(is.na(nwound), median(nwound, na.rm = TRUE), nwound)
  )

  # Imputacion para variables categoricas
  impute_mode <- function(x) {
    ux <- unique(x)
    ux[which.max(tabulate(match(x, ux)))]
  }

  selected_data <- selected_data %>% mutate(
    weaptype1_txt = ifelse(is.na(weaptype1_txt), impute_mode(weaptype1_txt), weaptype1_txt),
    attacktype1_txt = ifelse(is.na(attacktype1_txt), impute_mode(attacktype1_txt), attacktype1_txt),
    targtype1_txt = ifelse(is.na(targtype1_txt), impute_mode(targtype1_txt), targtype1_txt),
    gname = ifelse(is.na(gname), impute_mode(gname), gname),
    country_txt = ifelse(is.na(country_txt), impute_mode(country_txt), country_txt)
  )

  # Normalizacion de variables numericas (nkill, nwound)
  numeric_data <- selected_data %>% select(nkill, nwound)
  preproc <- preProcess(numeric_data, method = c("center", "scale"))
  normalized_data <- predict(preproc, numeric_data)

  # Combinar datos normalizados con datos no numericos
  selected_data <- bind_cols(selected_data %>% select(-nkill, -nwound), normalized_data)

  # Discretizacion de nkill (aplicada despues de la normalizacion)
  selected_data$nkill_discretizado <- cut(selected_data$nkill, breaks=c(-Inf, 0, 10, 50, Inf), labels=c("Muy bajo", "Bajo", "Medio", "Alto"))

  # Cambio de Character a factor
  selected_data[sapply(selected_data, is.character)] <- lapply(selected_data[sapply(selected_data, is.character)], factor)

  # Guardar los datos procesados
  table$nkill <- selected_data$nkill
  table$nwound <- selected_data$nwound
  table$individual <- selected_data$individual
  table$weaptype1_txt <- selected_data$weaptype1_txt 
  table$attacktype1_txt <- selected_data$attacktype1_txt
  table$targtype1_txt <- selected_data$ targtype1_txt
  table$gname <- selected_data$gname
  table$country_txt <- selected_data$country_txt
  
  return (selected_data)
}

data_aux <- manejo3(data)
summary(data_aux)



manejo4 <- function(table){
  atipicosIQR <- function(data_column){
    data_column
    iqr <- IQR(data_column, na.rm = TRUE)
    
    limite_superior <- quantile(data_column, 0.75, na.rm = TRUE) + 1.5 * iqr
    limite_inferior <- quantile(data_column, 0.25, na.rm = TRUE) - 1.5 * iqr
    
    valores_atipicos <- data_column[data_column > limite_superior | data_column < limite_inferior]
    #valores_atipicos <- unique(valores_atipicos)
    valores_atipicos <- valores_atipicos[!is.na(valores_atipicos)]
    return (valores_atipicos)
    
  }

  #Eliminación de columnas y valores atípicos ====================================================================================================================
  #column nwoundus
  table <- subset(table, select = -c(nwoundus))
  #column nwoundte
  table <- subset(table, select = -c(nwoundte))
  #column propextent
  table <- subset(table, select = -c(propextent))
  #column propextent_txt
  table <- subset(table, select = -c(propextent_txt))
  #column propvalue
  table <- table %>%
            mutate(propvalue = ifelse((property == 0), 0, propvalue))%>%
            mutate(propvalue = ifelse((property == -9), NA, propvalue))%>%
            mutate(propvalue = ifelse((propvalue == -99), NA, propvalue))
  table <- table[!(table$propvalue %in% atipicosIQR(table$propvalue)),]
  #column property
  table <- subset(table, select = -c(property))
  #column propcomment
  table <- subset(table, select = -c(propcomment))
  #column nhostkid
  table <- table %>%
            mutate(nhostkid = ifelse((ishostkid == 0), 0, nhostkid))%>%
            mutate(nhostkid = ifelse((ishostkid == -9), NA, nhostkid))%>%
            mutate(nhostkid = ifelse((nhostkid == -99), NA, nhostkid))
  data_aux2 <- table[!(table$nhostkid %in% atipicosIQR(table$nhostkid)),]
  #column ishostkid
  table <- subset(table, select = -c(ishostkid))
  #column nhostkidus
  table <- subset(table, select = -c(nhostkidus))
  #column nhours
  table <- table %>% 
                  mutate(ndays = ifelse((ndays == -99), NA, ndays))%>%
                  mutate(ndays = ifelse((ndays == -9), NA, ndays))
  table <- table %>% 
                  mutate(nhours = ifelse((nhours == -99), NA, nhours))%>%
                  mutate(nhours = ifelse((nhours == -9), NA, nhours))%>%
                  mutate(nhours = ifelse((is.na(nhours)),  (24*ndays), ifelse(is.na(ndays), nhours, (nhours+(24*ndays)))))
  table <- table[!(table$nhours %in% atipicosIQR(table$nhours)),]
  #column ndays
  table <- subset(table, select = -c(ndays))
  #column divert
  table$divert <- as.factor(table$divert)
  #column kidhijcountry
  table$kidhijcountry <- as.factor(table$kidhijcountry)
  #column ransomamt
  table <- table %>%
              mutate(ransomamt = ifelse((ransom == 0), 0, ransomamt))%>%
              mutate(ransomamt = ifelse((ransom == -9), NA, ransomamt))%>%
              mutate(ransomamt = ifelse((ransomamt == -99), NA, ransomamt))
  #column ransomamtus
  table <- subset(table, select = -c(ransomamtus))
  #column ransompaid
  table <- table %>%
    mutate(ransompaid = ifelse((ransom == 0), 0, ransompaid))%>%
    mutate(ransompaid = ifelse((ransom == -9), NA, ransompaid))%>%
    mutate(ransompaid = ifelse((ransom == -99), NA, ransompaid))

  table <- table[!(table$ransompaid %in% atipicosIQR(table$ransompaid)),]
  #column ransompaidus
  table <- subset(table, select = -c(ransompaidus))
  #column ransomnote
  table <- subset(table, select = -c(ransomnote))
  #column ransom
  table <- subset(table, select = -c(ransom))
  #column hostkidoutcome
  table <- subset(table, select = -c(hostkidoutcome))
  #column hostkidoutcome_txt
  table$hostkidoutcome_txt <- as.factor(table$hostkidoutcome_txt)
  #column nreleased
  table <- table[!(table$nreleased %in% atipicosIQR(table$nreleased)),]
  #column addnotes
  table <- subset(table, select = -c(addnotes))
  #column scite1
  table <- subset(table, select = -c(scite1))
  #column scite2
  table <- subset(table, select = -c(scite2))
  #column scite3
  table <- subset(table, select = -c(scite3))
  #column dbsource
  table <- subset(table, select = -c(dbsource))
  #column INT_LOG
  table <- table[!(table$INT_LOG %in% atipicosIQR(table$INT_LOG)),]
  #column INT_IDEO
  table <- table[!(table$INT_IDEO %in% atipicosIQR(table$INT_IDEO)),]
  #column INT_MISC
  table <- table[!(table$INT_MISC %in% atipicosIQR(table$INT_MISC)),]
  #column INT_ANY
  table <- table[!(table$INT_ANY %in% atipicosIQR(table$INT_ANY)),]
  #column related
  table <- subset(table, select = -c(related))

  #Imputación de columnas==================================================================================================================

  media_aux <- mean(table$propvalue, na.rm = TRUE)
  table$propvalue <- ifelse(is.na(table$propvalue), media_aux, table$propvalue)

  media_aux <- mean(table$nhostkid, na.rm = TRUE)
  table$nhostkid <- ifelse(is.na(table$nhostkid), media_aux, table$nhostkid)
  
  media_aux <- mean(table$nhours, na.rm = TRUE)
  table$nhours <- ifelse(is.na(table$nhours), media_aux, table$nhours)

  media_aux <- mean(table$ransomamt, na.rm = TRUE)
  table$ransomamt <- ifelse(is.na(table$ransomamt), media_aux, table$ransomamt)

  media_aux <- mean(table$ransompaid, na.rm = TRUE)
  table$ransompaid <- ifelse(is.na(table$ransompaid), media_aux, table$ransompaid)

  media_aux <- mean(table$nreleased, na.rm = TRUE)
  table$nreleased <- ifelse(is.na(table$nreleased), media_aux, table$nreleased)
  
  media_aux <- mean(table$INT_LOG, na.rm = TRUE)
  table$INT_LOG <- ifelse(is.na(table$INT_LOG), media_aux, table$INT_LOG)

  media_aux <- mean(table$INT_IDEO, na.rm = TRUE)
  table$INT_IDEO <- ifelse(is.na(table$INT_IDEO), media_aux, table$INT_IDEO)
  
  media_aux <- mean(table$INT_MISC, na.rm = TRUE)
  table$INT_MISC <- ifelse(is.na(table$INT_MISC), media_aux, table$INT_MISC)

  media_aux <- mean(table$INT_ANY, na.rm = TRUE)
  table$INT_ANY <- ifelse(is.na(table$INT_ANY), media_aux, table$INT_ANY)
  #Discretización de columnas

  #Normalización de columnas
  table$ransomamt <- scale(table$ransomamt)

  return (table)
}

  
  
data <- manejo4(data)

summary(data)
write.csv(data, "E:/Descargas/Repos/AMD-2024-1/datosPrepTerrorismo.csv", row.names=TRUE)

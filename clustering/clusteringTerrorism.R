#cargamos los paquetes necesarios
library(dplyr)
library(readxl)
library(tibble)
library(tidyverse)
library(cluster)
library(factoextra)
library(NbClust)
library(tidyr)
library(textshape)
library(stats)
library(ggplot2)
library(plotly)

#cargamos el frame work
data<-read.csv("C:/AMD/datosPrepTerrorismo.csv")

# Seleccionamos las regiones donde se presentaron los ataques, los años, y el
#numero de bajas
columnas_cluster <- data[, c( "iyear", "region", "region")]

# Eliminamos filas con valores NA en caso de ser necesario
columnas_cluster <- columnas_cluster[complete.cases(columnas_cluster), ]

# Escalamos los datos
data_escalados <- scale(columnas_cluster)
#como nuestro conjunto de datos es muy grande, arriba de 50 GB de informacion
#y no tenemos una computadora con el poder de computo suficiente
#tomaremos una muestra de los datos para hacer un grafo con wss y con silhouette
#de Partitioning Around Medoids 
#muestra de los datos
set.seed(123)
muestra <- columnas_cluster[sample(nrow(columnas_cluster), 10000), ]
fviz_nbclust(muestra, pam, method = "wss")
fviz_nbclust(muestra, pam, method = "silhouette")

#como arrojaron los grafos de arriba el numero de clusters deberia ser entre 5 y 7
#para determinar el optimo usaremos NbClust
resnumclust <- NbClust(muestra_data, distance = "euclidean", min.nc = 2, max.nc = 10, 
                       method = "kmeans", index = "all")
resnumclust


#calculamos los dos clústers, uno con 5(optimno) y otro con 2
pam5 <- pam(muestra, 5)
print(pam5)
pam2 <- pam(muestra, 2)
print(pam2)

#probamos algunas visualizaciones
fviz_cluster(pam2, data = muestra_data)
fviz_cluster(pam5, data = muestra_data)


# como en el dendograma perdemos visibilidad con la muestra de 2000 datos
#tomaremos una nueva muestra de 100
set.seed(123) 
muestra_dend<- data_escalados[sample(nrow(data_escalados), 100), ]

# Calculamos el clúster jerárquico con 5 grupos
res5 <- hcut(muestra_dend, k = 5, stand = TRUE, method = "median")
# Calculamos el clúster jerárquico con 2 grupos
res2 <- hcut(muestra_dend, k = 2, stand = TRUE, method = "median")

# Visualizar el dendrograma del subconjunto
fviz_dend(res5, rect = TRUE, cex = 0.5, k_colors = "simpsons")
# Visualizar el dendrograma del subconjunto
fviz_dend(res2, rect = TRUE, cex = 0.5, k_colors = "simpsons")

# Especificamos el número de clusters al obtenido con la muestra de 2000
num_clusters <- 5

# Realiza el análisis de k-means
kmeans_model <- kmeans(data_escalados, centers = num_clusters, nstart = 10)

# Añade la información de los clusters al dataFrame original
data$cluster <- as.factor(kmeans_model$cluster)

# Visualiza la asignación de los clusters
table(data$cluster)

# Visualización de las relaciones entre variables  iyear y bajas
ggplot(data = data, aes(x = iyear, y = nkill, color = factor(cluster))) +
  geom_point() +
  labs(title = "Scatter Plot de iyear vs. region por Cluster",
       x = "iyear",
       y = "nkill",
       color = "Cluster") +
  theme_minimal()

# Crear un gráfico de dispersión interactivo con plotly
interactiveplot <- plot_ly(
  data = columnas_cluster, 
  x = ~iyear, 
  y = ~region, 
  color = ~factor(data$cluster), 
  type = "scatter", 
  mode = "markers"
) %>%
  layout(
    title = "Scatter Plot de iyear vs. region por Cluster",
    xaxis = list(title = "Año"),
    yaxis = list(title = "Región")
  )

# Mostrar la visualización
interactiveplot

# creamos nuevos data.frame con las variables de interes

set.seed(123)
datos <- data[, c( "cluster", "region")]

# Diagrama de Violín
ggplot(datos, aes(x = factor(cluster), y = region, fill = factor(cluster))) +
  geom_violin() +
  geom_boxplot(width = 0.1, fill = "white", color = "black") +
  labs(title = "Diagrama de Violín por Cluster", x = "Cluster", y = "region") +
  theme_minimal()

# Perfil de Cluster (Media y Desviación Estándar)
perfil_cluster <- datos %>%
  group_by(cluster) %>%
  summarise(
    media_region = mean(region),
    sd_region = sd(region)
  )

# Visualización del Perfil de Cluster
ggplot(perfil_cluster, aes(x = factor(cluster), y = media_region, fill = factor(cluster))) +
  geom_bar(stat = "identity", position = "dodge", color = "black") +
  geom_errorbar(aes(ymin = media_region - sd_region, ymax = media_region + sd_region),
                position = position_dodge(width = 0.9), width = 0.25, color = "black") +
  labs(title = "Perfil de Cluster (Media ± SD)", x = "Cluster", y = "Media region") +
  theme_minimal()




set.seed(123)
datos <- data[, c( "cluster", "nkill")]

# Diagrama de Violín
ggplot(datos, aes(x = factor(cluster), y = nkill, fill = factor(cluster))) +
  geom_violin() +
  geom_boxplot(width = 0.1, fill = "white", color = "black") +
  labs(title = "Diagrama de Violín por Cluster", x = "Cluster", y = "nkill") +
  theme_minimal()

# Perfil de Cluster (Media y Desviación Estándar)
perfil_cluster <- datos %>%
  group_by(cluster) %>%
  summarise(
    media_nkill = mean(nkill),
    sd_nkill = sd(nkill)
  )

# Visualización del Perfil de Cluster
ggplot(perfil_cluster, aes(x = factor(cluster), y = media_nkill, fill = factor(cluster))) +
  geom_bar(stat = "identity", position = "dodge", color = "black") +
  geom_errorbar(aes(ymin = media_nkill - sd_nkill, ymax = media_nkill + sd_nkill),
                position = position_dodge(width = 0.9), width = 0.25, color = "black") +
  labs(title = "Perfil de Cluster (Media ± SD)", x = "Cluster", y = "Media nkill") +
  theme_minimal()


set.seed(123)
datos <- data[, c( "cluster", "iyear")]

# Diagrama de Violín
ggplot(datos, aes(x = factor(cluster), y = iyear, fill = factor(cluster))) +
  geom_violin() +
  geom_boxplot(width = 0.1, fill = "white", color = "black") +
  labs(title = "Diagrama de Violín por Cluster", x = "Cluster", y = "iyear") +
  theme_minimal()

# Perfil de Cluster (Media y Desviación Estándar)
perfil_cluster <- datos %>%
  group_by(cluster) %>%
  summarise(
    media_iyear = mean(iyear),
    sd_iyear = sd(iyear)
  )

# Visualización del Perfil de Cluster
ggplot(perfil_cluster, aes(x = factor(cluster), y = media_iyear, fill = factor(cluster))) +
  geom_bar(stat = "identity", position = "dodge", color = "black") +
  geom_errorbar(aes(ymin = media_iyear - sd_iyear, ymax = media_iyear + sd_iyear),
                position = position_dodge(width = 0.9), width = 0.25, color = "black") +
  labs(title = "Perfil de Cluster (Media ± SD)", x = "Cluster", y = "Media iyear") +
  theme_minimal()

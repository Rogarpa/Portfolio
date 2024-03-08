library(dplyr)
library(caret)
library(rpart.plot)

####### ÁRBOL DE DECISIÓN CART #######

original <- read.csv("../code/R/proyecto/src/datosPrepTerrorismo.csv")
summary(original)

# Atributos seleccinados
dataset <- original[,c("iday","attacktype1","attacktype2", "suicide")]

# Convertir la variable "suicide" a factor y asignar etiquetas a los factores
dataset$suicide <- as.factor(ifelse(dataset$suicide==0,"NoSuicidio","Suicidio"))
dataset$attacktype1 <- as.factor(dataset$attacktype1)
dataset$attacktype2 <- as.factor(dataset$attacktype2)

str(dataset)
summary(dataset)

dataset <- na.omit(dataset)
set.seed(9999)

# Crear partición de datos para entrenamiento y prueba
train <- createDataPartition(dataset[,"suicide"], p = 0.8, list = FALSE)
dataset.trn <- dataset[train,]
dataset.tst <- dataset[-train,]

# Configuración del control para la validación cruzada
ctrl <- trainControl(method = "cv", number = 10)

# Entrenar un modelo de árbol de decisión CART con validación cruzada
fit.cv <- train(suicide ~ ., data = dataset.trn, method = "rpart",
                trControl = ctrl,
                tuneLength = 30)

# Realizar predicciones en el conjunto de prueba
pred <- predict(fit.cv, dataset.tst)

# Calcular la matriz de confusión
confusionMatrix(table(dataset.tst[,"suicide"], pred))

# Impresión en pantalla el arbol de decisión
print(fit.cv)
plot(fit.cv)
rpart.plot(fit.cv$finalModel, fallen.leaves = FALSE)
# Salads Menu Project
![Java](https://img.shields.io/badge/java-%23ED8B00.svg?style=for-the-badge&logo=openjdk&logoColor=white)
![Spring](https://img.shields.io/badge/spring-%236DB33F.svg?style=for-the-badge&logo=spring&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![Bootstrap](https://img.shields.io/badge/bootstrap-%238511FA.svg?style=for-the-badge&logo=bootstrap&logoColor=white)

![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)



---
<p align="center">
  <img src="./README_utilites/landing_page.png" alt="image of landing page" width="450"/>
</p>
<p align="center">Landing page</p>

<p align="center">
  <img src="./README_utilites/input_checkers.png" alt="image of input red warning checker " width="450"/>
</p>
<p align="center">Form for ingredients with data backend checking</p>

<p align="center">
  <img src="./README_utilites/Inventary_filled.png" alt="inventary filled with ingredients " width="450"/>
</p>
<p align="center">Dynamic inventary</p>

<p align="center">
  <img src="./README_utilites/form_edition.png" alt="inventary filled with ingredients " width="450"/>
</p>
<p align="center">Edition and deletion of inserted ingredients</p>

## Overview

The Salads Menu Project is a web application designed to showcase a variety of delicious salad options. This project aims to provide users with an easy-to-use interface to explore different salad recipes, ingredients, and nutritional information.

## Universal Skills Involved
 - **OOP**
 - **Dependencies Management**
 - **Framework Documentation**
 - **Object Realational Mepper**
 - **Project Building Tools**

## Features

1. **Browse Salad Options**: Users can browse through a selection of diverse salad options.
2. **View Recipe Details**: Each salad option provides detailed information about its recipe, including ingredients, preparation steps, and nutritional facts.
2. **Ingredients stock**: Allows having a record of ingredients included their stock.

## Technologies Used

- **Frontend**:
  - HTML5
  - CSS3
  - Bootstrap (for styling)

- **Backend**:
  - Springboot framework for Java __(v17)__
  - PostgreSQL
  


## Technologies Used inside Spring Framework

1. **Spring Framework**: The core of the application is built using the Spring Framework.

2. **Spring Boot**: Often used to quickly bootstrap and set up Spring applications, Spring Boot simplifies the configuration and setup of Spring-based projects.

3. **Spring MVC (Model-View-Controller)**: Fundamental model-view-controller architecture tool.

4. **Spring Data JPA**: Used for high-level abstraction over JPA (Java Persistence API) allowing  developers to interact with the database using methods instead of queries.

10. **Thymeleaf**: Templating engine for server-side rendering.

10. **Lombok**: For java getters and setters shortcut.

11. **Hibernate**: Is used for object-relational mapping (ORM) and data persistence.

These are just some of the technologies commonly used in a Spring application. The actual technologies used may vary depending on the specific requirements and architecture of the application.



## Installation

To explore and utilize the capabilities of the Image Filtering Project, follow these installation instructions:

1. Download or clone this repository
2. Initialize database with:

```sh
docker compose -f ./docker-compose.yml up postgres
```
3. Once you assure it has started up:
  Starts up the springboot server

```sh
docker compose -f ./docker-compose.yml up spring-server
```
[!TIP] The server has changes autodetection, so autorestarts when modifications are made.
[!WARNING] Be carefull docker manually restart it when a major configuration file be 
made. Deleting all with:

```sh
docker compose -f ./docker-compose-db.yml down
```

## Usage
1. Access the application via your browser at 8080 port
  (http://localhost:8080).
- Browse through the list of salads available on the homepage.
- Click on a salad to view its recipe details.
- Manage ingredients on the inventary.

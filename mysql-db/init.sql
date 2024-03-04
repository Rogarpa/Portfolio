USE test;
DROP TABLE IF EXISTS persona;
CREATE TABLE IF NOT EXISTS persona(
id_persona serial PRIMARY KEY,
nombre VARCHAR ( 50 ),
apellidoPaterno VARCHAR ( 50 ),
apellidoMaterno VARCHAR ( 50 ),
cedula VARCHAR ( 50 ),
especialidad VARCHAR ( 50 ),
consultorio VARCHAR ( 50 ),
telefono VARCHAR ( 50 ),
precio FLOAT (15, 2),
universidad VARCHAR ( 50 )
);
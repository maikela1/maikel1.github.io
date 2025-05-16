create database cafeteria;
use cafeteria;


create table Usuarios(
Id_usuario int auto_increment primary key,
Clave int,
Correo varchar(10) null,
Dni int null,
Telefono int null
);

create table Mesas (
Id_mesa int auto_increment primary key,
Nombre_mesa int,
Ubicacion int,
Disponibilidad int
);

create table Administrador (
Id_administrador int auto_increment primary key,
Clave int,
Telefono int
);

Create table Reservas (
Id_reserva int auto_increment primary key,
Id_mesa int,
Id_usuario int,
comensales int,
Fecha Date,
Horas Time,
Requisitos text,
estado varchar(10),
foreign key (Id_mesa) references Mesas (Id_mesa),
foreign key (Id_usuario) references Usuarios (Id_usuario)
);

create table Historial_reservas (
Id_historial int auto_increment primary key,
Id_usuario int,
foreign key (Id_usuario) references Usuarios (Id_usuario)
);

create table Reservas_cautivas (
Id int auto_increment primary key,
Id_reserva int,
Id_historial int,
Requisitos text,
foreign key (Id_reserva) references Reservas (Id_reserva),
foreign key (Id_historial) references Historial_reservas (Id_historial)
);


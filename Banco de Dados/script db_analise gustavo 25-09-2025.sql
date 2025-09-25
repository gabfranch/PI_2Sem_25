create database db_analise;
use db_analise;

create table tb_centros(
centro_id int(10) not null auto_increment,
nome_centro varchar(255),
primary key (centro_id)
);
drop table tb_leituras;
create table tb_leituras (
id_leitura int(10) not null auto_increment,
dia_hora datetime,
temperatura float,
poeira_1 float,
poeira_2 float,
pressao float,
altitude float,
co2 float,
umidade float,
centro_id int(10),
primary key (id_leitura),
foreign key (centro_id) references tb_centros(centro_id)
);
select * from tb_leituras;
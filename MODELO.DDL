BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "auth_group" (
	"id"	integer NOT NULL,
	"name"	varchar(150) NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "auth_group_permissions" (
	"id"	integer NOT NULL,
	"group_id"	integer NOT NULL,
	"permission_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("group_id") REFERENCES "auth_group"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("permission_id") REFERENCES "auth_permission"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "auth_permission" (
	"id"	integer NOT NULL,
	"content_type_id"	integer NOT NULL,
	"codename"	varchar(100) NOT NULL,
	"name"	varchar(255) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("content_type_id") REFERENCES "django_content_type"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "auth_user" (
	"id"	integer NOT NULL,
	"password"	varchar(128) NOT NULL,
	"last_login"	datetime,
	"is_superuser"	bool NOT NULL,
	"username"	varchar(150) NOT NULL UNIQUE,
	"last_name"	varchar(150) NOT NULL,
	"email"	varchar(254) NOT NULL,
	"is_staff"	bool NOT NULL,
	"is_active"	bool NOT NULL,
	"date_joined"	datetime NOT NULL,
	"first_name"	varchar(150) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "auth_user_groups" (
	"id"	integer NOT NULL,
	"user_id"	integer NOT NULL,
	"group_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("group_id") REFERENCES "auth_group"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("user_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "auth_user_user_permissions" (
	"id"	integer NOT NULL,
	"user_id"	integer NOT NULL,
	"permission_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("permission_id") REFERENCES "auth_permission"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("user_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "cuentas_perfilusuario" (
	"id"	integer NOT NULL,
	"fecha_registro"	datetime NOT NULL,
	"puntuacion_total"	integer NOT NULL,
	"nivel"	integer NOT NULL,
	"retos_completados"	integer NOT NULL,
	"usuario_id"	integer NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("usuario_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "django_admin_log" (
	"id"	integer NOT NULL,
	"object_id"	text,
	"object_repr"	varchar(200) NOT NULL,
	"action_flag"	smallint unsigned NOT NULL CHECK("action_flag" >= 0),
	"change_message"	text NOT NULL,
	"content_type_id"	integer,
	"user_id"	integer NOT NULL,
	"action_time"	datetime NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("content_type_id") REFERENCES "django_content_type"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("user_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "django_content_type" (
	"id"	integer NOT NULL,
	"app_label"	varchar(100) NOT NULL,
	"model"	varchar(100) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "django_migrations" (
	"id"	integer NOT NULL,
	"app"	varchar(255) NOT NULL,
	"name"	varchar(255) NOT NULL,
	"applied"	datetime NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "django_session" (
	"session_key"	varchar(40) NOT NULL,
	"session_data"	text NOT NULL,
	"expire_date"	datetime NOT NULL,
	PRIMARY KEY("session_key")
);
CREATE TABLE IF NOT EXISTS "juego_intento" (
	"id"	integer NOT NULL,
	"respuesta_usuario"	text NOT NULL,
	"es_correcto"	bool NOT NULL,
	"puntuacion_obtenida"	integer NOT NULL,
	"fecha_intento"	datetime NOT NULL,
	"tiempo_respuesta"	bigint,
	"reto_id"	bigint NOT NULL,
	"usuario_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("reto_id") REFERENCES "retos_reto"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("usuario_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "juego_ranking" (
	"id"	integer NOT NULL,
	"posicion"	integer NOT NULL,
	"puntuacion_total"	integer NOT NULL,
	"retos_completados"	integer NOT NULL,
	"fecha_actualizacion"	datetime NOT NULL,
	"usuario_id"	integer NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("usuario_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "retos_categoria" (
	"id"	integer NOT NULL,
	"nombre"	varchar(100) NOT NULL UNIQUE,
	"descripcion"	text NOT NULL,
	"color"	varchar(7) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "retos_configuracionordenamiento" (
	"id"	integer NOT NULL,
	"nombre"	varchar(50) NOT NULL,
	"orden_por_defecto"	varchar(20) NOT NULL,
	"incluir_aleatorios"	bool NOT NULL,
	"max_retos_por_pagina"	integer NOT NULL,
	"activo"	bool NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "retos_respuestaalternativa" (
	"id"	integer NOT NULL,
	"texto"	text NOT NULL,
	"descripcion"	varchar(200) NOT NULL,
	"activa"	bool NOT NULL,
	"fecha_creacion"	datetime NOT NULL,
	"reto_id"	bigint NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("reto_id") REFERENCES "retos_reto"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "retos_reto" (
	"id"	integer NOT NULL,
	"titulo"	varchar(200) NOT NULL,
	"descripcion"	text NOT NULL,
	"enunciado"	text NOT NULL,
	"respuesta_correcta"	text NOT NULL,
	"explicacion"	text NOT NULL,
	"dificultad"	varchar(10) NOT NULL,
	"puntos"	integer NOT NULL,
	"fecha_creacion"	datetime NOT NULL,
	"fecha_modificacion"	datetime NOT NULL,
	"activo"	bool NOT NULL,
	"intentos_totales"	integer NOT NULL,
	"intentos_exitosos"	integer NOT NULL,
	"categoria_id"	bigint,
	"creado_por_id"	integer,
	"mostrar_aleatorio"	bool NOT NULL,
	"orden_prioridad"	integer NOT NULL,
	"max_intentos"	integer NOT NULL,
	"ejemplo_entrada"	text NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("categoria_id") REFERENCES "retos_categoria"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("creado_por_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE INDEX IF NOT EXISTS "auth_group_permissions_group_id_b120cbf9" ON "auth_group_permissions" (
	"group_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_group_permissions_group_id_permission_id_0cd325b0_uniq" ON "auth_group_permissions" (
	"group_id",
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "auth_group_permissions_permission_id_84c5c92e" ON "auth_group_permissions" (
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "auth_permission_content_type_id_2f476e4b" ON "auth_permission" (
	"content_type_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_permission_content_type_id_codename_01ab375a_uniq" ON "auth_permission" (
	"content_type_id",
	"codename"
);
CREATE INDEX IF NOT EXISTS "auth_user_groups_group_id_97559544" ON "auth_user_groups" (
	"group_id"
);
CREATE INDEX IF NOT EXISTS "auth_user_groups_user_id_6a12ed8b" ON "auth_user_groups" (
	"user_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_user_groups_user_id_group_id_94350c0c_uniq" ON "auth_user_groups" (
	"user_id",
	"group_id"
);
CREATE INDEX IF NOT EXISTS "auth_user_user_permissions_permission_id_1fbb5f2c" ON "auth_user_user_permissions" (
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "auth_user_user_permissions_user_id_a95ead1b" ON "auth_user_user_permissions" (
	"user_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_user_user_permissions_user_id_permission_id_14a6b632_uniq" ON "auth_user_user_permissions" (
	"user_id",
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "django_admin_log_content_type_id_c4bce8eb" ON "django_admin_log" (
	"content_type_id"
);
CREATE INDEX IF NOT EXISTS "django_admin_log_user_id_c564eba6" ON "django_admin_log" (
	"user_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "django_content_type_app_label_model_76bd3d3b_uniq" ON "django_content_type" (
	"app_label",
	"model"
);
CREATE INDEX IF NOT EXISTS "django_session_expire_date_a5c62663" ON "django_session" (
	"expire_date"
);
CREATE INDEX IF NOT EXISTS "juego_intento_reto_id_aa291205" ON "juego_intento" (
	"reto_id"
);
CREATE INDEX IF NOT EXISTS "juego_intento_usuario_id_e373507e" ON "juego_intento" (
	"usuario_id"
);
CREATE INDEX IF NOT EXISTS "retos_respuestaalternativa_reto_id_acafbb9a" ON "retos_respuestaalternativa" (
	"reto_id"
);
CREATE INDEX IF NOT EXISTS "retos_reto_categoria_id_dbdde23d" ON "retos_reto" (
	"categoria_id"
);
CREATE INDEX IF NOT EXISTS "retos_reto_creado_por_id_0e41b688" ON "retos_reto" (
	"creado_por_id"
);
COMMIT;

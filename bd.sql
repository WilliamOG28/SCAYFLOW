-- --------------------------------------------------------
-- Host:                         192.168.154.43
-- Versión del servidor:         11.8.2-MariaDB-deb12 - mariadb.org binary distribution
-- SO del servidor:              debian-linux-gnu
-- HeidiSQL Versión:             12.10.0.7000
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Volcando datos para la tabla db_scayflow.auth_group: ~0 rows (aproximadamente)

-- Volcando datos para la tabla db_scayflow.auth_group_permissions: ~0 rows (aproximadamente)

-- Volcando datos para la tabla db_scayflow.auth_permission: ~36 rows (aproximadamente)
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
	(1, 'Can add log entry', 1, 'add_logentry'),
	(2, 'Can change log entry', 1, 'change_logentry'),
	(3, 'Can delete log entry', 1, 'delete_logentry'),
	(4, 'Can view log entry', 1, 'view_logentry'),
	(5, 'Can add permission', 2, 'add_permission'),
	(6, 'Can change permission', 2, 'change_permission'),
	(7, 'Can delete permission', 2, 'delete_permission'),
	(8, 'Can view permission', 2, 'view_permission'),
	(9, 'Can add group', 3, 'add_group'),
	(10, 'Can change group', 3, 'change_group'),
	(11, 'Can delete group', 3, 'delete_group'),
	(12, 'Can view group', 3, 'view_group'),
	(13, 'Can add user', 4, 'add_user'),
	(14, 'Can change user', 4, 'change_user'),
	(15, 'Can delete user', 4, 'delete_user'),
	(16, 'Can view user', 4, 'view_user'),
	(17, 'Can add content type', 5, 'add_contenttype'),
	(18, 'Can change content type', 5, 'change_contenttype'),
	(19, 'Can delete content type', 5, 'delete_contenttype'),
	(20, 'Can view content type', 5, 'view_contenttype'),
	(21, 'Can add session', 6, 'add_session'),
	(22, 'Can change session', 6, 'change_session'),
	(23, 'Can delete session', 6, 'delete_session'),
	(24, 'Can view session', 6, 'view_session'),
	(25, 'Can add cliente', 7, 'add_cliente'),
	(26, 'Can change cliente', 7, 'change_cliente'),
	(27, 'Can delete cliente', 7, 'delete_cliente'),
	(28, 'Can view cliente', 7, 'view_cliente'),
	(29, 'Can add proyecto', 8, 'add_proyecto'),
	(30, 'Can change proyecto', 8, 'change_proyecto'),
	(31, 'Can delete proyecto', 8, 'delete_proyecto'),
	(32, 'Can view proyecto', 8, 'view_proyecto'),
	(33, 'Can add tramite', 9, 'add_tramite'),
	(34, 'Can change tramite', 9, 'change_tramite'),
	(35, 'Can delete tramite', 9, 'delete_tramite'),
	(36, 'Can view tramite', 9, 'view_tramite');

-- Volcando datos para la tabla db_scayflow.auth_user: ~0 rows (aproximadamente)
INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
	(1, 'pbkdf2_sha256$1000000$JTvkV74NjiEWEkzs9ZWIL2$KI69qS4h0yGDYa33RujF9Drs7bNxp18upBIxOxDCm/Y=', '2025-07-07 20:14:25.648352', 1, 'administrador', '', '', 'administrador@gmail.com', 1, 1, '2025-07-04 19:50:54.594378');

-- Volcando datos para la tabla db_scayflow.auth_user_groups: ~0 rows (aproximadamente)

-- Volcando datos para la tabla db_scayflow.auth_user_user_permissions: ~0 rows (aproximadamente)

-- Volcando datos para la tabla db_scayflow.clientes: ~2 rows (aproximadamente)
INSERT INTO `clientes` (`cliente_id`, `nombre`, `email`, `telefono`, `direccion`, `empresa`, `persona_contacto`, `tipo`, `rfc`, `notas`, `fecha_creacion`, `fecha_modificacion`) VALUES
	(1, 'William Orozco', 'williamorozco@gmail.com', '9993871892', 'calle 54 ', 'pei', 'alberto', 'Persona Moral', 'OOGW234312TKA', 'sadasdasdasd', '2025-07-08 00:59:48', '2025-07-08 01:33:26'),
	(3, 'William Orozco', 'williamorozco1@gmail.com', '9993871893', 'calle 54 ', 'pei', 'alberto', 'Persona Física', 'OOGW991228TKA', 'fdvdfgfdg', '2025-07-08 01:07:59', '2025-07-08 01:07:59');

-- Volcando datos para la tabla db_scayflow.django_admin_log: ~0 rows (aproximadamente)

-- Volcando datos para la tabla db_scayflow.django_content_type: ~9 rows (aproximadamente)
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
	(1, 'admin', 'logentry'),
	(3, 'auth', 'group'),
	(2, 'auth', 'permission'),
	(4, 'auth', 'user'),
	(5, 'contenttypes', 'contenttype'),
	(7, 'scayflow', 'cliente'),
	(8, 'scayflow', 'proyecto'),
	(9, 'scayflow', 'tramite'),
	(6, 'sessions', 'session');

-- Volcando datos para la tabla db_scayflow.django_migrations: ~25 rows (aproximadamente)
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
	(1, 'contenttypes', '0001_initial', '2025-06-30 17:16:33.780184'),
	(2, 'auth', '0001_initial', '2025-06-30 17:16:39.765095'),
	(3, 'admin', '0001_initial', '2025-06-30 17:16:40.942523'),
	(4, 'admin', '0002_logentry_remove_auto_add', '2025-06-30 17:16:40.964335'),
	(5, 'admin', '0003_logentry_add_action_flag_choices', '2025-06-30 17:16:40.992234'),
	(6, 'contenttypes', '0002_remove_content_type_name', '2025-06-30 17:16:41.779574'),
	(7, 'auth', '0002_alter_permission_name_max_length', '2025-06-30 17:16:42.236545'),
	(8, 'auth', '0003_alter_user_email_max_length', '2025-06-30 17:16:42.543898'),
	(9, 'auth', '0004_alter_user_username_opts', '2025-06-30 17:16:42.565700'),
	(10, 'auth', '0005_alter_user_last_login_null', '2025-06-30 17:16:43.119133'),
	(11, 'auth', '0006_require_contenttypes_0002', '2025-06-30 17:16:43.137815'),
	(12, 'auth', '0007_alter_validators_add_error_messages', '2025-06-30 17:16:43.159804'),
	(13, 'auth', '0008_alter_user_username_max_length', '2025-06-30 17:16:43.505551'),
	(14, 'auth', '0009_alter_user_last_name_max_length', '2025-06-30 17:16:43.794181'),
	(15, 'auth', '0010_alter_group_name_max_length', '2025-06-30 17:16:44.120292'),
	(16, 'auth', '0011_update_proxy_permissions', '2025-06-30 17:16:44.142262'),
	(17, 'auth', '0012_alter_user_first_name_max_length', '2025-06-30 17:16:44.454668'),
	(18, 'sessions', '0001_initial', '2025-06-30 17:16:44.996664'),
	(19, 'scayflow', '0001_initial', '2025-07-07 18:51:44.014075'),
	(20, 'scayflow', '0002_alter_cliente_rfc_alter_cliente_telefono_proyecto_and_more', '2025-07-07 20:17:39.053303'),
	(21, 'scayflow', '0003_rename_responsable_dependecnia_tramite_responsable_dependencia_and_more', '2025-07-08 14:15:51.009687'),
	(22, 'scayflow', '0004_alter_tramite_duracion_estimada_and_more', '2025-07-08 14:35:27.464852'),
	(23, 'scayflow', '0005_proyecto_utilidades_tramite_utilidades', '2025-07-08 19:08:42.701867'),
	(24, 'scayflow', '0006_rename_utilidades_tramite_utilidad_and_more', '2025-07-08 19:22:26.633481'),
	(25, 'scayflow', '0002_alter_proyecto_utilidad_total', '2025-07-08 19:55:43.383863'),
	(26, 'scayflow', '0002_tramite_tarifa_monto_alter_proyecto_utilidad_total', '2025-07-08 20:49:33.277786');

-- Volcando datos para la tabla db_scayflow.django_session: ~4 rows (aproximadamente)
INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
	('193xve6f4hcfelj0vxw39c3u14st293p', '.eJxVjMsOwiAQRf-FtSG8EZfu-w1kgBmpGkhKuzL-uzbpQrf3nHNfLMK21rgNXOJc2IVJdvrdEuQHth2UO7Rb57m3dZkT3xV-0MGnXvB5Pdy_gwqjfmvls05agCGUmcglq0QwPlApiCI5G84KUNqkMVhDBbXywTvpRcgEEtj7A_TEODs:1uYsEL:Y_ZyfpZ7A7bgAYtmFRHrUuaxpVvMW3fPjp_R8EiW5Fg', '2025-07-21 20:14:25.684954'),
	('e7bxgn1ckuw5lhr69r2ig5ox1xrvktvh', '.eJxVjMsOwiAQRf-FtSG8EZfu-w1kgBmpGkhKuzL-uzbpQrf3nHNfLMK21rgNXOJc2IVJdvrdEuQHth2UO7Rb57m3dZkT3xV-0MGnXvB5Pdy_gwqjfmvls05agCGUmcglq0QwPlApiCI5G84KUNqkMVhDBbXywTvpRcgEEtj7A_TEODs:1uYpmS:dQxXzzBsyixKJWvWZsbb59h7vmm8TmR1Cb97iEoxnnY', '2025-07-21 17:37:28.035149'),
	('ezdilptlyx6esvz497w3g4r3h4my6mlv', '.eJxVjMsOwiAQRf-FtSG8EZfu-w1kgBmpGkhKuzL-uzbpQrf3nHNfLMK21rgNXOJc2IVJdvrdEuQHth2UO7Rb57m3dZkT3xV-0MGnXvB5Pdy_gwqjfmvls05agCGUmcglq0QwPlApiCI5G84KUNqkMVhDBbXywTvpRcgEEtj7A_TEODs:1uXmRC:ZH1jGnbJEV7Qx9K_x_l2npq3QLLD4af-U3j4_vZjDFo', '2025-07-18 19:51:10.189453'),
	('t7rvi6abcd8qbs0cm7u17l4bdqjwc1mg', '.eJxVjMsOwiAQRf-FtSG8EZfu-w1kgBmpGkhKuzL-uzbpQrf3nHNfLMK21rgNXOJc2IVJdvrdEuQHth2UO7Rb57m3dZkT3xV-0MGnXvB5Pdy_gwqjfmvls05agCGUmcglq0QwPlApiCI5G84KUNqkMVhDBbXywTvpRcgEEtj7A_TEODs:1uYphd:a6eGZIo0W1yyr00vSD1vBbSIyPYU9vhL6OI0MfcVsLU', '2025-07-21 17:32:29.588386');

-- Volcando datos para la tabla db_scayflow.pagos: ~0 rows (aproximadamente)

-- Volcando datos para la tabla db_scayflow.proyectos: ~6 rows (aproximadamente)
INSERT INTO `proyectos` (`proyecto_id`, `nombre`, `tipo_proyecto`, `cliente_id`, `estado`, `fecha_inicio`, `fecha_fin`, `descripcion`, `sector`, `costo_base`, `tarifa_porcentaje`, `nota`, `utilidad_total`) VALUES
	(13, 'ACCEN', 'WEB', 1, 'Activo', '2025-07-08', NULL, 'SISTEMA ADMINISTRATIVO', 'SISTEMAS', 50000.00, 15.00, 'ELEMENTOS DE DESARROLLO', NULL),
	(14, 'SADASDAS', 'sadasdas', 1, 'Activo', '2025-07-08', NULL, 'sdasd', 'sadasd', 20000.00, 10.00, 'sdasdas', NULL),
	(15, 'SADASDAS', 'sadasdas', 1, 'Activo', '2025-07-08', NULL, 'sdasd', 'sadasd', 20000.00, 10.00, 'sdasdas', NULL),
	(16, 'ASDASD', 'ASDAS', 1, 'Activo', '2025-07-08', NULL, 'SADASDAS', 'SDSADSA', 20000.00, 10.00, 'SADASDAS', NULL),
	(17, 'SADASDAS', 'ASDASD', 1, 'Activo', '2025-07-08', NULL, 'SDASDAS', 'SADASD', 20000.00, 10.00, 'SADDDASD', NULL),
	(18, 'DSSADAS', 'SDASDAS', 1, 'Activo', '2025-07-08', NULL, 'SDASDAS', 'SADASD', 20000.00, 10.00, 'SDASDAS', 2600.00),
	(19, 'TULAAK', 'DESARROLLO', 1, 'Activo', '2025-07-08', '2025-08-09', 'DESARROLLO DE SISTEMA ADMINISTRATIVO', 'SISTEMAS', 40000.00, 15.00, 'CONTRATACION DE DESARROLLADORES', 6350.00);

-- Volcando datos para la tabla db_scayflow.tramites: ~7 rows (aproximadamente)
INSERT INTO `tramites` (`tramite_id`, `proyecto_id`, `nombre`, `descripcion`, `costo_base`, `tarifa_porcentaje`, `duracion_estimada`, `tiempo_resolucion`, `dependencia`, `responsable_dependencia`, `estatus`, `documentos_requeridos`, `observaciones`, `fecha_ultima_actualizacion`, `fecha_inicio`, `fecha_fin`) VALUES
	(5, 13, 'LICENCIAS', 'LICENCIAS DE ORACLE', 10000.00, 10.00, 10, 30, 'SISTEMAS', 'ALBERTO', 'Pendiente', 'FICHA DE PAGO', 'SELECCIONAR MIEMBROS ', NULL, '2025-07-08', '2025-07-31'),
	(6, 14, 'sadasdsa', 'sdasds', 2000.00, 10.00, 10, 15, 'sdasd', 'sdasd', 'Pendiente', 'sadasd', 'sdada', NULL, '2025-07-08', NULL),
	(7, 15, 'sadasdsa', 'sdasds', 2000.00, 10.00, 10, 15, 'sdasd', 'sdasd', 'Pendiente', 'sadasd', 'sdada', NULL, '2025-07-08', NULL),
	(8, 16, 'ASDDSAD', 'SDADS', 10000.00, 15.00, 10, 15, 'SDASDAS', 'SDAD', 'Pendiente', 'SADASD', 'SDASD', NULL, '2025-07-08', NULL),
	(9, 17, 'ASDASD', 'ADSASD', 5000.00, 10.00, 10, 15, 'SADASD', 'SDASD', 'Pendiente', 'SDASD', 'SDASDASD', NULL, '2025-07-08', NULL),
	(10, 18, 'SADASDAS', 'SDASD', 2000.00, 10.00, 10, 15, 'SDASD', 'SDASD', 'Pendiente', 'SDASD', 'DSASD', NULL, '2025-07-08', NULL),
	(11, 18, 'ADSADAS', 'SDAASD', 4000.00, 10.00, 10, 20, 'SDASDAS', 'DSASD', 'Pendiente', 'SADASD', 'SDASD', NULL, '2025-07-08', '2025-07-31'),
	(12, 19, 'LICENCIA', 'COMPRA DE LICENCIA DE SERVIDOR', 2000.00, 10.00, 10, 15, 'AREA DE SISTEMAS', 'ALBERTO', 'Pendiente', 'FICHA DE PAGO', 'COMPRA DE LICENCIA DE HOSTINGER', NULL, '2025-07-08', '2025-07-10'),
	(13, 19, 'ACTA', 'ACTA DE PERMISOS', 1500.00, 10.00, 1, 3, 'RH', 'LUIS', 'Pendiente', 'PERMISO', 'PRESENTARSE EN DIAS HABILES', NULL, '2025-07-08', '2025-07-12');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;

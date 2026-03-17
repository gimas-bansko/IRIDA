-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1
-- Време на генериране: 17 март 2026 в 22:45
-- Версия на сървъра: 10.4.32-MariaDB
-- Версия на PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данни: `irida`
--

-- --------------------------------------------------------

--
-- Структура на таблица `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура на таблица `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура на таблица `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Схема на данните от таблица `auth_permission`
--

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
(25, 'Can add Документ', 7, 'add_documents'),
(26, 'Can change Документ', 7, 'change_documents'),
(27, 'Can delete Документ', 7, 'delete_documents'),
(28, 'Can view Документ', 7, 'view_documents'),
(29, 'Can add Клас', 8, 'add_klass'),
(30, 'Can change Клас', 8, 'change_klass'),
(31, 'Can delete Клас', 8, 'delete_klass'),
(32, 'Can view Клас', 8, 'view_klass'),
(33, 'Can add Действие', 9, 'add_log'),
(34, 'Can change Действие', 9, 'change_log'),
(35, 'Can delete Действие', 9, 'delete_log'),
(36, 'Can view Действие', 9, 'view_log'),
(37, 'Can add Училище/организация', 10, 'add_school'),
(38, 'Can change Училище/организация', 10, 'change_school'),
(39, 'Can delete Училище/организация', 10, 'delete_school'),
(40, 'Can view Училище/организация', 10, 'view_school'),
(41, 'Can add Специалност', 11, 'add_specialty'),
(42, 'Can change Специалност', 11, 'change_specialty'),
(43, 'Can delete Специалност', 11, 'delete_specialty'),
(44, 'Can view Специалност', 11, 'view_specialty'),
(45, 'Can add Пофил на потребител', 12, 'add_userprofile'),
(46, 'Can change Пофил на потребител', 12, 'change_userprofile'),
(47, 'Can delete Пофил на потребител', 12, 'delete_userprofile'),
(48, 'Can view Пофил на потребител', 12, 'view_userprofile'),
(49, 'Can add Учебен предмет', 13, 'add_subject'),
(50, 'Can change Учебен предмет', 13, 'change_subject'),
(51, 'Can delete Учебен предмет', 13, 'delete_subject'),
(52, 'Can view Учебен предмет', 13, 'view_subject'),
(53, 'Can add Раздел от УП', 14, 'add_unit'),
(54, 'Can change Раздел от УП', 14, 'change_unit'),
(55, 'Can delete Раздел от УП', 14, 'delete_unit'),
(56, 'Can view Раздел от УП', 14, 'view_unit'),
(57, 'Can add Тема от раздел на УП', 15, 'add_tema'),
(58, 'Can change Тема от раздел на УП', 15, 'change_tema'),
(59, 'Can delete Тема от раздел на УП', 15, 'delete_tema'),
(60, 'Can view Тема от раздел на УП', 15, 'view_tema'),
(61, 'Can add Цел на обучението', 16, 'add_goals'),
(62, 'Can change Цел на обучението', 16, 'change_goals'),
(63, 'Can delete Цел на обучението', 16, 'delete_goals'),
(64, 'Can view Цел на обучението', 16, 'view_goals'),
(65, 'Can add Задачa на обучението', 17, 'add_objectives'),
(66, 'Can change Задачa на обучението', 17, 'change_objectives'),
(67, 'Can delete Задачa на обучението', 17, 'delete_objectives'),
(68, 'Can view Задачa на обучението', 17, 'view_objectives'),
(69, 'Can add Тема от раздел на УП', 18, 'add_topic'),
(70, 'Can change Тема от раздел на УП', 18, 'change_topic'),
(71, 'Can delete Тема от раздел на УП', 18, 'delete_topic'),
(72, 'Can view Тема от раздел на УП', 18, 'view_topic'),
(73, 'Can add Цел на обучението', 16, 'add_goal'),
(74, 'Can change Цел на обучението', 16, 'change_goal'),
(75, 'Can delete Цел на обучението', 16, 'delete_goal'),
(76, 'Can view Цел на обучението', 16, 'view_goal'),
(77, 'Can add Задачa на обучението', 17, 'add_objective'),
(78, 'Can change Задачa на обучението', 17, 'change_objective'),
(79, 'Can delete Задачa на обучението', 17, 'delete_objective'),
(80, 'Can view Задачa на обучението', 17, 'view_objective'),
(81, 'Can add Занятие', 19, 'add_session'),
(82, 'Can change Занятие', 19, 'change_session'),
(83, 'Can delete Занятие', 19, 'delete_session'),
(84, 'Can view Занятие', 19, 'view_session'),
(85, 'Can add Занятие (тема)', 20, 'add_sessiontopics'),
(86, 'Can change Занятие (тема)', 20, 'change_sessiontopics'),
(87, 'Can delete Занятие (тема)', 20, 'delete_sessiontopics'),
(88, 'Can view Занятие (тема)', 20, 'view_sessiontopics'),
(89, 'Can add Занятие (тема)', 20, 'add_sessiontopic'),
(90, 'Can change Занятие (тема)', 20, 'change_sessiontopic'),
(91, 'Can delete Занятие (тема)', 20, 'delete_sessiontopic'),
(92, 'Can view Занятие (тема)', 20, 'view_sessiontopic'),
(93, 'Can add Точка от плана', 21, 'add_sessionpoint'),
(94, 'Can change Точка от плана', 21, 'change_sessionpoint'),
(95, 'Can delete Точка от плана', 21, 'delete_sessionpoint'),
(96, 'Can view Точка от плана', 21, 'view_sessionpoint'),
(97, 'Can add Задача към точка от план', 22, 'add_sessiontask'),
(98, 'Can change Задача към точка от план', 22, 'change_sessiontask'),
(99, 'Can delete Задача към точка от план', 22, 'delete_sessiontask'),
(100, 'Can view Задача към точка от план', 22, 'view_sessiontask'),
(101, 'Can add Бележка към точка от план', 23, 'add_sessionnote'),
(102, 'Can change Бележка към точка от план', 23, 'change_sessionnote'),
(103, 'Can delete Бележка към точка от план', 23, 'delete_sessionnote'),
(104, 'Can view Бележка към точка от план', 23, 'view_sessionnote');

-- --------------------------------------------------------

--
-- Структура на таблица `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Схема на данните от таблица `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$600000$3iNEHTkQ6rkF6v46il2Dsp$wzYrjzST0uYMRVFUzIBCXDqFWdbed8vyiQCqZ39eB9o=', '2026-03-17 17:29:12.441157', 1, 'superadmin', 'Георги', 'Бориков', '', 1, 1, '2025-09-04 19:41:42.000000'),
(2, 'pbkdf2_sha256$600000$eF8P44rBpxEGxw8UdOutbg$+qiE1KzVTq+fMN+wsIIQXPmmw20z/zg9pA3u7AzJfOU=', NULL, 0, 'schooladmin1', 'Ущилищен', 'Админ 1', 'cd@abv.bg', 0, 1, '2025-10-03 20:55:16.170750'),
(3, 'pbkdf2_sha256$600000$3GjVTfdEWO8ZNWWxx7iSRZ$hV6MV4l8hoT4/PFuYlWy6GYeaIEQ9Fr+fTyPJAYhj8k=', NULL, 0, 'teacher1', 'Учител', '1', '1@2.34', 0, 1, '2025-10-04 13:13:29.875629'),
(4, 'pbkdf2_sha256$600000$9y7JQPADSwj3C11pTunuUL$deiOhmcaiAkTjdcrLf82sTmomhC4wjBk97Hw6lmRxtU=', NULL, 0, 'schooladmin2', 'Училищен', 'Админ 2', '', 0, 1, '2025-10-04 13:19:19.365209'),
(5, 'pbkdf2_sha256$600000$0w4UTheyLHaVwtR2ifnLg4$y96iMz0SqsKoXQT3bNXkFOT3vL6GZr8AXSdrLefBiw8=', NULL, 0, 'student1', 'Ученик', '1', '', 0, 1, '2025-10-04 13:37:34.091871'),
(6, 'pbkdf2_sha256$600000$kSVpyBeklvYLe5Xp3wxi98$70tm0LllKgCkIKZLI2pdcilanCD6YSeeg3VFKF69lLI=', NULL, 0, 'student2', 'Ученик', '2', '', 0, 1, '2025-10-04 13:39:07.766354'),
(7, 'pbkdf2_sha256$600000$amvEZB7ItS8fLaxH53i1gc$G6jnB8NPLYKWFIeAyt48kzyJk9FziCIxX5k9w5v+fyo=', NULL, 0, 'student3', 'Ученик', '3', '', 0, 1, '2025-10-06 20:49:33.950469');

-- --------------------------------------------------------

--
-- Структура на таблица `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура на таблица `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура на таблица `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Схема на данните от таблица `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2025-09-04 19:50:54.366076', '1', '481030: Приложен програмист', 1, '[{\"added\": {}}]', 11, 1),
(2, '2025-09-04 19:51:04.973531', '1', 'ПГЕЕ гр. Банско', 1, '[{\"added\": {}}]', 10, 1),
(3, '2025-09-04 19:51:18.892227', '1', 'Потребител #1:  ', 2, '[{\"changed\": {\"fields\": [\"\\u0423\\u0447\\u0438\\u043b\\u0438\\u0449\\u0435\"]}}]', 12, 1),
(4, '2025-09-04 19:51:42.581630', '1', 'Потребител #1:  ', 2, '[{\"changed\": {\"fields\": [\"\\u0421\\u043f\\u0435\\u0446\\u0438\\u0430\\u043b\\u043d\\u043e\\u0441\\u0442\"]}}]', 12, 1),
(5, '2025-09-04 19:54:54.293606', '1', '11 а', 1, '[{\"added\": {}}]', 8, 1),
(6, '2025-09-04 19:55:13.055435', '2', '11 в', 1, '[{\"added\": {}}]', 8, 1),
(7, '2025-09-04 19:55:25.332336', '1', 'Потребител #1:  ', 2, '[{\"changed\": {\"fields\": [\"\\u041a\\u043b\\u0430\\u0441\"]}}]', 12, 1),
(8, '2025-09-04 19:57:39.625757', '1', 'superadmin', 2, '[{\"changed\": {\"fields\": [\"First name\", \"Last name\"]}}]', 4, 1),
(9, '2025-09-04 20:01:07.624781', '1', 'Потребител #1: Георги Бориков', 2, '[{\"changed\": {\"fields\": [\"\\u0420\\u043e\\u043b\\u044f\"]}}]', 12, 1),
(10, '2025-09-04 20:28:55.272716', '1', 'ПГЕЕ гр. Банско', 2, '[{\"changed\": {\"fields\": [\"\\u041a\\u043b\\u0430\\u0441\\u043e\\u0432\\u0435\"]}}]', 10, 1),
(11, '2025-09-05 10:31:06.950656', '1', '481030: Приложен програмист', 2, '[{\"changed\": {\"fields\": [\"\\u0423\\u0447\\u0435\\u0431\\u0435\\u043d \\u043f\\u043b\\u0430\\u043d\"]}}]', 11, 1),
(12, '2025-09-18 13:56:28.255103', '1', '1. Първо занятие', 1, '[{\"added\": {}}]', 19, 1),
(13, '2025-09-18 13:57:07.881755', '1', 'Основи на интернет. Мрежови протоколи. HTTP', 1, '[{\"added\": {}}]', 20, 1),
(14, '2025-09-18 13:57:15.712272', '2', 'Видове HTTP заявки', 1, '[{\"added\": {}}]', 20, 1),
(15, '2025-09-18 16:39:10.000811', '2', 'Видове HTTP заявки', 2, '[{\"changed\": {\"fields\": [\"\\u041e\\u043f\\u0438\\u0441\\u0430\\u043d\\u0438\\u0435\"]}}]', 20, 1),
(16, '2025-09-18 16:39:15.741513', '1', 'Основи на интернет. Мрежови протоколи. HTTP', 2, '[]', 20, 1),
(17, '2025-09-19 14:42:34.752268', '2', 'Интернет програмиране', 2, '[]', 13, 1),
(18, '2025-09-19 14:51:13.490492', '1', '1. Първо занятие', 2, '[{\"changed\": {\"fields\": [\"Course\"]}}]', 19, 1),
(19, '2026-03-17 17:31:29.244376', '4', 'Конкурентно програмиране', 1, '[{\"added\": {}}]', 13, 1),
(20, '2026-03-17 17:32:44.825498', '5', 'Конкурентно програмиране', 1, '[{\"added\": {}}]', 13, 1),
(21, '2026-03-17 17:32:59.950671', '4', 'Конкурентно програмиране', 2, '[{\"changed\": {\"fields\": [\"\\u0411\\u0440\\u043e\\u0439 \\u0447\\u0430\\u0441\\u043e\\u0432\\u0435 \\u0441\\u0435\\u0434\\u043c\\u0438\\u0447\\u043d\\u043e (1-\\u0432\\u0438 \\u0441\\u0440\\u043e\\u043a)\"]}}]', 13, 1),
(22, '2026-03-17 17:33:53.217553', '1', '4810301: Приложно програмиране', 2, '[{\"changed\": {\"fields\": [\"\\u041f\\u0440\\u0435\\u0434\\u043c\\u0435\\u0442\\u0438\"]}}]', 11, 1);

-- --------------------------------------------------------

--
-- Структура на таблица `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Схема на данните от таблица `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(7, 'main', 'documents'),
(16, 'main', 'goal'),
(8, 'main', 'klass'),
(9, 'main', 'log'),
(17, 'main', 'objective'),
(10, 'main', 'school'),
(19, 'main', 'session'),
(23, 'main', 'sessionnote'),
(21, 'main', 'sessionpoint'),
(22, 'main', 'sessiontask'),
(20, 'main', 'sessiontopic'),
(11, 'main', 'specialty'),
(13, 'main', 'subject'),
(15, 'main', 'tema'),
(18, 'main', 'topic'),
(14, 'main', 'unit'),
(12, 'main', 'userprofile'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Структура на таблица `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Схема на данните от таблица `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-09-04 19:40:43.020714'),
(2, 'auth', '0001_initial', '2025-09-04 19:40:43.427189'),
(3, 'admin', '0001_initial', '2025-09-04 19:40:43.532309'),
(4, 'admin', '0002_logentry_remove_auto_add', '2025-09-04 19:40:43.539050'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2025-09-04 19:40:43.545211'),
(6, 'contenttypes', '0002_remove_content_type_name', '2025-09-04 19:40:43.589536'),
(7, 'auth', '0002_alter_permission_name_max_length', '2025-09-04 19:40:43.633140'),
(8, 'auth', '0003_alter_user_email_max_length', '2025-09-04 19:40:43.643445'),
(9, 'auth', '0004_alter_user_username_opts', '2025-09-04 19:40:43.649622'),
(10, 'auth', '0005_alter_user_last_login_null', '2025-09-04 19:40:43.684409'),
(11, 'auth', '0006_require_contenttypes_0002', '2025-09-04 19:40:43.686779'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2025-09-04 19:40:43.692865'),
(13, 'auth', '0008_alter_user_username_max_length', '2025-09-04 19:40:43.702746'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2025-09-04 19:40:43.712221'),
(15, 'auth', '0010_alter_group_name_max_length', '2025-09-04 19:40:43.722325'),
(16, 'auth', '0011_update_proxy_permissions', '2025-09-04 19:40:43.728759'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2025-09-04 19:40:43.742170'),
(18, 'main', '0001_initial', '2025-09-04 19:40:44.090131'),
(19, 'sessions', '0001_initial', '2025-09-04 19:40:44.139625'),
(20, 'main', '0002_userprofile_grade_section', '2025-09-04 19:54:24.142242'),
(21, 'main', '0003_school_classes', '2025-09-04 20:27:27.305303'),
(22, 'main', '0004_remove_specialty_plan', '2025-09-05 13:04:30.362475'),
(23, 'main', '0005_subject_specialty_subjects', '2025-09-06 05:32:51.447750'),
(24, 'main', '0006_userprofile_subject', '2025-09-06 06:21:57.373762'),
(25, 'main', '0007_subject_creator_subject_goals_subject_objectives_and_more', '2025-09-07 21:40:34.079087'),
(26, 'main', '0008_unit_hours', '2025-09-08 06:38:15.385646'),
(27, 'main', '0009_goals_objectives_topic_remove_subject_goals_and_more', '2025-09-09 13:29:39.867524'),
(28, 'main', '0010_rename_goals_goal_rename_objectives_objective', '2025-09-09 19:10:11.619726'),
(29, 'main', '0011_delete_objective', '2025-09-10 12:50:06.046698'),
(30, 'main', '0012_session_sessiontopics_and_more', '2025-09-13 11:38:10.647054'),
(31, 'main', '0013_rename_sessiontopics_sessiontopic', '2025-09-13 12:24:50.350357'),
(32, 'main', '0014_alter_session_options_session_unit_and_more', '2025-09-16 14:28:03.290262'),
(33, 'main', '0015_remove_session_unit', '2025-09-17 16:08:48.433012'),
(34, 'main', '0016_session_basic_level_session_session_type', '2025-09-18 13:50:08.751392'),
(35, 'main', '0017_session_collapsed', '2025-09-18 19:10:46.911658'),
(36, 'main', '0018_userprofile_session', '2025-09-21 17:56:44.623974'),
(37, 'main', '0019_sessiontopic_content_sessionpoint', '2025-09-22 07:05:32.947486'),
(38, 'main', '0020_sessionpoint_num', '2025-09-22 16:02:28.888759'),
(39, 'main', '0021_remove_sessiontopic_content_sessionpoint_content', '2025-09-22 16:07:03.457211'),
(40, 'main', '0022_alter_sessionpoint_duration_sessiontask_sessionnote', '2025-09-24 14:29:20.093741'),
(41, 'main', '0023_remove_school_classes_and_more', '2025-10-04 17:56:34.338177'),
(42, 'main', '0024_alter_subject_subject_type', '2025-10-09 18:33:57.407785');

-- --------------------------------------------------------

--
-- Структура на таблица `django_session`
--

DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Схема на данните от таблица `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('0eh0qtiiyzy350v0f98g0jjv9y2t8tur', '.eJxVjEsOwjAMBe-SNYqckDoNS_Y9Q2XHDi2gVOpnhbg7VOoCtm9m3sv0tK1Dvy0696OYi3Hm9Lsx5YfWHcid6m2yearrPLLdFXvQxXaT6PN6uH8HAy3Dt4aEiBoK5aAJYgNAUBiRmaMQu9SAOJdbiS76tlDwuSCKtl5SOJOa9wflkTgu:1vzKyO:F_qTwdZP5C3wxom__anvqrzv6ESGInoUOta_KmA7RH0', '2026-03-22 20:43:36.575031'),
('37c4gvr4ndeaeum9cueof5i54445oy1t', '.eJxVjEsOwjAMBe-SNYqckDoNS_Y9Q2XHDi2gVOpnhbg7VOoCtm9m3sv0tK1Dvy0696OYi3Hm9Lsx5YfWHcid6m2yearrPLLdFXvQxXaT6PN6uH8HAy3Dt4aEiBoK5aAJYgNAUBiRmaMQu9SAOJdbiS76tlDwuSCKtl5SOJOa9wflkTgu:1vLUfW:89HggwK9Sg5ctBRLzwVVJV-TAMrrk6Q9XxVjku4CvxY', '2025-12-02 22:59:26.781728'),
('586n80zjuqhr2hy0wzzpoyhq5x6hwxkb', '.eJxVjEsOwjAMBe-SNYqckDoNS_Y9Q2XHDi2gVOpnhbg7VOoCtm9m3sv0tK1Dvy0696OYi3Hm9Lsx5YfWHcid6m2yearrPLLdFXvQxXaT6PN6uH8HAy3Dt4aEiBoK5aAJYgNAUBiRmaMQu9SAOJdbiS76tlDwuSCKtl5SOJOa9wflkTgu:1v0hil:XIZFAp4KRWEzrXNhKQPIHEN6eVplzGCCzQMdNHGZm7w', '2025-10-06 14:40:51.815905'),
('67ihxd8pp6tetg0w1km7ktafs6v32dnc', '.eJxVjEsOwjAMBe-SNYqckDoNS_Y9Q2XHDi2gVOpnhbg7VOoCtm9m3sv0tK1Dvy0696OYi3Hm9Lsx5YfWHcid6m2yearrPLLdFXvQxXaT6PN6uH8HAy3Dt4aEiBoK5aAJYgNAUBiRmaMQu9SAOJdbiS76tlDwuSCKtl5SOJOa9wflkTgu:1w2YEC:6t9rfN7hOTAqWaKH2mQeE6E4YygYF7hNbeL4xxOlINo', '2026-03-31 17:29:12.445480'),
('gvpat2s67maguve9tusfmdslho9pn5ch', '.eJxVjEsOwjAMBe-SNYqckDoNS_Y9Q2XHDi2gVOpnhbg7VOoCtm9m3sv0tK1Dvy0696OYi3Hm9Lsx5YfWHcid6m2yearrPLLdFXvQxXaT6PN6uH8HAy3Dt4aEiBoK5aAJYgNAUBiRmaMQu9SAOJdbiS76tlDwuSCKtl5SOJOa9wflkTgu:1w2YCm:Ev9QqcwXPi8eCbVb43uoynSm8zE9RTqRLLLnaQu6Jh8', '2026-03-31 17:27:44.295672'),
('h19x1bpibkvt1o5h38fy5bp6x6ceqeqn', '.eJxVjEsOwjAMBe-SNYqckDoNS_Y9Q2XHDi2gVOpnhbg7VOoCtm9m3sv0tK1Dvy0696OYi3Hm9Lsx5YfWHcid6m2yearrPLLdFXvQxXaT6PN6uH8HAy3Dt4aEiBoK5aAJYgNAUBiRmaMQu9SAOJdbiS76tlDwuSCKtl5SOJOa9wflkTgu:1vqUeG:yaRnZM-lJYB3o5gMBeosZKjV1YoSuzzN5_K610V3-k4', '2026-02-26 11:14:16.663797'),
('rnge1fejyurh4l9glmsdtdojclth6i3t', '.eJxVjEsOwjAMBe-SNYqckDoNS_Y9Q2XHDi2gVOpnhbg7VOoCtm9m3sv0tK1Dvy0696OYi3Hm9Lsx5YfWHcid6m2yearrPLLdFXvQxXaT6PN6uH8HAy3Dt4aEiBoK5aAJYgNAUBiRmaMQu9SAOJdbiS76tlDwuSCKtl5SOJOa9wflkTgu:1v5pf2:STUganA261zIN50sQzS1urLL6SULmE3Sq8QVkP4kr6g', '2025-10-20 18:10:12.525119'),
('rrqct5ftw5c96z59i0crqa11y2fywlak', '.eJxVjEsOwjAMBe-SNYqckDoNS_Y9Q2XHDi2gVOpnhbg7VOoCtm9m3sv0tK1Dvy0696OYi3Hm9Lsx5YfWHcid6m2yearrPLLdFXvQxXaT6PN6uH8HAy3Dt4aEiBoK5aAJYgNAUBiRmaMQu9SAOJdbiS76tlDwuSCKtl5SOJOa9wflkTgu:1vzz8I:OuiNx1Nuwwx05DoLrGNh3sls9xLnNGvD34ox3d4JdN4', '2026-03-24 15:36:30.295692'),
('vm5guny96d3yf0m1oz6oeqquaq43p7qz', '.eJxVjEsOwjAMBe-SNYqckDoNS_Y9Q2XHDi2gVOpnhbg7VOoCtm9m3sv0tK1Dvy0696OYi3Hm9Lsx5YfWHcid6m2yearrPLLdFXvQxXaT6PN6uH8HAy3Dt4aEiBoK5aAJYgNAUBiRmaMQu9SAOJdbiS76tlDwuSCKtl5SOJOa9wflkTgu:1uuGHi:bvbp3ZBPAQMSLwqke4Qo-VzOftzearhwTIjV1d9OOxw', '2025-09-18 20:10:18.056843'),
('w7y1n1fr9kw9329izou2ppq5qci1tbiz', '.eJxVjEsOwjAMBe-SNYqckDoNS_Y9Q2XHDi2gVOpnhbg7VOoCtm9m3sv0tK1Dvy0696OYi3Hm9Lsx5YfWHcid6m2yearrPLLdFXvQxXaT6PN6uH8HAy3Dt4aEiBoK5aAJYgNAUBiRmaMQu9SAOJdbiS76tlDwuSCKtl5SOJOa9wflkTgu:1v5peU:TUbT5AWidIOcLdFkkvQFrWpuE1-1VknHjmMQegnowM8', '2025-10-20 18:09:38.217251');

-- --------------------------------------------------------

--
-- Структура на таблица `main_documents`
--

DROP TABLE IF EXISTS `main_documents`;
CREATE TABLE `main_documents` (
  `id` bigint(20) NOT NULL,
  `title` varchar(200) NOT NULL,
  `attachment` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура на таблица `main_goal`
--

DROP TABLE IF EXISTS `main_goal`;
CREATE TABLE `main_goal` (
  `id` bigint(20) NOT NULL,
  `num` smallint(6) NOT NULL,
  `name` varchar(200) NOT NULL,
  `course_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Схема на данните от таблица `main_goal`
--

INSERT INTO `main_goal` (`id`, `num`, `name`, `course_id`) VALUES
(1, 1, 'цел 1', 1),
(2, 2, 'цел 2', 1),
(3, 1, 'Придобиване на знания, свързани с изпълнението на програма', 3),
(4, 2, 'Придобиване на знания и разбирания за същността на термина „процес”', 3),
(5, 3, 'Разбиране на термина „блокираща операция” и влиянието на блокиращите операции върху процеса', 3),
(6, 4, 'Разбиране на термина „нишка”', 3),
(7, 5, 'Познаване на особеностите на многонишковото програмиране и правилното управление на нишките', 3),
(8, 6, 'Разбиране на проблемите и решенията при разработване на сървър за „клиент-сървър” приложения', 3),
(9, 7, 'Разбиране на проблемите и решенията при разработване на приложения с графичен потребителски интерфейс', 3),
(10, 8, 'Разбиране връзката нишка - процес - брой на процесори в системата', 3),
(11, 9, 'Разбиране на проблемите при използване на нишки и техните решения - Race conditions, Deadlocks, Livelocks, Starvation', 3),
(12, 10, 'Познаване на начина за асинхронизиране на блокиращи операции', 3),
(13, 11, 'Познаване и разбиране на концепцията за синхронизация и заключване', 3);

-- --------------------------------------------------------

--
-- Структура на таблица `main_log`
--

DROP TABLE IF EXISTS `main_log`;
CREATE TABLE `main_log` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `user_name` varchar(50) DEFAULT NULL,
  `action` varchar(200) NOT NULL,
  `date` datetime(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура на таблица `main_school`
--

DROP TABLE IF EXISTS `main_school`;
CREATE TABLE `main_school` (
  `id` bigint(20) NOT NULL,
  `short_name` varchar(20) NOT NULL,
  `full_name` longtext NOT NULL,
  `city` varchar(50) NOT NULL,
  `logo` varchar(100) NOT NULL,
  `address` varchar(50) NOT NULL,
  `phone_number` varchar(15) NOT NULL,
  `email` varchar(35) NOT NULL,
  `boss` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Схема на данните от таблица `main_school`
--

INSERT INTO `main_school` (`id`, `short_name`, `full_name`, `city`, `logo`, `address`, `phone_number`, `email`, `boss`) VALUES
(1, 'ПГЕЕ', 'Професионална гимназия по елктроника и енергетика', 'гр. Банско', 'sys_pics/school_logo_None_lZ6TrUT.png', '', '', '', '');

-- --------------------------------------------------------

--
-- Структура на таблица `main_school_specialities`
--

DROP TABLE IF EXISTS `main_school_specialities`;
CREATE TABLE `main_school_specialities` (
  `id` bigint(20) NOT NULL,
  `school_id` bigint(20) NOT NULL,
  `specialty_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Схема на данните от таблица `main_school_specialities`
--

INSERT INTO `main_school_specialities` (`id`, `school_id`, `specialty_id`) VALUES
(1, 1, 1),
(2, 1, 3),
(3, 1, 4),
(4, 1, 5);

-- --------------------------------------------------------

--
-- Структура на таблица `main_session`
--

DROP TABLE IF EXISTS `main_session`;
CREATE TABLE `main_session` (
  `id` bigint(20) NOT NULL,
  `num` smallint(6) NOT NULL,
  `name` varchar(200) NOT NULL,
  `focus` longtext NOT NULL,
  `goals` longtext NOT NULL,
  `duration` smallint(6) NOT NULL,
  `course_id` bigint(20) NOT NULL,
  `basic_level` tinyint(1) NOT NULL,
  `session_type` varchar(3) NOT NULL,
  `collapsed` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Схема на данните от таблица `main_session`
--

INSERT INTO `main_session` (`id`, `num`, `name`, `focus`, `goals`, `duration`, `course_id`, `basic_level`, `session_type`, `collapsed`) VALUES
(1, 1, 'Първо занятие 1', 'някакъв фокус на занятието 2', 'основните цели на занятието 1', 2, 1, 1, 'НЗ', 1),
(3, 2, '2', '4', '3', 2, 1, 1, 'НЗ', 1),
(4, 1, 'ПП УП ИП 1', '', '', 1, 2, 1, 'НЗ', 1),
(5, 1, 'Въведение в конкурентността. Разлика между последователно (серийно), конкурентно и паралелно изпълнение. Аналогии от реалния живот.', '', '', 1, 4, 1, 'НЗ', 1),
(6, 2, 'Процеси. Какво е процес в операционната система. Спецификата на Python: Въведение в концепцията за GIL (Global Interpreter Lock) и защо Python използва multiprocessing за тежки математически задачи.', '', '', 1, 4, 1, 'НЗ', 1),
(7, 3, 'Блокиращи операции. Същност и класификация на задачите: CPU-bound (натоварващи процесора) срещу I/O-bound (чакащи мрежа/диск).', '', '', 1, 4, 1, 'НЗ', 1),
(8, 5, 'Същност на нишките (Threads). Разлика между процес и нишка (памет, ресурси, бързина на създаване).', '', 'В края на часа учениците трябва да знаят:\n\nДа дефинират какво е \"нишка\" (Thread) в контекста на операционната система.\nДа обяснят критичната разлика между процес и нишка, най-вече по отношение на паметта.\nДа могат аргументирано да изберат кога архитектурно е по-подходящо да ползват нишка вместо процес.', 1, 4, 1, 'НЗ', 0),
(9, 4, 'Проблемът със \"замръзващите\" програми. Демонстрация на синхронен код, който блокира (напр. чакане на отговор от уеб сървър). Постановка на проблема, който ще решаваме в следващите раздели.', '', '', 1, 4, 1, 'НЗ', 1),
(10, 6, 'Жизнен цикъл и създаване. Как се ражда и умира една нишка. Синтактичен преглед на модула threading в Python (Main thread срещу Worker threads).', 'жизнен цикъл на нишката;  синтаксис за създаването ѝ в Python', 'В края на часа учениците трябва да могат да:\n\nОписват трите основни състояния в жизнения цикъл на нишката (Нова, Работеща, Мъртва).\nОбясняват предназначението на параметрите target и args при създаване на обект от тип threading.Thread.\nРазпознават често срещани синтактични и логически грешки при стартиране на нишки.', 1, 4, 1, 'НЗ', 0),
(11, 7, 'Управление на изпълнението. Методи за синхронизиране на основната програма с работните нишки (концепцията зад .start() и .join()).', '', '', 1, 4, 1, 'НЗ', 1),
(12, 8, 'Споделена памет. Разбиране на факта, че всички нишки в един процес \"виждат\" едни и същи глобални променливи. Предимства и рискове.', '', '', 1, 4, 1, 'НЗ', 1),
(13, 9, 'Race conditions (Състезателни състояния). Какво се случва, когато две нишки се опитат да променят една променлива едновременно. Анализ на класическия проблем с брояча.', '', '', 1, 4, 1, 'НЗ', 1),
(14, 10, 'Deadlocks (Мъртва схватка). Как решаването на един проблем създава друг. Архитектурен анализ на ситуация, в която две нишки се чакат вечно една друга.', '', '', 1, 4, 1, 'НЗ', 1),
(15, 11, 'Синхронизация и защита. Концепцията за критична секция и заключване на ресурси. Как работи Lock (Mutex) и защо предпазва от Race conditions.', '', '', 1, 4, 1, 'НЗ', 1),
(16, 12, 'Разширени проблеми (Livelocks и Starvation). Информативен преглед на състоянията, при които системата работи, но не върши полезна работа или \"оставя гладна\" конкретна нишка.', '', '', 1, 4, 1, 'НЗ', 1),
(17, 13, 'Въведение в асинхронността. Обещания (Futures) и концепцията за Event Loop (Цикъл на събитията). Как един сервитьор може да обслужва 10 маси едновременно.', '', '', 1, 4, 1, 'НЗ', 1),
(18, 14, 'Обратни извиквания (Callbacks). Историческият подход. Анализ на структурата на кода и проблемът с нечетимостта (\"Callback hell\").', '', '', 1, 4, 1, 'НЗ', 1),
(19, 15, 'Модерният стандарт: Корутини. Синтаксисът async и await в Python. Разлика между обикновена функция и корутина.', '', '', 1, 4, 1, 'НЗ', 1),
(20, 16, 'Архитектура с asyncio. Кога да използваме asyncio и кога threading? Сравнителен анализ на подходите преди учениците да ги приложат в практиката.', '', '', 1, 4, 1, 'НЗ', 1);

-- --------------------------------------------------------

--
-- Структура на таблица `main_sessionnote`
--

DROP TABLE IF EXISTS `main_sessionnote`;
CREATE TABLE `main_sessionnote` (
  `id` bigint(20) NOT NULL,
  `num` smallint(6) NOT NULL,
  `name` varchar(200) NOT NULL,
  `content` longtext NOT NULL,
  `point_id` bigint(20) DEFAULT NULL,
  `session_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Схема на данните от таблица `main_sessionnote`
--

INSERT INTO `main_sessionnote` (`id`, `num`, `name`, `content`, `point_id`, `session_id`) VALUES
(1, 1, 'note1', '<p><span style=\"font-size: 12.0pt; line-height: 115%; font-family: \'Times New Roman\',\'serif\'; mso-fareast-font-family: \'Times New Roman\'; mso-ansi-language: BG; mso-fareast-language: BG; mso-bidi-language: AR-SA;\"><img style=\"float: left;\" src=\"../../media_files/session_pics/Flowers-element-09.png\" alt=\"\" width=\"88\" height=\"108\">Проектиране и изграждане на малка оптична или безжична </span></p>', NULL, 1),
(2, 2, 'просто бележка', '<p style=\"text-align: left;\"><img style=\"float: right;\" src=\"../../media_files/session_pics/Flowers-element-05.png\" alt=\"\" width=\"150\" height=\"154\">тест на картинка с някакъв текст и още и още и още и още и още и още и още и още и още и още и още и още и още и още и още и още и още и още и още и още и още и ощеи още и още и още</p>', 1, 1),
(3, 3, 'дфсдф асдф сдф сдфсадф', '<p>бележка към точка 3</p>', 3, 1),
(5, 1, 'Елементи от бланката за планиране на урок', '<table class=\"single !mb-2 w-fit !max-w-none\">\n<thead>\n<tr>\n<th>Елемент</th>\n<th>Описание</th>\n</tr>\n</thead>\n<tbody>\n<tr>\n<td><strong>Предметно знание</strong>&nbsp;(Какво трябва да знаят/могат в края на часа?)</td>\n<td>Учениците да могат да дефинират понятието \"нишка\", да обясняват критичната разлика между процес и нишка (спрямо паметта) и да аргументират кога се използва нишка.</td>\n</tr>\n<tr>\n<td><strong>Цел по умения за учене</strong>&nbsp;(GROW модел / визия)</td>\n<td><strong>Развитие на критичното и аналитично мислене</strong>&nbsp;чрез пренасяне на концепции от реалния живот (аналогия с ресторант) към абстрактни компютърни архитектури.</td>\n</tr>\n<tr>\n<td><strong>Цел за благополучие</strong></td>\n<td>Създаване на безопасна среда за изразяване на предположения. Учениците да се чувстват комфортно да дават \"грешни\" отговори по време на дискусията за процеси, знаейки, че това е част от процеса на учене.</td>\n</tr>\n<tr>\n<td><strong>Обратна връзка и Рефлексия</strong>&nbsp;(Критерии)</td>\n<td><strong>Критерии:</strong>&nbsp;Ученикът правилно ли идентифицира кога е нужна нишка и кога процес в зададените 3 сценария накрая на часа.<br><strong>Обратна връзка:</strong>&nbsp;Дава се веднага по време на гласуването със сценариите (Post-assessment).</td>\n</tr>\n<tr>\n<td><strong>Необходими ресурси и материали</strong></td>\n<td>Бяла дъска/маркери (за чертане на паметта), цветни картончета за гласуване (зелено/червено) за всеки ученик, презентация (по желание).</td>\n</tr>\n</tbody>\n</table>\n<p>&nbsp;</p>', NULL, 8),
(6, 2, 'Дейности и времево разпределение:', '<p><strong>1. Начало на часа (8 минути)</strong></p>\n<ul>\n<li><strong>Описание на дейността:</strong>&nbsp;<em>Bridge-in &amp; Pre-assessment.</em>&nbsp;Учителят въвлича учениците чрез ролева ситуация (\"Вие сте собственик на ресторант...\"). След като се стигне до извода за \"новия сервитьор\", се прави кратка връзка с предишния материал за изолираната памет на процесите.</li>\n<li><strong>Обобщение:</strong>&nbsp;Съобщават се целите на урока (Objective).</li>\n</ul>\n<p><strong>2. Същинска част (27 минути)</strong></p>\n<ul>\n<li><strong>Описание на дейността:</strong>&nbsp;<em>Participatory Learning.</em>&nbsp;Микро-лекция с визуално чертаене на дъската (Процес = голям квадрат; Нишки = стрелки вътре в него, споделящи едни и същи променливи). Следва съвместно изграждане на сравнителна таблица \"Процес срещу Нишка\". Въвежда се проблемът с GIL в Python като тема за размисъл.</li>\n<li><strong>Инструкция за задача (за дискусията с таблицата):</strong>\n<ul>\n<li><strong>Какво правим?</strong>&nbsp;➔ Съставяме заедно сравнителна таблица между процес и нишка.</li>\n<li><strong>Как работим?</strong>&nbsp;➔ Фронтално. Аз задавам въпрос (напр. \"Кое според вас се създава по-бързо?\"), вие обмисляте 10 секунди и вдигате ръка с предположение.</li>\n<li><strong>Колко време имаме?</strong>&nbsp;➔ 8 минути за попълване на цялата таблица.</li>\n</ul>\n</li>\n</ul>\n<p><strong>3. Край на часа (10 минути)</strong></p>\n<ul>\n<li><strong>Описание на дейността:</strong>&nbsp;<em>Post-assessment.</em>&nbsp;Проверка на наученото чрез конкретни сценарии.</li>\n<li><strong>Инструкция за задача:</strong>\n<ul>\n<li><strong>Какво правим?</strong>&nbsp;➔ Ще прочета 3 кратки софтуерни сценария. Вие трябва да решите дали ще ползвате Процес или Нишка за решаването им.</li>\n<li><strong>Как работим?</strong>&nbsp;➔ Вдигате зелено картонче за \"Нишка\" и червено за \"Процес\" едновременно на бройката \"три\".</li>\n<li><strong>Колко време имаме?</strong>&nbsp;➔ 5 минути за трите сценария.</li>\n</ul>\n</li>\n<li><strong>Обобщение на наученото и рефлексия:</strong>\n<ul>\n<li><em>Обобщение:</em>&nbsp;Нишките са леки и споделят памет, но това крие рискове.</li>\n<li><em>Рефлексия:</em>&nbsp;Учителят пита:&nbsp;<em>\"Кое ви се стори най-объркващо днес в концепцията за споделена памет?\"</em> (Дава се възможност на 1-2 ученици да споделят).</li>\n</ul>\n</li>\n</ul>', NULL, 8),
(7, 1, '', '<p><img src=\"../../media_files/session_pics/%D0%9A%D0%BE%D0%B4_1.png\" alt=\"\" width=\"451\" height=\"235\"></p>', 21, 10),
(8, 2, 'Интегриране в бланката за урок на ПГЕЕ', '<table class=\"single !mb-2 w-fit !max-w-none\">\n<thead>\n<tr>\n<th>Елемент</th>\n<th>Описание</th>\n</tr>\n</thead>\n<tbody>\n<tr>\n<td><strong>Предметно знание</strong></td>\n<td>Учениците да разпознават етапите от жизнения цикъл на нишката и да обясняват синтаксиса за създаването ѝ в Python (параметри&nbsp;<code>target</code>&nbsp;и&nbsp;<code>args</code>).</td>\n</tr>\n<tr>\n<td><strong>Цел по умения за учене</strong>&nbsp;(GROW модел)</td>\n<td><strong>Развитие на умения за четене и анализ на код (Code Reading)</strong>&nbsp;&ndash; способност да откриват логически и синтактични грешки в чужд код, без да го изпълняват на компютър.</td>\n</tr>\n<tr>\n<td><strong>Цел за благополучие</strong></td>\n<td>Насърчаване на&nbsp;<strong>екипната подкрепа</strong>. Задачата \"Открий бъга\" се изпълнява по чинове (по двойки), за да се намали стресът от индивидуалното изпитване при сблъсъка с нов и сложен синтаксис.</td>\n</tr>\n<tr>\n<td><strong>Обратна връзка и Рефлексия</strong>&nbsp;(Критерии)</td>\n<td><strong>Критерии:</strong>&nbsp;Успешно откриване на грешките (липсващ&nbsp;<code>.start()</code>, грешно подаден&nbsp;<code>target</code>) в предоставените фрагменти.<br><strong>Обратна връзка:</strong>&nbsp;Дава се фронтално по време на обсъждането на фрагментите.</td>\n</tr>\n<tr>\n<td><strong>Необходими ресурси и материали</strong></td>\n<td>Бяла дъска (за чертане на жизнения цикъл), мултимедиен проектор/екран за показване на фрагментите код.</td>\n</tr>\n</tbody>\n</table>\n<p>&nbsp;</p>', NULL, 10),
(9, 3, 'Дейности и времево разпределение:', '<p><strong>1. Начало на часа (10 минути)</strong></p>\n<ul>\n<li><strong>Описание на дейността:</strong>&nbsp;Въвеждане в темата чрез аналогията с мениджъра и работника (Bridge). Кратко припомняне на споделената памет от миналия час (Pre-assessment) и обявяване на целите.</li>\n<li><strong>Обобщение:</strong>&nbsp;Ясно се заявява разликата между \"наемане на работник\" (създаване) и \"задаване на старт\" (изпълнение).</li>\n</ul>\n<p><strong>2. Същинска част (20 минути)</strong></p>\n<ul>\n<li><strong>Описание на дейността:</strong>&nbsp;Учителят чертае жизнения цикъл на дъската (New ➔ Running ➔ Dead). Следва анализ на минималния Python код за създаване на нишка. Обръща се специално внимание на предаването на функция като референция (без скоби).</li>\n<li><strong>Инструкция за задача (към анализа на кода):</strong>\n<ul>\n<li><strong>Какво правим?</strong>&nbsp;➔ Разглобяваме анатомията на класа&nbsp;<code>Thread</code>&nbsp;ред по ред.</li>\n<li><strong>Как работим?</strong>&nbsp;➔ Фронтално. Аз обяснявам параметрите, вие си водите записки за разликата между&nbsp;<code>target=my_task</code>&nbsp;и&nbsp;<code>target=my_task()</code>.</li>\n<li><strong>Колко време имаме?</strong>&nbsp;➔ 13 минути за синтаксиса.</li>\n</ul>\n</li>\n</ul>\n<p><strong>3. Край на часа (15 минути)</strong></p>\n<ul>\n<li><strong>Описание на дейността:</strong>&nbsp;Практическа (теоретична) задача \"Открий бъга\" (Post-assessment). Прожектират се 3 сгрешени кода.</li>\n<li><strong>Инструкция за задача:</strong>\n<ul>\n<li><strong>Какво правим?</strong>&nbsp;➔ Ще видите 3 кратки програми, които се опитват да стартират нишка, но се провалят. Трябва да откриете защо.</li>\n<li><strong>Как работим?</strong>&nbsp;➔ Работите по двойки с човека до вас. Имате по 1 минута да обсъдите всеки пример, след което посочвам двойка, която да защити тезата си.</li>\n<li><strong>Колко време имаме?</strong>&nbsp;➔ Общо 10 минути за откриване и обсъждане на грешките.</li>\n</ul>\n</li>\n<li><strong>Обобщение на наученото и рефлексия:</strong>\n<ul>\n<li><em>Обобщение:</em>&nbsp;Нишката има нужда от 3 неща: модул&nbsp;<code>threading</code>, обект с&nbsp;<code>target</code>&nbsp;и извикване на&nbsp;<code>.start()</code>.</li>\n<li><em>Рефлексия:</em>&nbsp;Учителят пита:&nbsp;<em>\"Според вас, по-лесно ли се чете чужд код, когато го обсъждате по двойки, отколкото сами?\"</em> (Кратка дискусия за екипната работа).</li>\n</ul>\n</li>\n</ul>', NULL, 10);

-- --------------------------------------------------------

--
-- Структура на таблица `main_sessionpoint`
--

DROP TABLE IF EXISTS `main_sessionpoint`;
CREATE TABLE `main_sessionpoint` (
  `id` bigint(20) NOT NULL,
  `name` varchar(200) NOT NULL,
  `description` varchar(200) NOT NULL,
  `duration` smallint(6) NOT NULL,
  `session_id` bigint(20) NOT NULL,
  `num` smallint(6) NOT NULL,
  `content` longtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Схема на данните от таблица `main_sessionpoint`
--

INSERT INTO `main_sessionpoint` (`id`, `name`, `description`, `duration`, `session_id`, `num`, `content`) VALUES
(1, 'Въведение и мотивиране', 'Bridging-In', 5, 1, 1, '<ul style=\"list-style-type:disc;\"><li>Мотивационен въпрос („Как бихте описали автомобил като <i>обект</i>?“).</li><li>Кратък разговор/примери за „обекти“, които ученикът среща ежедневно.</li><li>Преговор – обясняване връзката между реалния свят и класове в програмирането.</li></ul>'),
(2, 'Излагане на основните понятия', 'Stated Outcomes', 5, 1, 2, '<ul style=\"list-style-type:disc;\"><li>Ясно заявяване на целите:&nbsp;<ul style=\"list-style-type:circle;\"><li>Да могат да дефинират клас.</li><li>Да създават и използват полета, свойства и методи.</li><li>Да разграничават основните части на класа.</li></ul></li></ul>'),
(3, 'Изложение и примери', 'Обяснение + Демо код', 15, 1, 3, '<ul style=\"list-style-type:disc;\"><li><strong>3.1. Дефиниране на клас</strong><ul style=\"list-style-type:circle;\"><li>Синтаксис, основни правила.</li><li>Пример клас: Car, Student, или друг лесно разбираем пример.</li><li>Практическа демонстрация – показване на кода в реално време.</li></ul></li><li><strong>3.2. Полета и свойства</strong><ul style=\"list-style-type:circle;\"><li>Дефиниция на полета (член-променливи).</li><li>Дефиниция на свойства (getters/setters, ако езикът ги поддържа).</li><li>Разлика между публично и частно поле.</li></ul></li><li><strong>3.3. Методи</strong><ul style=\"list-style-type:circle;\"><li>Какво е метод, как се създава и извиква.</li><li>Примери на прости методи – напр. PrintInfo(), IncreaseSpeed().</li></ul></li></ul>'),
(4, 'Кратка дискусия и рефлексия', '', 7, 1, 4, '<ul style=\"list-style-type: disc;\">\n<li>Въпроси към класа: &bdquo;Може ли да дадете друг пример за обект?&ldquo;</li>\n<li>Критични въпроси: &bdquo;Защо свойствата са по-добри от директен достъп до полетата?&ldquo;</li>\n<li>Обратна връзка дали на всички е ясно.</li>\n</ul>'),
(5, 'Упражнение 1', 'Работа в клас – съвместно', 8, 1, 5, '<ul style=\"list-style-type:disc;\"><li>Заедно с учениците дефинирате клас (например Book) с няколко полета и методи.</li><li>Въвеждане на кода, моментално обяснение на всеки ред.</li></ul>'),
(6, 'Самостоятелна практика', '(Практическа задача', 22, 1, 6, '<p><strong>Задача:</strong></p>\n<p style=\"margin-left: 40px;\">&bdquo;Създайте клас Animal с полета (например name, age), свойства за всяко поле, и поне два метода (напр. CelebrateBirthday, Speak).&ldquo;</p>\n<p>Упътване:&nbsp;</p>\n<p style=\"margin-left: 40px;\">Дава се шаблон/пример, ако някой има нужда. Учителят обикаля и подпомага индивидуално.</p>'),
(7, 'Проверка и споделяне на резултати', '', 10, 1, 7, '<ul style=\"list-style-type:disc;\"><li>Доброволци представят своето решение на дъската/проектора.</li><li>Дискусия: Дали всички са използвали свойства? Кой метод изглежда по-оригинално?</li></ul>'),
(8, 'Кратък тест/мини-викторина', 'Pre/Post Assessment', 7, 1, 8, '<ul style=\"list-style-type:disc;\"><li>3 бързи въпроса (на хартия или дигитално), например:&nbsp;<ul style=\"list-style-type:circle;\"><li>Как се дефинира клас?</li><li>Каква е разликата между поле и свойство?</li><li><span style=\"color:#082A75;\"><strong>Как се извиква метод?</strong></span></li></ul></li></ul>'),
(9, 'Обобщение и Самостоятелнa работа', 'Summary & Homework', 8, 1, 9, '<ul style=\"list-style-type: disc;\">\n<li>Обобщаване на ключовите моменти:&nbsp;\n<ul style=\"list-style-type: circle;\">\n<li>Клас = шаблон, полета = данни, свойства = контрол, методи = действия.</li>\n</ul>\n</li>\n<li>Домашна задача:&nbsp;\n<ul style=\"list-style-type: circle;\">\n<li>Подобно на упражнението в клас &ndash; направи клас Person с уникално име, възраст, и няколко метода по избор.</li>\n</ul>\n</li>\n</ul>'),
(10, 'Bridge-in (Мотивация и въвличане) – 5 мин.', 'Да грабнем вниманието чрез аналогия от реалния живот, преди да въведем абстрактните термини.', 5, 8, 1, '<ul>\n<li><strong>Сценарият \"Ресторантът\":</strong>&nbsp;Представете си, че сте собственик на успешен ресторант. Имате една сграда, една кухня (ресурси) и един сервитьор (основният поток на изпълнение). Клиентите се увеличават и сервитьорът не смогва &ndash; хората чакат (програмата блокира).</li>\n<li><strong>Въпрос към класа:</strong>&nbsp;<em>\"Какво е по-логично и евтино да направите, за да обслужите повече клиенти едновременно: да построите изцяло нова сграда с нова кухня (нов Процес) или просто да наемете втори сервитьор, който да ползва същата кухня (нова Нишка)?\"</em></li>\n<li><strong>Извод:</strong> Създаването на нова сграда е бавно и скъпо. Наемането на нов работник в същата сграда е бързо и ефективно. Точно това е разликата между процесите и нишките в операционната система.</li>\n</ul>'),
(11, 'Objective (Цели на урока) – 2 мин.', 'Ясно заявяваме на учениците какво ще знаят в края на часа:', 10, 8, 2, '<ol>\n<li>Да дефинират какво е \"нишка\" (Thread) в контекста на операционната система.</li>\n<li>Да обяснят критичната разлика между процес и нишка, най-вече по отношение на паметта.</li>\n<li>Да могат аргументирано да изберат кога архитектурно е по-подходящо да ползват нишка вместо процес.</li>\n</ol>'),
(12, 'Pre-assessment (Предварително оценяване)', 'Цел: Активиране на знанията от Урок 2 (Процеси).', 3, 8, 3, '<ul>\n<li><strong>Кратка дискусия:</strong>&nbsp;<em>\"Спомняте ли си какво се случва в RAM паметта, когато стартираме една Python програма?\"</em>&nbsp;(Отговор: ОС заделя изолирано парче памет &ndash; процес).</li>\n<li><em>\"Ако стартираме същата програма втори път паралелно, могат ли двете програми да си говорят директно и да променят едни и същи променливи?\"</em> (Отговор: Не, процесите са напълно изолирани).</li>\n</ul>'),
(13, 'Participatory Learning (Активно учене) - Дефиниция и Анатомия.', 'Това е началото на сърцевината на урока, където преподаваме новия материал чрез интеракция.', 7, 8, 4, '<ul>\n<li>Въвеждаме понятието: Нишката е най-малката единица от инструкции, която може да бъде управлявана от операционната система.</li>\n<li>Всяка програма има поне една нишка (Main Thread).</li>\n<li><strong>Визуализация (на дъската или презентация):</strong> Рисуваме голям квадрат (Процес). Вътре рисуваме обекти (Променливи, Отворени файлове). Рисуваме стрелка (Main Thread). После добавяме втора стрелка (Worker Thread) в същия квадрат.</li>\n</ul>'),
(14, 'Participatory Learning (Активно учене) - Сравнителен анализ: Процес срещу Нишка.', 'Навлизам в сърцевината на урока, където преподавам новия материал.', 8, 8, 5, '<p>Съставяме таблица заедно с учениците:</p>\n<ul>\n<li style=\"list-style-type: none;\">\n<ul>\n<li style=\"list-style-type: none;\">\n<ul>\n<li><em>Памет:</em>&nbsp;Процесите имат собствена изолирана памет. Нишките&nbsp;<strong>споделят</strong>&nbsp;паметта на процеса-родител.</li>\n<li><em>Създаване:</em>&nbsp;Процесите са \"тежки\" (OS отделя време за заделяне на ресурси). Нишките са \"леки\" (създават се почти мигновено).</li>\n<li><em>Срив:</em> Ако един процес крашне, другите продължават. Ако една нишка предизвика фатална грешка (напр. Segmentation fault), целият процес (и всички останали нишки в него) умира.</li>\n</ul>\n</li>\n</ul>\n</li>\n</ul>'),
(15, 'Participatory Learning (Активно учене) – Дискусия: Спецификата на Python (GIL).', 'Финализирам сърцевината на урока, където преподавам новия материал.', 5, 8, 6, '<ul>\n<li>Задаваме въпроса:&nbsp;<em>\"След като нишките са толкова леки и бързи, защо просто не сложим 1000 нишки да смятат сложни математически уравнения в Python?\"</em></li>\n<li>Споменаваме накратко&nbsp;<strong>GIL (Global Interpreter Lock)</strong> като \"правилото на Python\", че само една нишка може да изпълнява Python код в даден момент. (Това подготвя почвата за бъдещите уроци, без да се навлиза в дълбок код).</li>\n</ul>'),
(16, 'Post-assessment (Последващо оценяване)', 'Цел: Проверка на концептуалното разбиране чрез сценарии. Учениците вдигат ръка или ползват цветни картончета (зелено за Нишка, червено за Процес).', 10, 8, 7, '<ul>\n<li><strong>Сценарий 1:</strong>&nbsp;Имаме глобална променлива&nbsp;<code>counter = 0</code>. Искаме две паралелни задачи да я увеличават едновременно. Какво трябва да използваме?&nbsp;<em>(Отговор: Нишки, защото споделят една и съща памет).</em></li>\n<li><strong>Сценарий 2:</strong>&nbsp;Правим браузър като Google Chrome. Искаме, ако един таб забие тотално, останалите табове да продължат да работят.&nbsp;<em>(Отговор: Процеси, заради изолацията при срив).</em></li>\n<li><strong>Сценарий 3:</strong>&nbsp;Имаме малък скрипт, който трябва бързо да провери дали 50 уебсайта са онлайн (I/O операция). Искаме да стартираме 50 задачи максимално \"евтино\" за RAM паметта.&nbsp;<em>(Отговор: Нишки).</em></li>\n</ul>'),
(17, 'Bridge-in (Мотивация и въвличане)', '', 5, 10, 1, '<ul>\n<li><strong>Аналогията \"Мениджър и Работник\":</strong>&nbsp;Представете си, че сте мениджър (Main Thread - основната нишка на програмата). Наемате нов работник (Worker Thread), за да свърши конкретна задача &ndash; например да боядиса стена.</li>\n<li><strong>Въпрос към класа:</strong>&nbsp;<em>\"Ако само подпишете договор с работника (създадете нишката) и му дадете четка, той ще започне ли да боядисва веднага?\"</em>&nbsp;(Отговор: Не, трябва изрично да му кажете \"Започвай!\").</li>\n<li><strong>Извод:</strong> В програмирането създаването на нишка и нейното стартиране са две напълно отделни действия. Днес ще видим как точно става това в Python.</li>\n</ul>'),
(18, 'Objective (Цели на урока)', '', 2, 10, 2, '<p>В края на часа учениците ще могат да:</p>\n<ol>\n<li>Описват трите основни състояния в жизнения цикъл на нишката (Нова, Работеща, Мъртва).</li>\n<li>Обясняват предназначението на параметрите&nbsp;<code>target</code>&nbsp;и&nbsp;<code>args</code>&nbsp;при създаване на обект от тип&nbsp;<code>threading.Thread</code>.</li>\n<li>Разпознават често срещани синтактични и логически грешки при стартиране на нишки.</li>\n</ol>'),
(19, 'Pre-assessment (Предварително оценяване)', '', 3, 10, 3, '<ul>\n<li><strong>Бърз въпрос:</strong>&nbsp;<em>\"От миналия път &ndash; ако имаме една променлива&nbsp;<code>A = 5</code>&nbsp;и стартираме 3 нишки, всяка от тези нишки собствено копие на&nbsp;<code>A</code>&nbsp;ли ще има, или всички ще гледат едно и също&nbsp;<code>A</code>?\"</em> (Отговор: Едно и също, защото нишките споделят паметта на процеса). Това затвърждава защо трябва да внимаваме, когато ги създаваме.</li>\n</ul>'),
(20, 'Participatory Learning (Активно учене) - Жизнен цикъл (Визуализация):', '', 7, 10, 4, '<ul>\n<li>Чертаем три кръга със стрелки между тях:&nbsp;<strong>New</strong>&nbsp;(Създадена, но не работи) ➔&nbsp;<strong>Runnable/Running</strong>&nbsp;(Работи или чака процесора) ➔&nbsp;<strong>Dead</strong> (Приключила задачата си).</li>\n</ul>'),
(21, 'Participatory Learning (Активно учене) – Синтаксисът в Python (Анализ на код на екрана)', 'Показваме минималния нужен код', 13, 10, 5, '<ul>\n<li><strong>Критичен момент за дискусия:</strong>&nbsp;Защо пишем&nbsp;<code>target=my_task</code>, а НЕ пишем&nbsp;<code>target=my_task()</code>&nbsp;(с кръгли скоби)?</li>\n<li><em>Обяснение:</em> Ако сложим скобите, главната нишка ще изпълни функцията веднага и ще блокира, вместо да я предаде на новата нишка като \"инструкция за работа\". Това е най-честата грешка в практиката!</li>\n</ul>'),
(22, 'Post-assessment (Последващо оценяване)', '', 10, 10, 6, '<ul>\n<li><strong>Игра \"Открий бъга\":</strong>&nbsp;На екрана (или на разпечатки) се показват 3 кратки фрагмента код с грешки. Учениците (по двойки) трябва да открият защо кодът няма да създаде правилно паралелна нишка.\n<ul>\n<li><em>Пример 1:</em>&nbsp;Забравено извикване на&nbsp;<code>t.start()</code>. (Нишката остава в състояние New).</li>\n<li><em>Пример 2:</em>&nbsp;Написано&nbsp;<code>target=download_file()</code>. (Функцията се изпълнява синхронно/блокиращо).</li>\n<li><em>Пример 3:</em>&nbsp;Подаване на аргументи без запетая в тупъла:&nbsp;<code>args=(\"Иван\")</code>&nbsp;вместо&nbsp;<code>args=(\"Иван\",)</code>. (Специфика на Python, която предизвиква краш).</li>\n</ul>\n</li>\n</ul>'),
(23, 'Summary (Обобщение)', '', 5, 10, 7, '<ul>\n<li><strong>Синтез:</strong>&nbsp;За да имаме паралелизъм, трябва да импортираме&nbsp;<code>threading</code>, да създадем обект&nbsp;<code>Thread</code>, да му подадем функция (без скоби!) и задължително да извикаме&nbsp;<code>.start()</code>.</li>\n<li><strong>Мост към следващия урок (Урок 7):</strong>&nbsp;<em>\"Днес се научихме как да пускаме работниците да работят. Но какво става, ако главният мениджър (Main Thread) си тръгне от работа, преди те да са приключили? Програмата ще се затвори аварийно. Следващият път ще учим как да ги изчакваме (метода&nbsp;<code>.join()</code>).\"</em></li>\n</ul>');

-- --------------------------------------------------------

--
-- Структура на таблица `main_sessiontask`
--

DROP TABLE IF EXISTS `main_sessiontask`;
CREATE TABLE `main_sessiontask` (
  `id` bigint(20) NOT NULL,
  `num` smallint(6) NOT NULL,
  `name` varchar(200) NOT NULL,
  `condition` longtext NOT NULL,
  `answer` longtext NOT NULL,
  `point_id` bigint(20) DEFAULT NULL,
  `session_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Схема на данните от таблица `main_sessiontask`
--

INSERT INTO `main_sessiontask` (`id`, `num`, `name`, `condition`, `answer`, `point_id`, `session_id`) VALUES
(1, 1, 'Задача 1', '<p><span><span style=\"font-size: 14.0pt; mso-bidi-font-size: 11.0pt; line-height: 115%; font-family: \'Calibri\',\'sans-serif\'; mso-ascii-theme-font: minor-latin; mso-fareast-font-family: \'MS Mincho\'; mso-fareast-theme-font: minor-fareast; mso-hansi-theme-font: minor-latin; mso-bidi-font-family: \'Times New Roman\'; mso-bidi-theme-font: minor-bidi; color: #082a75; mso-themecolor: text2; mso-ansi-language: BG; mso-fareast-language: EN-US; mso-bidi-language: AR-SA;\">Създайте клас Animal с полета (например name, age), свойства за всяко поле, и поне два метода (напр. CelebrateBirthday, Speak).</span></span></p>', '<p style=\"mso-margin-top-alt: auto; mso-margin-bottom-alt: auto; line-height: normal; mso-list: l0 level1 lfo1; tab-stops: list 36.0pt;\">Упътване: Дава се шаблон/пример, ако някой има нужда.</p>\n<p style=\"mso-margin-top-alt: auto; mso-margin-bottom-alt: auto; line-height: normal; mso-list: l0 level1 lfo1; tab-stops: list 36.0pt;\">Учителят обикаля и подпомага индивидуално.</p>', 6, 1);

-- --------------------------------------------------------

--
-- Структура на таблица `main_sessiontopic`
--

DROP TABLE IF EXISTS `main_sessiontopic`;
CREATE TABLE `main_sessiontopic` (
  `id` bigint(20) NOT NULL,
  `description` varchar(200) NOT NULL,
  `session_id` bigint(20) NOT NULL,
  `topic_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Схема на данните от таблица `main_sessiontopic`
--

INSERT INTO `main_sessiontopic` (`id`, `description`, `session_id`, `topic_id`) VALUES
(1, 'описание, касаещо точка **', 1, 1),
(2, 'описание, касаещо точка ***', 1, 2),
(3, 'sdas asdasd asda', 1, 4),
(4, 'tertertert', 1, 8),
(5, '', 5, 16),
(6, '', 6, 16),
(7, '', 7, 17),
(8, '', 8, 18),
(9, '', 9, 17),
(10, '', 10, 19),
(11, '', 11, 19),
(12, '', 12, 20),
(13, '', 13, 21),
(14, '', 14, 21),
(15, '', 15, 21),
(16, '', 16, 24),
(17, '', 17, 22),
(18, '', 18, 25),
(19, '', 19, 23),
(20, '', 20, 23);

-- --------------------------------------------------------

--
-- Структура на таблица `main_specialty`
--

DROP TABLE IF EXISTS `main_specialty`;
CREATE TABLE `main_specialty` (
  `id` bigint(20) NOT NULL,
  `specialty_num` varchar(8) NOT NULL,
  `specialty_name` varchar(100) NOT NULL,
  `level` smallint(5) UNSIGNED NOT NULL CHECK (`level` >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Схема на данните от таблица `main_specialty`
--

INSERT INTO `main_specialty` (`id`, `specialty_num`, `specialty_name`, `level`) VALUES
(1, '4810301', 'Приложно програмиране', 3),
(2, '1', '2', 3),
(3, '4810201', 'Системно програмиране', 3),
(4, '6666', '77777', 3),
(5, '4444', '555555', 3);

-- --------------------------------------------------------

--
-- Структура на таблица `main_specialty_subjects`
--

DROP TABLE IF EXISTS `main_specialty_subjects`;
CREATE TABLE `main_specialty_subjects` (
  `id` bigint(20) NOT NULL,
  `specialty_id` bigint(20) NOT NULL,
  `subject_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Схема на данните от таблица `main_specialty_subjects`
--

INSERT INTO `main_specialty_subjects` (`id`, `specialty_id`, `subject_id`) VALUES
(1, 1, 1),
(2, 1, 2),
(3, 1, 3),
(20, 1, 4),
(21, 1, 5);

-- --------------------------------------------------------

--
-- Структура на таблица `main_subject`
--

DROP TABLE IF EXISTS `main_subject`;
CREATE TABLE `main_subject` (
  `id` bigint(20) NOT NULL,
  `name` varchar(200) NOT NULL,
  `grade` smallint(6) NOT NULL,
  `subject_type` varchar(10) NOT NULL,
  `hpy` int(10) UNSIGNED NOT NULL CHECK (`hpy` >= 0),
  `wpy` smallint(6) NOT NULL,
  `hpw1` smallint(6) NOT NULL,
  `hpw2` smallint(6) NOT NULL,
  `creator_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Схема на данните от таблица `main_subject`
--

INSERT INTO `main_subject` (`id`, `name`, `grade`, `subject_type`, `hpy`, `wpy`, `hpw1`, `hpw2`, `creator_id`) VALUES
(1, 'Интернет програмиране', 12, 'теория', 58, 29, 2, 2, NULL),
(2, 'Интернет програмиране', 12, 'практика', 116, 29, 4, 4, NULL),
(3, 'Функционално програмиране', 12, 'теория', 29, 29, 1, 1, NULL),
(4, 'Конкурентно програмиране', 11, 'теория', 18, 18, 0, 1, 1),
(5, 'Конкурентно програмиране', 11, 'практика', 36, 18, 0, 2, 1);

-- --------------------------------------------------------

--
-- Структура на таблица `main_topic`
--

DROP TABLE IF EXISTS `main_topic`;
CREATE TABLE `main_topic` (
  `id` bigint(20) NOT NULL,
  `num` smallint(6) NOT NULL,
  `name` varchar(200) NOT NULL,
  `MoSCoW_cat` varchar(1) NOT NULL,
  `MoSCoW_rem` varchar(200) NOT NULL,
  `unit_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Схема на данните от таблица `main_topic`
--

INSERT INTO `main_topic` (`id`, `num`, `name`, `MoSCoW_cat`, `MoSCoW_rem`, `unit_id`) VALUES
(1, 1, 'Основи на интернет. Мрежови протоколи. HTTP', 'M', 'Основополагащи понятия', 1),
(2, 2, 'Видове HTTP заявки', 'S', '', 1),
(3, 3, 'Клиент - сървър комуникация', 'C', '', 1),
(4, 4, 'Практически проект: Реализиране на чат приложение в модел „Клиент-сървър”', 'C', '', 1),
(5, 1, 'Работа с HTML. Основни тагове', 'M', '', 2),
(6, 2, 'Работа със CSS. Селектори и основни правила', 'M', '', 2),
(7, 1, 'Работа с MVC концепцията - модел, изглед, контролер', 'M', '', 3),
(8, 3, 'Работа с инструментите за разработчици на съвременните уеб браузъри', 'M', '', 2),
(9, 4, 'Създаване на формуляри', 'M', '', 2),
(10, 5, 'Създаване на семантични страници', 'M', '', 2),
(11, 6, 'Увод в JavaScript. Работа с обекти и събития', 'M', '', 2),
(12, 7, 'Принципи на DOM. Манипулиране на DOM', 'M', '', 2),
(13, 8, 'Практически проект: Реализиране на адаптивен фронт-енд за уеб сайт', 'M', '', 2),
(14, 2, 'Комуникация на БД в уеб приложение', 'M', '', 3),
(15, 3, 'Работа с ORM (обектно-релационно съпоставящи) системи', 'M', '', 3),
(16, 1, 'Конкурентност. Изпълнение на програма. Процес.', 'M', 'Фундаментални понятия. Без разбиране какво е процес и как се изпълнява програмата, не може да се премине към паралелизъм.', 4),
(17, 2, 'Видове блокиращи операции.', 'S', 'Важно е да разберат защо програмата \"забива\" (напр. при изчакване на база данни или мрежа), но не е нужно задълбочаване във всички хардуерни/софтуерни I/O детайли.', 4),
(18, 1, 'Нишка. Връзка между процес и нишка.', 'M', 'Критична разлика за разбирането на споделената памет и ресурсите на операционната система.', 5),
(19, 2, 'Създаване на нишки.', 'M', 'Абсолютно задължително за практическите задачи и прехода към реално кодене.', 5),
(20, 3, 'Управление на нишки. Споделена памет между нишки.', 'M', 'Ядрото на конкурентното програмиране. Без това учениците не могат да създадат работещо многонишково приложение.', 5),
(21, 4, 'Проблеми при работа с нишки - Race conditions, Deadlocks', 'M', 'Най-честите и фатални грешки при споделена памет. Задължително е да знаят как да ги избягват (синхронизация/заключване).', 5),
(22, 1, 'Работа с асинхронни операции. Обещания (Promise/Task)', 'M', 'Гръбнакът на модерното програмиране (особено в C#, Java и JS, които се препоръчват в програмата).', 6),
(23, 3, 'Работа с асинхронни операции чрез async/await и др. механизми за реализиране на асинхронни операции', 'M', 'Де факто индустриалният стандарт за писане на чист и четим асинхронен код днес. Задължително практическо умение.', 6),
(24, 5, 'Проблеми при работа с нишки - Livelocks, Starvation', 'S', 'Сравнително сложни концепции за 11. клас. Добре е да се споменат информативно, ако остане време, но не са фатални за базовото ниво.', 5),
(25, 2, 'Обратни извиквания (Callback)', 'C', 'Исторически важно и се среща в по-стар код, но често води до \"callback hell\". Може да се прегледа по-бързо в полза на съвременните методи.', 6);

-- --------------------------------------------------------

--
-- Структура на таблица `main_unit`
--

DROP TABLE IF EXISTS `main_unit`;
CREATE TABLE `main_unit` (
  `id` bigint(20) NOT NULL,
  `num` smallint(6) NOT NULL,
  `name` varchar(200) NOT NULL,
  `subject_id` bigint(20) NOT NULL,
  `hours` smallint(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Схема на данните от таблица `main_unit`
--

INSERT INTO `main_unit` (`id`, `num`, `name`, `subject_id`, `hours`) VALUES
(1, 1, 'Въведение в Интернет, мрежови протоколи и модел „Клиент - Сървър”', 1, 6),
(2, 2, 'Разработка на външен интерфейс (front-end) на уеб приложения', 1, 20),
(3, 3, 'Разработка на сървърна часст (back-end) на уеб приложения', 1, 33),
(4, 1, 'Конкурентност и блокиращи операции', 4, 4),
(5, 2, 'Нишки', 4, 8),
(6, 3, 'Асинхронни операции', 4, 4);

-- --------------------------------------------------------

--
-- Структура на таблица `main_userprofile`
--

DROP TABLE IF EXISTS `main_userprofile`;
CREATE TABLE `main_userprofile` (
  `id` bigint(20) NOT NULL,
  `gender` tinyint(1) NOT NULL,
  `access_level` smallint(5) UNSIGNED NOT NULL CHECK (`access_level` >= 0),
  `session_screen` smallint(5) UNSIGNED NOT NULL CHECK (`session_screen` >= 0),
  `school_id` bigint(20) DEFAULT NULL,
  `speciality_id` bigint(20) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `subject_id` bigint(20) DEFAULT NULL,
  `session_id` bigint(20) DEFAULT NULL,
  `grade` smallint(5) UNSIGNED NOT NULL CHECK (`grade` >= 0),
  `section` varchar(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Схема на данните от таблица `main_userprofile`
--

INSERT INTO `main_userprofile` (`id`, `gender`, `access_level`, `session_screen`, `school_id`, `speciality_id`, `user_id`, `subject_id`, `session_id`, `grade`, `section`) VALUES
(1, 1, 1, 1, 1, 1, 1, 4, 10, 11, 'а'),
(2, 1, 3, 1, 1, NULL, 2, NULL, NULL, 11, 'а'),
(3, 1, 4, 1, 1, NULL, 3, NULL, NULL, 11, 'а'),
(4, 1, 3, 1, 1, NULL, 4, NULL, NULL, 11, 'а'),
(5, 1, 5, 1, 1, 1, 5, NULL, NULL, 10, 'б'),
(6, 1, 5, 1, 1, 1, 6, NULL, NULL, 10, 'б'),
(7, 1, 5, 1, 1, 3, 7, NULL, NULL, 10, 'б');

--
-- Indexes for dumped tables
--

--
-- Индекси за таблица `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Индекси за таблица `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Индекси за таблица `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Индекси за таблица `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Индекси за таблица `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Индекси за таблица `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Индекси за таблица `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Индекси за таблица `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Индекси за таблица `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Индекси за таблица `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Индекси за таблица `main_documents`
--
ALTER TABLE `main_documents`
  ADD PRIMARY KEY (`id`);

--
-- Индекси за таблица `main_goal`
--
ALTER TABLE `main_goal`
  ADD PRIMARY KEY (`id`),
  ADD KEY `main_goals_course_id_8bd6ab9d_fk_main_subject_id` (`course_id`);

--
-- Индекси за таблица `main_log`
--
ALTER TABLE `main_log`
  ADD PRIMARY KEY (`id`);

--
-- Индекси за таблица `main_school`
--
ALTER TABLE `main_school`
  ADD PRIMARY KEY (`id`);

--
-- Индекси за таблица `main_school_specialities`
--
ALTER TABLE `main_school_specialities`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `main_school_specialities_school_id_specialty_id_c782cac5_uniq` (`school_id`,`specialty_id`),
  ADD KEY `main_school_speciali_specialty_id_78354343_fk_main_spec` (`specialty_id`);

--
-- Индекси за таблица `main_session`
--
ALTER TABLE `main_session`
  ADD PRIMARY KEY (`id`),
  ADD KEY `main_session_course_id_ac5cca43_fk_main_subject_id` (`course_id`);

--
-- Индекси за таблица `main_sessionnote`
--
ALTER TABLE `main_sessionnote`
  ADD PRIMARY KEY (`id`),
  ADD KEY `main_sessionnote_point_id_401f254e_fk_main_sessionpoint_id` (`point_id`),
  ADD KEY `main_sessionnote_session_id_2855ecf5_fk_main_session_id` (`session_id`);

--
-- Индекси за таблица `main_sessionpoint`
--
ALTER TABLE `main_sessionpoint`
  ADD PRIMARY KEY (`id`),
  ADD KEY `main_sessionpoint_session_id_27aa5fef_fk_main_session_id` (`session_id`);

--
-- Индекси за таблица `main_sessiontask`
--
ALTER TABLE `main_sessiontask`
  ADD PRIMARY KEY (`id`),
  ADD KEY `main_sessiontask_point_id_e4306d96_fk_main_sessionpoint_id` (`point_id`),
  ADD KEY `main_sessiontask_session_id_a55642f3_fk_main_session_id` (`session_id`);

--
-- Индекси за таблица `main_sessiontopic`
--
ALTER TABLE `main_sessiontopic`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_session_topic` (`session_id`,`topic_id`),
  ADD KEY `main_sessiontopics_topic_id_63ff71a8_fk_main_topic_id` (`topic_id`);

--
-- Индекси за таблица `main_specialty`
--
ALTER TABLE `main_specialty`
  ADD PRIMARY KEY (`id`);

--
-- Индекси за таблица `main_specialty_subjects`
--
ALTER TABLE `main_specialty_subjects`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `main_specialty_subjects_specialty_id_subject_id_1c305dfb_uniq` (`specialty_id`,`subject_id`),
  ADD KEY `main_specialty_subjects_subject_id_3ef6ae1a_fk_main_subject_id` (`subject_id`);

--
-- Индекси за таблица `main_subject`
--
ALTER TABLE `main_subject`
  ADD PRIMARY KEY (`id`),
  ADD KEY `main_subject_creator_id_9de985e5_fk_auth_user_id` (`creator_id`);

--
-- Индекси за таблица `main_topic`
--
ALTER TABLE `main_topic`
  ADD PRIMARY KEY (`id`),
  ADD KEY `main_topic_unit_id_f68f2c9e_fk_main_unit_id` (`unit_id`);

--
-- Индекси за таблица `main_unit`
--
ALTER TABLE `main_unit`
  ADD PRIMARY KEY (`id`),
  ADD KEY `main_unit_subject_id_d1dc5482_fk_main_subject_id` (`subject_id`);

--
-- Индекси за таблица `main_userprofile`
--
ALTER TABLE `main_userprofile`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`),
  ADD KEY `main_userprofile_school_id_74f42cf3_fk_main_school_id` (`school_id`),
  ADD KEY `main_userprofile_speciality_id_475d0b2d_fk_main_specialty_id` (`speciality_id`),
  ADD KEY `main_userprofile_subject_id_5a0cbf6b_fk_main_subject_id` (`subject_id`),
  ADD KEY `main_userprofile_session_id_c9e7aff8_fk_main_session_id` (`session_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=105;

--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=43;

--
-- AUTO_INCREMENT for table `main_documents`
--
ALTER TABLE `main_documents`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `main_goal`
--
ALTER TABLE `main_goal`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `main_log`
--
ALTER TABLE `main_log`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `main_school`
--
ALTER TABLE `main_school`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `main_school_specialities`
--
ALTER TABLE `main_school_specialities`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `main_session`
--
ALTER TABLE `main_session`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `main_sessionnote`
--
ALTER TABLE `main_sessionnote`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `main_sessionpoint`
--
ALTER TABLE `main_sessionpoint`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT for table `main_sessiontask`
--
ALTER TABLE `main_sessiontask`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `main_sessiontopic`
--
ALTER TABLE `main_sessiontopic`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `main_specialty`
--
ALTER TABLE `main_specialty`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `main_specialty_subjects`
--
ALTER TABLE `main_specialty_subjects`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `main_subject`
--
ALTER TABLE `main_subject`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `main_topic`
--
ALTER TABLE `main_topic`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT for table `main_unit`
--
ALTER TABLE `main_unit`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `main_userprofile`
--
ALTER TABLE `main_userprofile`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Ограничения за дъмпнати таблици
--

--
-- Ограничения за таблица `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Ограничения за таблица `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Ограничения за таблица `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Ограничения за таблица `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Ограничения за таблица `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Ограничения за таблица `main_goal`
--
ALTER TABLE `main_goal`
  ADD CONSTRAINT `main_goals_course_id_8bd6ab9d_fk_main_subject_id` FOREIGN KEY (`course_id`) REFERENCES `main_subject` (`id`);

--
-- Ограничения за таблица `main_school_specialities`
--
ALTER TABLE `main_school_specialities`
  ADD CONSTRAINT `main_school_speciali_specialty_id_78354343_fk_main_spec` FOREIGN KEY (`specialty_id`) REFERENCES `main_specialty` (`id`),
  ADD CONSTRAINT `main_school_specialities_school_id_9588fab6_fk_main_school_id` FOREIGN KEY (`school_id`) REFERENCES `main_school` (`id`);

--
-- Ограничения за таблица `main_session`
--
ALTER TABLE `main_session`
  ADD CONSTRAINT `main_session_course_id_ac5cca43_fk_main_subject_id` FOREIGN KEY (`course_id`) REFERENCES `main_subject` (`id`);

--
-- Ограничения за таблица `main_sessionnote`
--
ALTER TABLE `main_sessionnote`
  ADD CONSTRAINT `main_sessionnote_point_id_401f254e_fk_main_sessionpoint_id` FOREIGN KEY (`point_id`) REFERENCES `main_sessionpoint` (`id`),
  ADD CONSTRAINT `main_sessionnote_session_id_2855ecf5_fk_main_session_id` FOREIGN KEY (`session_id`) REFERENCES `main_session` (`id`);

--
-- Ограничения за таблица `main_sessionpoint`
--
ALTER TABLE `main_sessionpoint`
  ADD CONSTRAINT `main_sessionpoint_session_id_27aa5fef_fk_main_session_id` FOREIGN KEY (`session_id`) REFERENCES `main_session` (`id`);

--
-- Ограничения за таблица `main_sessiontask`
--
ALTER TABLE `main_sessiontask`
  ADD CONSTRAINT `main_sessiontask_point_id_e4306d96_fk_main_sessionpoint_id` FOREIGN KEY (`point_id`) REFERENCES `main_sessionpoint` (`id`),
  ADD CONSTRAINT `main_sessiontask_session_id_a55642f3_fk_main_session_id` FOREIGN KEY (`session_id`) REFERENCES `main_session` (`id`);

--
-- Ограничения за таблица `main_sessiontopic`
--
ALTER TABLE `main_sessiontopic`
  ADD CONSTRAINT `main_sessiontopics_session_id_c9a604e5_fk_main_session_id` FOREIGN KEY (`session_id`) REFERENCES `main_session` (`id`),
  ADD CONSTRAINT `main_sessiontopics_topic_id_63ff71a8_fk_main_topic_id` FOREIGN KEY (`topic_id`) REFERENCES `main_topic` (`id`);

--
-- Ограничения за таблица `main_specialty_subjects`
--
ALTER TABLE `main_specialty_subjects`
  ADD CONSTRAINT `main_specialty_subje_specialty_id_e3d0262f_fk_main_spec` FOREIGN KEY (`specialty_id`) REFERENCES `main_specialty` (`id`),
  ADD CONSTRAINT `main_specialty_subjects_subject_id_3ef6ae1a_fk_main_subject_id` FOREIGN KEY (`subject_id`) REFERENCES `main_subject` (`id`);

--
-- Ограничения за таблица `main_subject`
--
ALTER TABLE `main_subject`
  ADD CONSTRAINT `main_subject_creator_id_9de985e5_fk_auth_user_id` FOREIGN KEY (`creator_id`) REFERENCES `auth_user` (`id`);

--
-- Ограничения за таблица `main_topic`
--
ALTER TABLE `main_topic`
  ADD CONSTRAINT `main_topic_unit_id_f68f2c9e_fk_main_unit_id` FOREIGN KEY (`unit_id`) REFERENCES `main_unit` (`id`);

--
-- Ограничения за таблица `main_unit`
--
ALTER TABLE `main_unit`
  ADD CONSTRAINT `main_unit_subject_id_d1dc5482_fk_main_subject_id` FOREIGN KEY (`subject_id`) REFERENCES `main_subject` (`id`);

--
-- Ограничения за таблица `main_userprofile`
--
ALTER TABLE `main_userprofile`
  ADD CONSTRAINT `main_userprofile_school_id_74f42cf3_fk_main_school_id` FOREIGN KEY (`school_id`) REFERENCES `main_school` (`id`),
  ADD CONSTRAINT `main_userprofile_session_id_c9e7aff8_fk_main_session_id` FOREIGN KEY (`session_id`) REFERENCES `main_session` (`id`),
  ADD CONSTRAINT `main_userprofile_speciality_id_475d0b2d_fk_main_specialty_id` FOREIGN KEY (`speciality_id`) REFERENCES `main_specialty` (`id`),
  ADD CONSTRAINT `main_userprofile_subject_id_5a0cbf6b_fk_main_subject_id` FOREIGN KEY (`subject_id`) REFERENCES `main_subject` (`id`),
  ADD CONSTRAINT `main_userprofile_user_id_15c416f4_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

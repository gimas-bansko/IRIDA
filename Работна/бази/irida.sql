-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1
-- Време на генериране:  9 септ 2025 в 20:41
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

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура на таблица `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура на таблица `auth_permission`
--

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
(72, 'Can view Тема от раздел на УП', 18, 'view_topic');

-- --------------------------------------------------------

--
-- Структура на таблица `auth_user`
--

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
(1, 'pbkdf2_sha256$600000$3iNEHTkQ6rkF6v46il2Dsp$wzYrjzST0uYMRVFUzIBCXDqFWdbed8vyiQCqZ39eB9o=', '2025-09-06 11:29:58.683807', 1, 'superadmin', 'Георги', 'Бориков', '', 1, 1, '2025-09-04 19:41:42.000000');

-- --------------------------------------------------------

--
-- Структура на таблица `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура на таблица `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура на таблица `django_admin_log`
--

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
(11, '2025-09-05 10:31:06.950656', '1', '481030: Приложен програмист', 2, '[{\"changed\": {\"fields\": [\"\\u0423\\u0447\\u0435\\u0431\\u0435\\u043d \\u043f\\u043b\\u0430\\u043d\"]}}]', 11, 1);

-- --------------------------------------------------------

--
-- Структура на таблица `django_content_type`
--

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
(16, 'main', 'goals'),
(8, 'main', 'klass'),
(9, 'main', 'log'),
(17, 'main', 'objectives'),
(10, 'main', 'school'),
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
(27, 'main', '0009_goals_objectives_topic_remove_subject_goals_and_more', '2025-09-09 13:29:39.867524');

-- --------------------------------------------------------

--
-- Структура на таблица `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Схема на данните от таблица `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('sugbi9tyy6lihsnijhrdhf3vax8f2h7t', '.eJxVjEsOwjAMBe-SNYqckDoNS_Y9Q2XHDi2gVOpnhbg7VOoCtm9m3sv0tK1Dvy0696OYi3Hm9Lsx5YfWHcid6m2yearrPLLdFXvQxXaT6PN6uH8HAy3Dt4aEiBoK5aAJYgNAUBiRmaMQu9SAOJdbiS76tlDwuSCKtl5SOJOa9wflkTgu:1uur7G:OWgXVODCfoWhfwmFrrlTpl219oaq7k-cfSvuMFl6S-c', '2025-09-20 11:29:58.689543'),
('vm5guny96d3yf0m1oz6oeqquaq43p7qz', '.eJxVjEsOwjAMBe-SNYqckDoNS_Y9Q2XHDi2gVOpnhbg7VOoCtm9m3sv0tK1Dvy0696OYi3Hm9Lsx5YfWHcid6m2yearrPLLdFXvQxXaT6PN6uH8HAy3Dt4aEiBoK5aAJYgNAUBiRmaMQu9SAOJdbiS76tlDwuSCKtl5SOJOa9wflkTgu:1uuGHi:bvbp3ZBPAQMSLwqke4Qo-VzOftzearhwTIjV1d9OOxw', '2025-09-18 20:10:18.056843');

-- --------------------------------------------------------

--
-- Структура на таблица `main_documents`
--

CREATE TABLE `main_documents` (
  `id` bigint(20) NOT NULL,
  `title` varchar(200) NOT NULL,
  `attachment` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура на таблица `main_goals`
--

CREATE TABLE `main_goals` (
  `id` bigint(20) NOT NULL,
  `num` smallint(6) NOT NULL,
  `name` varchar(200) NOT NULL,
  `course_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура на таблица `main_klass`
--

CREATE TABLE `main_klass` (
  `id` bigint(20) NOT NULL,
  `grade` smallint(5) UNSIGNED DEFAULT NULL CHECK (`grade` >= 0),
  `section` varchar(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Схема на данните от таблица `main_klass`
--

INSERT INTO `main_klass` (`id`, `grade`, `section`) VALUES
(1, 11, 'а'),
(2, 11, 'в');

-- --------------------------------------------------------

--
-- Структура на таблица `main_log`
--

CREATE TABLE `main_log` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `user_name` varchar(50) DEFAULT NULL,
  `action` varchar(200) NOT NULL,
  `date` datetime(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура на таблица `main_objectives`
--

CREATE TABLE `main_objectives` (
  `id` bigint(20) NOT NULL,
  `num` smallint(6) NOT NULL,
  `name` varchar(200) NOT NULL,
  `course_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура на таблица `main_school`
--

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
-- Структура на таблица `main_school_classes`
--

CREATE TABLE `main_school_classes` (
  `id` bigint(20) NOT NULL,
  `school_id` bigint(20) NOT NULL,
  `klass_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Схема на данните от таблица `main_school_classes`
--

INSERT INTO `main_school_classes` (`id`, `school_id`, `klass_id`) VALUES
(1, 1, 1),
(2, 1, 2);

-- --------------------------------------------------------

--
-- Структура на таблица `main_school_specialities`
--

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
-- Структура на таблица `main_specialty`
--

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
(3, 1, 3);

-- --------------------------------------------------------

--
-- Структура на таблица `main_subject`
--

CREATE TABLE `main_subject` (
  `id` bigint(20) NOT NULL,
  `name` varchar(200) NOT NULL,
  `grade` smallint(6) NOT NULL,
  `subject_type` tinyint(1) NOT NULL,
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
(1, 'Интернет програмиране', 12, 1, 58, 29, 2, 2, NULL),
(2, 'Интернет програмиране', 12, 0, 116, 29, 4, 4, NULL),
(3, 'Функционално програмиране', 12, 1, 29, 29, 1, 1, NULL);

-- --------------------------------------------------------

--
-- Структура на таблица `main_topic`
--

CREATE TABLE `main_topic` (
  `id` bigint(20) NOT NULL,
  `num` smallint(6) NOT NULL,
  `name` varchar(200) NOT NULL,
  `MoSCoW_cat` varchar(1) NOT NULL,
  `MoSCoW_rem` varchar(200) NOT NULL,
  `unit_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура на таблица `main_unit`
--

CREATE TABLE `main_unit` (
  `id` bigint(20) NOT NULL,
  `num` smallint(6) NOT NULL,
  `name` varchar(200) NOT NULL,
  `subject_id` bigint(20) NOT NULL,
  `hours` smallint(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура на таблица `main_userprofile`
--

CREATE TABLE `main_userprofile` (
  `id` bigint(20) NOT NULL,
  `gender` tinyint(1) NOT NULL,
  `access_level` smallint(5) UNSIGNED NOT NULL CHECK (`access_level` >= 0),
  `session_screen` smallint(5) UNSIGNED NOT NULL CHECK (`session_screen` >= 0),
  `school_id` bigint(20) DEFAULT NULL,
  `speciality_id` bigint(20) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `grade_section_id` bigint(20) DEFAULT NULL,
  `subject_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Схема на данните от таблица `main_userprofile`
--

INSERT INTO `main_userprofile` (`id`, `gender`, `access_level`, `session_screen`, `school_id`, `speciality_id`, `user_id`, `grade_section_id`, `subject_id`) VALUES
(1, 1, 1, 1, 1, 1, 1, 1, NULL);

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
-- Индекси за таблица `main_goals`
--
ALTER TABLE `main_goals`
  ADD PRIMARY KEY (`id`),
  ADD KEY `main_goals_course_id_8bd6ab9d_fk_main_subject_id` (`course_id`);

--
-- Индекси за таблица `main_klass`
--
ALTER TABLE `main_klass`
  ADD PRIMARY KEY (`id`);

--
-- Индекси за таблица `main_log`
--
ALTER TABLE `main_log`
  ADD PRIMARY KEY (`id`);

--
-- Индекси за таблица `main_objectives`
--
ALTER TABLE `main_objectives`
  ADD PRIMARY KEY (`id`),
  ADD KEY `main_objectives_course_id_2d2f3221_fk_main_subject_id` (`course_id`);

--
-- Индекси за таблица `main_school`
--
ALTER TABLE `main_school`
  ADD PRIMARY KEY (`id`);

--
-- Индекси за таблица `main_school_classes`
--
ALTER TABLE `main_school_classes`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `main_school_classes_school_id_klass_id_a38111c2_uniq` (`school_id`,`klass_id`),
  ADD KEY `main_school_classes_klass_id_bebf6d30_fk_main_klass_id` (`klass_id`);

--
-- Индекси за таблица `main_school_specialities`
--
ALTER TABLE `main_school_specialities`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `main_school_specialities_school_id_specialty_id_c782cac5_uniq` (`school_id`,`specialty_id`),
  ADD KEY `main_school_speciali_specialty_id_78354343_fk_main_spec` (`specialty_id`);

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
  ADD KEY `main_userprofile_grade_section_id_45484bc6_fk_main_klass_id` (`grade_section_id`),
  ADD KEY `main_userprofile_subject_id_5a0cbf6b_fk_main_subject_id` (`subject_id`);

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=73;

--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- AUTO_INCREMENT for table `main_documents`
--
ALTER TABLE `main_documents`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `main_goals`
--
ALTER TABLE `main_goals`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `main_klass`
--
ALTER TABLE `main_klass`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `main_log`
--
ALTER TABLE `main_log`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `main_objectives`
--
ALTER TABLE `main_objectives`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `main_school`
--
ALTER TABLE `main_school`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `main_school_classes`
--
ALTER TABLE `main_school_classes`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `main_school_specialities`
--
ALTER TABLE `main_school_specialities`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `main_specialty`
--
ALTER TABLE `main_specialty`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `main_specialty_subjects`
--
ALTER TABLE `main_specialty_subjects`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `main_subject`
--
ALTER TABLE `main_subject`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `main_topic`
--
ALTER TABLE `main_topic`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `main_unit`
--
ALTER TABLE `main_unit`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `main_userprofile`
--
ALTER TABLE `main_userprofile`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

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
-- Ограничения за таблица `main_goals`
--
ALTER TABLE `main_goals`
  ADD CONSTRAINT `main_goals_course_id_8bd6ab9d_fk_main_subject_id` FOREIGN KEY (`course_id`) REFERENCES `main_subject` (`id`);

--
-- Ограничения за таблица `main_objectives`
--
ALTER TABLE `main_objectives`
  ADD CONSTRAINT `main_objectives_course_id_2d2f3221_fk_main_subject_id` FOREIGN KEY (`course_id`) REFERENCES `main_subject` (`id`);

--
-- Ограничения за таблица `main_school_classes`
--
ALTER TABLE `main_school_classes`
  ADD CONSTRAINT `main_school_classes_klass_id_bebf6d30_fk_main_klass_id` FOREIGN KEY (`klass_id`) REFERENCES `main_klass` (`id`),
  ADD CONSTRAINT `main_school_classes_school_id_dd8e44f3_fk_main_school_id` FOREIGN KEY (`school_id`) REFERENCES `main_school` (`id`);

--
-- Ограничения за таблица `main_school_specialities`
--
ALTER TABLE `main_school_specialities`
  ADD CONSTRAINT `main_school_speciali_specialty_id_78354343_fk_main_spec` FOREIGN KEY (`specialty_id`) REFERENCES `main_specialty` (`id`),
  ADD CONSTRAINT `main_school_specialities_school_id_9588fab6_fk_main_school_id` FOREIGN KEY (`school_id`) REFERENCES `main_school` (`id`);

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
  ADD CONSTRAINT `main_userprofile_grade_section_id_45484bc6_fk_main_klass_id` FOREIGN KEY (`grade_section_id`) REFERENCES `main_klass` (`id`),
  ADD CONSTRAINT `main_userprofile_school_id_74f42cf3_fk_main_school_id` FOREIGN KEY (`school_id`) REFERENCES `main_school` (`id`),
  ADD CONSTRAINT `main_userprofile_speciality_id_475d0b2d_fk_main_specialty_id` FOREIGN KEY (`speciality_id`) REFERENCES `main_specialty` (`id`),
  ADD CONSTRAINT `main_userprofile_subject_id_5a0cbf6b_fk_main_subject_id` FOREIGN KEY (`subject_id`) REFERENCES `main_subject` (`id`),
  ADD CONSTRAINT `main_userprofile_user_id_15c416f4_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1
-- Време на генериране: 28 септ 2026 в 23:04
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
(104, 'Can view Бележка към точка от план', 23, 'view_sessionnote'),
(105, 'Can add Приложение към точка от план', 24, 'add_sessionattachment'),
(106, 'Can change Приложение към точка от план', 24, 'change_sessionattachment'),
(107, 'Can delete Приложение към точка от план', 24, 'delete_sessionattachment'),
(108, 'Can view Приложение към точка от план', 24, 'view_sessionattachment'),
(109, 'Can add Параметри на учебния ден', 25, 'add_schooldayconfig'),
(110, 'Can change Параметри на учебния ден', 25, 'change_schooldayconfig'),
(111, 'Can delete Параметри на учебния ден', 25, 'delete_schooldayconfig'),
(112, 'Can view Параметри на учебния ден', 25, 'view_schooldayconfig'),
(113, 'Can add AI Промпт', 26, 'add_aiprompt'),
(114, 'Can change AI Промпт', 26, 'change_aiprompt'),
(115, 'Can delete AI Промпт', 26, 'delete_aiprompt'),
(116, 'Can view AI Промпт', 26, 'view_aiprompt'),
(117, 'Can add Приложение / Файл', 27, 'add_appattachment'),
(118, 'Can change Приложение / Файл', 27, 'change_appattachment'),
(119, 'Can delete Приложение / Файл', 27, 'delete_appattachment'),
(120, 'Can view Приложение / Файл', 27, 'view_appattachment');

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
(1, 'pbkdf2_sha256$600000$3iNEHTkQ6rkF6v46il2Dsp$wzYrjzST0uYMRVFUzIBCXDqFWdbed8vyiQCqZ39eB9o=', '2026-09-28 20:27:38.003358', 1, 'superadmin', 'Георги', 'Бориков', '', 1, 1, '2025-09-04 19:41:42.000000'),
(2, 'pbkdf2_sha256$600000$eF8P44rBpxEGxw8UdOutbg$+qiE1KzVTq+fMN+wsIIQXPmmw20z/zg9pA3u7AzJfOU=', NULL, 0, 'schooladmin1', 'Ущилищен', 'Админ 1', 'cd@abv.bg', 0, 1, '2025-10-03 20:55:16.170750'),
(3, 'pbkdf2_sha256$600000$MYtPjVuUgmUmNFr3Ncn3Dk$E0EFKKP6SGaYgdve4aUxQxy0NxifekAq/N6cyK7QlvQ=', '2026-09-13 14:19:14.922027', 0, 'teacher1', 'Учител', '1', '1@2.34', 0, 1, '2025-10-04 13:13:29.875629'),
(4, 'pbkdf2_sha256$600000$9y7JQPADSwj3C11pTunuUL$deiOhmcaiAkTjdcrLf82sTmomhC4wjBk97Hw6lmRxtU=', NULL, 0, 'schooladmin2', 'Училищен', 'Админ 2', '', 0, 1, '2025-10-04 13:19:19.365209'),
(5, 'pbkdf2_sha256$600000$teag8xBYAQM9o7Omf78hOE$UP7Scnv9jbv3pct5H7DiwapjdrpvcyhazRfhmsbb2rc=', '2026-09-28 14:53:12.954495', 0, 'student1', 'Ученик', '1', '', 0, 1, '2025-10-04 13:37:34.091871'),
(6, 'pbkdf2_sha256$600000$kSVpyBeklvYLe5Xp3wxi98$70tm0LllKgCkIKZLI2pdcilanCD6YSeeg3VFKF69lLI=', NULL, 0, 'student2', 'Ученик', '2', '', 0, 1, '2025-10-04 13:39:07.766354'),
(7, 'pbkdf2_sha256$600000$amvEZB7ItS8fLaxH53i1gc$G6jnB8NPLYKWFIeAyt48kzyJk9FziCIxX5k9w5v+fyo=', NULL, 0, 'student3', 'Ученик', '3', '', 0, 1, '2025-10-06 20:49:33.950469'),
(9, 'pbkdf2_sha256$600000$p7zx7QUwMNDyklnq9AMfRN$5ahYZoZQFf2ugwwvOxWGknTWs6GIymYHKdHvYLUpXYA=', '2026-09-22 19:05:24.558090', 0, 'test_admin', 'Test', 'Admin', '', 0, 1, '2026-09-22 11:24:02.107566'),
(10, 'pbkdf2_sha256$600000$wh8X7EZqoPVDCRFHHyY4zT$VV/tMaxGXdYmXvdzGjbjmacggYuAW2qgGOXvPlox/pE=', NULL, 0, 'test_teacher', 'Test', 'Teacher', '', 0, 1, '2026-09-22 11:24:44.921117');

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
(22, '2026-03-17 17:33:53.217553', '1', '4810301: Приложно програмиране', 2, '[{\"changed\": {\"fields\": [\"\\u041f\\u0440\\u0435\\u0434\\u043c\\u0435\\u0442\\u0438\"]}}]', 11, 1),
(23, '2026-09-13 10:42:56.454040', '5', 'student1', 2, '[{\"changed\": {\"fields\": [\"password\"]}}]', 4, 1),
(24, '2026-09-13 12:12:51.406765', '5', 'student1', 2, '[{\"changed\": {\"fields\": [\"password\"]}}]', 4, 1),
(25, '2026-09-13 12:29:12.724155', '5', 'Потребител #5: Ученик 1', 2, '[{\"changed\": {\"fields\": [\"\\u041a\\u043b\\u0430\\u0441\"]}}]', 12, 1),
(26, '2026-09-13 14:10:50.558658', '3', 'teacher1', 2, '[{\"changed\": {\"fields\": [\"password\"]}}]', 4, 1),
(27, '2026-09-13 22:53:19.791782', '11', 'Анализ на учебна програма (МОН) и генериране на раздели и теми с MoSCoW анализ (Учебни раздели/модули)', 2, '[{\"changed\": {\"fields\": [\"\\u0422\\u0435\\u043a\\u0441\\u0442 \\u043d\\u0430 \\u043f\\u0440\\u043e\\u043c\\u043f\\u0442\\u0430\", \"\\u0423\\u043a\\u0430\\u0437\\u0430\\u043d\\u0438\\u044f \\u0437\\u0430 \\u043f\\u043e\\u043b\\u0437\\u0432\\u0430\\u043d\\u0435\", \"\\u041f\\u043e\\u0434\\u0440\\u0435\\u0434\\u0431\\u0430\"]}}]', 26, 1),
(28, '2026-09-13 22:53:27.868135', '6', 'Разпределение на учебни раздели и часове (Учебни раздели/модули)', 2, '[{\"changed\": {\"fields\": [\"\\u041f\\u043e\\u0434\\u0440\\u0435\\u0434\\u0431\\u0430\"]}}]', 26, 1),
(29, '2026-09-13 22:54:38.861551', '6', 'Разпределение на учебни раздели и часове (Учебни раздели/модули)', 2, '[{\"changed\": {\"fields\": [\"\\u0423\\u043a\\u0430\\u0437\\u0430\\u043d\\u0438\\u044f \\u0437\\u0430 \\u043f\\u043e\\u043b\\u0437\\u0432\\u0430\\u043d\\u0435\"]}}]', 26, 1),
(30, '2026-09-21 20:39:45.956982', '4', '4 Test txt', 2, '[{\"changed\": {\"fields\": [\"\\u0421\\u0438\\u0441\\u0442\\u0435\\u043c\\u0435\\u043d \\u0444\\u0430\\u0439\\u043b / \\u043f\\u0440\\u0438\\u043b\\u043e\\u0436\\u0435\\u043d\\u0438\\u0435\"]}}]', 27, 1),
(31, '2026-09-21 20:39:56.067570', '5', '5 Test MD original', 2, '[{\"changed\": {\"fields\": [\"\\u0421\\u0438\\u0441\\u0442\\u0435\\u043c\\u0435\\u043d \\u0444\\u0430\\u0439\\u043b / \\u043f\\u0440\\u0438\\u043b\\u043e\\u0436\\u0435\\u043d\\u0438\\u0435\"]}}]', 27, 1),
(32, '2026-09-21 20:40:12.025807', '3', '3 Test PDF edited', 2, '[{\"changed\": {\"fields\": [\"\\u0421\\u0438\\u0441\\u0442\\u0435\\u043c\\u0435\\u043d \\u0444\\u0430\\u0439\\u043b / \\u043f\\u0440\\u0438\\u043b\\u043e\\u0436\\u0435\\u043d\\u0438\\u0435\"]}}]', 27, 1),
(33, '2026-09-21 20:40:30.781517', '8', '8 ИнтернетПрограмиране_ПП_теория_lesson_plan_1.json', 2, '[{\"changed\": {\"fields\": [\"\\u0421\\u044a\\u0437\\u0434\\u0430\\u0434\\u0435\\u043d \\u043e\\u0442\"]}}]', 27, 1),
(34, '2026-09-26 13:33:10.365994', '14', '14 Иван Петров', 2, '[{\"changed\": {\"fields\": [\"\\u0412\\u0438\\u0434\\u0438\\u043c\\u043e \\u0437\\u0430 \\u0443\\u0447\\u0435\\u043d\\u0438\\u0446\\u0438\\u0442\\u0435\"]}}]', 24, 1);

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
(26, 'main', 'aiprompt'),
(27, 'main', 'appattachment'),
(7, 'main', 'documents'),
(16, 'main', 'goal'),
(8, 'main', 'klass'),
(9, 'main', 'log'),
(17, 'main', 'objective'),
(10, 'main', 'school'),
(25, 'main', 'schooldayconfig'),
(19, 'main', 'session'),
(24, 'main', 'sessionattachment'),
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
(42, 'main', '0024_alter_subject_subject_type', '2025-10-09 18:33:57.407785'),
(43, 'main', '0025_alter_session_options_alter_sessiontopic_options_and_more', '2026-09-09 21:00:24.057577'),
(44, 'main', '0026_sessionattachment', '2026-09-11 23:12:54.161053'),
(45, 'main', '0027_alter_sessionattachment_options_and_more', '2026-09-11 23:30:42.472842'),
(46, 'main', '0028_alter_topic_moscow_rem', '2026-09-13 09:14:45.879294'),
(47, 'main', '0029_schooldayconfig', '2026-09-13 09:14:45.895875'),
(48, 'main', '0030_aiprompt', '2026-09-13 19:22:22.728444'),
(49, 'main', '0031_seed_ai_prompts', '2026-09-13 19:23:17.979391'),
(50, 'main', '0032_seed_curriculum_import_prompt', '2026-09-13 22:18:10.503495'),
(51, 'main', '0033_seed_goals_import_prompt', '2026-09-13 23:14:50.190258'),
(52, 'main', '0034_seed_lessons_import_prompt', '2026-09-14 09:21:13.755965'),
(53, 'main', '0035_seed_practice_lessons_prompt', '2026-09-14 09:58:54.479353'),
(54, 'main', '0036_seed_lesson_plan_prompt', '2026-09-14 10:34:10.355893'),
(55, 'main', '0037_seed_lesson_theory_notes_prompt', '2026-09-14 11:41:17.955078'),
(56, 'main', '0038_seed_topic_distribution_template_prompts', '2026-09-14 13:10:05.369900'),
(57, 'main', '0039_seed_python_stack_curriculum_prompt', '2026-09-15 15:14:30.977705'),
(58, 'main', '0040_alter_subject_options', '2026-09-17 21:16:28.841098'),
(59, 'main', '0041_appattachment', '2026-09-17 21:16:28.858242'),
(61, 'main', '0042_update_topic_distribution_template_prompts', '2026-09-18 18:40:29.359474'),
(62, 'main', '0043_fix_grade_12_term_weeks', '2026-09-18 19:06:06.187471'),
(63, 'main', '0044_unique_ascii_upload_paths', '2026-09-18 22:27:54.129970'),
(64, 'main', '0045_appattachment_created_by_appattachment_is_system', '2026-09-21 20:18:36.475613'),
(65, 'main', '0046_appattachment_original_filename', '2026-09-22 08:40:36.890403'),
(66, 'main', '0047_sessionattachment_original_filename', '2026-09-22 19:52:48.727783'),
(67, 'main', '0048_seed_pgee_lesson_blank_prompt', '2026-09-25 16:21:44.591853'),
(68, 'main', '0049_seed_lesson_evaluation_rubric_prompt', '2026-09-25 19:34:15.253415'),
(69, 'main', '0050_sessionattachment_is_student_visible', '2026-09-25 20:13:54.585769'),
(70, 'main', '0051_update_pgee_lesson_blank_prompt', '2026-09-25 20:54:29.103564'),
(71, 'main', '0052_seed_lesson_micro_prompts', '2026-09-25 21:14:57.023372'),
(72, 'main', '0053_session_social_emotional_goals_and_more', '2026-09-25 21:50:30.853288');

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
('0eh0qtiiyzy350v0f98g0jjv9y2t8tur', '.eJxVjEsOwjAMBe-SNYqckDoNS_Y9Q2XHDi2gVOpnhbg7VOoCtm9m3sv0tK1Dvy0696OYi3Hm9Lsx5YfWHcid6m2yearrPLLdFXvQxXaT6PN6uH8HAy3Dt4aEiBoK5aAJYgNAUBiRmaMQu9SAOJdbiS76tlDwuSCKtl5SOJOa9wflkTgu:1vzKyO:F_qTwdZP5C3wxom__anvqrzv6ESGInoUOta_KmA7RH0', '2026-03-22 20:43:36.575031'),
('37c4gvr4ndeaeum9cueof5i54445oy1t', '.eJxVjEsOwjAMBe-SNYqckDoNS_Y9Q2XHDi2gVOpnhbg7VOoCtm9m3sv0tK1Dvy0696OYi3Hm9Lsx5YfWHcid6m2yearrPLLdFXvQxXaT6PN6uH8HAy3Dt4aEiBoK5aAJYgNAUBiRmaMQu9SAOJdbiS76tlDwuSCKtl5SOJOa9wflkTgu:1vLUfW:89HggwK9Sg5ctBRLzwVVJV-TAMrrk6Q9XxVjku4CvxY', '2025-12-02 22:59:26.781728'),
('3nkjy5duqs20igrjxq7m5d08g0dudv0q', '.eJxVjEsOwjAMBe-SNYqckDoNS_Y9Q2XHDi2gVOpnhbg7VOoCtm9m3sv0tK1Dvy0696OYi3Hm9Lsx5YfWHcid6m2yearrPLLdFXvQxXaT6PN6uH8HAy3Dt4aEiBoK5aAJYgNAUBiRmaMQu9SAOJdbiS76tlDwuSCKtl5SOJOa9wflkTgu:1w7KBF:DWVuIe8Kt37eQkhhqxNAgkW4slYu2VU0pP80phpDUBY', '2026-04-13 21:29:53.602986'),
('586n80zjuqhr2hy0wzzpoyhq5x6hwxkb', '.eJxVjEsOwjAMBe-SNYqckDoNS_Y9Q2XHDi2gVOpnhbg7VOoCtm9m3sv0tK1Dvy0696OYi3Hm9Lsx5YfWHcid6m2yearrPLLdFXvQxXaT6PN6uH8HAy3Dt4aEiBoK5aAJYgNAUBiRmaMQu9SAOJdbiS76tlDwuSCKtl5SOJOa9wflkTgu:1v0hil:XIZFAp4KRWEzrXNhKQPIHEN6eVplzGCCzQMdNHGZm7w', '2025-10-06 14:40:51.815905'),
('67ihxd8pp6tetg0w1km7ktafs6v32dnc', '.eJxVjEsOwjAMBe-SNYqckDoNS_Y9Q2XHDi2gVOpnhbg7VOoCtm9m3sv0tK1Dvy0696OYi3Hm9Lsx5YfWHcid6m2yearrPLLdFXvQxXaT6PN6uH8HAy3Dt4aEiBoK5aAJYgNAUBiRmaMQu9SAOJdbiS76tlDwuSCKtl5SOJOa9wflkTgu:1w2YEC:6t9rfN7hOTAqWaKH2mQeE6E4YygYF7hNbeL4xxOlINo', '2026-03-31 17:29:12.445480'),
('epip6g62svmqomuul6qbzco6thhncm1j', '.eJxVjDsOwyAQBe9CHSF-i03K9D4DYlkITiKQjF1FuXtsyUXSvpl5b-bDtha_9bT4mdiVSXb53TDEZ6oHoEeo98Zjq-syIz8UftLOp0bpdTvdv4MSetnr0VktkaQWCMIpERC0MDrHmMXOQEhFwSkaBpuz1Qo0gSEck7EYIQH7fAG8Cjc8:1xBHwo:lg6gBgZSvIloLyo_2b8GEPk6JdiRZW3wFVgbaav7uEk', '2026-10-12 20:27:38.016670'),
('gvpat2s67maguve9tusfmdslho9pn5ch', '.eJxVjEsOwjAMBe-SNYqckDoNS_Y9Q2XHDi2gVOpnhbg7VOoCtm9m3sv0tK1Dvy0696OYi3Hm9Lsx5YfWHcid6m2yearrPLLdFXvQxXaT6PN6uH8HAy3Dt4aEiBoK5aAJYgNAUBiRmaMQu9SAOJdbiS76tlDwuSCKtl5SOJOa9wflkTgu:1w2zS2:CIt4pa6rqxmeJBO7aaoMngmw2ywMfdu1I7WnWM7iA9A', '2026-04-01 22:33:18.500556'),
('h19x1bpibkvt1o5h38fy5bp6x6ceqeqn', '.eJxVjEsOwjAMBe-SNYqckDoNS_Y9Q2XHDi2gVOpnhbg7VOoCtm9m3sv0tK1Dvy0696OYi3Hm9Lsx5YfWHcid6m2yearrPLLdFXvQxXaT6PN6uH8HAy3Dt4aEiBoK5aAJYgNAUBiRmaMQu9SAOJdbiS76tlDwuSCKtl5SOJOa9wflkTgu:1vqUeG:yaRnZM-lJYB3o5gMBeosZKjV1YoSuzzN5_K610V3-k4', '2026-02-26 11:14:16.663797'),
('rnge1fejyurh4l9glmsdtdojclth6i3t', '.eJxVjEsOwjAMBe-SNYqckDoNS_Y9Q2XHDi2gVOpnhbg7VOoCtm9m3sv0tK1Dvy0696OYi3Hm9Lsx5YfWHcid6m2yearrPLLdFXvQxXaT6PN6uH8HAy3Dt4aEiBoK5aAJYgNAUBiRmaMQu9SAOJdbiS76tlDwuSCKtl5SOJOa9wflkTgu:1v5pf2:STUganA261zIN50sQzS1urLL6SULmE3Sq8QVkP4kr6g', '2025-10-20 18:10:12.525119'),
('rrqct5ftw5c96z59i0crqa11y2fywlak', '.eJxVjEsOwjAMBe-SNYqckDoNS_Y9Q2XHDi2gVOpnhbg7VOoCtm9m3sv0tK1Dvy0696OYi3Hm9Lsx5YfWHcid6m2yearrPLLdFXvQxXaT6PN6uH8HAy3Dt4aEiBoK5aAJYgNAUBiRmaMQu9SAOJdbiS76tlDwuSCKtl5SOJOa9wflkTgu:1vzz8I:OuiNx1Nuwwx05DoLrGNh3sls9xLnNGvD34ox3d4JdN4', '2026-03-24 15:36:30.295692'),
('vd28gf8an0d9gjn8dsb9xyuln6rrpts0', '.eJxVjEsOwjAMBe-SNYqckDoNS_Y9Q2XHDi2gVOpnhbg7VOoCtm9m3sv0tK1Dvy0696OYi3Hm9Lsx5YfWHcid6m2yearrPLLdFXvQxXaT6PN6uH8HAy3Dt4aEiBoK5aAJYgNAUBiRmaMQu9SAOJdbiS76tlDwuSCKtl5SOJOa9wflkTgu:1wV3Me:6ZHRibmbqfMjKG38E0yq8owOaUav4PAS-Is8dPn5fsM', '2026-06-18 08:23:44.933424'),
('vm5guny96d3yf0m1oz6oeqquaq43p7qz', '.eJxVjEsOwjAMBe-SNYqckDoNS_Y9Q2XHDi2gVOpnhbg7VOoCtm9m3sv0tK1Dvy0696OYi3Hm9Lsx5YfWHcid6m2yearrPLLdFXvQxXaT6PN6uH8HAy3Dt4aEiBoK5aAJYgNAUBiRmaMQu9SAOJdbiS76tlDwuSCKtl5SOJOa9wflkTgu:1uuGHi:bvbp3ZBPAQMSLwqke4Qo-VzOftzearhwTIjV1d9OOxw', '2025-09-18 20:10:18.056843'),
('w7y1n1fr9kw9329izou2ppq5qci1tbiz', '.eJxVjEsOwjAMBe-SNYqckDoNS_Y9Q2XHDi2gVOpnhbg7VOoCtm9m3sv0tK1Dvy0696OYi3Hm9Lsx5YfWHcid6m2yearrPLLdFXvQxXaT6PN6uH8HAy3Dt4aEiBoK5aAJYgNAUBiRmaMQu9SAOJdbiS76tlDwuSCKtl5SOJOa9wflkTgu:1v5peU:TUbT5AWidIOcLdFkkvQFrWpuE1-1VknHjmMQegnowM8', '2025-10-20 18:09:38.217251');

-- --------------------------------------------------------

--
-- Структура на таблица `main_aiprompt`
--

CREATE TABLE `main_aiprompt` (
  `id` bigint(20) NOT NULL,
  `title` varchar(200) NOT NULL,
  `page_key` varchar(50) NOT NULL,
  `prompt_text` longtext NOT NULL,
  `instructions` longtext NOT NULL,
  `is_system` tinyint(1) NOT NULL,
  `order` smallint(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_by_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Схема на данните от таблица `main_aiprompt`
--

INSERT INTO `main_aiprompt` (`id`, `title`, `page_key`, `prompt_text`, `instructions`, `is_system`, `order`, `created_at`, `updated_at`, `created_by_id`) VALUES
(1, 'Генериране на структуриран план на урок с точки и времетраене', 'lesson_main', 'Действай като опитен преподавател по {предмет} за ученици от {клас} клас (специалност {специалност}). Състави подробен и балансиран план за 45-минутен урок на тема: \"{тема}\". Фокус на урока: {фокус}. Формулирай 3 до 5 основни точки от плана с приблизително времетраене за всяка част (въведение, ново учебно съдържание, практическа работа, затвърждаване и обобщение).', 'Копирайте промпта в AI чат. Резултатът ще ви предостави готова педагогическа структура за точките в полето \"План на урока\".', 1, 8, '2026-09-13 19:23:17.962041', '2026-09-25 19:34:15.247167', NULL),
(2, 'Създаване на практически задачи и упражнения', 'lesson_main', 'Като учител по {предмет}, създай 3 практически задачи за упражнение към урок \"{тема}\" за {клас} клас. Цели на урока: {цели}. Точки от плана: {точки}. За всяка задача включи: 1) Условие; 2) Очаквано стъпково решение/отговор; 3) Критерий за оценка на разбирането.', 'Използвайте този промпт, за да генерирате задачи с решения, които след това да добавите директно в таб \"Задачи\" на урока.', 1, 9, '2026-09-13 19:23:17.965178', '2026-09-25 19:34:15.246653', NULL),
(3, 'Формулиране на кратко обобщение и ключови изводи за учениците', 'lesson_main', 'Напиши синтезирано обобщение (до 200 думи) на разбираем за ученици от {клас} клас език за урок на тема: \"{тема}\" по {предмет}. Основни ��очки от урока: {точки}. Включи 3 ключови извода и 1 въпрос за размисъл/дискусия.', 'Подходящо за бележки към урока, теоретично въведение или раздаване на учениците в края на часа.', 1, 10, '2026-09-13 19:23:17.969020', '2026-09-25 19:34:15.245971', NULL),
(4, 'Тестов въпросник с множествен избор (Quiz)', 'lesson_main', 'Генерирай 5 тестови въпроса с по 4 избираеми отговора (A, B, C, D) и посочен верен отговор с кратко обяснение по тема: \"{тема}\" ({предмет}, {клас} клас). Точки от плана: {точки}.', 'Бърз начин за генериране на междинна или финална проверка на знанията.', 1, 11, '2026-09-13 19:23:17.970288', '2026-09-25 19:34:15.244692', NULL),
(5, 'Формулиране на педагогически цели по таксономията на Блум и учебна програма (МОН)', 'course_goals', 'Действай като опитен методист и учител по професионална подготовка. Прикачвам официална учебна програма (утвърдена от МОН) за учебен предмет: \"{предмет}\" ({клас} клас, специалност/професия: {специалност}).\n\nМоля, анализирай целите и очакваните резултати от приложената учебна програма и формулирай ясни, конкретни и измерими педагогически цели на обучението по предмета, структурирани по нивата на познавателната таксономия на Блум:\n1. Знания и разбиране – дефинира, описва, разпознава фундаментални концепции и синтаксис;\n2. Приложение и анализ – прилага алгоритми, разработва модули, открива грешки и анализира структури;\n3. Практически компетентности и синтез/оценка – проектира цялостни решения, тества, документира и оценява софтуерни продукти.\n\nФормулирай стегнати цели (между 4 и 8 цели), формулирани с глаголи за действие в 3 л. ед. ч., съобразени с възрастта на учениците и специфичния профил на специалността.\n\nВърни резултата ЕДИНСТВЕНО като валиден JSON масив (без излишен съпътстващ свободен текст), готов за директен импорт в приложението ИРИДА:\n[\n  {\n    \"num\": 1,\n    \"name\": \"Дефинира и обяснява основните концепции, синтаксис и базови структури от данни\"\n  },\n  {\n    \"num\": 2,\n    \"name\": \"Проектира, разработва и тества модулни алгоритмични решения за практически задачи\"\n  },\n  {\n    \"num\": 3,\n    \"name\": \"Прилага добри практики за дебъгване, структуриране и документиране на програмен код\"\n  }\n]', '1. Копирайте промпта;\n2. Отворете външния си AI инструмент (ChatGPT, Claude, Gemini, DeepSeek и др.);\n3. Прикачете файла с учебната програма (DOCX/PDF от МОН);\n4. Поставете промпта и изпратете съобщението;\n5. Копирайте генерирания JSON код;\n6. Натиснете бутона „Импорт на цели“ до „Добави цел“ на тази страница и поставете JSON кода (или качете записания файл) за автоматично зареждане.', 1, 1, '2026-09-13 19:23:17.971410', '2026-09-13 23:14:50.186437', NULL),
(6, 'Разпределение на учебни раздели и часове', 'course_units', 'Предложи логично тематично разпределение на учебните раздели (модули) за предмет \"{предмет}\" за ученици от {клас} клас (специалност {специалност}). Предложи препоръчителен брой учебни часове за всеки раздел и кратко описание на обхвата му.', 'Използвайте този промпт за планиране на модулната структура и разпределянето на хорариума.', 1, 2, '2026-09-13 19:23:17.972533', '2026-09-13 22:54:38.860111', NULL),
(7, 'Разпределяне на учебното съдържание по уроци и занятия (BOPPPS / MSCW)', 'course_lessons', 'Действай като старши методист и учител по професионална подготовка. Трябва да разработиш цялостно тематично разпределение на уроците (занятията) за учебен предмет: \"{предмет}\" ({клас}, специалност/професия: {специалност}).\n\n### 1. ВХОДНИ ДАННИ И ПАРАМЕТРИ:\n- Хорариум и седмици:\n{структура_часове}\n- Общи цели на обучението по предмета:\n{цели}\n- Учебни раздели и теми с MoSCoW анализ:\n{раздели_и_теми}\n\n### 2. ПРАВИЛА ЗА ПЛАНИРАНЕ И РАЗПРЕДЕЛЕНИЕ:\n1. Продължителност на сроковете: I учебен срок е винаги 18 учебни седмици. II учебен срок е 11 учебни седмици (за 12 клас) или 18 учебни седмици (за 8, 9, 10 и 11 клас).\n2. Продължителност на едно занятие (урок): Определя се спрямо седмичния хорариум (напр. при 1 час/седмично -> 1 уч.ч. на урок; при 2 ч./седм. -> 1 урок от 2 уч.ч.; при 3 ч./седм. -> 1 урок от 3 уч.ч.; при 4 ч./седм. -> 2 урока седмично по 2 уч.ч. и т.н.).\n3. Разпределение на резерва: Предвиденият резерв от часове се разпределя пропорционално в двата срока (ако предметът се изучава два срока). Резервните часове НЕ се планират като отделни уроци – те намаляват броя на планираните основни уроци за срока (напр. при 18 седмици по 2 часа = 36 часа и 2 часа резерв се планират 17 урока по 2 часа, а 2 часа остават като свободен резерв).\n4. Закръгляне по раздели: Ако за даден раздел са предвидени брой часове, които не са кратни на продължителността на урока (напр. 7 часа при уроци по 2 часа), закръгли броя уроци надолу (3 урока по 2 ч. = 6 ч.), а остатъка (1 час) прехвърли към общия резерв.\n5. Дидактическа структура и видове уроци (BOPPPS модел):\n   - Балансирай видовете уроци: \"НЗ\" (Нови знания), \"УПР\" (Упражнение / Практика), \"ПК\" (Проверка и контрол / Тест / Проектна защита), \"ОС\" (Обобщаване и систематизиране), \"K\" (Комбиниран урок);\n   - Темите с категория \"M\" (Must) залагай в основата на уроците за нови знания;\n   - Темите с \"S\" (Should) и \"C\" (Could) залагай за упражнения, водена и самостоятелна практика и обобщения;\n   - За всяко занятие формулирай 2-3 ясни оперативни цели (goals) и 1-2 изречения за фокуса/акцентите на урока (focus);\n   - В полето \"topics\" посочи съответния раздел (unit_num) и тема (topic_num) от учебната програма с кратко пояснение (description).\n\n### 3. ФОРМАТ НА РЕЗУЛТАТА:\nВърни резултата ЕДИНСТВЕНО като валиден JSON масив от обекти (без излишен свободен текст около него), готов за директен импорт в приложението ИРИДА:\n[\n  {\n    \"num\": 1,\n    \"name\": \"Въведение в синтаксиса и базовата структура на езика\",\n    \"session_type\": \"НЗ\",\n    \"duration\": 2,\n    \"basic_level\": true,\n    \"goals\": \"1. Разпознава основните типове данни и променливи;\\n2. Създава първата си работеща програма.\",\n    \"focus\": \"Среда за разработка, базови типове данни, оператори и компилация.\",\n    \"topics\": [\n      {\n        \"unit_num\": 1,\n        \"topic_num\": 1,\n        \"description\": \"Теоретично въведение и демонстрационен код\"\n      }\n    ]\n  },\n  {\n    \"num\": 2,\n    \"name\": \"Практическо упражнение: Работа с променливи и оператори\",\n    \"session_type\": \"УПР\",\n    \"duration\": 2,\n    \"basic_level\": true,\n    \"goals\": \"1. Прилага оператори в практически изчисления;\\n2. Открива и коригира синтактични грешки.\",\n    \"focus\": \"Водена и самостоятелна практика с програмни фрагменти.\",\n    \"topics\": [\n      {\n        \"unit_num\": 1,\n        \"topic_num\": 2,\n        \"description\": \"Практически задачи и дебъгване\"\n      }\n    ]\n  }\n]', '1. Копирайте промпта (всички параметри за седмици, часове, раздели и теми са попълнени автоматично);\n2. Отворете вашия предпочитан AI асистент (ChatGPT, Claude, Gemini, DeepSeek и др.);\n3. Поставете промпта и изпратете заявката;\n4. Копирайте върнатия от AI JSON масив;\n5. Натиснете бутона „Импорт на уроци“ на тази страница, поставете JSON кода (или качете записания .json файл) и натиснете „Импортирай“.', 1, 1, '2026-09-13 19:23:17.973618', '2026-09-18 19:06:06.181883', NULL),
(8, 'Планиране на последователност от уроци и практически упражнения', 'session_list', 'Предложи списък от уроци за раздел по \"{предмет}\" ({клас} клас), включващ баланс между теория (нови знания) и практически упражнения за затвърждаване.', 'Помага за организиране на седмичната и месечната програма от уроци.', 1, 1, '2026-09-13 19:23:17.974717', '2026-09-13 19:23:17.974729', NULL),
(9, 'Диференцирано обучение и допълнителни насоки', 'general', 'Предложи методически насоки за диференцирано преподаване по тема \"{тема}\" ({предмет}): 1) Дейности за напреднали ученици, които завършват по-рано; 2) Насоки и подпомагащи въпроси за ученици с трудности при усвояването на материала.', 'Подходящо за адаптиране на учебния процес към индивидуалните темпове и нужди на учениците.', 1, 1, '2026-09-13 19:23:17.975836', '2026-09-13 19:23:17.975848', NULL),
(10, 'Идеи за интерактивни и практически проекти', 'general', 'Предложи 2 кратки интерактивни групови дейности или мини-проекта за класната стая по тема \"{тема}\" ({предмет}, {клас} клас), които насърчават екипната работа и практическото приложение на знанията.', 'Осигурява ангажираност на учениците и повишава практическата насоченост на обучението.', 1, 2, '2026-09-13 19:23:17.976891', '2026-09-13 19:23:17.976903', NULL),
(11, 'Анализ на учебна програма (МОН) и генериране на раздели и теми с MoSCoW анализ', 'course_units', 'Действай като опитен методист и експерт по професионално образование. Прикачвам официална учебна програма (утвърдена от МОН) за учебен предмет: \"{предмет}\" ({клас} клас, специалност/професия: {специалност}).\r\n\r\nМоля, анализирай учебното съдържание от приложения документ и направи детайлен MoSCoW (MSCW) анализ по следната методика:\r\n1. Извлечи всички раздели от програмата и посочи минималния им препоръчителен брой учебни часове (hours).\r\n2. За всеки раздел извлечи конкретните теми (topics) и определи за всяка тема нейната категория по MoSCoW:\r\n   - \"M\" (Must / Задължителна) – Фундаментални концепции, базови синтактични основи и критични принципи, покриващи ДОС;\r\n   - \"S\" (Should / Важна) – Важни теми и добри практики за практическо задълбочаване;\r\n   - \"C\" (Could / Пожелателна) – Обогатяващи теми за напреднали ученици и разширения;\r\n   - \"W\" (Won\'t / Отпадаща) – Тясно специализирани или остарели детайли, които не са приоритет за този курс.\r\n3. За всяка тема посочи кратка и точна педагогическа обосновка (MoSCoW_rem) за избора на съответната категория.\r\n\r\nВърни резултата ЕДИНСТВЕНО като валиден JSON масив (без излишен съпътстващ свободен текст), готов за директен импорт в приложението ИРИДА:\r\n[\r\n  {\r\n    \"num\": 1,\r\n    \"name\": \"Име на раздел 1\",\r\n    \"hours\": 10,\r\n    \"topics\": [\r\n      {\r\n        \"num\": 1,\r\n        \"name\": \"Име на тема 1.1\",\r\n        \"MoSCoW_cat\": \"M\",\r\n        \"MoSCoW_rem\": \"Основни концепции и базисен синтаксис\"\r\n      },\r\n      {\r\n        \"num\": 2,\r\n        \"name\": \"Име на тема 1.2\",\r\n        \"MoSCoW_cat\": \"S\",\r\n        \"MoSCoW_rem\": \"Практическо приложение и упражнение\"\r\n      }\r\n    ]\r\n  }\r\n]', '1. Копирайте промпта;\r\n2. Отворете външния си AI инструмент (ChatGPT, Claude, Gemini, DeepSeek и др.);\r\n3. Прикачете файла с учебната програма (DOCX/PDF от МОН);\r\n4. Поставете промпта и изпратете съобщението;\r\n5. Копирайте генерирания JSON код;\r\n6. Натиснете бутона „Импорт на програма“ до „Добави раздел“ на тази страница и поставете JSON кода (или качете записания файл) за автоматично зареждане.', 1, 1, '2026-09-13 22:18:10.500018', '2026-09-13 22:53:19.789693', NULL),
(12, 'Разпределяне на уроци за Учебна практика в синхрон с Теорията (BOPPPS / Практика)', 'course_lessons', 'Действай като старши методист и учител-практик по професионална подготовка. Трябва да разработиш цялостно тематично разпределение на уроците за учебен предмет по **Учебна практика**: \"{предмет}\" ({клас}, специалност/професия: {специалност}), който да бъде в **пълен дидактически и времеви синхрон** с преподавания паралелно предмет по теория.\n\n### 1. ВХОДНИ ДАННИ ЗА ПРАКТИКАТА:\n- Хорариум и седмици на практиката:\n{структура_часове}\n- Общи цели на обучението по предмета:\n{цели}\n- Учебни раздели и практически теми с MoSCoW анализ:\n{раздели_и_теми}\n- **ПРИКАЧЕН / ВЪВЕДЕН ПЛАН ПО ТЕОРИЯ:** (Към заявката е прикачен .json файл или е предоставен списък с вече разпределените уроци по съответния теоретичен предмет).\n\n### 2. ПРАВИЛА ЗА ПРАКТИЧЕСКА НАСОЧЕНОСТ И СИНХРОНИЗАЦИЯ:\n1. **Педагогически синхрон с теорията (Златно правило):** Учебната практика НЕ МОЖЕ да изпреварва часовете по теория. Всяко практическо занятие трябва да се провежда в същата или следващата учебна седмица спрямо съответните теоретични уроци, така че учениците вече да са запознати с основните понятия и синтаксис.\n2. **Практическа ориентация и типове уроци (BOPPPS / GRR):**\n   - В часовете по практика преобладават уроците от тип \"УПР\" (Практическо упражнение / Лабораторен практикум / Казус), \"ПК\" (Практическа проверка и контрол / Защита на проект) и \"K\" (Комбинирано лабораторно занятие);\n   - Избягвай уроци за чисти нови знания (\"НЗ\") – теоретичните концепции са положени в теорията, а тук фокусът е върху реално писане на код, дебъгване, рефакториране, работа в екип (pair programming) и създаване на работещи приложения;\n   - Темите с категория \"M\" (Must) развивай в задължителни базови лабораторни упражнения;\n   - Темите с \"S\" (Should) и \"C\" (Could) развивай в разширени практически проекти, оптимизации и предизвикателства за напреднали.\n3. **Продължителност и хорариум:**\n   - I учебен срок: 18 учебни седмици; II учебен срок: 11 учебни седмици (за 12 клас) или 18 учебни седмици (за 8, 9, 10 и 11 клас);\n   - Продължителност на едно практическо занятие (урок): според седмичния хорариум (обикновено блокове от 2, 3 или 4 учебни часа);\n   - Резервът от часове се разпределя пропорционално и намалява броя на планираните занятия за срока, като остава свободен за допълнителни проектни сесии или преговор.\n4. **Формулиране на цели и фокус:**\n   - За всяко практическо занятие формулирай 2-3 ясни оперативни практически цели (\"goals\") с глаголи за действие (напр. \"1. Създава...\", \"2. Тества и отстранява грешки...\", \"3. Прилага...\");\n   - В полето \"focus\" посочи конкретната практическа задача, софтуерен модул, казус или среда за разработка;\n   - В полето \"topics\" посочи съответния раздел (unit_num) и тема (topic_num) от учебната програма по практика.\n\n### 3. ФОРМАТ НА РЕЗУЛТАТА:\nВърни резултата ЕДИНСТВЕНО като валиден JSON масив от обекти (готов за директен импорт в приложението ИРИДА):\n[\n  {\n    \"num\": 1,\n    \"name\": \"Лабораторен практикум: Изграждане на базов софтуерен модул и тестване\",\n    \"session_type\": \"УПР\",\n    \"duration\": 2,\n    \"basic_level\": true,\n    \"goals\": \"1. Реализира работещ програмен код по зададена спецификация;\\n2. Тества входно-изходните данни и отстранява синтактични грешки.\",\n    \"focus\": \"Практическа разработка в среда за програмиране, конзолен вход/изход и дебъгване.\",\n    \"topics\": [\n      {\n        \"unit_num\": 1,\n        \"topic_num\": 1,\n        \"description\": \"Практическо лабораторно упражнение\"\n      }\n    ]\n  }\n]', '1. Копирайте промпта (всички параметри за предмета по практика са попълнени автоматично);\n2. Отворете вашия предпочитан AI асистент (ChatGPT, Claude, Gemini, DeepSeek и др.);\n3. Прикачете .json файла с вече импортираните уроци по теория (или поставете текста му веднага след промпта);\n4. Изпратете заявката към AI;\n5. Копирайте върнатия от AI JSON масив с практически уроци;\n6. Натиснете бутона „Импорт на уроци“ на страницата за учебна практика, поставете JSON кода и натиснете „Импортирай“.', 1, 2, '2026-09-14 09:58:54.474857', '2026-09-18 19:06:06.183114', NULL),
(13, 'Детайлен BOPPPS план на занятие с демо код, задачи и викторина (Готов за импорт)', 'lesson_main', 'Действай като старши преподавател и методист по професионална подготовка ({специалност}, {клас}). Трябва да разработиш цялостен, детайлен педагогически план за занятие (урок) №{урок_номер} на тема: \"{тема}\".\n\n### 1. ВХОДНИ ДАННИ ЗА ЗАНЯТИЕТО:\n- Предмет: {предмет}\n- Специалност / Професия: {специалност} ({клас})\n- Вид на занятието: {вид_урок}\n- Продължителност: {продължителност} ({продължителност_минути})\n- Включени теми от учебната програма:\n{включени_теми}\n- Очаквани резултати / Основни цели:\n{цели}\n- Акценти на урока:\n{фокус}\n\n### 2. МЕТОДИЧЕСКИ ИЗИСКВАНИЯ (МОДЕЛ BOPPPS & GRR):\nСледвай стриктно дидактическия модел BOPPPS (Bridge-In, Outcomes, Презентация+Демо, Дискусия, Ръководена практика, Самостоятелна практика, Споделяне, Post-Assessment, Summary) и модела за плавно освобождаване на отговорността GRR (Аз правя -> Ние правим -> Вие правите -> Ти правиш сам):\n\n1. **Точки от плана (Session Points):**\n   - Разпредели точно времето между точките, така че **СУМАТА ОТ МИНУТИТЕ ДА Е ТОЧНО РАВНА НА {продължителност_минути}** (напр. за 90 минути: 5 + 5 + 15 + 7 + 8 + 25 + 10 + 7 + 8 = 90 мин.; ако продължителността е 45 мин., мащабирай времената пропорционално);\n   - За всяка точка посочи номер (num), наименование (name), кратка забележка/фаза (description), времетраене в минути (duration) и подробно съдържание (content като форматиран HTML параграфи/списъци с конкретни въпроси, сценарий за преподаване и указания).\n\n2. **Теоретични бележки и демо код (Session Notes):**\n   - Подготви структуриран конспект (notes) с ясни дефиниции, правила и работещ, коментиран демо код (в <pre><code>...</code></pre>);\n   - Свържи всяка бележка със съответната точка от плана чрез point_num (напр. точка 3 за демонстрация на нов синтаксис).\n\n3. **Практически задачи и оценяване (Session Tasks):**\n   - **Съвместна задача (GRR: Ние правим заедно):** малък практически пример с условие (condition) и пълно стъпково решение (answer), обвързана с точката за съвместно упражнение (point_num: 5);\n   - **Самостоятелна задача (GRR: Ти правиш сам):** цялостно практическо задание с ясно условие, изисквания и примерно решение/тестови данни (point_num: 6);\n   - **Мини-викторина / Post-Assessment:** 3-4 бързи въпроса (множествен избор или открити въпроси) в condition и техните верни отговори с обосновка в answer (point_num: 8);\n   - **Домашна работа / Предизвикателство:** допълнителна самостоятелна задача за затвърждаване или разширение (point_num: 9).\n\n### 3. ФОРМАТ НА РЕЗУЛТАТА:\nВърни резултата ЕДИНСТВЕНО като валиден JSON обект (готов за директен импорт в приложението ИРИДА):\n{\n  \"goals\": \"1. Формулира...; 2. Създава...; 3. Тества...\",\n  \"focus\": \"Акценти на занятието: основни синтактични конструкции, работа със софтуерни инструменти и дебъгване.\",\n  \"points\": [\n    {\n      \"num\": 1,\n      \"name\": \"Bridge-In: Въведение и софтуерен казус\",\n      \"description\": \"Въведение и мотивация\",\n      \"duration\": 5,\n      \"content\": \"<p>Поставяне на проблема чрез реален казус от практиката...</p>\"\n    },\n    {\n      \"num\": 2,\n      \"name\": \"Outcomes: Обявяване на очакваните резултати\",\n      \"description\": \"Цели и компетентности\",\n      \"duration\": 5,\n      \"content\": \"<p>Запознаване на учениците с практическите умения, които ще придобият...</p>\"\n    },\n    {\n      \"num\": 3,\n      \"name\": \"Презентация и демонстрация на демо код\",\n      \"description\": \"GRR: Директно обучение (Аз правя)\",\n      \"duration\": 15,\n      \"content\": \"<p>Обяснение на концепцията и показване на демо код на живо в средата за разработка...</p>\"\n    },\n    {\n      \"num\": 4,\n      \"name\": \"Дискусия и рефлексия\",\n      \"description\": \"Въпроси за разбиране\",\n      \"duration\": 7,\n      \"content\": \"<p>Кратка дискусия с учениците и проверка на първоначалното разбиране...</p>\"\n    },\n    {\n      \"num\": 5,\n      \"name\": \"Съвместно упражнение\",\n      \"description\": \"GRR: Ръководена практика (Ние правим заедно)\",\n      \"duration\": 8,\n      \"content\": \"<p>Съвместно писане на код на дъската/екрана заедно с целия клас...</p>\"\n    },\n    {\n      \"num\": 6,\n      \"name\": \"Самостоятелна практика\",\n      \"description\": \"GRR: Самостоятелна работа (Ти правиш сам)\",\n      \"duration\": 25,\n      \"content\": \"<p>Учениците работят индивидуално по поставената задача; диференцирана помощ от учителя...</p>\"\n    },\n    {\n      \"num\": 7,\n      \"name\": \"Проверка и споделяне на решения\",\n      \"description\": \"Демонстрация и анализ\",\n      \"duration\": 10,\n      \"content\": \"<p>Демонстрация на решения на екран и анализ на добри практики...</p>\"\n    },\n    {\n      \"num\": 8,\n      \"name\": \"Мини-викторина (Post-Assessment)\",\n      \"description\": \"Проверка на усвояването\",\n      \"duration\": 7,\n      \"content\": \"<p>3-4 бързи въпроса за моментална обратна връзка...</p>\"\n    },\n    {\n      \"num\": 9,\n      \"name\": \"Обобщение и поставяне на домашно\",\n      \"description\": \"Summary & Домашна работа\",\n      \"duration\": 8,\n      \"content\": \"<p>Кратко обобщение на ключовите изводи и разясняване на домашната работа...</p>\"\n    }\n  ],\n  \"notes\": [\n    {\n      \"num\": 1,\n      \"name\": \"Теоретичен конспект и демо код\",\n      \"point_num\": 3,\n      \"content\": \"<p><strong>Основни концепции:</strong></p><pre><code># Пример за чист и коментиран демо код\\n...</code></pre>\"\n    }\n  ],\n  \"tasks\": [\n    {\n      \"num\": 1,\n      \"name\": \"Съвместна задача (Ръководена практика)\",\n      \"point_num\": 5,\n      \"condition\": \"<p>Условие на задачата за съвместна работа...</p>\",\n      \"answer\": \"<pre><code># Решение и насоки...</code></pre>\"\n    },\n    {\n      \"num\": 2,\n      \"name\": \"Самостоятелна практическа задача\",\n      \"point_num\": 6,\n      \"condition\": \"<p>Условие на самостоятелната задача...</p>\",\n      \"answer\": \"<pre><code># Примерно решение...</code></pre>\"\n    },\n    {\n      \"num\": 3,\n      \"name\": \"Мини-викторина за проверка\",\n      \"point_num\": 8,\n      \"condition\": \"<p>1. Въпрос едно...?<br>2. Въпрос две...?</p>\",\n      \"answer\": \"<p>1. Верен отговор и обосновка...<br>2. Верен отговор...</p>\"\n    },\n    {\n      \"num\": 4,\n      \"name\": \"Домашна работа / Предизвикателство\",\n      \"point_num\": 9,\n      \"condition\": \"<p>Условие на задачата за самостоятелна подготовка вкъщи...</p>\",\n      \"answer\": \"<p>Указания и насоки за изпълнение...</p>\"\n    }\n  ]\n}', '1. Копирайте промпта (всички параметри на избрания урок са попълнени автоматично);\n2. Отворете вашия предпочитан AI асистент (ChatGPT, Claude, Gemini, DeepSeek и др.) и изпратете промпта;\n3. Копирайте върнатия от AI структуриран JSON обект;\n4. Върнете се на страницата на урока и натиснете бутона „Импорт на план“;\n5. Поставете JSON кода и натиснете „Импортирай“. Всички точки, времетраене, демо бележки и задачи ще бъдат записани автоматично!', 1, 1, '2026-09-14 10:34:10.351879', '2026-09-14 10:34:10.351898', NULL),
(14, 'Генериране на учебен файл (.docx / .pdf) с кратки теоретични бележки по темите', 'lesson_main', 'Действай като старши преподавател и автор на учебно съдържание по {предмет} за {клас} клас (специалност: {специалност}). Състави цялостен, структуриран и достъпен учебен материал (Handout / Теоретичен конспект) за учениците за урок №{урок_номер}: \"{тема}\".\n\n### 1. КОНТЕКСТ НА УРОКА:\n- Предмет: {предмет}\n- Специалност: {специалност} ({клас})\n- Вид на занятието: {вид_урок}\n- Включени теми от програмата:\n{включени_теми}\n- Основни цели на урока:\n{цели}\n- Фокус и акценти:\n{фокус}\n\n### 2. СТРУКТУРА НА ДОКУМЕНТА (ГОТОВ ЗА ЕКСПОРТ В .DOCX ИЛИ .PDF):\nОформи съдържанието в прегледен, професионално форматиран вид със заглавия, списъци, таблици и кодови блокове:\n\n1. **Заглавна част:**\n   - Заглавие на урока, предмет, клас, специалност и поле за име на ученика и дата.\n\n2. **Въведение и цели на темата:**\n   - Кратко мотивиращо въведение (2-3 изречения): защо тази тема е важна в реалната практика;\n   - Списък с 3-4 ключови компетентности („След този урок ще можете да...“).\n\n3. **Синтезиран теоретичен конспект по всяка от темите:**\n   - **Основни понятия и дефиниции:** максимално кратки, точни и лесни за запомняне;\n   - **Принципи на работа и синтаксис:** синтезирани правила и визуални/текстови схеми;\n   - **Примери с чист демо код / практически стъпки:** кратки, коментирани примери с обяснение на всеки ключов ред;\n   - **„Внимание / Чести грешки и добри практики“:** акцент върху типични капани и съвети от професионалната разработка.\n\n4. **Обобщаваща таблица / Речник на новите термини (Cheatsheet):**\n   - Таблица с 2-3 колони (Термин / Синтаксис -> Описание / Значение -> Кратък пример).\n\n5. **Въпроси и кратки задачи за самопроверка:**\n   - 3-4 контролни въпроса за проверка на разбирането;\n   - 1-2 мини практически задачи за самостоятелно упражнение с кратки насоки.\n\n### 3. ФОРМАТ НА ИЗХОДА:\nГенерирай материала във форматиран Markdown (с ясни заглавия `#`, `##`, `###`, таблици, списъци и кодови блокове), така че да може директно да бъде копиран и запазен/експортиран като .docx документ (напр. през Word / Google Docs) или експортиран като .pdf файл за раздаване на учениците или прикачване в системата.', '1. Копирайте промпта (всички данни за темата, целите и програмата са попълнени автоматично);\n2. Поставете го във вашия AI асистент (ChatGPT, Claude, Gemini, DeepSeek и др.);\n3. AI ще генерира готов структуриран теоретичен конспект с дефиниции, код, таблици и въпроси за самопроверка;\n4. Можете да копирате резултата в Word / Google Docs и да го запишете като .docx или експортирате като .pdf файл;\n5. Можете да качите готовия файл директно в секцията „Прикачени файлове“ на урока за достъп от учениците!', 1, 2, '2026-09-14 11:41:17.950659', '2026-09-14 11:41:17.950670', NULL),
(15, 'Генериране на Excel тематично разпределение (topic_plan_template.xlsx)', 'course_lessons', 'Действай като старши методист и учител по професионална подготовка. Трябва да разработиш и попълниш пълно годишно тематично разпределение на уроците за учебен предмет: \"{предмет}\" ({клас}, специалност/професия: {специалност}), съответстващо на структурата на шаблона \"topic_plan_template.xlsx\".\n\n### 1. ВХОДНИ ДАННИ И КОНТЕКСТ:\n- Хорариум и седмици:\n{структура_часове}\n- Списък с разработените уроци и занятия:\n{списък_уроци}\n\n### 2. СТРУКТУРА НА ТАБЛИЦАТА (EXCEL ШАБЛОН):\nТаблицата се състои от следните колони (започвайки от ред 2, след заглавния ред):\n1. Колона A: \"Учебна седмица*\" – номер на учебната седмица (число от 1 до 36 за 8, 9, 10 и 11 клас, или от 1 до 29 за 12 клас). Ако за една седмица има предвидени 2 занятия (напр. при 4 ч./седмично с 2 урока по 2 часа), номерът на седмицата се повтаря на отделен ред за всяко занятие.\n2. Колона B: \"Тема*\" – кратко заглавие на урока от предоставения списък с уроци.\n3. Колона C: \"Вид\" – вид на урока, задължително едно от следните стандартни съкращения:\n   - НЗ (Нови знания)\n   - УПР (Упражнение / Практика)\n   - ПК (Проверка и контрол / Тест / Проектна защита)\n   - ОС (Обобщаване и систематизиране)\n   - K (Комбиниран урок)\n   (или оставено празно, ако видът не е дефиниран)\n\n### 3. ДИДАКТИЧЕСКИ И ПЕДАГОГИЧЕСКИ ПРАВИЛА:\n1. Използвай точно подадения списък с разработени уроци, като запазиш тяхната последователност, заглавия и видове.\n2. Продължителност на сроковете: I учебен срок = 18 седмици; II учебен срок = 11 седмици (12 клас) или 18 седмици (8-11 клас).\n3. Продължителност на занятие: определя се според седмичния хорариум (напр. 2 ч./седм. -> 1 урок от 2 часа; 3 ч./седм. -> 1 урок от 3 часа; 4 ч./седм. -> 2 урока по 2 часа седмично).\n4. Разпредели последователно уроците по учебните седмици. Ако в списъка с уроци има означени резервни уроци или часове за обобщение/консултации, ги позиционирай в края на съответните срокове или раздели.\n\n### 4. ФОРМАТ НА ИЗХОДА:\nПредостави резултата в следния формат:\nГотова таблица, която потребителят може директно да маркира, копира и постави в Excel без нужда от допълнително форматиране:\n| Учебна седмица | Тема | Вид |\n| --- | --- | --- |\n| 1 | ... | ПК |\n| 2 | ... | НЗ |\n...', '1. Копирайте промпта чрез бутона „Копирай промпта“ (всички параметри за предмета, хорариума, седмиците и списъка с уроци са попълнени автоматично);\n2. Отворете вашия предпочитан AI асистент (ChatGPT, Claude, Gemini, DeepSeek и др.);\n3. Поставете промпта и изпратете заявката;\n4. Копирайте генерираната таблица и я поставете в Excel файла „topic_plan_template.xlsx“ (от клетка A2 надолу).', 1, 3, '2026-09-14 13:10:05.364238', '2026-09-18 19:06:06.183859', NULL),
(16, 'Генериране на Word тематично разпределение (Шаблон Тематично разпределение.docx)', 'course_lessons', 'Действай като старши методист и учител по професионална подготовка. Трябва да разработиш и оформиш официално годишно тематично разпределение по учебен предмет: \"{предмет}\" ({клас}, специалност/професия: {специалност}), точно съобразено със структурата на шаблона \"Шаблон Тематично разпределение.docx\".\n\n### 1. ВХОДНИ ДАННИ И КОНТЕКСТ:\n- Хорариум и седмици:\n{структура_часове}\n- Списък с разработените уроци и занятия:\n{списък_уроци}\n\n### 2. СТРУКТУРА НА WORD ДОКУМЕНТА (DOCX ШАБЛОН):\n1. Заглавна част:\n   Разпределение на темите\n   за учебната 2026/2027 г.\n   по учебен предмет „{предмет}“,\n   специалност код [код] „{специалност}“, {клас}\n\n2. Основна таблица с 3 колони:\n   - Колона 1: \"№\" (Пореден номер на урока: 1, 2, 3...)\n   - Колона 2: \"Наименование на темите\" – кратко заглавие на урока от предоставения списък с разработени уроци.\n   - Колона 3: \"Минимален брой часове\" – брой учебни часове за съответното занятие (напр. 2).\n\n3. Обобщаващи редове в края на таблицата (под колони 2 и 3):\n   - \"Общ минимален брой часове\": [сума от часовете за всички планирани уроци, напр. 68]\n   - \"Резерв часове\": [изчислен резерв от часове съобразно годишния хорариум, напр. 4]\n   - \"Общ брой часове\": [пълен хорариум по учебен план, напр. 72]\n\n4. Долна част:\n   Разработил : ....................................... / [Учител] /\n\n### 3. МЕТОДИЧЕСКИ ПРАВИЛА:\n1. Използвай точно подадения списък с разработени уроци ({списък_уроци}), като запазиш техните номера, наименования, часове и видове.\n2. Общият брой часове (минимален брой + резерв) трябва точно да съответства на годишния хорариум по учебния план.\n3. Обобщаващите суми в края на таблицата трябва да бъдат математически коректни.\n\n### 4. ФОРМАТ НА ИЗХОДА:\nПредостави резултата в следния формат, готов за директно копиране и поставяне в Word документа:\n\nРазпределение на темите\nза учебната 2026/2027 г.\nпо учебен предмет „{предмет}“,\nспециалност код [код] „{специалност}“, {клас}\n\n| № | Наименование на темите | Минимален брой часове |\n| --- | --- | --- |\n| 1 | ... | 2 |\n| ... | ... | ... |\n| | Общ минимален брой часове | [сума] |\n| | Резерв часове | [резерв] |\n| | Общ брой часове | [общо] |\n\nРазработил : ....................................... / [Учител] /', '1. Копирайте промпта чрез бутона „Копирай промпта“ (всички параметри се заместват автоматично с актуалните данни от страницата);\n2. Отворете вашия AI чат асистент (ChatGPT, Claude, Gemini, DeepSeek и др.);\n3. Поставете промпта и изпратете заявката;\n4. Копирайте генерираното съдържание и таблица и ги поставете в Word документа „Шаблон Тематично разпределение.docx“.', 1, 4, '2026-09-14 13:10:05.366597', '2026-09-18 18:40:29.355096', NULL),
(17, 'Анализ на учебна програма (МОН) и MoSCoW анализ (Python, Django, Vue.js, Bootstrap)', 'course_units', 'Действай като опитен методист и експерт по професионално образование и софтуерни технологии. Прикачвам официална учебна програма (утвърдена от МОН) за учебен предмет: \"{предмет}\" ({клас} клас, специалност/професия: {специалност}).\n\n### 1. ТЕХНОЛОГИЧЕН СТЕК В УЧИЛИЩЕТО:\nВажно методическо уточнение за профила на обучението:\n- Основен език за програмиране: Python;\n- Основни библиотеки и frameworks: Django (Backend / Web API), Vue.js (CDN версия за реактивен Frontend), Axios.js (HTTP заявки и REST комуникация), Bootstrap 5 (потребителски интерфейс и стилове).\n\n### 2. МЕТОДИКА ЗА АНАЛИЗ И ПРИОРИТИЗАЦИЯ (MoSCoW):\nМоля, анализирай учебното съдържание от приложения документ и направи детайлен MoSCoW (MSCW) анализ, като стриктно съобразиш приоритизацията с изучавания технологичен стек (Python, Django, Vue.js, Axios, Bootstrap) по следната методика:\n1. Извлечи всички раздели от програмата и посочи минималния им препоръчителен брой учебни часове (hours).\n2. За всеки раздел извлечи конкретните теми (topics) и определи за всяка тема нейната категория по MoSCoW, отчитайки избрания стек:\n   - \"M\" (Must / Задължителна) – Фундаментални концепции, базови синтактични основи и критични принципи, покриващи ДОС и директно приложими в стека Python / Django / Vue / Bootstrap;\n   - \"S\" (Should / Важна) – Важни теми, архитектурни модели и добри практики за практическо задълбочаване с Python, Django, Vue.js и REST интеграция;\n   - \"C\" (Could / Пожелателна) – Обогатяващи теми за напреднали ученици, допълнителни библиотеки, усъвършенствани компоненти и разширения;\n   - \"W\" (Won\'t / Отпадаща) – Тясно специализирани, несъвместими с избрания стек (напр. чужди за стека езици/технологии или остарели библиотеки) или детайли, които не са приоритет за този курс.\n3. За всяка тема посочи кратка и точна педагогическа обосновка (MoSCoW_rem) за избора на съответната категория, отразяваща връзката с изучавания технологичен стек.\n\n### 3. ФОРМАТ НА ИЗХОДА:\nВърни резултата ЕДИНСТВЕНО като валиден JSON масив (без излишен съпътстващ свободен текст), готов за директен импорт в приложението ИРИДА:\n[\n  {\n    \"num\": 1,\n    \"name\": \"Име на раздел 1\",\n    \"hours\": 10,\n    \"topics\": [\n      {\n        \"num\": 1,\n        \"name\": \"Име на тема 1.1\",\n        \"MoSCoW_cat\": \"M\",\n        \"MoSCoW_rem\": \"Основни концепции и базисен синтаксис в Python\"\n      },\n      {\n        \"num\": 2,\n        \"name\": \"Име на тема 1.2\",\n        \"MoSCoW_cat\": \"S\",\n        \"MoSCoW_rem\": \"Практическо приложение и интеграция с Django / Vue\"\n      }\n    ]\n  }\n]', '1. Копирайте промпта;\n2. Отворете външния си AI инструмент (ChatGPT, Claude, Gemini, DeepSeek и др.);\n3. Прикачете файла с учебната програма (DOCX/PDF от МОН);\n4. Поставете промпта и изпратете съобщението;\n5. Копирайте генерирания JSON код;\n6. Натиснете бутона „Импорт на програма“ до „Добави раздел“ на тази страница и поставете JSON кода (или качете записания файл) за автоматично зареждане.', 1, 3, '2026-09-15 15:14:30.972505', '2026-09-15 15:14:30.972530', NULL),
(18, 'Попълване на бланка за планиране на урок (ПГЕЕ / .docx шаблон)', 'lesson_main', 'Действай като старши преподавател и методист по професионална подготовка ({предмет}, специалност: {специалност}, {клас}). Трябва да попълниш официална педагогическа бланка за планиране на урок (план-конспект на занятие) по образец на ПГЕЕ за урок №{урок_номер}: \"{тема}\".\n\n### 1. ВХОДНИ ДАННИ ЗА УРОКА:\n- Предмет: {предмет}\n- Специалност / Професия: {специалност} ({клас})\n- Тема на урока: {тема}\n- Вид на занятието: {вид_урок}\n- Продължителност: {продължителност} ({продължителност_минути})\n- Включени теми от учебната програма:\n{включени_теми}\n- Очаквани резултати / Основни цели:\n{цели}\n- Акценти и фокус на урока:\n{фокус}\n- План / точки на занятието (ако има вече въведени):\n{точки}\n\n### 2. МЕТОДИЧЕСКИ ИЗИСКВАНИЯ КЪМ ПОПЪЛВАНЕТО НА БЛАНКАТА (СТАНДАРТ ЗА КАЧЕСТВО):\nПопълни детайлно и изчерпателно всеки един елемент от таблицата на бланката, съобразявайки се с дидактическия модел за преподаване и стандартите за качество на обучението:\n\n1. **Клас, Предмет, Тема, Продължителност:** Обобщи точно данните за урока (вкл. брой часове и минути).\n2. **Академични цели (знания и умения):** Формулирай ясни, измерими резултати според таксономията на Блум (Нива: Запомняне/Разбиране, Прилагане, Анализ/Създаване) и дефинирай ясен критерий за успех.\n3. **Социално-емоционални цели и оценяването им:** Формулирай конкретна социално-емоционална цел (работа в екип/по двойки, изслушване, аргументиране, устойчивост при отстраняване на грешки) и посочи конкретен начин/рубрика за нейното проследяване и оценяване в часа.\n4. **Необходими ресурси и материали:** Изброй конкретен списък с хардуерни, софтуерни и дидактически ресурси (компютърен кабинет, IDE/терминали, мултимедия, презентация, демо код, помощен лист/шпаргалка за подкрепа, онлайн документация).\n5. **ДЕЙНОСТИ:**\n   - Разпредели точно времето за дейностите спрямо продължителността **{продължителност_минути}** (напр. за 45 мин.: Начало 5 мин. + Същинска част 35 мин. + Край 5 мин.; за 90 мин.: Начало 10 мин. + Същинска част 70 мин. + Край 10 мин.).\n   - **Начало на часа (минути):**\n     * Организация и поздрав;\n     * Мотивационно въведение / реален практически казус от практиката и индустрията (Bridge-In кукичка);\n     * Свързване с предишни знания, обявяване на темата и очакваните резултати;\n     * **Правила за работа:** Формулирай 2–3 ясни правила за безопасна работа в лабораторията, ред за въпроси и конструктивна екипна среда.\n   - **Същинска част (минути) - Описание на дейностите по модела GRR (Gradual Release of Responsibility):**\n     * **1. Демонстрация и преподаване (Аз правя):** представяне на новите концепции/синтаксис, визуално обяснение, демонстрация на жив пример/код от учителя и връзка с реалния живот;\n     * **2. Ръководена п��актика и съвместна работа (Ние правим заедно):** съвместно решаване на задача/казус, въпроси за задълбочено мислене (по-високи нива на Блум) и разпределение на роли при работа по двойки (напр. Водещ/Навигатор);\n     * **3. Самостоятелна диференцирана работа (Ти правиш сам):** ясен алгоритъм/инструкции и **3 нива на диференциация**:\n       - *Ниво А (Базово):* изпълнение по стъпков образец / базово упражнение;\n       - *Ниво Б (Стандартно):* самостоятелна задача с прилагане и анализ;\n       - *Ниво В (Разширено / Предизвикателство):* творческа/изследователска задача или оптимизация за по-бързо напредващите;\n       - *Стратегия за подкрепа при затруднения (Scaffolding):* конкретни насоки и помощен алгоритъм при грешка/затруднение.\n   - **Обобщение:** Синтезиране на наученото в края на същинската част – изводи, ключови термини и кратка рефлексия.\n   - **Оценяване:** Критерии за оценка на напредъка, формираща обратна връзка и инструменти за **самооценка и взаимно оценяване** (напр. кратък чек-лист / критериална скала).\n   - **Край на часа (минути):** **Изходен билет (Exit Ticket)** с 2 въпроса (1 за проверка на разбирането и 1 за обратна връзка от учениците), диференцирана домашна работа и насоки за следващия урок.\n\n### 3. ФОРМАТ НА РЕЗУЛТАТА (ГОТОВ ЗА COPY/PASTE В \"Бланка урок ПГЕЕ.docx\"):\nГенерирай резултата във форматиран Markdown документ със заглавна част и **ЕДНА ЦЯЛОСТНА ТАБЛИЦА С 2 КОЛОНИ (`ЕЛЕМЕНТ` и `ОПИСАНИЕ`)**, която точно съответства на таблицата в бланката на ПГЕЕ, като всяка основна фаза и дейност е оформена в **отделен ред** на таблицата:\n\n# Бланка за планиране на урок\n**Име на учител:** [Поле за попълване на име]\n\n| ЕЛЕМЕНТ | ОПИСАНИЕ |\n| --- | --- |\n| **Клас: Предмет: Тема на урока: Продължителност:** | **Клас:** {клас}<br>**Предмет:** {предмет}<br>**Специалност:** {специалност}<br>**Тема на урока:** {тема}<br>**Вид на занятието:** {вид_урок}<br>**Продължителност:** {продължителност} ({продължителност_минути}) |\n| **Академични цели (знания и умения)**<br>- *Опишете какви знания и умения ще усвоят учениците по предмета и темата.* | - **Запомняне и разбиране:** ...<br>- **Прилагане:** ...<br>- **Анализ и създаване:** ...<br>- **Критерий за успех:** ... |\n| **Социално-емоционални цели**<br>- *Опишете какви социално-емоционални умения ще развиват и как се оценяват.* | - **Сътрудничество и екипни роли (напр. Водещ/Навигатор):** ...<br>- **Критично мислене, аргументация и изслушване:** ...<br>- **Устойчивост при грешки и увереност:** ...<br>- **Начин за оценяване на СЕО целта:** ... |\n| **Необходими ресурси и материали** | - Компютърен кабинет и софтуерни инструменти: ...<br>- Демо материали, презентация и конспект: ...<br>- Помощен лист за подкрепа (шпаргалка) и онлайн документация: ... |\n| **ДЕЙНОСТИ** | **Общо разпределение на времето:** Начало — [X] мин.; Същинска част — [Y] мин.; Край — [Z] мин. |\n| **Начало на часа — [X] мин.**<br>- *Поздрав, мотивация, цели и правила за работа.* | - **Организация и присъствие:** ...<br>- **Мотивация и кукичка (Bridge-In казус от практиката):** ...<br>- **Свързване с предишни знания:** ...<br>- **Обявяване на тема и очаквани резултати:** ...<br>- **Правила за поведение и работа в кабинета:** ... |\n| **Същинска част — 1. Демонстрация (Аз правя) — [A] мин.**<br>- *Преподаване, жив демо пример и визуално обяснение.* | - **Обяснение на концепциите и връзка с практиката:** ...<br>- **Демонстрация на жив пример / код от учителя:** ...<br>- **Ключови правила и насоки:** ... |\n| **Същинска част — 2. Ръководена практика (Ние правим заедно) — [B] мин.**<br>- *Съвместна работа, въпроси за мислене и роли.* | - **Съвместно решаване на задача/казус:** ...<br>- **Въпроси за задълбочено мислене (високи нива на Блум):** ...<br>- **Екипно взаимодействие и роли:** ... |\n| **Същинска част — 3. Самостоятелна диференцирана работа (Ти правиш сам) — [C] мин.**<br>- *Инструкции, задачи на 3 нива и подкрепа.* | - **Алгоритъм и инструкции за изпълнение:** ...<br>- **Ниво А (Базово):** ...<br>- **Ниво Б (Стандартно):** ...<br>- **Ниво В (Разширено / Предизвикателство):** ...<br>- **Стратегия за подкрепа при затруднения (Scaffolding):** ... |\n| **Обобщение**<br>- *Синтезиране на наученото и затвърждаване.* | - **Обобщаваща схема / ключови изводи:** ...<br>- **Рефлексия на учениците:** ... |\n| **Оценяване**<br>- *Критерии за успех, самооценка и обратна връзка.* | - **Критерии за успех (академични и СЕО):** ...<br>- **Чек-лист за самооценка / взаимна проверка по двойки:** ...<br>- **Формираща обратна връзка от учителя:** ... |\n| **Край на часа — [Z] мин.**<br>- *Изходен билет, обратна връзка и домашна работа.* | - **Изходен билет (Exit Ticket — 2 кратки въпроса):** ...<br>- **Диференцирана домашна работа:** ...<br>- **Насоки за следващия урок:** ... |\n\n*(Забележка: Не поставяй многоредови кодови блокове с тройни кавички вътре в клетките на таблицата, а форматирай кода с инлайн синтаксис напр. `код` или кратки редове с тире. Таблицата може директно да се копира и постави в \"Бланка урок ПГЕЕ.docx\" или да се експортира директно като .pdf и .docx файл).*', '1. Копирайте промпта (всички параметри на избрания урок са попълнени автоматично);\n2. Поставете го във вашия AI асистент (ChatGPT, Claude, Gemini, DeepSeek и др.);\n3. AI ще генерира готова попълнена бланка за урок с детайлна 2-колонна таблица по стандарта на ПГЕЕ с диференцирани задачи (Нива А/Б/В), СЕО цели, правила, помощен алгоритъм и изходен билет;\n4. Маркирайте и копирайте генерираната таблица, след което я поставете (Paste) в документа „Бланка урок ПГЕЕ.docx“ за да замените празната таблица, или запазете целия изход като нов Word (.docx) документ.', 1, 3, '2026-09-25 16:21:44.585215', '2026-09-25 20:54:29.096119', NULL);
INSERT INTO `main_aiprompt` (`id`, `title`, `page_key`, `prompt_text`, `instructions`, `is_system`, `order`, `created_at`, `updated_at`, `created_by_id`) VALUES
(19, 'Предварителна оценка на урок (Стандарт за качество / Оценъчна карта)', 'lesson_main', 'Действай като старши педагогически експерт, инспектор по качеството на образованието и методист по професионална подготовка ({предмет}, специалност: {специалност}, {клас}).\n\nТвоята задача е да извършиш независима предварителна експертна оценка на планирания урок №{урок_номер}: \"{тема}\" съгласно официалния **„Стандарт за качество на преподаване“ (Оценъчна карта)**, включващ точно 23 стандартизирани критерия.\n\n### 1. ВХОДНИ ДАННИ ЗА УРОКА ОТ СИСТЕМАТА:\n- Предмет: {предмет}\n- Специалност / Професия: {специалност} ({клас})\n- Тема на урока: {тема}\n- Вид на занятието: {вид_урок}\n- Продължителност: {продължителност} ({продължителност_минути})\n- Включени теми от учебната програма:\n{включени_теми}\n- Очаквани резултати / Основни цели:\n{цели}\n- Акценти и фокус на урока:\n{фокус}\n- Структура и точки от плана на занятието:\n{точки}\n\n### 2. ДЕТАЙЛЕН ПЛАН-КОНСПЕКТ / ПОПЪЛНЕНА БЛАНКА НА УРОКА:\n[Поставете тук съдържанието на попълнената „Бланка урок ПГЕЕ“ / генерирания Markdown план-конспект или прикачете съответния файл (.docx/.md/.pdf). Ако не е приложен допълнителен детайлен конспект, оцени урока въз основа на наличните базови данни и точки от плана в раздел 1].\n\n---\n\n### 3. ПРАВИЛА И МЕТОДИКА НА ОЦЕНЯВАНЕТО:\n1. **Хипотеза за стриктно изпълнение:** Приеми, че при реалното провеждане на урока предвиденият план се спазва стриктно и професионално.\n2. **Бинарно оценяване на всеки критерий:**\n   - Оцени всеки от 23-те критерия единствено с **„Да“** (1 точка) или **„Не“** (0 точки).\n   - Присъди **„Да“ (1 т.)**, само ако в предоставените материали и дейности има конкретно планирани дидактически стъпки, инструменти или формулировки, доказващи покриването на критерия.\n   - Присъди **„Не“ (0 т.)**, ако критерият липсва, не е изрично заложен или дейностите не са достатъчни за неговото постигане.\n3. **Аргументация и коментар:** За всеки критерий напиши стегнат, ясен и професионален коментар – посочи конкретната дейност от плана, която осигурява изпълнението, или какво точно липсва и как може да се доразвие.\n4. **Сумиране и процентна оценка:**\n   - Изчисли **Общ брой точки:** сума от точките (максимум 23 точки).\n   - Изчисли **Процент на съответствие:** `(Общ брой точки / 23) * 100%`.\n   - Определи ниво на методическа готовност: Отлична готовност (90-100%), Много добра (75-89%), Добра/Удовлетворителна (50-74%), Изисква преработване (<50%).\n5. **Следващи стъпки:** Формулирай точно **3 конкретни, практически и приложими препоръки** към учителя за надграждане и оптимизиране на урока.\n\n### 4. ФОРМАТ НА РЕЗУЛТАТА (ТАБЛИЦА СЪГЛАСНО \"оценъчна карта.docx\"):\nГенерирай оценката във форматиран Markdown документ с таблица за директно копиране или експортиране:\n\n# Оценъчна карта — Стандарт за качество на преподаване\n**Преподавател:** [Име на учител] | **Дата:** [Дата на оценка]\n**Предмет:** {предмет} | **Клас:** {клас} | **Тема:** {тема} | **Продължителност:** {продължителност}\n\n| № | Критерий | Оценка | Точки | Коментар и констатации |\n|---|---|:---:|:---:|---|\n| 1 | Целите за академичния напредък на учениците са ясно формулирани, конкретни и съобразени с възможностите и потребностите на учениците. | [Да/Не] | [1/0] | ... |\n| 2 | Социално-емоционалните цели са ясно формулирани, конкретни и съобразени с възможностите и потребностите на учениците. | [Да/Не] | [1/0] | ... |\n| 3 | Учебните дейности и използваните методи отговарят на изискванията на учебната програма и подпомагат постигането на целите на урока. | [Да/Не] | [1/0] | ... |\n| 4 | Времето в урока е разпределено рационално, така че всяка планирана дейност да се изпълни качествено и ефективно. | [Да/Не] | [1/0] | ... |\n| 5 | Планирани са начини за оценяване на академичната цел. | [Да/Не] | [1/0] | ... |\n| 6 | Планирани и реализирани са начини за оценяване на социално-емоционалната цел. | [Да/Не] | [1/0] | ... |\n| 7 | Учителят организира и провежда урочните дейности така, че да насърчава ангажираността и активното участие на учениците. | [Да/Не] | [1/0] | ... |\n| 8 | Учителят задава ясни правила за поведение и работа в класната стая. | [Да/Не] | [1/0] | ... |\n| 9 | Учителят формулира ясни инструкции и алгоритъм за работа при изпълнение на поставената задача. | [Да/Не] | [1/0] | ... |\n| 10 | Учителят демонстрира еднакво справедливо и уважително отношение към всички ученици, независимо от техния пол, етническа принадлежност или религия. | [Да/Не] | [1/0] | ... |\n| 11 | Учителят създава среда, в която учениците се чувстват значими, като им делегира права и отговорности, съответстващи на техните възможности и роля в учебния процес. | [Да/Не] | [1/0] | ... |\n| 12 | Учителят диференцира урочните дейности в съответствие с потребностите и възможностите на учениците, така че всеки да бъде ангажиран на оптимално ниво на предизвикателност. | [Да/Не] | [1/0] | ... |\n| 13 | Учителят създава условия учениците самостоятелно да достигат до решения, като ги насърчава да търсят помощ от съученици и налични ресурси. | [Да/Не] | [1/0] | ... |\n| 14 | Учителят създава условия учениците да предоставят обратна връзка и да изразяват мнение за структурата и съдържанието на урока. | [Да/Не] | [1/0] | ... |\n| 15 | Учителят създава завладяващи уроци, като прави връзка с приложение на новото знание в реалния живот. | [Да/Не] | [1/0] | ... |\n| 16 | Учителят създава условия за работа в екип и ефективно сътрудничество, като задава алгоритъм на работа и примерни роли за екипна работа. | [Да/Не] | [1/0] | ... |\n| 17 | Учителят предвижда дейности, които изискват от учениците задълбочено мислене (по високите нива на Блум). | [Да/Не] | [1/0] | ... |\n| 18 | Учителят развива умения и предоставя възможност за самооценка и взаимно оценяване по предварително зададени критерии. | [Да/Не] | [1/0] | ... |\n| 19 | Учителят представя и визуализира по ясен и разбираем начин новото знание, свързано с целите на урока. | [Да/Не] | [1/0] | ... |\n| 20 | Учителят използва различни похвати за обобщаване и затвърждаване на ключовото знание след задачите и в края на урока. | [Да/Не] | [1/0] | ... |\n| 21 | Учителят прилага разнообразни и подходящи средства за (формиращо) оценяване и проверка на разбирането на учениците. | [Да/Не] | [1/0] | ... |\n| 22 | Учителят използва поне една ефективна стратегия за обяснение при затруднения в разбирането. | [Да/Не] | [1/0] | ... |\n| 23 | Учителят предоставя обратна връзка на учениците по ясно определени и обсъдени с тях критерии за успех (напр. чрез чек-лист, критериална матрица и др.). | [Да/Не] | [1/0] | ... |\n\n### Резултати от оценяването:\n- **Общ брой точки:** [X] / 23 точки\n- **Степен на покритие на стандарта:** [Y]%\n- **Ниво на методическа готовност:** [Отлична / Много добра / Добра / За доработване]\n\n### Следващи стъпки:\n| № | Препоръка за оптимизация и надграждане |\n|---|---|\n| 1 | [Първа конкретна насока за подобряване] |\n| 2 | [Втора конкретна насока за подобряване] |\n| 3 | [Трета конкретна насока за подобряване] |', '1. Копирайте промпта (всички параметри на избрания урок са попълнени автоматично);\n2. Поставете го във вашия AI асистент (ChatGPT, Claude, Gemini и др.);\n3. (Препоръчително) В раздел 2 на промпта поставете генерирания план-конспект / бланка на урока (или прикачете файла), за да получи максимално точна и пълна оценка по всички 23 критерия;\n4. AI ще анализира ��рока, ще оцени всеки критерий с Да (1 т.) / Не (0 т.), ще сумира точките, ще пресметне процентното покритие и ще предложи 3 конкретни следващи стъпки за усъвършенстване.', 1, 7, '2026-09-25 19:34:15.249167', '2026-09-25 19:34:15.249190', NULL),
(20, 'Критериална матрица, чек-лист за самооценка и изходен билет (Exit Ticket)', 'lesson_main', 'Действай като експерт по формиращо оценяване и методист по професионална подготовка ({предмет}, специалност: {специалност}, {клас}).\n\nЗа урок №{урок_номер}: \"{тема}\" (вид: {вид_урок}, продължителност: {продължителност_минути}), състави цялостен дидактически комплект от 3 инструмента за формиращо оценяване, взаимна проверка и обратна връзка:\n\n### 1. ВХОДЕН КОНТЕКСТ НА УРОКА:\n- Предмет: {предмет} ({клас}, {специалност})\n- Тема на урока: {тема} (Вид: {вид_урок})\n- Очаквани академични цели / резултати:\n{цели}\n- Фокус и акценти:\n{фокус}\n- Основни точки от плана:\n{точки}\n\n---\n\n### 2. ИЗИСКВАНИЯ КЪМ СЪДЪРЖАНИЕТО НА КОМПЛЕКТА:\n\n#### Инструмент 1: ЧЕК-ЛИСТ ЗА САМООЦЕНКА НА УЧЕНИКА (Student Self-Assessment)\n- Формулирай **3 до 4 ясни, конкретни и измерими твърдения** в 1-во лице единствено число (напр. *„Мога да дефинирам и обясня...“*, *„Успях самостоятелно да изпълня/напиша...“*, *„Мога да открия и коригирам грешка в...“*), съответстващи на заложените цели.\n- Оформи ги в прегледна таблица с три колони за самопроверка:\n  1. *„Справям се уверено (Зелено)“*\n  2. *„Нуждая се от още упражнения (Жълто)“*\n  3. *„Имам въпрос към учителя (Червено)“*\n- Добави поле за лична цел/записка на ученика: *„Какво успях да науча днес най-добре“*.\n\n#### Инструмент 2: КРИТЕРИАЛНА МАТРИЦА (РУБРИКА) ЗА ВЗАИМНА ПРОВЕРКА ПО ДВОЙКИ (Peer Review)\n- Дефинирай **3 конкретни критерия за оценка** на практическата работа в часа:\n  1. *Коректност и функционалност на решението/кода;*\n  2. *Спазване на синтаксис, структура и добри практики;*\n  3. *Умение за аргументация и обяснение на резултата пред съученика.*\n- Разпиши **3 нива на изпълнение** за всеки критерий:\n  - *Ниво 3 (Отлично / 3 т.):* Без грешки, отлично разбиране и структуриране;\n  - *Ниво 2 (Добро / 2 т.):* Работещо решение с малки неточности или нужда от минимална помощ;\n  - *Ниво 1 (Нужда от подобрение / 1 т.):* Непълно решение или съществени пропуски.\n- Добави протокол за партньорска обратна връзка по модела **\"TAG\"**:\n  - **T (Tell):** Кажи едно нещо, което съученикът ти е направил отлично;\n  - **A (Ask):** Задай един въпрос относно решението;\n  - **G (Give):** Дай един конкретен съвет за подобрение.\n\n#### Инструмент 3: ИЗХОДЕН БИЛЕТ (EXIT TICKET — КРАЙ НА ЧАСА, 3–5 МИН.)\n- Подготви 2 стегнати въпроса за попълване в края на занятието:\n  - **Въпрос 1 (Концептуална проверка):** Кратък въпрос или мини-казус по същество за проверка на ключовото ново понятие от темата \"{тема}\".\n  - **Въпрос 2 (Рефлексия и обратна връзка):** Въпрос за личния напредък и затрудненията (напр. *„Коя част от днешните задачи ти беше най-лесна и коя те затрудни най-много?“* или *„Какво би искал да упражним отново следващия час?“*).\n\n---\n\n### 3. ФОРМАТ НА РЕЗУЛТАТА:\nГенерирай резултата като форматиран Markdown документ с прегледни таблици и ясни раздели, готов за разпечатване на хартиен носител, експортиране като .docx/.pdf или споделяне в електронната платформа.', '1. Копирайте промпта (всички параметри на избрания урок са попълнени автоматично);\n2. Поставете го във вашия AI асистент (ChatGPT, Claude, Gemini и др.);\n3. AI ще генерира готов комплект от 3 инструмента за формиращо оценяване: чек-лист за самооценка, рубрика за взаимна проверка по двойки и изходен билет (покрива критерии № 14, 18, 23 от стандарта за качество);\n4. Разпечатайте материалите или ги качете като приложение (работен лист) към урока.', 1, 4, '2026-09-25 21:14:57.003943', '2026-09-25 21:14:57.003975', NULL),
(21, 'Диференцирани работни карти и карти за подкрепа при затруднения (Scaffolding)', 'lesson_main', 'Действай като старши преподавател по професионална подготовка и експерт по диференцирано преподаване ({предмет}, {специалност}, {клас}).\n\nЗа урок №{урок_номер}: \"{тема}\" (вид: {вид_урок}, продължителност: {продължителност_минути}), разработи пълен диференциран работен лист с практически задачи на 3 нива на трудност и методическа карта за подкрепа при затруднения (Scaffolding):\n\n### 1. ВХОДЕН КОНТЕКСТ НА УРОКА:\n- Предмет: {предмет} ({клас}, {специалност})\n- Тема на урока: {тема}\n- Очаквани резултати и цели:\n{цели}\n- Фокус и акценти:\n{фокус}\n- Учебна програма / теми:\n{включени_теми}\n- План на занятието:\n{точки}\n\n---\n\n### 2. СТРУКТУРА НА ДИФЕРЕНЦИРАНИЯ РАБОТЕН ЛИСТ:\n\n#### Част 1: ПРАКТИЧЕСКИ ЗАДАЧИ НА 3 НИВА (СЪОБРАЗЕНИ С ТАКСОНОМИЯТА НА БЛУМ)\n\n1. **НИВО А — БАЗОВО (Запомняне и Разбиране / Guided Practice):**\n   - *Целева група:* Ученици, които усвояват основните концепции или се нуждаят от начална увереност.\n   - *Формат:* Стъпкова задача с попълване на липсващи елементи (Fill-in-the-blank / Parson’s problem) или модифициране на готов работещ демо образец.\n   - *Изискване:* Ясни попътни указания и гарантиран бърз успех при изпълнение.\n\n2. **НИВО Б — СТАНДАРТНО (Прилагане и Анализ / Independent Application):**\n   - *Целева група:* Основната част от класа, покриваща държавните образователни стандарти.\n   - *Формат:* Самостоятелна практическа задача за цялостна реализация на функционалност/казус по темата \"{тема}\".\n   - *Изискване:* Ученикът сам проектира и реализира решението, анализира получените резултати и тества за коректност.\n\n3. **НИВО В — РАЗШИРЕНО / ПРЕДИЗВИКАТЕЛСТВО (Оценка и Създаване / Advanced Challenge):**\n   - *Целева група:* Бързо напредващи ученици с повишен интерес и изявени възможности.\n   - *Формат:* Творческа задача, добавяне на разширена функционалност, оптимизация на код/алгоритъм, симулиране на гранични условия или отстраняване на сложен казус (Troubleshooting/Edge Cases).\n   - *Изискване:* Изисква задълбочено мислене, изследователски подход и самостоятелно търсене на решения.\n\n---\n\n#### Част 2: КАРТА ЗА ПОДКРЕПА ПРИ ЗАТРУДНЕНИЯ (SCAFFOLDING & TROUBLESHOOTING GUIDE)\n*Оформи раздел „Ако се затрудняваш – погледни тук!“, съдържащ:*\n\n1. **Алгоритъм за справяне със затруднение в 3 стъпки (Three Before Me):**\n   - *Стъпка 1:* Прочети внимателно съобщението за грешка/условието и прегледай кода ред по ред.\n   - *Стъпка 2:* Направи справка с помощната шпаргалка и демо примера от презентацията.\n   - *Стъпка 3:* Консултирай се с навигатора/съученика до теб и обсъдете проблема, преди да потърсите намеса от учителя.\n2. **Синтактична шпаргалка / Cheat-Sheet:**\n   - 3–4 най-важни синтактични правила, команди или структури за днешната тема.\n3. **Топ 3 най-чести грешки и как да ги поправим:**\n   - Описание на типични грешки (напр. синтактични, логически, грешни параметри) и точното им решение.\n4. **Насочващи въпроси за саморефлексия:**\n   - 2 въпроса, които помагат на ученика сам да открие пропуснатото действие.\n\n---\n\n### 3. ФОРМАТ НА РЕЗУЛТАТА:\nГенерирай чист, четим Markdown документ с форматирани кодови примери, инструкции и обособени секции за всяко ниво, готов за незабавно използване в час или експорт към .docx / .pdf.', '1. Копирайте промпта (всички параметри на избрания урок са попълнени автоматично);\n2. Поставете го във вашия AI асистент (ChatGPT, Claude, Gemini и др.);\n3. AI ще генерира структуриран работен лист с диференцирани практически задачи на 3 нива (А/Б/В) и подробна карта за подкрепа при затруднения с алгоритъм за дебъгване (покрива критерии № 9, 12, 13, 22 от стандарта за качество);\n4. Използвайте го за директна работа с учениците в компютърния кабинет.', 1, 5, '2026-09-25 21:14:57.006851', '2026-09-25 21:14:57.006875', NULL),
(22, 'Социално-емоционални цели, екипни роли и правила за лабораторно занятие', 'lesson_main', 'Действай като педагогически съветник, методист и водещ преподавател по {предмет} за {клас} ({специалност}).\n\nЗа урок №{урок_номер}: \"{тема}\" (вид: {вид_урок}, продължителност: {продължителност_минути}), изготви цялостна методическа рамка за изграждане на безопасна, приобщаваща, организирана и емоционално подкрепяща среда в компютърната лаборатория:\n\n### 1. ВХОДЕН КОНТЕКСТ НА УРОКА:\n- Предмет: {предмет} ({клас}, {специалност})\n- Тема на урока: {тема} (Вид: {вид_урок})\n- Основни академични цели:\n{цели}\n- Фокус на занятието:\n{фокус}\n- План и дейности:\n{точки}\n\n---\n\n### 2. СЪСТАВНИ ЕЛЕМЕНТИ НА МЕТОДИЧЕСКАТА РАМКА:\n\n#### 1. СОЦИАЛНО-ЕМОЦИОНАЛНИ ЦЕЛИ (СЕО) И МЕТОДИКА ЗА ОЦЕНЯВАНЕТО ИМ\n- **Формулировка на 2 ключови СЕО цели:**\n  * *Цел 1 (Сътрудничество и комуникация):* Учениците развиват умения за активно изслушване, споделяне на отговорността и конструктивно обсъждане на идеи при работа по двойки.\n  * *Цел 2 (Устойчивост и преодоляване на фрустрация):* Учениците демонстрират спокойствие и упоритост при откриване на грешки в кода/задачите, като разглеждат грешката като естествена стъпка в ученето.\n- **Инструмент за оценяване на СЕО целите:**\n  * Дефинирай кратка 3-степенна скала за формиращо наблюдение от учителя (Наблюдава се регулярно / В процес на изграждане / Изисква насочване) с конкретни поведенчески индикатори.\n\n#### 2. ПРАВИЛА ЗА БЕЗОПАСНА И ПРОДУКТИВНА РАБОТА В КОМПЮТЪРНАТА ЛАБОРАТОРИЯ\n- Формулирай точно **3 кратки, позитивни и ясни правила за поведение и ред**, които учителят въвежда в началото на часа:\n  1. *Безопасност и грижа за оборудването (хардуер, мрежа, електричество);*\n  2. *Ред за въпроси и тишина при концентрация (сигнали за помощ, уважение към говорещия);*\n  3. *Равнопоставеност и взаимно уважение (толерантност към всички съученици без оглед на темпото или опита).*\n\n#### 3. МОДЕЛ ЗА РАБОТА ПО ДВОЙКИ (PAIR PROGRAMMING) И РАЗПРЕДЕЛЕНИЕ НА РОЛИ\n- Разпредели ролите за практическата част на урока:\n  - **Роля 1: „Водещ програмист / Изпълнител (Driver)“** — управлява клавиатурата/мишката, пише кода/командите, фокусира се върху синтактичната точност и изпълнението на текущата стъпка.\n  - **Роля 2: „Навигатор / Анализатор (Navigator)“** — следи общата логика и алгоритъма, проверява за пропуски и грешки, прави справка с документацията и направлява посоката.\n- **Инструкция за смяна на ролите (Switch Roles):**\n  * Задай точен момент за размяна (напр. на средата на практическата част / след завършване на всяка задача), така че всеки ученик да упражни и двете роли.\n\n#### 4. ПРОТОКОЛ ЗА ЕКИПНА ОБРАТНА ВРЪЗКА И ПОДКРЕПА\n- Разпиши правила за взаимопомощ между съседните екипи, насърчаващи автономността на учениците и споделеното учене.\n\n---\n\n### 3. ФОРМАТ НА РЕЗУЛТАТА:\nГенерирай прегледен Markdown документ с таблици за СЕО рубриката и ролите, готов за включване в методическата документация на урока, за разпечатване на постери в кабинета или за раздаване на учениците.', '1. Копирайте промпта (всички параметри на избрания урок са попълнени автоматично);\n2. Поставете го във вашия AI асистент (ChatGPT, Claude, Gemini и др.);\n3. AI ще разработи социално-емоционални цели с рубрика за оценяване, правила за кабинета и разпределение на роли при работа по двойки (покрива критерии № 2, 6, 8, 10, 11, 16 от стандарта за качество);\n4. Използвайте генерирания протокол за организация на учебната среда и екипната работа.', 1, 6, '2026-09-25 21:14:57.009358', '2026-09-25 21:14:57.009381', NULL);

-- --------------------------------------------------------

--
-- Структура на таблица `main_appattachment`
--

CREATE TABLE `main_appattachment` (
  `id` bigint(20) NOT NULL,
  `num` smallint(6) NOT NULL,
  `name` varchar(200) NOT NULL,
  `file` varchar(100) DEFAULT NULL,
  `description` longtext NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `updated_at` datetime(6) DEFAULT NULL,
  `created_by_id` int(11) DEFAULT NULL,
  `is_system` tinyint(1) NOT NULL,
  `original_filename` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Схема на данните от таблица `main_appattachment`
--

INSERT INTO `main_appattachment` (`id`, `num`, `name`, `file`, `description`, `created_at`, `updated_at`, `created_by_id`, `is_system`, `original_filename`) VALUES
(3, 2, 'Test PDF edited', 'app_attachments/test.pdf', 'Updated', '2026-09-17 21:24:20.768038', '2026-09-21 20:40:12.024493', NULL, 1, ''),
(4, 1, 'Test txt', 'app_attachments/test.txt', '', '2026-09-17 21:24:20.772853', '2026-09-21 20:39:45.955769', NULL, 1, ''),
(5, 1, 'Test MD original', 'app_attachments/tmp.md', '', '2026-09-17 21:24:20.777456', '2026-09-21 20:39:56.066066', NULL, 1, ''),
(8, 3, 'ИнтернетПрограмиране_ПП_теория_lesson_plan_1.json', 'app_attachments/c25b8ef298da4b7db1df51a91d5bc905.json', '', '2026-09-21 20:19:59.135533', '2026-09-21 20:40:30.780170', 3, 0, ''),
(9, 4, 'Урок 1 - Въведение в алчните алгоритми.docx', 'app_attachments/706d9846b6034be0b27a8d08fc702d14.docx', '', '2026-09-21 20:28:00.373325', '2026-09-21 20:28:00.373345', 1, 0, ''),
(10, 5, 'Учебен материал.docx', 'app_attachments/21ebafd09f774addbdd436d548093247.docx', '', '2026-09-22 08:41:20.687624', '2026-09-22 08:41:20.687646', 1, 0, 'Учебен материал.docx');

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
-- Структура на таблица `main_goal`
--

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
(3, 1, 'Придобиване на знания, свързани с изпълнението на програма', 4),
(4, 2, 'Придобиване на знания и разбирания за същността на термина „процес”', 4),
(5, 3, 'Разбиране на термина „блокираща операция” и влиянието на блокиращите операции върху процеса', 4),
(6, 4, 'Разбиране на термина „нишка”', 4),
(7, 5, 'Познаване на особеностите на многонишковото програмиране и правилното управление на нишките', 4),
(8, 6, 'Разбиране на проблемите и решенията при разработване на сървър за „клиент-сървър” приложения', 4),
(9, 7, 'Разбиране на проблемите и решенията при разработване на приложения с графичен потребителски интерфейс', 4),
(10, 8, 'Разбиране на връзката нишка - процес - брой на процесори в системата', 4),
(11, 9, 'Разбиране на проблемите при използване на нишки и техните решения - Race conditions, Deadlocks, Livelocks, Starvation', 4),
(12, 10, 'Познаване на начина за асинхронизиране на блокиращи операции', 4),
(13, 11, 'Познаване и разбиране на концепцията за синхронизация и заключване', 4),
(14, 1, 'цел 1', 5),
(15, 1, 'Описва и обяснява същността на Интернет, мрежовите протоколи, модела „клиент-сървър“ и видовете HTTP заявки', 1),
(16, 2, 'Разпознава архитектурния модел MVC, принципите на REST комуникацията и механизмите за управление на сесии и сигурност', 1),
(17, 3, 'Разработва адаптивен и семантично коректен потребителски интерфейс чрез HTML, CSS и динамично манипулиране на DOM с JavaScript', 1),
(18, 4, 'Изгражда функционални сървърни компоненти с реализация на CRUD операции чрез директна връзка или ORM система към база данни', 1),
(19, 5, 'Анализира и тества мрежовия трафик, HTTP заявките и клиентския код чрез инструментите за разработчици в уеб браузъра', 1),
(20, 6, 'Проектира и реализира собствени REST API услуги и осъществява тяхното асинхронно консумиране от клиентската част', 1),
(21, 7, 'Интегрира цялостни уеб приложения с автентикация, авторизация и защита срещу често срещани уязвимости в уеб среда', 1);

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
-- Структура на таблица `main_schooldayconfig`
--

CREATE TABLE `main_schooldayconfig` (
  `id` bigint(20) NOT NULL,
  `school_day_start` varchar(5) NOT NULL,
  `school_lessons_count` smallint(5) UNSIGNED NOT NULL CHECK (`school_lessons_count` >= 0),
  `lesson_duration_minutes` smallint(5) UNSIGNED NOT NULL CHECK (`lesson_duration_minutes` >= 0),
  `first_break_duration_minutes` smallint(5) UNSIGNED NOT NULL CHECK (`first_break_duration_minutes` >= 0),
  `regular_break_duration_minutes` smallint(5) UNSIGNED NOT NULL CHECK (`regular_break_duration_minutes` >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Схема на данните от таблица `main_schooldayconfig`
--

INSERT INTO `main_schooldayconfig` (`id`, `school_day_start`, `school_lessons_count`, `lesson_duration_minutes`, `first_break_duration_minutes`, `regular_break_duration_minutes`) VALUES
(1, '00:00', 7, 45, 20, 10);

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
-- Структура на таблица `main_session`
--

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
  `collapsed` tinyint(1) NOT NULL,
  `social_emotional_goals` longtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Схема на данните от таблица `main_session`
--

INSERT INTO `main_session` (`id`, `num`, `name`, `focus`, `goals`, `duration`, `course_id`, `basic_level`, `session_type`, `collapsed`, `social_emotional_goals`) VALUES
(4, 1, 'ПП УП ИП 1', 'Организационен старт на практиката по Разработка на софтуер, 11 клас: групиране на учениците в екипи от учителя; разпределяне и разчитане на проектните задания; договаряне на начални роли и правила за сътрудничество; определяне на реалистичен обхват и първи задачи. Вид на занятието: упражнение. Продължителност: 90 минути учебна работа.', '1. Участва в сформиран от учителя работен екип, назовава своята начална роля и поне две свързани отговорности; 2. Анализира полученото проектно задание, определя целевия потребител и формулира целта на проекта; 3. Разграничава задължителните функционалности, ограниченията и дейностите извън обхвата на първата версия; 4. Разбива заданието на начални задачи с отговорник, очакван резултат и проверим критерий за приемане.', 1, 2, 1, 'НЗ', 1, ''),
(5, 1, 'Въведение в конкурентността. Разлика между последователно (серийно), конкурентно и паралелно изпълнение. Аналогии от реалния живот.', '', '', 1, 4, 1, 'НЗ', 1, ''),
(6, 2, 'Процеси. Какво е процес в операционната система. Спецификата на Python: Въведение в концепцията за GIL (Global Interpreter Lock) и защо Python използва multiprocessing за тежки математически задачи.', '', '', 1, 4, 1, 'НЗ', 1, ''),
(7, 3, 'Блокиращи операции. Същност и класификация на задачите: CPU-bound (натоварващи процесора) срещу I/O-bound (чакащи мрежа/диск).', '', '', 1, 4, 1, 'НЗ', 1, ''),
(8, 5, 'Същност на нишките (Threads). Разлика между процес и нишка (памет, ресурси, бързина на създаване).', '', 'В края на часа учениците трябва да знаят:\n\nДа дефинират какво е \"нишка\" (Thread) в контекста на операционната система.\nДа обяснят критичната разлика между процес и нишка, най-вече по отношение на паметта.\nДа могат аргументирано да изберат кога архитектурно е по-подходящо да ползват нишка вместо процес.', 1, 4, 1, 'НЗ', 0, ''),
(9, 4, 'Проблемът със \"замръзващите\" програми. Демонстрация на синхронен код, който блокира (напр. чакане на отговор от уеб сървър). Постановка на проблема, който ще решаваме в следващите раздели.', '', '', 1, 4, 1, 'НЗ', 1, ''),
(10, 6, 'Жизнен цикъл и създаване. Как се ражда и умира една нишка. Синтактичен преглед на модула threading в Python (Main thread срещу Worker threads).', 'жизнен цикъл на нишката;  синтаксис за създаването ѝ в Python', 'В края на часа учениците трябва да могат да:\n\nОписват трите основни състояния в жизнения цикъл на нишката (Нова, Работеща, Мъртва).\nОбясняват предназначението на параметрите target и args при създаване на обект от тип threading.Thread.\nРазпознават често срещани синтактични и логически грешки при стартиране на нишки.', 1, 4, 1, 'НЗ', 0, ''),
(11, 7, 'Управление на изпълнението. Методи за синхронизиране на основната програма с работните нишки (концепцията зад .start() и .join()).', '', '', 1, 4, 1, 'НЗ', 1, ''),
(12, 8, 'Споделена памет. Разбиране на факта, че всички нишки в един процес \"виждат\" едни и същи глобални променливи. Предимства и рискове.', '', '', 1, 4, 1, 'НЗ', 1, ''),
(13, 9, 'Race conditions (Състезателни състояния). Какво се случва, когато две нишки се опитат да променят една променлива едновременно. Анализ на класическия проблем с брояча.', '', '', 1, 4, 1, 'НЗ', 1, ''),
(14, 10, 'Deadlocks (Мъртва схватка). Как решаването на един проблем създава друг. Архитектурен анализ на ситуация, в която две нишки се чакат вечно една друга.', '', '', 1, 4, 1, 'НЗ', 1, ''),
(15, 11, 'Синхронизация и защита. Концепцията за критична секция и заключване на ресурси. Как работи Lock (Mutex) и защо предпазва от Race conditions.', '', '', 1, 4, 1, 'НЗ', 1, ''),
(16, 12, 'Разширени проблеми (Livelocks и Starvation). Информативен преглед на състоянията, при които системата работи, но не върши полезна работа или \"оставя гладна\" конкретна нишка.', '', '', 1, 4, 1, 'НЗ', 1, ''),
(17, 13, 'Въведение в асинхронността. Обещания (Futures) и концепцията за Event Loop (Цикъл на събитията). Как един сервитьор може да обслужва 10 маси едновременно.', '', '', 1, 4, 1, 'НЗ', 1, ''),
(18, 14, 'Обратни извиквания (Callbacks). Историческият подход. Анализ на структурата на кода и проблемът с нечетимостта (\"Callback hell\").', '', '', 1, 4, 1, 'НЗ', 1, ''),
(19, 15, 'Модерният стандарт: Корутини. Синтаксисът async и await в Python. Разлика между обикновена функция и корутина.', '', '', 1, 4, 1, 'НЗ', 1, ''),
(20, 16, 'Архитектура с asyncio. Кога да използваме asyncio и кога threading? Сравнителен анализ на подходите преди учениците да ги приложат в практиката.', '', '', 1, 4, 1, 'НЗ', 1, ''),
(21, 1, 'Основи на Интернет и мрежовите протоколи. Протоколът HTTP', 'Фундаментални понятия за Интернет, мрежова комуникация, TCP/IP стек и анатомия на съобщенията в HTTP протокола.', '1. Обяснява принципите на мрежовата комуникация в Интернет, ролята на IP адресацията, DNS системата и нивата в модела TCP/IP;\n2. Анализира синтаксиса и структурата на текстовия протокол HTTP (Start-line, Headers, Body) и описва жизнения цикъл на заявка-отговор (Request-Response Lifecycle);\n3. Изследва и ръчно симулира HTTP заявки и отговори чрез мрежови инструменти (cURL / Telnet / Браузър DevTools).', 2, 1, 1, 'НЗ', 1, ''),
(22, 2, 'Видове HTTP заявки и методи за обмен на ресурси', 'HTTP методи за манипулиране на данни, статус кодове на отговорите и структура на HTTP заглавките.', '1. Различава основните HTTP методи (GET, POST, PUT, DELETE, PATCH);\n2. Анализира HTTP статус кодовете и предназначението на заглавните части (headers).', 2, 1, 1, 'НЗ', 1, ''),
(23, 3, 'Архитектурен модел „Клиент - сървър” и уеб комуникация', 'Разпределени системи, роля на потребителския агент, обработка на заявките на сървъра и рендиране.', '1. Описва ролите и взаимодействията между клиент, уеб сървър и сървър за бази данни;\n2. Проследява пътя на заявката от въвеждане на URL до визуализиране в браузъра.', 2, 1, 1, 'K', 1, ''),
(24, 4, 'Основи на HTML: Структура на документа и базови тагове', 'Скелет на HTML5 страница, метаданни, текстова йерархия и организиране на съдържанието.', '1. Изгражда валидна синтактична структура на HTML5 документ;\n2. Прилага текстови тагове, списъци, таблици и хипервръзки.', 2, 1, 1, 'НЗ', 1, ''),
(25, 5, 'Стилизиране с CSS: Селектори, каскадност и боксов модел', 'Свързване на стилове, каскадност, специфичност на селекторите и боксов модел на елементите.', '1. Дефинира и комбинира CSS селектори по таг, клас, идентификатор и атрибут;\n2. Прилага CSS Box Model (margin, border, padding, content) за позициониране на елементи.', 2, 1, 1, 'НЗ', 1, ''),
(26, 6, 'Диагностика и дебъгване с Developer Tools в уеб браузъра', 'Практическа работа с Elements, Console и Network панелите за диагностика и анализ.', '1. Инспектира и модифицира в реално време HTML елементи и приложени CSS стилове;\n2. Анализира мрежовия трафик и HTTP заявките през панела Network.', 2, 1, 0, 'УПР', 1, ''),
(27, 7, 'Създаване и валидиране на уеб формуляри', 'Елементи на уеб формата, типове входни полета, атрибути за валидация и подготовка на данни за изпращане.', '1. Проектира HTML формуляри с разнообразни входни полета (input, select, textarea);\n2. Конфигурира атрибутите action и method за изпращане на данни и прилага клиентска валидация.', 2, 1, 1, 'НЗ', 1, ''),
(28, 8, 'Семантична структура и уеб достъпност (Accessibility)', 'Семантичен уеб, подобряване на четимостта на кода, оптимизация за търсещи машини (SEO) и екранни четци.', '1. Изгражда структура на уеб страница чрез семантични тагове (header, nav, main, article, section, footer);\n2. Прилага стандарти за уеб достъпност (ARIA роли, алтернативни текстове).', 2, 1, 0, 'УПР', 1, ''),
(29, 9, 'Адаптивен уеб дизайн: Flexbox, CSS Grid и Media Queries', 'Принципи на Responsive Web Design (Mobile-First), еластични контейнери и точки на пречупване (breakpoints).', '1. Проектира гъвкави оформления чрез Flexbox и CSS Grid системи;\n2. Създава мобилно-адаптивни изгледи с помощта на CSS Media Queries.', 2, 1, 0, 'НЗ', 1, ''),
(30, 10, 'Практическо изграждане на адаптивен потребителски интерфейс', 'Комбиниране на семантичен HTML и адаптивен CSS за завършен front-end компонент.', '1. Реализира цялостна адаптивна целева страница (Landing Page);\n2. Тества поведението на интерфейса при различни размери на екрана през браузърните емулатори.', 2, 1, 0, 'УПР', 1, ''),
(31, 11, 'Увод в JavaScript: Синтаксис, типове данни, обекти и функции', 'Основи на JavaScript синтаксиса, обхват на променливите, структури от данни и функционална декомпозиция.', '1. Прилага променливи (let, const), базови типове данни и управляващи конструкции в JavaScript;\n2. Дефинира и извиква функции и борави с литерали на JavaScript обекти.', 2, 1, 1, 'НЗ', 1, ''),
(32, 12, 'Обектен модел на документа (DOM) и обработка на събития', 'Дървовидна структура на DOM, промяна на съдържание и атрибути, прехващане и обработка на потребителски събития.', '1. Достъпва и манипулира DOM елементи чрез методи за селекция (querySelector, getElementById);\n2. Регистрира слушатели за събития (addEventListener) и управлява реакцията на клик, вход и промяна.', 2, 1, 1, 'НЗ', 1, ''),
(33, 13, 'Динамично манипулиране на DOM и валидация на форми с JavaScript', 'Практическа манипулация на стилове и класове чрез JS, спиране на събития по подразбиране и интерактивен интерфейс.', '1. Създава, променя и премахва елементи в DOM дървото програмно;\n2. Реализира динамична проверка на входни данни във формуляр преди изпращане.', 2, 1, 0, 'УПР', 1, ''),
(34, 14, 'Практическо обобщение: Изграждане на интерактивен клиентски модул', 'Систематизиране на знанията за front-end разработка чрез изграждане на динамичен компонент.', '1. Интегрира семантичен HTML, адаптивен CSS и интерактивен JavaScript в завършен SPA компонент;\n2. Открива и коригира грешки в клиентския код чрез инструментите за разработка.', 2, 1, 1, 'ОС', 1, ''),
(35, 15, 'Контролна работа: Проектиране и разработка на Front-end интерфейс', 'Оценка на усвоените компетентности от Раздел 1 и Раздел 2 чрез теоретичен тест и практическа задача.', '1. Демонстрира теоретични знания за протоколите и клиентските уеб технологии;\n2. Изгражда самостоятелно валидна, стилизирана и интерактивна уеб форма по зададено техническо задание.', 2, 1, 1, 'ПК', 1, ''),
(36, 16, 'Въведение в сървърната разработка и MVC архитектурния модел', 'Концепция за разделяне на отговорностите (SoC), роля на модела, изгледа и контролера в сървърна среда.', '1. Разпознава компонентите и ролите в модела Model-View-Controller;\n2. Проследява маршрутизирането на HTTP заявки към контролери и действия (actions).', 2, 1, 1, 'НЗ', 1, ''),
(37, 17, 'Директна комуникация с релационни бази данни в уеб приложение', 'Управление на връзките към БД (Connection pooling), подготовка на заявки (Prepared Statements) и предотвратяване на SQL инжекции.', '1. Установява защитена връзка от сървърния код към релационна база данни;\n2. Изпълнява параметризирани SQL заявки за четене и запис на данни.', 2, 1, 1, 'НЗ', 1, ''),
(38, 18, 'Обектно-релационно съпоставяне (ORM): Моделиране на данни', 'Принципи на ORM слоя, мапване на таблици към класове, конфигурация на първични и външни ключове.', '1. Дефинира същности (entities) и релации между тях чрез ORM библиотека/рамка;\n2. Извършва миграции на базата данни и управлява схемата чрез код.', 2, 1, 0, 'НЗ', 1, ''),
(39, 19, 'Реализиране на CRUD операции: Създаване и визуализиране на ресурси', 'Обработка на входящи HTTP POST данни, валидация на сървърно ниво и визуализиране на списъци.', '1. Проектира сървърни контролери за създаване (Create) на нов запис в БД;\n2. Извлича и структурира данни за визуализиране на списък и детайлен изглед (Read).', 2, 1, 1, 'НЗ', 1, ''),
(40, 20, 'Реализиране на CRUD операции: Редактиране и изтриване на ресурси', 'Управление на състоянията при редакция, обработка на грешки и осигуряване на цялост на данните.', '1. Реализира бизнес логика за актуализиране (Update) на съществуващи записи;\n2. Изпълнява сигурно изтриване (Delete) на данни с валидация на идентификатора.', 2, 1, 1, 'УПР', 1, ''),
(41, 21, 'Създаване на шаблонни изгледи и динамично рендиране', 'Повторно използване на визуален код, синтаксис на шаблонни структури, циклични конструкции и условия в изгледа.', '1. Прилага шаблонен енджин за разделяне на презентационния слой от сървърната логика;\n2. Изгражда базови оформления (layouts), паршъли (partials) и подава данни от контролера към изгледа.', 2, 1, 0, 'УПР', 1, ''),
(42, 22, 'Управление на състоянието: Сесии и бисквитки (Cookies)', 'Жизнен цикъл на бисквитките, флагове за сигурност (HttpOnly, Secure, SameSite) и механизми за сесийно съхранение.', '1. Обяснява безсъстоятелния (stateless) характер на HTTP и ролята на бисквитките за запазване на контекст;\n2. Управлява сървърни сесии (Session ID, Session storage) за поддържане на потребителско състояние.', 2, 1, 0, 'НЗ', 1, ''),
(43, 23, 'Автентикация и авторизация в уеб приложения', 'Сигурно съхранение на идентификационни данни, генериране на сесии/токени и ролева валидация на потребители.', '1. Проектира логика за регистрация, хеширане на пароли (bcrypt/Argon2) и вход в системата;\n2. Разграничава права за достъп (Role-Based Access Control) и защитава критични маршрути.', 2, 1, 1, 'НЗ', 1, ''),
(44, 24, 'Сигурност в уеб среда: Превенция на SQLi, XSS и CSRF уязвимости', 'Най-често срещани уязвимости от OWASP Top 10, методи за защита на входните потоци и защитни HTTP заглавки.', '1. Разпознава механизмите на уязвимостите SQL Injection, Cross-Site Scripting (XSS) и CSRF;\n2. Прилага защитни мерки: ескейпване на данни, CSRF токени и Content Security Policy (CSP).', 2, 1, 1, 'НЗ', 1, ''),
(45, 25, 'Архитектура на RESTful API: Принципи и проектиране на крайни точки', 'Ресурсно-ориентирана архитектура, правилно мапване на HTTP методи към CRUD операции и добри практики при URI дизайн.', '1. Обяснява шестте архитектурни ограничения на REST (безсъстоятелност, кешируемост, единен интерфейс);\n2. Проектира йерархични RESTful URI структури за управление на колекции и отделни ресурси.', 2, 1, 1, 'НЗ', 1, ''),
(46, 26, 'Сериализация и работа със структурирани данни в JSON формат', 'Синтаксис на JSON, съпоставка с XML, заглавки за съдържание (Content-Type) и форматиране на REST съобщения.', '1. Извършва сериализация и десериализация на обекти от/към JSON форматиран текст;\n2. Настройва контролери за връщане на стандартизирани JSON отговори с подходящи HTTP статус кодове.', 2, 1, 0, 'УПР', 1, ''),
(47, 27, 'Асинхронна комуникация: Консумиране на REST API чрез Fetch API и AJAX', 'Асинхронен JavaScript, Promises, обработка на грешки при мрежова комуникация и рендиране на динамични списъци.', '1. Изпраща асинхронни HTTP заявки от клиентската част чрез Fetch API и async/await синтаксис;\n2. Обработва получения JSON отговор и обновява динамично съдържанието на DOM дървото без презареждане.', 2, 1, 0, 'УПР', 1, ''),
(48, 28, 'Обобщение: Интеграция на цялостно уеб приложение (Full-Stack)', 'Систематизиране на знанията за клиент-сървър комуникация, RESTful обмен и многослойна софтуерна архитектура.', '1. Свързва външния интерфейс (Front-end), сървърната логика (Back-end) и базата данни в работеща система;\n2. Тества коректността на обмена на данни и механизмите за автентикация в интеграционна среда.', 2, 1, 1, 'ОС', 1, ''),
(49, 29, 'Практическа защита на цялостен проект за уеб приложение', 'Оценяване на придобитите практически умения за проектиране, разработка, сигурност и представяне на завършен уеб софтуер.', '1. Демонстрира функционалностите на разработено уеб приложение с включени CRUD и REST API операции;\n2. Обосновава архитектурните решения, структурата на базата данни и приложените мерки за сигурност.', 2, 1, 1, 'ПК', 1, '');

-- --------------------------------------------------------

--
-- Структура на таблица `main_sessionattachment`
--

CREATE TABLE `main_sessionattachment` (
  `id` bigint(20) NOT NULL,
  `num` smallint(6) NOT NULL,
  `name` varchar(200) NOT NULL,
  `point_id` bigint(20) DEFAULT NULL,
  `session_id` bigint(20) NOT NULL,
  `attachment_type` varchar(20) NOT NULL,
  `description` longtext NOT NULL,
  `file` varchar(100) DEFAULT NULL,
  `original_filename` varchar(255) NOT NULL,
  `is_student_visible` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Схема на данните от таблица `main_sessionattachment`
--

INSERT INTO `main_sessionattachment` (`id`, `num`, `name`, `point_id`, `session_id`, `attachment_type`, `description`, `file`, `original_filename`, `is_student_visible`) VALUES
(2, 1, 'теоретичен материал по т.1', NULL, 10, 'theory', 'Просто някакво описание', 'session_attachments/upload_HQKpl9w.txt', '', 1),
(3, 1, 'nrdb4-2017-zaplashtane_izm120221.pdf', NULL, 10, 'other', 'коментар', 'session_attachments/nrdb4-2017-zaplashtane_izm120221.pdf', '', 1),
(9, 1, 'index.html', NULL, 4, 'other', '', 'session_attachments/d3765eb836e24d199e1afc75a2ef6a2d.html', 'index.html', 1),
(10, 1, 'Lesson 1 — Internet, URL abd HTTP.pdf', NULL, 4, 'theory', '', 'session_attachments/f6a261075e1f474ea52892f02f481e39.pdf', 'Lesson 1 — Internet, URL abd HTTP.pdf', 1),
(11, 2, 'Презентация_1.pptx', NULL, 4, 'other', '', 'session_attachments/8b45b96213ba4219820d963bab42ec2f.pptx', 'Презентация_1.pptx', 1),
(12, 1, 'План-конспект урок 1 HTTP.pdf', NULL, 21, 'other', '', 'session_attachments/65611bf112ea49fd834a7e76f93ad458.pdf', 'План-конспект урок 1 HTTP (3).pdf', 0),
(13, 2, 'План-конспект урок 1 HTTP (3).docx', NULL, 21, 'other', '', 'session_attachments/e889764190884996b3733e1a42f0ede2.docx', 'План-конспект урок 1 HTTP (3).docx', 1),
(14, 1, 'Иван Петров', NULL, 21, 'task', 'Обратна връзка: Иван Петров', 'session_attachments/b466f15fe9394bc78c273a9b43d55ac2.json', 'tmp.json', 0),
(15, 1, 'Петър Иванов', NULL, 21, 'exit_ticket', 'Обратна връзка: Петър Иванов', 'session_attachments/2d36112274de425bafaa42c0cbe7e98a.pdf', 'lesson1.pdf', 0),
(16, 1, 'тест Обратна връзка', NULL, 21, 'self_study', 'Обратна връзка: тест Обратна връзка', 'session_attachments/5bf0a9b510404c2b8a830149cb2b0884.html', 'index.html', 0);

-- --------------------------------------------------------

--
-- Структура на таблица `main_sessionnote`
--

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
(5, 1, 'Елементи от бланката за планиране на урок', '<table class=\"single !mb-2 w-fit !max-w-none\">\n<thead>\n<tr>\n<th>Елемент</th>\n<th>Описание</th>\n</tr>\n</thead>\n<tbody>\n<tr>\n<td><strong>Предметно знание</strong>&nbsp;(Какво трябва да знаят/могат в края на часа?)</td>\n<td>Учениците да могат да дефинират понятието \"нишка\", да обясняват критичната разлика между процес и нишка (спрямо паметта) и да аргументират кога се използва нишка.</td>\n</tr>\n<tr>\n<td><strong>Цел по умения за учене</strong>&nbsp;(GROW модел / визия)</td>\n<td><strong>Развитие на критичното и аналитично мислене</strong>&nbsp;чрез пренасяне на концепции от реалния живот (аналогия с ресторант) към абстрактни компютърни архитектури.</td>\n</tr>\n<tr>\n<td><strong>Цел за благополучие</strong></td>\n<td>Създаване на безопасна среда за изразяване на предположения. Учениците да се чувстват комфортно да дават \"грешни\" отговори по време на дискусията за процеси, знаейки, че това е част от процеса на учене.</td>\n</tr>\n<tr>\n<td><strong>Обратна връзка и Рефлексия</strong>&nbsp;(Критерии)</td>\n<td><strong>Критерии:</strong>&nbsp;Ученикът правилно ли идентифицира кога е нужна нишка и кога процес в зададените 3 сценария накрая на часа.<br><strong>Обратна връзка:</strong>&nbsp;Дава се веднага по време на гласуването със сценариите (Post-assessment).</td>\n</tr>\n<tr>\n<td><strong>Необходими ресурси и материали</strong></td>\n<td>Бяла дъска/маркери (за чертане на паметта), цветни картончета за гласуване (зелено/червено) за всеки ученик, презентация (по желание).</td>\n</tr>\n</tbody>\n</table>\n<p>&nbsp;</p>', NULL, 8),
(6, 2, 'Дейности и времево разпределение:', '<p><strong>1. Начало на часа (8 минути)</strong></p>\n<ul>\n<li><strong>Описание на дейността:</strong>&nbsp;<em>Bridge-in &amp; Pre-assessment.</em>&nbsp;Учителят въвлича учениците чрез ролева ситуация (\"Вие сте собственик на ресторант...\"). След като се стигне до извода за \"новия сервитьор\", се прави кратка връзка с предишния материал за изолираната памет на процесите.</li>\n<li><strong>Обобщение:</strong>&nbsp;Съобщават се целите на урока (Objective).</li>\n</ul>\n<p><strong>2. Същинска част (27 минути)</strong></p>\n<ul>\n<li><strong>Описание на дейността:</strong>&nbsp;<em>Participatory Learning.</em>&nbsp;Микро-лекция с визуално чертаене на дъската (Процес = голям квадрат; Нишки = стрелки вътре в него, споделящи едни и същи променливи). Следва съвместно изграждане на сравнителна таблица \"Процес срещу Нишка\". Въвежда се проблемът с GIL в Python като тема за размисъл.</li>\n<li><strong>Инструкция за задача (за дискусията с таблицата):</strong>\n<ul>\n<li><strong>Какво правим?</strong>&nbsp;➔ Съставяме заедно сравнителна таблица между процес и нишка.</li>\n<li><strong>Как работим?</strong>&nbsp;➔ Фронтално. Аз задавам въпрос (напр. \"Кое според вас се създава по-бързо?\"), вие обмисляте 10 секунди и вдигате ръка с предположение.</li>\n<li><strong>Колко време имаме?</strong>&nbsp;➔ 8 минути за попълване на цялата таблица.</li>\n</ul>\n</li>\n</ul>\n<p><strong>3. Край на часа (10 минути)</strong></p>\n<ul>\n<li><strong>Описание на дейността:</strong>&nbsp;<em>Post-assessment.</em>&nbsp;Проверка на наученото чрез конкретни сценарии.</li>\n<li><strong>Инструкция за задача:</strong>\n<ul>\n<li><strong>Какво правим?</strong>&nbsp;➔ Ще прочета 3 кратки софтуерни сценария. Вие трябва да решите дали ще ползвате Процес или Нишка за решаването им.</li>\n<li><strong>Как работим?</strong>&nbsp;➔ Вдигате зелено картонче за \"Нишка\" и червено за \"Процес\" едновременно на бройката \"три\".</li>\n<li><strong>Колко време имаме?</strong>&nbsp;➔ 5 минути за трите сценария.</li>\n</ul>\n</li>\n<li><strong>Обобщение на наученото и рефлексия:</strong>\n<ul>\n<li><em>Обобщение:</em>&nbsp;Нишките са леки и споделят памет, но това крие рискове.</li>\n<li><em>Рефлексия:</em>&nbsp;Учителят пита:&nbsp;<em>\"Кое ви се стори най-объркващо днес в концепцията за споделена памет?\"</em> (Дава се възможност на 1-2 ученици да споделят).</li>\n</ul>\n</li>\n</ul>', NULL, 8),
(7, 1, 'код за нализ', '<p><img src=\"../../media_files/session_pics/%D0%9A%D0%BE%D0%B4_1.png\" alt=\"\" width=\"451\" height=\"235\"></p>', 21, 10),
(8, 2, 'Интегриране в бланката за урок на ПГЕЕ', '<table class=\"single !mb-2 w-fit !max-w-none\">\n<thead>\n<tr>\n<th>Елемент</th>\n<th>Описание</th>\n</tr>\n</thead>\n<tbody>\n<tr>\n<td><strong>Предметно знание</strong></td>\n<td>Учениците да разпознават етапите от жизнения цикъл на нишката и да обясняват синтаксиса за създаването ѝ в Python (параметри&nbsp;<code>target</code>&nbsp;и&nbsp;<code>args</code>).</td>\n</tr>\n<tr>\n<td><strong>Цел по умения за учене</strong>&nbsp;(GROW модел)</td>\n<td><strong>Развитие на умения за четене и анализ на код (Code Reading)</strong>&nbsp;&ndash; способност да откриват логически и синтактични грешки в чужд код, без да го изпълняват на компютър.</td>\n</tr>\n<tr>\n<td><strong>Цел за благополучие</strong></td>\n<td>Насърчаване на&nbsp;<strong>екипната подкрепа</strong>. Задачата \"Открий бъга\" се изпълнява по чинове (по двойки), за да се намали стресът от индивидуалното изпитване при сблъсъка с нов и сложен синтаксис.</td>\n</tr>\n<tr>\n<td><strong>Обратна връзка и Рефлексия</strong>&nbsp;(Критерии)</td>\n<td><strong>Критерии:</strong>&nbsp;Успешно откриване на грешките (липсващ&nbsp;<code>.start()</code>, грешно подаден&nbsp;<code>target</code>) в предоставените фрагменти.<br><strong>Обратна връзка:</strong>&nbsp;Дава се фронтално по време на обсъждането на фрагментите.</td>\n</tr>\n<tr>\n<td><strong>Необходими ресурси и материали</strong></td>\n<td>Бяла дъска (за чертане на жизнения цикъл), мултимедиен проектор/екран за показване на фрагментите код.</td>\n</tr>\n</tbody>\n</table>\n<p>&nbsp;</p>', NULL, 10),
(9, 3, 'Дейности и времево разпределение:', '<p><strong>1. Начало на часа (10 минути)</strong></p>\n<ul>\n<li><strong>Описание на дейността:</strong>&nbsp;Въвеждане в темата чрез аналогията с мениджъра и работника (Bridge). Кратко припомняне на споделената памет от миналия час (Pre-assessment) и обявяване на целите.</li>\n<li><strong>Обобщение:</strong>&nbsp;Ясно се заявява разликата между \"наемане на работник\" (създаване) и \"задаване на старт\" (изпълнение).</li>\n</ul>\n<p><strong>2. Същинска част (20 минути)</strong></p>\n<ul>\n<li><strong>Описание на дейността:</strong>&nbsp;Учителят чертае жизнения цикъл на дъската (New ➔ Running ➔ Dead). Следва анализ на минималния Python код за създаване на нишка. Обръща се специално внимание на предаването на функция като референция (без скоби).</li>\n<li><strong>Инструкция за задача (към анализа на кода):</strong>\n<ul>\n<li><strong>Какво правим?</strong>&nbsp;➔ Разглобяваме анатомията на класа&nbsp;<code>Thread</code>&nbsp;ред по ред.</li>\n<li><strong>Как работим?</strong>&nbsp;➔ Фронтално. Аз обяснявам параметрите, вие си водите записки за разликата между&nbsp;<code>target=my_task</code>&nbsp;и&nbsp;<code>target=my_task()</code>.</li>\n<li><strong>Колко време имаме?</strong>&nbsp;➔ 13 минути за синтаксиса.</li>\n</ul>\n</li>\n</ul>\n<p><strong>3. Край на часа (15 минути)</strong></p>\n<ul>\n<li><strong>Описание на дейността:</strong>&nbsp;Практическа (теоретична) задача \"Открий бъга\" (Post-assessment). Прожектират се 3 сгрешени кода.</li>\n<li><strong>Инструкция за задача:</strong>\n<ul>\n<li><strong>Какво правим?</strong>&nbsp;➔ Ще видите 3 кратки програми, които се опитват да стартират нишка, но се провалят. Трябва да откриете защо.</li>\n<li><strong>Как работим?</strong>&nbsp;➔ Работите по двойки с човека до вас. Имате по 1 минута да обсъдите всеки пример, след което посочвам двойка, която да защити тезата си.</li>\n<li><strong>Колко време имаме?</strong>&nbsp;➔ Общо 10 минути за откриване и обсъждане на грешките.</li>\n</ul>\n</li>\n<li><strong>Обобщение на наученото и рефлексия:</strong>\n<ul>\n<li><em>Обобщение:</em>&nbsp;Нишката има нужда от 3 неща: модул&nbsp;<code>threading</code>, обект с&nbsp;<code>target</code>&nbsp;и извикване на&nbsp;<code>.start()</code>.</li>\n<li><em>Рефлексия:</em>&nbsp;Учителят пита:&nbsp;<em>\"Според вас, по-лесно ли се чете чужд код, когато го обсъждате по двойки, отколкото сами?\"</em> (Кратка дискусия за екипната работа).</li>\n</ul>\n</li>\n</ul>', NULL, 10),
(10, 3, 'тестова бележка към точка 1', '<p>текст на тестова бележка към точка 1</p>', 10, 8),
(11, 4, 'Втора бележка към тази точка', '<p>текст на втората бележка към тази точка</p>', 21, 10),
(12, 1, 'Теоретичен конспект: Стек TCP/IP, DNS и анатомия на HTTP протокола', '<p><strong>1. TCP/IP модел и роля в уеб комуникацията:</strong></p><ul><li><strong>Приложен слой (Application Layer):</strong> HTTP, HTTPS, FTP, DNS. Определя формата на предаваните данни между конкретните приложни програми.</li><li><strong>Транспортен слой (Transport Layer):</strong> TCP (Transmission Control Protocol) – гарантира надеждна доставка, подреждане на пакетите и контрол на потока чрез 3-way handshake (SYN, SYN-ACK, ACK); UDP (User Datagram Protocol) – бърз, без гаранция за доставка. Стандартен порт за HTTP е 80, за HTTPS – 443.</li><li><strong>Интернет слой (Internet Layer):</strong> IP (Internet Protocol) – отговаря за логическата адресация (IPv4 / IPv6) и маршрутизацията на пакетите през мрежите.</li><li><strong>Мрежов достъп (Network Access Layer):</strong> Физически среди и канален контрол (Ethernet, Wi-Fi, MAC адреси).</li></ul><p><strong>2. DNS (Domain Name System):</strong> Йерархична разпределена база данни, транслираща четими от човек домейн имена (напр. <code>api.school.bg</code>) в числови IP адреси (напр. <code>91.215.216.12</code>).</p><p><strong>3. Структура на HTTP съобщението (RFC 7230 / RFC 9112):</strong></p><p>HTTP е текстово-базиран протокол тип <em>заявка-отговор (Request-Response)</em>, функциониращ без състояние (stateless).</p><p><strong>Структура на HTTP заявка (Request):</strong></p><pre><code>GET /index.html HTTP/1.1\\r\\n\nHost: example.com\\r\\n\nUser-Agent: IridaWebClient/1.0\\r\\n\nAccept: text/html,application/xhtml+xml\\r\\n\nConnection: close\\r\\n\n\\r\\n\n[Незадължително тяло (Message Body) - празно при GET]</code></pre><p><strong>Структура на HTTP отговор (Response):</strong></p><pre><code>HTTP/1.1 200 OK\\r\\n\nDate: Mon, 14 Sep 2026 08:30:00 GMT\\r\\n\nServer: Apache/2.4.52 (Ubuntu)\\r\\n\nContent-Type: text/html; charset=UTF-8\\r\\n\nContent-Length: 48\\r\\n\nConnection: close\\r\\n\n\\r\\n\n&lt;!DOCTYPE html&gt;&lt;html&gt;&lt;body&gt;Hello World!&lt;/body&gt;&lt;/html&gt;</code></pre><p><strong>Важно правило за форматиране:</strong> Всеки ред в HTTP заглавната част завършва с последователност от символи за нов ред <code>CRLF</code> (<code>\\\\r\\\\n</code>). Празен ред <code>CRLF</code> маркира задължителния край на заглавната част и началото на тялото (тялото липсва при заявки от тип GET).</p>', 26, 21),
(16, 1, 'Методическа подготовка и организация', '<p><strong>Занятие №1:</strong> „Формиране на екипи и разпределение на заданията“. Предмет: Разработка на софтуер; специалност: Приложно програмиране; 11 клас; вид: упражнение.</p><p><strong>Подготовка преди часа:</strong> Учителят подготвя предварителен състав на екипите според наблюдения от предходната работа, а не според публично класиране на учениците. Осигурява проектор, текстов редактор или споделени документи, задания А–В, празен екипен паспорт, индивидуални билети и достъп до Python 3 за кратката демонстрация. При липса на техника всички основни дейности могат да се изпълнят на хартия; кодът се разчита по разпечатка.</p><p><strong>Предпоставки:</strong> Основна компютърна грамотност и опит с кратки програмни задачи. Не се изискват познания по конкретна уеб рамка, Git или система за управление на проекти.</p><p><strong>Дидактическа организация:</strong> Входната диагностика на BOPPPS е в точка 1; активното учене обхваща точки 3–7; заключителната проверка и обобщението са в точки 8–9. GRR се реализира последователно: демонстрация в точка 3, общо решение в точка 5, самостоятелна екипна работа и след нея индивидуална работа в точка 6.</p><p><strong>Проверка на времето:</strong> 5 + 5 + 15 + 7 + 8 + 25 + 10 + 7 + 8 = 90 минути. Времето е за учебна работа и не включва междучасие.</p>', 43, 4),
(17, 2, 'Основни понятия: екип, роля, задание и обхват', '<ul><li><strong>Работен екип:</strong> група с обща цел, координирани дейности и споделена отговорност за общия резултат.</li><li><strong>Роля:</strong> набор от отговорности в екипа. Ролята не е оценка за способностите и не е постоянна професионална длъжност.</li><li><strong>Проектно задание:</strong> описание на проблема, потребителите, очакваните възможности, ограниченията и резултатите от проекта.</li><li><strong>Обхват:</strong> границата между това, което ще бъде разработено в договорената версия, и това, което няма да бъде разработено в нея.</li><li><strong>Изискване:</strong> необходимо поведение или условие за продукта, например „потребителят може да търси книга по заглавие“.</li><li><strong>Работна задача:</strong> конкретна дейност с отговорник и проверим резултат, например „подготви три примера за търсене и очакваните резултати“.</li><li><strong>Критерий за приемане:</strong> наблюдаемо условие, чрез което проверяваме дали резултатът удовлетворява уговореното.</li><li><strong>Ограничение:</strong> предварително условие за работата или продукта, например локална среда и само измислени данни.</li></ul><p><strong>Последователност:</strong> прочети заданието → определи потребителя и целта → извлечи изискванията → отдели изключенията и неяснотите → разпиши начални задачи → определи отговорници → провери общото разбиране.</p><p><strong>Правило:</strong> Неясното изискване се записва като въпрос, а не се превръща мълчаливо в собствено предположение. Предложението за допълнителна функция се обсъжда и се включва само след одобрение от учителя в ролята на възложител.</p>', 44, 4),
(18, 3, 'Начални роли и правила за сътрудничество', '<table><thead><tr><th>Начална роля</th><th>Основни отговорности</th><th>Видим принос днес</th></tr></thead><tbody><tr><td>Координатор</td><td>Следи времето и общата дъска; организира обсъждането и търси помощ при блокиране.</td><td>Подреден списък със задачи и отговорници.</td></tr><tr><td>Отговорник по изискванията</td><td>Проследява връзката със заданието; записва обхвата и въпросите към възложителя.</td><td>Карта на обхвата.</td></tr><tr><td>Отговорник по интерфейса и техническото планиране</td><td>Предлага начални екрани и основни данни; отбелязва технически зависимости.</td><td>Първа скица или описание на екраните.</td></tr><tr><td>Отговорник по качеството и документацията</td><td>Проверява яснотата на критериите; организира примерите и общия документ.</td><td>Списък с проверки и подреден екипен паспорт.</td></tr></tbody></table><p>При трима участници се съчетават координацията и документацията. Всички участват в обсъждането, а при последващото разработване — в програмиране и проверка според учебните цели. Ролите се преразглеждат в началото на следващ етап, за да не се ограничава един ученик постоянно само до писане на документи.</p><p><strong>Примерни правила:</strong> всеки получава възможност да предложи решение; всяка задача има един водещ отговорник, но може да има помощници; затруднение се съобщава своевременно; несъгласията се решават чрез аргументи и заданието, а при нужда — с учителя.</p><p><strong>Работен поток:</strong> „Предстои“ → „В работа“ → „За преглед“ → „Готово“. При неизпълнен критерий задачата се връща в „В работа“. Статусът описва състояние, а не качество на ученика.</p>', 45, 4),
(19, 4, 'Работещ демо код: Проверка на описанията на задачи', '<p>Самостоятелен пример за Python 3 без външни библиотеки. Запазете като <code>check_tasks.py</code> и изпълнете с <code>python check_tasks.py</code>. Примерът подпомага организацията, а не въвежда нова задължителна програмна тема.</p><pre><code># Учебни записи за две начални задачи.\ntasks = [\n    {\n        \'title\': \'Скица на списъка със срещи\',\n        \'owner\': \'Участник 1\',\n        \'result\': \'Една скица\',\n        \'acceptance\': \'Всяка среща показва тема и дата.\',\n        \'status\': \'Предстои\'\n    },\n    {\n        \'title\': \'Описание на формата\',\n        \'owner\': \'\',\n        \'result\': \'Списък на полетата\',\n        \'acceptance\': \'\',\n        \'status\': \'Предстои\'\n    }\n]\n\nrequired_fields = (\'title\', \'owner\', \'result\', \'acceptance\')\nallowed_statuses = {\'Предстои\', \'В работа\', \'За преглед\', \'Готово\'}\n\nfor number, task in enumerate(tasks, start=1):\n    # Проверяваме дали задължителните описания са непразен текст.\n    missing = []\n    for field in required_fields:\n        value = task.get(field)\n        if not isinstance(value, str) or not value.strip():\n            missing.append(field)\n\n    problems = []\n    if missing:\n        problems.append(\'Липсват: \' + \', \'.join(missing))\n    if task.get(\'status\') not in allowed_statuses:\n        problems.append(\'Невалиден статус\')\n\n    # Попълнен запис не означава автоматично изпълнена задача.\n    report = \'; \'.join(problems) if problems else \'Записът е попълнен.\'\n    print(f\'Задача {number}: {report}\')\n</code></pre><p><strong>Очакван изход:</strong></p><pre><code>Задача 1: Записът е попълнен.\nЗадача 2: Липсват: owner, acceptance\n</code></pre><p><strong>Ключови редове:</strong> <code>required_fields</code> задава задължителните полета; <code>strip()</code> позволява празните интервали да бъдат разпознати като липсващ текст; <code>allowed_statuses</code> ограничава допустимите статуси; цикълът проверява всяка задача поотделно.</p><p><strong>Граница на автоматизацията:</strong> Текстът „да е хубаво“ ще премине проверката за непразно поле, но не е добър критерий. Смисълът, съответствието със заданието и действителното изпълнение се проверяват от хората.</p>', 44, 4),
(20, 5, 'Проектни задания за разпределяне от учителя', '<p><strong>Общи условия за трите варианта:</strong> Планира се малко локално приложение с учебни данни. Технологичният избор се уточнява в следващо занятие. Днес се предават организационни документи, а не завършен софтуер. Не се използват реални лични данни. Трите варианта имат съпоставим начален обхват: списък, добавяне и търсене.</p><p><strong>Задание А — Каталог на учебни книги:</strong> Потребителят е отговорникът за учебния библиотечен кът. Приложението показва списък с книги, добавя книга със заглавие, автор и година и търси по част от заглавието без значение на главни и малки букви. Заглавието и авторът са задължителни след премахване на външните интервали; годината е цяло число от 1450 до текущата година. Извън обхвата са заемане на книги, регистрация и плащане. Въпрос за уточняване: позволени ли са еднакви заглавие и автор в повече от един запис?</p><p><strong>Задание Б — Каталог на училищни клубове:</strong> Потребителят е училищният организатор на клубни дейности. Приложението показва списък с клубове, добавя клуб с име, направление и помещение и търси по част от името без значение на главни и малки букви. Трите полета са задължителни след премахване на външните интервали. Извън обхвата са записване на ученици, присъствени списъци и известия. Въпрос за уточняване: позволени ли са два клуба с еднакво име?</p><p><strong>Задание В — Каталог на учебни ресурси:</strong> Потребителят е учител, който подрежда учебни материали. Приложението показва списък с ресурси, добавя ресурс със заглавие, предмет и вид и търси по част от заглавието без значение на главни и малки букви. Заглавието и предметът са задължителни след премахване на външните интервали; видът е един от „текст“, „видео“ и „упражнение“. Извън обхвата са качване на файлове, коментари и потребителски профили. Въпрос за уточняване: позволени ли са повтарящи се записи?</p><p>Въпросите за уточняване не се третират като вече одобрени правила. Екипите ги записват и ги отправят към учителя в ролята на възложител.</p>', 45, 4),
(21, 6, 'Структура на продуктите и критерии за оценяване', '<p><strong>Екипен документ:</strong> номер и име на екипа; вариант на заданието; участници и начални роли; четири правила; цел и потребител; включени функционалности; ограничения; изключени функционалности; въпроси; минимум четири задачи с отговорник, резултат, критерий и статус. Документът се озаглавява например <code>Екип 1 — Задание А — Начален план</code>.</p><table><thead><tr><th>Доказателство</th><th>Критерий</th><th>Точки</th></tr></thead><tbody><tr><td>Екипен документ</td><td>Състав, роли за всички и четири правила — 1 т.; цел, потребител и трите задължителни функционалности — 1 т.; ограничения, изключения и въпрос — 1 т.; поне четири пълно описани задачи — 1 т.</td><td>0–4</td></tr><tr><td>Индивидуален билет</td><td>Роля с две отговорности — 1 т.; цел и потребител — 1 т.; три включени функционалности — 1 т.; две изключени функционалности — 1 т.; лична задача с резултат и проверим критерий — 1 т.; уместен въпрос за уточняване — 1 т.</td><td>0–6</td></tr></tbody></table><p><strong>Отчитане:</strong> Екипният резултат и индивидуалният резултат се записват отделно; общият сбор е до 10 точки и служи за формираща обратна връзка. Ориентирът за индивидуално усвояване е поне 5 от 6 точки на билета и поне 3 от 4 точки на викторината. Екипният успех не компенсира липсващо индивидуално разбиране. Не се оценяват художественият вид на скиците или количеството написан код.</p><p><strong>Чести грешки:</strong> „Всички отговарят“ без водещ отговорник; задача без резултат; „работи добре“ като критерий; добавяне на функции без одобрение; объркване на роля с привилегия; оставяне на един ученик без реална работа.</p>', 47, 4);

-- --------------------------------------------------------

--
-- Структура на таблица `main_sessionpoint`
--

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
(10, 'Bridge-in (Мотивация и въвличане) – 5 мин.', 'Да грабнем вниманието чрез аналогия от реалния живот, преди да въведем абстрактните термини.', 5, 8, 1, '<ul>\n<li><strong>Сценарият \"Ресторантът\":</strong>&nbsp;Представете си, че сте собственик на успешен ресторант. Имате една сграда, една кухня (ресурси) и един сервитьор (основният поток на изпълнение). Клиентите се увеличават и сервитьорът не смогва &ndash; хората чакат (програмата блокира).</li>\n<li><strong>Въпрос към класа:</strong>&nbsp;<em>\"Какво е по-логично и евтино да направите, за да обслужите повече клиенти едновременно: да построите изцяло нова сграда с нова кухня (нов Процес) или просто да наемете втори сервитьор, който да ползва същата кухня (нова Нишка)?\"</em></li>\n<li><strong>Извод:</strong> Създаването на нова сграда е бавно и скъпо. Наемането на нов работник в същата сграда е бързо и ефективно. Точно това е разликата между процесите и нишките в операционната система.</li>\n</ul>'),
(11, 'Objective (Цели на урока) – 2 мин.', 'Ясно заявяваме на учениците какво ще знаят в края на часа:', 10, 8, 2, '<ol>\n<li>Да дефинират какво е \"нишка\" (Thread) в контекста на операционната система.</li>\n<li>Да обяснят критичната разлика между процес и нишка, най-вече по отношение на паметта.</li>\n<li>Да могат аргументирано да изберат кога архитектурно е по-подходящо да ползват нишка вместо процес.</li>\n</ol>'),
(12, 'Pre-assessment (Предварително оценяване)', 'Цел: Активиране на знанията от Урок 2 (Процеси).', 3, 8, 3, '<ul>\n<li><strong>Кратка дискусия:</strong>&nbsp;<em>\"Спомняте ли си какво се случва в RAM паметта, когато стартираме една Python програма?\"</em>&nbsp;(Отговор: ОС заделя изолирано парче памет &ndash; процес).</li>\n<li><em>\"Ако стартираме същата програма втори път паралелно, могат ли двете програми да си говорят директно и да променят едни и същи променливи?\"</em> (Отговор: Не, процесите са напълно изолирани).</li>\n</ul>'),
(13, 'Participatory Learning (Активно учене) - Дефиниция и Анатомия.', 'Това е началото на сърцевината на урока, където преподаваме новия материал чрез интеракция.', 7, 8, 4, '<ul>\n<li>Въвеждаме понятието: Нишката е най-малката единица от инструкции, която може да бъде управлявана от операционната система.</li>\n<li>Всяка програма има поне една нишка (Main Thread).</li>\n<li><strong>Визуализация (на дъската или презентация):</strong> Рисуваме голям квадрат (Процес). Вътре рисуваме обекти (Променливи, Отворени файлове). Рисуваме стрелка (Main Thread). После добавяме втора стрелка (Worker Thread) в същия квадрат.</li>\n</ul>'),
(14, 'Participatory Learning (Активно учене) - Сравнителен анализ: Процес срещу Нишка.', 'Навлизам в сърцевината на урока, където преподавам новия материал.', 8, 8, 5, '<p>Съставяме таблица заедно с учениците:</p>\n<ul>\n<li style=\"list-style-type: none;\">\n<ul>\n<li style=\"list-style-type: none;\">\n<ul>\n<li><em>Памет:</em>&nbsp;Процесите имат собствена изолирана памет. Нишките&nbsp;<strong>споделят</strong>&nbsp;паметта на процеса-родител.</li>\n<li><em>Създаване:</em>&nbsp;Процесите са \"тежки\" (OS отделя време за заделяне на ресурси). Нишките са \"леки\" (създават се почти мигновено).</li>\n<li><em>Срив:</em> Ако един процес крашне, другите продължават. Ако една нишка предизвика фатална грешка (напр. Segmentation fault), целият процес (и всички останали нишки в него) умира.</li>\n</ul>\n</li>\n</ul>\n</li>\n</ul>'),
(15, 'Participatory Learning (Активно учене) – Дискусия: Спецификата на Python (GIL).', 'Финализирам сърцевината на урока, където преподавам новия материал.', 5, 8, 6, '<ul>\n<li>Задаваме въпроса:&nbsp;<em>\"След като нишките са толкова леки и бързи, защо просто не сложим 1000 нишки да смятат сложни математически уравнения в Python?\"</em></li>\n<li>Споменаваме накратко&nbsp;<strong>GIL (Global Interpreter Lock)</strong> като \"правилото на Python\", че само една нишка може да изпълнява Python код в даден момент. (Това подготвя почвата за бъдещите уроци, без да се навлиза в дълбок код).</li>\n</ul>'),
(16, 'Post-assessment (Последващо оценяване)', 'Цел: Проверка на концептуалното разбиране чрез сценарии. Учениците вдигат ръка или ползват цветни картончета (зелено за Нишка, червено за Процес).', 10, 8, 7, '<ul>\n<li><strong>Сценарий 1:</strong>&nbsp;Имаме глобална променлива&nbsp;<code>counter = 0</code>. Искаме две паралелни задачи да я увеличават едновременно. Какво трябва да използваме?&nbsp;<em>(Отговор: Нишки, защото споделят една и съща памет).</em></li>\n<li><strong>Сценарий 2:</strong>&nbsp;Правим браузър като Google Chrome. Искаме, ако един таб забие тотално, останалите табове да продължат да работят.&nbsp;<em>(Отговор: Процеси, заради изолацията при срив).</em></li>\n<li><strong>Сценарий 3:</strong>&nbsp;Имаме малък скрипт, който трябва бързо да провери дали 50 уебсайта са онлайн (I/O операция). Искаме да стартираме 50 задачи максимално \"евтино\" за RAM паметта.&nbsp;<em>(Отговор: Нишки).</em></li>\n</ul>'),
(17, 'Bridge-in (Мотивация и въвличане)', '', 5, 10, 1, '<ul>\n<li><strong>Аналогията \"Мениджър и Работник\":</strong>&nbsp;Представете си, че сте мениджър (Main Thread - основната нишка на програмата). Наемате нов работник (Worker Thread), за да свърши конкретна задача &ndash; например да боядиса стена.</li>\n<li><strong>Въпрос към класа:</strong>&nbsp;<em>\"Ако само подпишете договор с работника (създадете нишката) и му дадете четка, той ще започне ли да боядисва веднага?\"</em>&nbsp;(Отговор: Не, трябва изрично да му кажете \"Започвай!\").</li>\n<li><strong>Извод:</strong> В програмирането създаването на нишка и нейното стартиране са две напълно отделни действия. Днес ще видим как точно става това в Python.</li>\n</ul>'),
(18, 'Objective (Цели на урока)', '', 2, 10, 2, '<p>В края на часа учениците ще могат да:</p>\n<ol>\n<li>Описват трите основни състояния в жизнения цикъл на нишката (Нова, Работеща, Мъртва).</li>\n<li>Обясняват предназначението на параметрите&nbsp;<code>target</code>&nbsp;и&nbsp;<code>args</code> при създаване на обект&nbsp;от тип&nbsp;<code>threading.Thread</code>.</li>\n<li>Разпознават често срещани синтактични и логически грешки при стартиране на нишки.</li>\n</ol>'),
(19, 'Pre-assessment (Предварително оценяване)', '', 3, 10, 3, '<ul>\n<li><strong>Бърз въпрос:</strong>&nbsp;<em>\"От миналия път &ndash; ако имаме една променлива&nbsp;<code>A = 5</code>&nbsp;и стартираме 3 нишки, всяка от тези нишки собствено копие на&nbsp;<code>A</code>&nbsp;ли ще има, или всички ще гледат едно и също&nbsp;<code>A</code>?\"</em> (Отговор: Едно и също, защото нишките споделят паметта на процеса). Това затвърждава защо трябва да внимаваме, когато ги създаваме.</li>\n</ul>'),
(20, 'Participatory Learning (Активно учене) - Жизнен цикъл (Визуализация):', '', 7, 10, 4, '<ul>\n<li>Чертаем три кръга със стрелки между тях:&nbsp;<strong>New</strong>&nbsp;(Създадена, но не работи) ➔&nbsp;<strong>Runnable/Running</strong>&nbsp;(Работи или чака процесора) ➔&nbsp;<strong>Dead</strong> (Приключила задачата си).</li>\n</ul>'),
(21, 'Participatory Learning (Активно учене) – Синтаксисът в Python (Анализ на код на екрана)', 'Показваме минималния нужен код', 13, 10, 5, '<ul>\n<li><strong>Критичен момент за дискусия:</strong>&nbsp;Защо пишем&nbsp;<code>target=my_task</code>, а НЕ пишем&nbsp;<code>target=my_task()</code>&nbsp;(с кръгли скоби)?</li>\n<li><em>Обяснение:</em> Ако сложим скобите, главната нишка ще изпълни функцията веднага и ще блокира, вместо да я предаде на новата нишка като \"инструкция за работа\". Това е най-честата грешка в практиката!</li>\n</ul>'),
(22, 'Post-assessment (Последващо оценяване)', '', 10, 10, 6, '<ul>\n<li><strong>Игра \"Открий бъга\":</strong>&nbsp;На екрана (или на разпечатки) се показват 3 кратки фрагмента код с грешки. Учениците (по двойки) трябва да открият защо кодът няма да създаде правилно паралелна нишка.\n<ul>\n<li><em>Пример 1:</em>&nbsp;Забравено извикване на&nbsp;<code>t.start()</code>. (Нишката остава в състояние New).</li>\n<li><em>Пример 2:</em>&nbsp;Написано&nbsp;<code>target=download_file()</code>. (Функцията се изпълнява синхронно/блокиращо).</li>\n<li><em>Пример 3:</em>&nbsp;Подаване на аргументи без запетая в тупъла:&nbsp;<code>args=(\"Иван\")</code>&nbsp;вместо&nbsp;<code>args=(\"Иван\",)</code>. (Специфика на Python, която предизвиква краш).</li>\n</ul>\n</li>\n</ul>'),
(23, 'Summary (Обобщение)', '', 5, 10, 7, '<ul>\n<li><strong>Синтез:</strong>&nbsp;За да имаме паралелизъм, трябва да импортираме&nbsp;<code>threading</code>, да създадем обект&nbsp;<code>Thread</code>, да му подадем функция (без скоби!) и задължително да извикаме&nbsp;<code>.start()</code>.</li>\n<li><strong>Мост към следващия урок (Урок 7):</strong>&nbsp;<em>\"Днес се научихме как да пускаме работниците да работят. Но какво става, ако главният мениджър (Main Thread) си тръгне от работа, преди те да са приключили? Програмата ще се затвори аварийно. Следващият път ще учим как да ги изчакваме (метода&nbsp;<code>.join()</code>).\"</em></li>\n</ul>'),
(24, 'Bridge-In: Какво се случва, когато напишем google.com в браузъра?', 'Въведение и мотивация чрез практически казус', 5, 21, 1, '<p>Учителят отваря празен уеб браузър на мултимедийния екран и въвежда URL адреса <code>https://example.com</code>. Задава провокативен въпрос към учениците: <em>\"Какво точно се случва в милисекундите между натискането на клавиша Enter и появата на страницата на екрана?\"</em></p><p>Обсъжда се разликата между физическата свързаност и приложните протоколи, като се прави мост към ролята на софтуерния разработчик: <em>\"За да пишем надежден бекенд и фронтенд код, ние не можем да разглеждаме мрежата като черна кутия – трябва да разбираме правилата, по които пътуват данните.\"</em></p>'),
(25, 'Outcomes: Обявяване на очакваните резултати и критерии за успех', 'Цели и компетентности на занятието', 5, 21, 2, '<p>Учителят представя оперативните цели на урока и формулира какво ще може всеки ученик в края на 90-те минути:</p><ul><li>Да проследява пътя на мрежовия пакет от клиентско приложение през DNS и TCP/IP до целевия сървър;</li><li>Да деконструира сурова HTTP заявка и HTTP отговор, идентифицирайки метод, URI, хедъри, статус код и тяло (payload);</li><li>Да изпраща директни сурови HTTP заявки чрез конзолни инструменти (cURL) и да анализира отговорите на сървъра.</li></ul>'),
(26, 'Презентация и демонстрация: TCP/IP модел и анатомия на HTTP', 'GRR: Директно обучение (Аз правя)', 15, 21, 3, '<p>Учителят представя теоретичната база, подкрепена с визуални диаграми и демонстрация на живо:</p><ol><li><strong>TCP/IP стек:</strong> Разглеждане на 4-слойния модел (Мрежов достъп, Интернет/IP, Транспортен/TCP, Приложен/HTTP). Обяснява се адресацията (IP адрес) и логическите портове (порт 80 за HTTP, 443 за HTTPS).</li><li><strong>DNS резолюция:</strong> Ролята на Domain Name System като телефонен указател на Интернет.</li><li><strong>Трипътно ръкостискане (TCP Three-Way Handshake):</strong> SYN -> SYN-ACK -> ACK преди преноса на HTTP данни.</li><li><strong>Анатомия на HTTP съобщението:</strong> Демонстрира се, че HTTP е чист текст (human-readable text protocol). Разглеждат се: <em>Request Line (Method, Path, Protocol Version)</em>, <em>Request Headers</em>, празен ред (CRLF) и <em>Message Body</em>. Аналогично се разглежда HTTP отговорът: <em>Status Line (Version, Status Code, Reason Phrase)</em>, <em>Response Headers</em> и съдържанието.</li></ol>'),
(27, 'Дискусия и рефлексия: Stateless природата на HTTP', 'Въпроси за разбиране и проверка на концепциите', 7, 21, 4, '<p>Провежда се кратка дискусия по ключови въпроси:</p><ul><li><em>\"Защо казваме, че HTTP е stateless (протокол без състояние)? Ако сървърът забравя клиента веднага след връщането на отговора, как онлайн магазините \'помнят\' съдържанието на нашата количка?\"</em> (Въвеждане на контекст за бисквитки и сесии, които ще се изучават в следващите дялове).</li><li><em>\"Каква е разликата между TCP и UDP и защо уеб страниците използват надеждния TCP вместо по-бързия UDP?\"</em></li><li><em>\"Какво прави един уеб сървър, ако получи HTTP заявка без празен ред между хедърите и тялото?\"</em></li></ul>'),
(28, 'Съвместно упражнение: Ръчно конструиране и анализ на HTTP заявка', 'GRR: Ръководена практика (Ние правим заедно)', 8, 21, 5, '<p>Учителят и учениците работят синхронно в терминала на работните станции:</p><ol><li>Отваря се терминал и се стартира дебъг сесия с <code>curl -v http://example.com</code>.</li><li>Учителят насочва вниманието към символите <code>></code> (изпратено от клиента) и <code><</code> (върнато от сървъра).</li><li>Заедно изолират и анализират всяка линия от HTTP хедърите (Host, User-Agent, Accept, Content-Type, Content-Length).</li><li>Учителят показва как умишлено изтриване на задължителния хедър <code>Host</code> в HTTP/1.1 води до грешка <code>400 Bad Request</code>.</li></ol>'),
(29, 'Самостоятелна практика: Изследване на мрежовия слой и HTTP ресурси', 'GRR: Самостоятелна работа (Ти правиш сам)', 25, 21, 6, '<p>Учениците изпълняват индивидуална лабораторна задача, състояща се от две части:</p><ol><li><strong>Мрежово трасиране:</strong> Използване на системните команди <code>nslookup</code> / <code>ping</code> за определяне на IP адреса на даден хост и проследяване на DNS преобразуването.</li><li><strong>HTTP инспекция и конструиране на заявки:</strong> Учениците изпращат специфицирани GET и HEAD заявки към публичен тестов API сървър (напр. <code>httpbin.org</code>) чрез конзолата или браузърните Developer Tools (панел Network). Те трябва да извлекат точните статус кодове, типа на съдържанието и размера на тялото.</li></ol><p>Учителят оказва диференцирана подкрепа на ученици с технически затруднения и поставя допълнителни предизвикателства за по-напредналите (напр. изпращане на заявка с потребителски хедър).</p>'),
(30, 'Проверка и споделяне на резултатите', 'Демонстрация и анализ на лабораторните резултати', 10, 21, 7, '<p>Двама ученици споделят екраните си и представят изпълнението на практическата задача:</p><ul><li>Анализират се разликите между поведението на браузъра при заявка към съществуващ ресурс (200 OK) и пренасочване (301 Moved Permanently / 302 Found);</li><li>Коментира се защо хедърът <code>Content-Type: application/json</code> информира клиента как да парсира получените байтове;</li><li>Обобщават се откритите грешки и типични капани при ръчно въвеждане на HTTP команди.</li></ul>'),
(31, 'Мини-викторина (Post-Assessment)', 'Проверка на усвояването и моментална обратна връзка', 7, 21, 8, '<p>Учениците отговарят на 3 въпроса чрез интерактивна анкета (или на работните си бланки):</p><ol><li>Определяне на слоя от TCP/IP стека за протокола HTTP;</li><li>Разпознаване на коректния формат на Start-line при HTTP GET заявка;</li><li>Интерпретация на ролята на статус кода <code>404 Not Found</code> спрямо жизнения цикъл на заявката.</li></ol><p>Учителят прави светкавичен преглед на обобщените резултати и изяснява възникнали колебания.</p>'),
(32, 'Обобщение на занятието и поставяне на домашна работа', 'Summary & Домашна работа', 8, 21, 9, '<p>Учителят прави синтезирано резюме: <em>\"Днес разгледахме фундаменталната магистрала на уеб разработката: от IP пакетите и TCP свързаността до текстовия протокол HTTP. Всяко уеб приложение, независимо дали е на React, Node.js, PHP или C#, стъпва на тази основа.\"</em></p><p>Разясняват се изискванията за домашната работа и се маркира темата на следващия урок: <em>\"В следващото занятие ще навлезем в дълбочина в семантиката на различните HTTP методи (POST, PUT, DELETE, PATCH) и типовете ресурсен обмен.\"</em></p>'),
(42, 'Bridge-In: Един проект, различни очаквания', 'Мотивация и входна диагностика, вградена в началния казус', 5, 4, 1, '<p><strong>0–2 минути:</strong> Учителят представя ситуация: „Четирима ученици получават задача да създадат каталог на книги. Двама започват различни начални екрани, един добавя онлайн плащане, а четвъртият чака указания. В края няма общ резултат.“ Пита: „Какво не е уточнено преди започването на работата?“</p><p><strong>2–4 минути — входна диагностика:</strong> Всеки ученик записва кратки отговори: „Какво означава отговорник за задача?“ и „Кое трябва да се уточни първо: цветовете на бутоните или какво трябва да прави приложението? Защо?“ Учителят изслушва два отговора и установява дали учениците разграничават задача, роля и изискване.</p><p><strong>4–5 минути:</strong> Извежда основния проблем: екипът се нуждае от обща цел, разбран обхват и видимо разпределение на работата. Уточнява: „Днес крайният продукт не е готово приложение, а работеща организация за неговото разработване.“</p>'),
(43, 'Outcomes: Цели, резултати и критерии за успех', 'Очаквани компетентности и организация на упражнението', 5, 4, 2, '<p><strong>0–2 минути:</strong> Учителят представя целите: „Ще знаете в кой екип работите и за какво отговаряте; ще можете да обясните полученото задание; ще определите какво влиза и какво не влиза в първата версия.“</p><p><strong>2–4 минути:</strong> Показва очакваните продукти:</p><ul><li>Екипен паспорт със състав, начални роли и правила за работа.</li><li>Карта на обхвата с потребител, цел, задължителни функционалности, ограничения и изключения.</li><li>Начален списък от минимум четири задачи с отговорници и критерии за приемане.</li><li>Индивидуален билет, чрез който всеки доказва собствено разбиране.</li></ul><p><strong>4–5 минути:</strong> Разяснява критериите: всеки има смислен принос; задължителните изисквания не са пропуснати; допълнителните идеи не се представят като задължителни; задачите имат проверим резултат. Посочва, че груповият документ не заменя индивидуалната проверка.</p>'),
(44, 'Презентация и демонстрация: От задание към план', 'GRR: Аз правя — моделиране на анализа и работния процес', 15, 4, 3, '<p><strong>0–3 минути:</strong> Учителят обяснява понятията екип, роля, проектно задание, обхват, задача и критерий за приемане. Разграничава: „Ролята описва отговорности; задачата има конкретен резултат; човекът с роля координатор не върши работата вместо останалите.“</p><p><strong>3–9 минути:</strong> Демонстрира мислене на глас върху краткото задание: „Приложение за училищен клуб показва срещите и позволява добавяне на среща с тема и дата. Работи локално с учебни данни. Не включва регистрация и известия.“ Подчертава потребителя, извлича две функционалности, записва ограниченията и отделя изключените дейности. Превръща „направи екрана“ в проверима задача: „Изработи скица на списъка със срещи; приемаме я, ако всяка среща показва тема и дата.“</p><p><strong>9–12 минути:</strong> Демонстрира дъска с колони „Предстои“, „В работа“, „За преглед“, „Готово“. Показва как задачата преминава към „Готово“ след проверка на критерия, а не само след заявлението „приключих“.</p><p><strong>12–15 минути:</strong> Изпълнява краткия Python пример от бележките за проверка на описанията на задачи. Обяснява, че кодът проверява само попълването и допустимия статус, но не може да прецени дали обхватът е правилен. Учениците предвиждат коя задача ще бъде отчетена като непълна. Не се изисква преписване на кода.</p>'),
(45, 'Дискусия, формиране на екипи и раздаване на задания', 'Осмисляне и изпълнение на задължителните организационни теми', 7, 4, 4, '<p><strong>0–3 минути — дискусия:</strong> Учителят пита: „Добра задача ли е ‘Работи по проекта’?“; „Ако липсва изискване за плащане, трябва ли веднага да го добавим?“; „Може ли един човек постоянно да пише целия код?“ Учениците аргументират отговорите. Учителят подчертава проверимия резултат, контрола на обхвата и споделеното учене.</p><p><strong>3–5 минути — групиране от учителя:</strong> Обявява предварително подготвените балансирани екипи. Работният пример е клас от 24 ученици: шест екипа по четирима. При различна численост се използват екипи от три или четирима с комбинирани начални роли при нужда. Балансирането отчита наблюдавани умения, интереси и потребности от подкрепа, без публично подреждане по способности.</p><p><strong>5–7 минути — разпределяне на задания:</strong> Учителят предоставя задание А на екипи 1 и 4, Б на екипи 2 и 5, В на екипи 3 и 6. Еднаквите варианти позволяват сравняване на различни решения. Всеки екип отбелязва номера си и получения вариант в общия документ. Учителят проверява достъпа и уточнява, че учениците договарят началните роли, а той утвърждава разпределението.</p>'),
(46, 'Съвместно упражнение: Разчитаме задание заедно', 'GRR: Ние правим — ръководено попълване на карта на обхвата', 8, 4, 5, '<p><strong>0–2 минути:</strong> Учителят прочита условието на съвместната задача за списък с учебни задачи. Пита: „Кой ще използва приложението и какъв проблем решава то?“ Записва общата формулировка на целта.</p><p><strong>2–5 минути:</strong> Заедно с класа попълва три колони: „Задължително“, „Извън обхвата“, „За уточняване“. Подканва учениците да посочат конкретните думи от заданието, които подкрепят всяко решение.</p><p><strong>5–7 минути:</strong> Класът формулира две начални задачи. Учителят пита: „Кой е отговорникът? Какво ще видим, когато задачата е изпълнена? Как ще го проверим?“ Допълват критерии за приемане.</p><p><strong>7–8 минути:</strong> Един ученик преразказва обхвата, а друг посочва разликата между изискването „добавяне на задача“ и подготвителната задача „скициране на формата“. Учителят отстранява оставащите неточности преди самостоятелната работа.</p>'),
(47, 'Практика: Екипен план и индивидуално разбиране', 'GRR: Вие правите → Ти правиш сам; самостоятелност с намаляваща подкрепа', 25, 4, 6, '<p><strong>0–5 минути — Вие правите:</strong> Екипите договарят началните роли и четири правила за взаимодействие. Учителят утвърждава ролите и следи всеки да има конкретна отговорност. При два отделни учебни часа тук завършва първият 45-минутен час; междучасието е извън посочените 90 минути.</p><p><strong>5–15 минути — Вие правите:</strong> Без водене стъпка по стъпка екипите анализират раздаденото задание, попълват карта на обхвата и съставят минимум четири начални задачи. За всяка задача записват отговорник, резултат, критерий за приемане и статус. Учителят наблюдава и пита: „Къде в заданието е това изискване?“; „Как ще докажете, че задачата е готова?“ Не попълва документа вместо учениците.</p><p><strong>15–23 минути — Ти правиш сам:</strong> Всеки ученик попълва индивидуалния билет от задача 2 без консултация с екипа. Описва своята роля, целта и обхвата на проекта, една лична задача с критерий и един въпрос за уточняване. Може да използва текста на заданието, но не преписва екипния документ.</p><p><strong>23–25 минути:</strong> Предават екипния документ и индивидуалните билети. Учителят отбелязва липсващи продукти и чести затруднения.</p><p><strong>Диференциране:</strong> При затруднение се предоставят заглавията на полетата и изреченията „Нашият потребител е...“, „Задачата е приета, когато...“. За напредналите: една зависимост между задачи и един риск с мярка за ограничаване. Не се изисква работещо приложение в това занятие.</p>'),
(48, 'Споделяне и проверка на екипните решения', 'Представяне, взаимна обратна връзка и корекция', 10, 4, 7, '<p><strong>0–6 минути:</strong> При шест екипа всеки разполага с една минута: представя целта, една включена и една изключена функционалност, както и една начална задача с отговорник и критерий. Говорителят може да е различен от координатора. При друг брой екипи учителят разпределя същия общ шестминутен прозорец.</p><p><strong>6–8 минути:</strong> Екипите с еднакви варианти сравняват решенията си. Всеки формулира една конкретна обратна връзка: „Този критерий е проверим, защото...“ или „Не намираме това изискване в заданието; необходимо ли е уточняване?“</p><p><strong>8–10 минути:</strong> Учителят обсъжда две типични неточности и позволява кратка корекция на екипния документ. Индивидуалните билети остават самостоятелно доказателство и не се променят чрез групово преписване. При индивидуално затруднение се планира последваща подкрепа.</p>'),
(49, 'Post-Assessment: Мини-викторина', 'Индивидуална проверка на ролите, обхвата и задачите', 7, 4, 8, '<p><strong>0–4 минути:</strong> Учениците отговарят самостоятелно на четирите въпроса от задача 3, без общия екипен документ.</p><p><strong>4–6 минути:</strong> Учителят представя верните отговори с кратка обосновка. Учениците отбелязват какво са объркали: роля, задача, обхват или критерий за приемане.</p><p><strong>6–7 минути:</strong> Учителят отчита резултатите: по една точка на въпрос; ориентир за усвояване е минимум 3 от 4 точки. При по-нисък резултат възлага кратък коригиращ пример в началото на следващото занятие. Резултатът се разглежда заедно с индивидуалния билет, а не само с представянето на екипа.</p>'),
(50, 'Summary: Обобщение и домашна работа', 'Рефлексия, затвърждаване и подготовка за следващата стъпка', 8, 4, 9, '<p><strong>0–3 минути:</strong> Учителят обобщава: „Първо изграждаме екип и общо разбиране. После уточняваме обхвата. Едва тогава разпределяме конкретни задачи.“ Учениците завършват писмено: „Моята начална отговорност е...“ и „Преди разработването трябва да уточним...“</p><p><strong>3–6 минути:</strong> Представя домашната работа от задача 4: индивидуална карта на лична начална задача и предложение за подобрение, което не се добавя автоматично към обхвата. Уточнява предаването до началото на следващото занятие като текстов документ или на хартия.</p><p><strong>6–8 минути:</strong> Проверява дали всеки знае екипа си, варианта на заданието, мястото за обща работа и следващата си стъпка. Посочва, че в следващото занятие ще се доуточнят изискванията и ще започне планираното проектиране, без да се обещава завършено приложение веднага.</p>');

-- --------------------------------------------------------

--
-- Структура на таблица `main_sessiontask`
--

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
(2, 1, 'задача 1', '<p>Задача за нещо</p>', '<p>Отговор на задачата</p>', 17, 10),
(3, 2, 'Обща задача', '<p>текст на общата задача</p>', '<p>отговор на общата задача</p>', NULL, 10),
(4, 1, 'Съвместна задача (Ръководена практика): Анализ на HTTP трафик през cURL', '<p><strong>Условие:</strong></p><p>Като използвате конзолния инструмент <code>curl</code>, изпълнете подробна (verbose) заявка към тестовия домейн <code>http://example.com</code>. Извлечете и документирайте следните параметри на мрежовия обмен:</p><ol><li>Целевия IP адрес и използвания мрежов порт за връзка;</li><li>Пълния вид на стартовия ред на заявката (Request line);</li><li>Стойността на хедъра <code>Content-Type</code>, върнат от сървъра;</li><li>HTTP статус кода и текста на статуса (Reason phrase).</li></ol>', '<p><strong>Решение и стъпки за изпълнение:</strong></p><p>1. Изпълнение на командата в терминала:</p><pre><code>curl -v http://example.com</code></pre><p>2. Анализ на конзолния изход:</p><pre><code>* Connected to example.com (93.184.216.34) port 80\n> GET / HTTP/1.1\n> Host: example.com\n> User-Agent: curl/7.88.1\n> Accept: */*\n> \n< HTTP/1.1 200 OK\n< Age: 543210\n< Cache-Control: max-age=604800\n< Content-Type: text/html; charset=UTF-8\n< Content-Length: 1256</code></pre><p>3. Извлечени параметри:</p><ul><li><strong>IP адрес и порт:</strong> <code>93.184.216.34</code>, порт <code>80</code> (стандартен незащитен HTTP порт).</li><li><strong>Start-line на заявка:</strong> <code>GET / HTTP/1.1</code> (Метод: GET, Път: /, Версия: HTTP/1.1).</li><li><strong>Content-Type:</strong> <code>text/html; charset=UTF-8</code> (HTML документ с UTF-8 кодиране).</li><li><strong>Статус код и текст:</strong> <code>200 OK</code> (Заявката е обслужена успешно).</li></ul>', 28, 21),
(5, 2, 'Самостоятелна практическа задача: Дебъгване и конструиране на HTTP заявки', '<p><strong>Условие:</strong></p><p>Вие сте младши разработчик в софтуерна компания и трябва да тествате отдалечен тестов уеб сървър <code>httpbin.org</code> чрез командния ред и браузъра.</p><p>Изпълнете следните подзадачи и запишете отговорите в текстов отчет:</p><ol><li><strong>DNS резолюция:</strong> Чрез командата <code>nslookup httpbin.org</code> определете поне един от публичните IP адреси на сървъра.</li><li><strong>Извличане само на заглавки (HEAD заявка):</strong> Използвайте командата <code>curl -I http://httpbin.org/get</code>. Запишете стойността на върнатия <code>Server</code> хедър и статус кода.</li><li><strong>Специфициране на клиентски хедъри:</strong> Изпратете GET заявка към <code>http://httpbin.org/headers</code> с добавен персонализиран хедър <code>X-Student-Id: 12A-15</code> чрез флага <code>-H</code> на cURL. Проверете дали сървърът отразява вашия хедър в JSON тялото на отговора.</li><li><strong>Симулация на грешка 404:</strong> Опитайте да достъпите несъществуващ маршрут <code>http://httpbin.org/unknown-page</code> и анализирайте първия ред на HTTP отговора.</li></ol>', '<p><strong>Примерно решение и критерии за оценка:</strong></p><p>1. Резултат от <code>nslookup httpbin.org</code>:</p><pre><code>Non-authoritative answer:\nName:    httpbin.org\nAddresses:  54.160.105.15, 34.206.56.120</code></pre><p>2. Резултат от <code>curl -I http://httpbin.org/get</code>:</p><pre><code>HTTP/1.1 200 OK\nDate: Mon, 14 Sep 2026 08:45:12 GMT\nContent-Type: application/json\nContent-Length: 308\nConnection: keep-alive\nServer: gunicorn/19.9.0\nAccess-Control-Allow-Origin: *</code></pre><p><em>Сървър:</em> gunicorn/19.9.0; <em>Статус:</em> 200 OK.</p><p>3. Изпращане на персонализиран хедър:</p><pre><code>curl -H \"X-Student-Id: 12A-15\" http://httpbin.org/headers</code></pre><p><em>Очакван фрагмент в тялото на отговора:</em></p><pre><code>{\\n  \"headers\": {\\n    \"Accept\": \"*/*\",\\n    \"Host\": \"httpbin.org\",\\n    \"User-Agent\": \"curl/7.88.1\",\\n    \"X-Student-Id\": \"12A-15\"\\n  }\\n}</code></pre><p>4. Резултат при липсващ ресурс:</p><pre><code>curl -I http://httpbin.org/unknown-page\nHTTP/1.1 404 NOT FOUND</code></pre><p>Статус кодът 404 указва, че сървърът е достъпен и функционира, но заявеният URI не съответства на наличен ресурс.</p>', 29, 21),
(6, 3, 'Мини-викторина за проверка (Post-Assessment)', '<p><strong>Отговорете на следните въпроси:</strong></p><p>1. В кой слой на модела TCP/IP оперира протоколът HTTP?<br>A) Мрежов достъп<br>Б) Интернет слой (IP)<br>В) Транспортен слой (TCP)<br>Г) Приложен слой (Application)</p><p>2. Кой ред представлява валиден начален ред (Request-line) на клиентска HTTP/1.1 заявка?<br>A) <code>HTTP/1.1 200 OK</code><br>Б) <code>GET /products/list HTTP/1.1</code><br>В) <code>Host: myshop.bg:80</code><br>Г) <code>Content-Type: application/json</code></p><p>3. Какво задължително разделя HTTP заглавките (headers) от тялото на съобщението (body)?<br>A) Символът за край на файл (EOF)<br>Б) Празен ред (двойно CRLF / \\\\r\\\\n\\\\r\\\\n)<br>В) Двоеточие ( : )<br>Г) Заглавката <code>Content-Length: 0</code></p>', '<p><strong>Верни отговори и методическа обосновка:</strong></p><p><strong>1. Верен отговор: Г) Приложен слой (Application).</strong><br><em>Обосновка:</em> HTTP определя формата на съобщенията между клиентски софтуер (браузър) и уеб сървър, използвайки услугите на транспортния слой (TCP) под него.</p><p><strong>2. Верен отговор: Б) GET /products/list HTTP/1.1.</strong><br><em>Обосновка:</em> Стартовият ред на заявка съдържа точно три части, разделени с интервал: HTTP метод, относителен път към ресурса (URI) и версията на протокола. Отговор А е Status-line на отговор, а В и Г са хедъри.</p><p><strong>3. Верен отговор: Б) Празен ред (двойно CRLF / \\\\r\\\\n\\\\r\\\\n).</strong><br><em>Обосновка:</em> По стандарт RFC 7230 празен ред уведомява парсера на сървъра/клиента, че списъкът с метаданни (хедъри) е приключил и следващите байтове принадлежат на полезния товар (body).</p>', 31, 21),
(7, 4, 'Домашна работа / Предизвикателство: Изследване на мрежовия стек на реално приложение', '<p><strong>Условие на заданието за домашна работа:</strong></p><ol><li>Отворете браузър по избор и заредете произволен новинарски или технологичен уебсайт с отворен панел <strong>Developer Tools -> Network</strong>.</li><li>Филтрирайте само първата (основната) заявка от тип <code>Doc</code> (HTML документа) и направете екранна снимка на секцията <em>Headers</em>.</li><li>В текстов файл опишете ролята на следните извлечени параметри от вашия сайт:<ul><li>Status Code (напр. 200, 304);</li><li>Response Header: <code>Content-Type</code>;</li><li>Response Header: <code>Content-Encoding</code> (напр. gzip, br);</li><li>Request Header: <code>User-Agent</code>.</li></ul></li><li><em>Предизвикателство за отлична оценка:</em> Обяснете защо браузърът изпраща десетки допълнителни HTTP заявки веднага след получаването на първия HTML файл.</li></ol>', '<p><strong>Указания за проверка и оценяване:</strong></p><ul><li><strong>Критерий 1:</strong> Коректно експортирани хедъри и точно определяне на значението на <code>Content-Type</code> (определя MIME типа за интерпретация от браузъра) и <code>Content-Encoding</code> (указва алгоритъма за компресия на данните в мрежата за спестяване на трафик).</li><li><strong>Критерий 2:</strong> Точно разбиране на <code>User-Agent</code> като низ, идентифициращ браузъра, операционната система и рендиращия енджин пред сървъра.</li><li><strong>Критерий 3 (Предизвикателство):</strong> Ученикът трябва да обясни, че браузърът парсира първоначалния HTML ред по ред и при срещане на външни ресурси (тагове <code>&lt;link rel=\"stylesheet\"&gt;</code>, <code>&lt;script src=\"...\"&gt;</code>, <code>&lt;img src=\"...\"&gt;</code>) инициира паралелни допълнителни HTTP заявки за изтегляне на CSS, JS и мултимедия.</li></ul>', 32, 21),
(12, 1, 'Съвместна задача: Обхват и първи задачи', '<p><strong>Задание:</strong> „Създайте локално приложение за ученик, което показва списък с учебни задачи и позволява добавяне на задача със заглавие. Заглавието не може да е празно след премахване на външните интервали. За първата версия не са необходими регистрация, срокове и известия.“</p><ol><li>Определете потребителя и целта.</li><li>Отделете задължителното от дейностите извън обхвата.</li><li>Формулирайте един въпрос за уточняване.</li><li>Опишете две начални задачи с отговорник, резултат и критерий за приемане.</li></ol><p>Работете заедно с учителя. Не е необходимо програмиране на приложението.</p>', '<p><strong>Стъпка 1 — потребител и цел:</strong> Потребителят е ученик. Целта е да подрежда учебните си задачи чрез прост списък.</p><p><strong>Стъпка 2 — обхват:</strong> Включени са показване на списък, добавяне на задача и проверка за непразно заглавие. Ограничението е локална работа. Изключени са регистрация, срокове и известия.</p><p><strong>Стъпка 3 — уточняване:</strong> „Трябва ли задачите да се запазват след затваряне на приложението?“ Текстът не дава достатъчно информация; не приемаме автоматично отговор.</p><p><strong>Стъпка 4 — начални задачи:</strong></p><table><thead><tr><th>Задача и отговорник</th><th>Резултат</th><th>Критерий за приемане</th></tr></thead><tbody><tr><td>Участник 1: Скициране на основния екран</td><td>Една скица</td><td>Показани са списък, поле за заглавие, бутон за добавяне и място за грешка.</td></tr><tr><td>Участник 2: Описание на проверки за заглавието</td><td>Таблица с три тестови примера</td><td>Има непразно заглавие с очаквано приемане, празен текст с отказ и само интервали с отказ.</td></tr></tbody></table><p><strong>Стъпка 5 — проверка:</strong> И двете задачи започват със статус „Предстои“. Преглеждащият ги приема след сравнение с критериите. Скицата и тестовите примери са подготвителни резултати, а не доказателство за вече работещо приложение.</p>', 46, 4),
(13, 2, 'Практическа задача: Екипен старт и индивидуален билет', '<p><strong>Контекст:</strong> Използвайте получения от учителя вариант А, Б или В. За всички варианти се предават еднакви по структура документи.</p><p><strong>Част А — самостоятелна екипна работа, 15 минути:</strong></p><ol><li>Попълнете състава, началните роли и четири правила за взаимодействие.</li><li>Запишете потребителя и целта с едно изречение.</li><li>Посочете трите задължителни функционалности, правилата за входните данни, ограниченията и поне две изключени функционалности.</li><li>Запишете поне един въпрос към възложителя.</li><li>Създайте минимум четири начални задачи. Всяка трябва да има водещ отговорник, конкретен резултат, проверим критерий и статус. Всеки участник трябва да има поне една задача.</li></ol><p><strong>Част Б — Ти правиш сам, 8 минути:</strong> Без съвети от съекипници напишете: своята роля и две отговорности; целта и потребителя; три функционалности в обхвата; две извън него; една лична начална задача с резултат и критерий; един въпрос за уточняване. Можете да четете оригиналното задание, но не и да преписвате екипния документ.</p><p><strong>Последни 2 минути:</strong> Предайте общия документ и отделните индивидуални билети. Не разработвайте завършен софтуер в рамките на тази задача.</p>', '<p><strong>Примерно екипно решение за задание А:</strong> Екип „Книга“, четирима участници. Използваните по-долу имена са примерни.</p><ul><li>Ани — координатор: следи задачите и времето.</li><li>Борис — отговорник по изискванията: описва обхвата и въпросите.</li><li>Виктор — отговорник по интерфейса и техническото планиране: подготвя екраните и полетата.</li><li>Деси — отговорник по качеството и документацията: подготвя проверките и подрежда общите материали.</li></ul><p><strong>Четири правила:</strong> изслушваме всяко предложение; записваме решенията в общия документ; съобщаваме затрудненията своевременно; отбелязваме „Готово“ само след преглед по критерия.</p><p><strong>Цел и потребител:</strong> Отговорникът за учебния библиотечен кът поддържа и намира информация за наличните учебни книги.</p><p><strong>В обхвата:</strong> списък с книги; добавяне на книга; търсене по част от заглавието без значение на регистъра. Заглавието и авторът са непразни след премахване на външните интервали; годината е цяло число от 1450 до текущата година.</p><p><strong>Ограничения:</strong> локална работа и учебни данни. <strong>Извън обхвата:</strong> заемане, регистрация и плащане. <strong>Въпрос:</strong> „Разрешени ли са повтарящи се записи с еднакво заглавие и автор?“</p><table><thead><tr><th>Задача и отговорник</th><th>Резултат и критерий за приемане</th><th>Статус</th></tr></thead><tbody><tr><td>Ани: Организиране на началната дъска</td><td>Дъска с четири задачи; всяка има отговорник, резултат, критерий и допустим статус.</td><td>Предстои</td></tr><tr><td>Борис: Описване на обхвата</td><td>Карта с потребител, цел, трите функции, правилата, ограниченията, изключенията и въпроса за дублиране.</td><td>Предстои</td></tr><tr><td>Виктор: Скициране на списък и форма</td><td>Скица със списък, търсене, полета за заглавие, автор и година, бутон и място за грешка.</td><td>Предстои</td></tr><tr><td>Деси: Подготовка на тестови примери</td><td>Таблица с валидно добавяне, празно заглавие, бъдеща година и търсене; всеки пример има очакван резултат.</td><td>Предстои</td></tr></tbody></table><p><strong>Примерни тестови данни за планиране, не отчет за изпълнени софтуерни тестове:</strong></p><ul><li>„Под игото“, „Иван Вазов“, 1894 → приемане.</li><li>Заглавие от три интервала, „Иван Вазов“, 1894 → отказ за празно заглавие.</li><li>„Учебна книга“, „Примерен автор“, текущата година + 1 → отказ за бъдеща година.</li><li>При налична книга „Под игото“, търсене „ИГО“ → книгата присъства в резултатите.</li></ul><p><strong>Примерен индивидуален билет на Деси:</strong> „Моята роля е отговорник по качеството и документацията. Проверявам критериите и подреждам тестовите примери. Потребителят е отговорникът за учебния библиотечен кът; целта е поддържане и намиране на информация за книгите. Включени са списък, добавяне и търсене. Изключени са заемане и плащане. Моята задача е таблица с тестови примери; тя е приета, когато съдържа четирите договорени случая и очакван резултат за всеки. Трябва да уточним дали се разрешават повтарящи се записи.“</p><p><strong>Ориентири за другите варианти:</strong> При Б се планират списък, добавяне и търсене на клубове; пример за отказ е празно помещение. При В се планират списък, добавяне и търсене на ресурси; пример за отказ е вид „аудио“, който не е сред разрешените. Ролите, структурата на документите и критериите за оценяване остават същите.</p>', 47, 4),
(14, 3, 'Мини-викторина: Роли, обхват и приемане', '<p><strong>1. Изберете един отговор.</strong> Кое най-точно описва началната роля на координатора?</p><p>а) Пише сам целия код.<br>б) Следи организацията и задачите и подпомага общуването.<br>в) Освобождава останалите от отговорност.</p><p><strong>2. Изберете един отговор.</strong> Заданието изрично изключва регистрация, но екипът иска да я добави. Какво е правилното действие?</p><p>а) Започва веднага, защото идеята е интересна.<br>б) Премахва друга задължителна функция без съгласуване.<br>в) Записва предложението и иска одобрение, без засега да променя договорения обхват.</p><p><strong>3. Изберете един отговор.</strong> Кой критерий за приемане е проверим?</p><p>а) Екранът трябва да е страхотен.<br>б) Скицата показва списък, поле за търсене и бутон за добавяне.<br>в) Участникът е работил много.</p><p><strong>4. Кратък отговор.</strong> Заданието не уточнява дали са позволени дублиращи се записи. Как трябва да постъпи екипът?</p>', '<p><strong>1. б) — 1 точка.</strong> Координаторът подпомага организацията, но не замества индивидуалния принос на останалите.</p><p><strong>2. в) — 1 точка.</strong> Допълнителна идея не променя автоматично одобрения обхват; необходимо е съгласуване с възложителя.</p><p><strong>3. б) — 1 точка.</strong> Посочените елементи могат да бъдат наблюдавани и проверени. Положеният труд сам по себе си не доказва изпълнен критерий.</p><p><strong>4. Примерен отговор — 1 точка:</strong> „Записваме въпроса и го отправяме към учителя като възложител; не приемаме собственото предположение за одобрено изискване.“ За точката са необходими както отбелязване на неяснотата, така и търсене на уточнение.</p><p><strong>Максимум:</strong> 4 точки. Ориентир за усвояване: минимум 3 точки.</p>', 49, 4),
(15, 4, 'Домашна работа: Моята първа задача в екипа', '<p>Подгответе индивидуална карта до една страница за своята начална задача. Предайте я до началото на следващото занятие като текстов документ или на хартия. Ориентировъчно време: 15–20 минути.</p><ol><li>Посочете екипа, варианта на заданието, ролята си и конкретната задача.</li><li>Обяснете кое изискване от заданието подпомага задачата.</li><li>Разпишете три стъпки за изпълнение.</li><li>Опишете очаквания резултат и два проверими критерия за приемане.</li><li>Посочете един риск или зависимост и начин за реакция.</li><li>Предложете една допълнителна функция и обяснете защо тя не влиза автоматично в текущия обхват.</li></ol><p><strong>Предизвикателство по избор:</strong> Променете непълната задача в демонстрационния Python код така, че да премине проверката. Обяснете защо успешният изход на програмата не доказва, че задачата е изпълнена.</p>', '<p><strong>Пример за задание А:</strong> Екип „Книга“; роля — отговорник по интерфейса и техническото планиране; задача — скица на списъка и формата. Задачата подпомага изискванията за показване, добавяне и търсене на книги.</p><p><strong>Три стъпки:</strong> 1. Извличам необходимите полета и действия от заданието. 2. Начертавам списък и форма. 3. Сравнявам скицата с изискванията и я предоставям за преглед.</p><p><strong>Резултат:</strong> Една четлива скица на хартия или в документ. <strong>Критерий 1:</strong> показани са списък, поле за търсене и форма със заглавие, автор и година. <strong>Критерий 2:</strong> показани са бутон за добавяне и място за съобщение при невалидни данни.</p><p><strong>Риск:</strong> Неясното поведение при дублирана книга може да изисква допълнително съобщение. <strong>Реакция:</strong> записвам въпроса и търся уточнение от учителя, преди да го представя като окончателно поведение.</p><p><strong>Допълнителна идея:</strong> заемане на книги. Не я включвам автоматично, защото е изрично извън първата версия и изисква нови правила и данни.</p><p><strong>Решение на предизвикателството:</strong> Във втората задача попълвам <code>owner</code> с „Участник 2“, а <code>acceptance</code> с „Описани са полетата тема и дата и е отбелязано кои са задължителни.“ Програмата отчита попълнен запис. Тя не проверява съществуването на готовия документ или неговата правилност.</p><p><strong>Проверка на домашната работа:</strong> Търсят се връзка със заданието, изпълними стъпки, два наблюдаеми критерия, реалистична реакция при затруднение и разграничение между договорен обхват и предложение.</p>', 50, 4);

-- --------------------------------------------------------

--
-- Структура на таблица `main_sessiontopic`
--

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
(20, '', 20, 23),
(21, 'Основни концепции за Интернет, мрежови протоколи и анатомия на HTTP съобщението.', 21, 26),
(22, 'Класификация и семантика на HTTP методите и статус кодовете.', 22, 27),
(23, 'Взаимодействие клиент-сървър и синхронен модел на комуникация.', 23, 28),
(24, 'Синтаксис на HTML, вложеност на елементи и основни тагове за маркиране.', 24, 29),
(25, 'Синтаксис на CSS, видове селектори и свойства на боксовия модел.', 25, 30),
(26, 'Инструменти за разработчици: инспектиране на стилове, дебъгване и мрежов мониторинг.', 26, 31),
(27, 'Структуриране на HTML формуляри и видове контроли за въвеждане на данни.', 27, 32),
(28, 'Семантично структуриране на HTML5 съдържание и принципи на достъпност.', 28, 33),
(29, 'Съвременни оформления чрез Flexbox, Grid и правила за медийни заявки.', 29, 34),
(30, 'Интегриране на семантична структура в реален проект.', 30, 33),
(31, 'Практическа адаптация за мобилни, таблетни и настолни устройства.', 30, 34),
(32, 'Основи на езика JavaScript, типове данни, масиви и обекти.', 31, 35),
(33, 'Работа със събития и интерактивност в клиентската част.', 32, 35),
(34, 'Принципи на DOM архитектурата и достъп до възлите на документа.', 32, 36),
(35, 'Програмно създаване и премахване на DOM елементи и интерактивна логика.', 33, 36),
(36, 'Семантично оформление на модула.', 34, 29),
(37, 'Стилизиране и визуална йерархия.', 34, 30),
(38, 'Динамично поведение и DOM управление.', 34, 36),
(39, 'Проверка на знанията за HTTP заявки и клиент-сървър комуникация.', 35, 27),
(40, 'Проверка на уменията за изграждане и валидиране на HTML формуляри.', 35, 32),
(41, 'Проверка на практическото използване на JavaScript събития.', 35, 35),
(42, 'Архитектура на MVC модела и маршрутизация на заявки.', 36, 37),
(43, 'Интеграция на база данни в уеб приложение и сигурен обмен на данни чрез SQL.', 37, 38),
(44, 'Архитектура на ORM системите, дефиниране на модели и схеми.', 38, 39),
(45, 'Реализация на операции по вмъкване и извличане на данни в MVC среда.', 39, 40),
(46, 'Сървърни алгоритми за модификация и премахване на ресурси.', 40, 40),
(47, 'Използване на шаблонни енджини за генерация на динамичен HTML.', 41, 41),
(48, 'Механизми за управление на бисквитки и съхранение на сесии на сървъра.', 42, 42),
(49, 'Концепции и алгоритми за потребителска автентикация и контрол на достъпа.', 43, 43),
(50, 'Анализ на уязвимостите в сигурността на уеб приложения и практики за сигурно програмиране.', 44, 44),
(51, 'Принципи на REST архитектурата и стандарти за изграждане на уеб услуги.', 45, 45),
(52, 'Работа с JSON и XML формати за обмен на данни през REST API.', 46, 46),
(53, 'Асинхронно извличане и изпращане на данни от front-end към back-end REST услуги.', 47, 47),
(54, 'Сървърна организация и бизнес логика.', 48, 37),
(55, 'Интегриране на REST API точки.', 48, 45),
(56, 'Асинхронна комуникация с клиентския интерфейс.', 48, 47),
(57, 'Оценка на реализираните CRUD операции и база данни.', 49, 40),
(58, 'Оценка на механизма за автентикация и защита на ресурсите.', 49, 43),
(59, 'Оценка на асинхронната интеграция между клиент и сървър.', 49, 47);

-- --------------------------------------------------------

--
-- Структура на таблица `main_specialty`
--

CREATE TABLE `main_specialty` (
  `id` bigint(20) NOT NULL,
  `specialty_num` varchar(8) NOT NULL,
  `specialty_name` varchar(100) NOT NULL,
  `level` smallint(5) UNSIGNED NOT NULL CHECK (`level` >= 0),
  `specialty_type` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Схема на данните от таблица `main_specialty`
--

INSERT INTO `main_specialty` (`id`, `specialty_num`, `specialty_name`, `level`, `specialty_type`) VALUES
(1, '4810301', 'Приложно програмиране', 3, 'специалност'),
(2, '1', '2', 3, 'специалност'),
(3, '4810201', 'Системно програмиране', 3, 'специалност'),
(4, '6666', '77777', 3, 'специалност'),
(5, '4444', '555555', 3, 'професия');

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
(20, 1, 4),
(21, 1, 5),
(23, 1, 6);

-- --------------------------------------------------------

--
-- Структура на таблица `main_subject`
--

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
(2, 'Интернет програмиране ПП', 12, 'практика', 116, 29, 4, 4, NULL),
(4, 'Конкурентно програмиране', 11, 'теория', 18, 18, 0, 1, 1),
(5, 'Конкурентно програмиране', 11, 'практика', 36, 18, 0, 2, 1),
(6, 'Нов учебен предмет', 10, 'теория', 72, 36, 2, 2, NULL);

-- --------------------------------------------------------

--
-- Структура на таблица `main_topic`
--

CREATE TABLE `main_topic` (
  `id` bigint(20) NOT NULL,
  `num` smallint(6) NOT NULL,
  `name` varchar(200) NOT NULL,
  `MoSCoW_cat` varchar(1) NOT NULL,
  `MoSCoW_rem` longtext NOT NULL,
  `unit_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Схема на данните от таблица `main_topic`
--

INSERT INTO `main_topic` (`id`, `num`, `name`, `MoSCoW_cat`, `MoSCoW_rem`, `unit_id`) VALUES
(16, 1, 'Конкурентност. Изпълнение на програма. Процес.', 'M', 'Фундаментални понятия. Без разбиране какво е процес и как се изпълнява програмата, не може да се премине към паралелизъм.', 4),
(17, 2, 'Видове блокиращи операции.', 'S', 'Важно е да разберат защо програмата \"забива\" (напр. при изчакване на база данни или мрежа), но не е нужно задълбочаване във всички хардуерни/софтуерни I/O детайли.', 4),
(18, 1, 'Нишка. Връзка между процес и нишка.', 'M', 'Критична разлика за разбирането на споделената памет и ресурсите на операционната система.', 5),
(19, 2, 'Създаване на нишки.', 'M', 'Абсолютно задължително за практическите задачи и прехода към реално кодене.', 5),
(20, 3, 'Управление на нишки. Споделена памет между нишки.', 'M', 'Ядрото на конкурентното програмиране. Без това учениците не могат да създадат работещо многонишково приложение.', 5),
(21, 4, 'Проблеми при работа с нишки - Race conditions, Deadlocks', 'M', 'Най-честите и фатални грешки при споделена памет. Задължително е да знаят как да ги избягват (синхронизация/заключване).', 5),
(22, 1, 'Работа с асинхронни операции. Обещания (Promise/Task)', 'M', 'Гръбнакът на модерното програмиране (особено в C#, Java и JS, които се препоръчват в програмата).', 6),
(23, 3, 'Работа с асинхронни операции чрез async/await и др. механизми за реализиране на асинхронни операции', 'M', 'Де факто индустриалният стандарт за писане на чист и четим асинхронен код днес. Задължително практическо умение.', 6),
(24, 5, 'Проблеми при работа с нишки - Livelocks, Starvation', 'S', 'Сравнително сложни концепции за 11. клас. Добре е да се споменат информативно, ако остане време, но не са фатални за базовото ниво.', 5),
(25, 2, 'Обратни извиквания (Callback)', 'C', 'Исторически важно и се среща в по-стар код, но често води до \"callback hell\". Може да се прегледа по-бързо в полза на съвременните методи.', 6),
(26, 1, 'Основни на интернет. Мрежови протоколи. HTTP', 'M', 'Базови понятия за Интернет и HTTP; фундамент за разбиране на уеб комуникацията и покрива основните изисквания на ДОС.', 7),
(27, 2, 'Видове HTTP заявки', 'M', 'Критично знание за работа с уеб ресурси и формиране на разбиране за клиент-сървър обмена.', 7),
(28, 3, 'Клиент - сървър комуникация', 'M', 'Основен архитектурен модел в уеб разработката; необходим за всички следващи front-end и back-end теми.', 7),
(29, 1, 'Работа с HTML. Основни тагове', 'M', 'Фундаментален синтаксис за изграждане на уеб страници; задължителна основа за front-end разработка.', 8),
(30, 2, 'Работа със CSS. Селектори и основни правила', 'M', 'Необходима основа за оформление и визуално представяне на съдържание в уеб страници.', 8),
(31, 3, 'Работа с инструментите за разработчици на съвременните уеб браузъри', 'S', 'Важна практическа тема за диагностика, тестване и отстраняване на грешки, но стъпва върху базовите знания.', 8),
(32, 4, 'Създаване на формуляри', 'M', 'Ключово за въвеждане и изпращане на данни към сървъра; пряко свързано с основните очаквани резултати.', 8),
(33, 5, 'Създаване на семантични страници', 'S', 'Подобрява правилното структуриране, достъпността и добрите практики при разработка на HTML страници.', 8),
(34, 6, 'Създаване на адаптивно (responsive) оформление на страници', 'S', 'Съществено за съвременната практика и приложимостта на уеб сайтовете на различни устройства.', 8),
(35, 7, 'Увод в JavaScript. Работа с обекти и събития', 'M', 'Осигурява основата за интерактивност и динамично поведение на клиентската част.', 8),
(36, 8, 'Принципи на DOM. Манипулиране на DOM', 'S', 'Важна тема за практическо управление на съдържанието и поведението на страницата чрез JavaScript.', 8),
(37, 1, 'Работа с MVC концепцията - модел, изглед, контролер', 'M', 'Основен архитектурен принцип за организиране на уеб приложения и за разбиране на сървърната логика.', 9),
(38, 2, 'Комуникация на БД в уеб приложение', 'M', 'Фундаментално умение за свързване на приложение с данни и за реализиране на динамично съдържание.', 9),
(39, 3, 'Работа с ORM (обектно-релационно съпоставящи) системи', 'S', 'Важна съвременна практика за работа с бази данни, но надгражда базовата директна комуникация с БД.', 9),
(40, 4, 'Реализиране на CRUD операции', 'M', 'Ключово практическо умение за създаване, четене, редакция и изтриване на данни в уеб приложение.', 9),
(41, 5, 'Създаване на шаблонни изгледи', 'S', 'Подобрява повторната употреба и организацията на потребителския интерфейс в сървърно генерирани приложения.', 9),
(42, 6, 'Управление на сесии и бисквитки', 'S', 'Важно за поддържане на състояние и персонализация в уеб приложенията.', 9),
(43, 7, 'Автентикация и авторизация', 'M', 'Критично за защитен достъп и управление на потребителски права; пряко свързано със сигурността.', 9),
(44, 8, 'Често срещани уязвимости в сигурността на уеб приложенията', 'M', 'Задължителна тема за безопасна разработка и за формиране на базова култура по киберсигурност.', 9),
(45, 1, 'Принципи на REST API. Създаване на собствено REST API.', 'M', 'Фундаментална тема за съвременна интеграция между системи и за изграждане на уеб услуги.', 10),
(46, 2, 'Работа с REST API в JSON/XML формат', 'S', 'Важна за практическа съвместимост и обмен на данни, като JSON е основен, а XML има допълваща роля.', 10),
(47, 3, 'Консумиране на REST API от външния интерфейс (front-end) с помощта на AJAX', 'S', 'Съществено практическо умение за свързване на front-end и back-end чрез асинхронна комуникация.', 10);

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

--
-- Схема на данните от таблица `main_unit`
--

INSERT INTO `main_unit` (`id`, `num`, `name`, `subject_id`, `hours`) VALUES
(4, 1, 'Конкурентност и блокиращи операции', 4, 4),
(5, 2, 'Нишки', 4, 8),
(6, 3, 'Асинхронни операции', 4, 4),
(7, 1, 'Въведение в Интернет, мрежови протоколи и модел „Клиент - сървър”', 1, 6),
(8, 2, 'Разработка на външен интерфейс (front-end) на уеб приложения', 1, 20),
(9, 3, 'Разработка на сървърната част (back-end) на уеб приложения', 1, 20),
(10, 4, 'Създаване и работа с REST API', 1, 8);

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
  `subject_id` bigint(20) DEFAULT NULL,
  `session_id` bigint(20) DEFAULT NULL,
  `grade` smallint(5) UNSIGNED NOT NULL CHECK (`grade` >= 0),
  `section` varchar(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Схема на данните от таблица `main_userprofile`
--

INSERT INTO `main_userprofile` (`id`, `gender`, `access_level`, `session_screen`, `school_id`, `speciality_id`, `user_id`, `subject_id`, `session_id`, `grade`, `section`) VALUES
(1, 1, 1, 1, 1, 1, 1, 1, 21, 11, 'а'),
(2, 1, 3, 1, 1, NULL, 2, NULL, NULL, 11, 'а'),
(3, 1, 4, 1, 1, 1, 3, 4, 10, 11, 'а'),
(4, 1, 3, 1, 1, NULL, 4, NULL, NULL, 11, 'а'),
(5, 1, 5, 1, 1, 1, 5, NULL, NULL, 12, 'б'),
(6, 1, 5, 1, 1, 1, 6, NULL, NULL, 10, 'б'),
(7, 1, 5, 1, 1, 3, 7, NULL, NULL, 10, 'б'),
(9, 1, 3, 1, 1, 1, 9, 2, NULL, 8, 'а'),
(10, 1, 4, 1, 1, NULL, 10, NULL, NULL, 8, 'а');

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
-- Индекси за таблица `main_aiprompt`
--
ALTER TABLE `main_aiprompt`
  ADD PRIMARY KEY (`id`),
  ADD KEY `main_aiprompt_created_by_id_07047b1d_fk_auth_user_id` (`created_by_id`),
  ADD KEY `main_aiprompt_page_key_d90f54b9` (`page_key`);

--
-- Индекси за таблица `main_appattachment`
--
ALTER TABLE `main_appattachment`
  ADD PRIMARY KEY (`id`),
  ADD KEY `main_appattachment_created_by_id_dac4c7d3_fk_auth_user_id` (`created_by_id`);

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
-- Индекси за таблица `main_schooldayconfig`
--
ALTER TABLE `main_schooldayconfig`
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
-- Индекси за таблица `main_sessionattachment`
--
ALTER TABLE `main_sessionattachment`
  ADD PRIMARY KEY (`id`),
  ADD KEY `main_sessionattachment_point_id_3ef7b715_fk_main_sessionpoint_id` (`point_id`),
  ADD KEY `main_sessionattachment_session_id_2a327f6c_fk_main_session_id` (`session_id`);

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=121;

--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=73;

--
-- AUTO_INCREMENT for table `main_aiprompt`
--
ALTER TABLE `main_aiprompt`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `main_appattachment`
--
ALTER TABLE `main_appattachment`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `main_documents`
--
ALTER TABLE `main_documents`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `main_goal`
--
ALTER TABLE `main_goal`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

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
-- AUTO_INCREMENT for table `main_schooldayconfig`
--
ALTER TABLE `main_schooldayconfig`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `main_school_specialities`
--
ALTER TABLE `main_school_specialities`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `main_session`
--
ALTER TABLE `main_session`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=79;

--
-- AUTO_INCREMENT for table `main_sessionattachment`
--
ALTER TABLE `main_sessionattachment`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `main_sessionnote`
--
ALTER TABLE `main_sessionnote`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `main_sessionpoint`
--
ALTER TABLE `main_sessionpoint`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=51;

--
-- AUTO_INCREMENT for table `main_sessiontask`
--
ALTER TABLE `main_sessiontask`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `main_sessiontopic`
--
ALTER TABLE `main_sessiontopic`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=94;

--
-- AUTO_INCREMENT for table `main_specialty`
--
ALTER TABLE `main_specialty`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `main_specialty_subjects`
--
ALTER TABLE `main_specialty_subjects`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT for table `main_subject`
--
ALTER TABLE `main_subject`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `main_topic`
--
ALTER TABLE `main_topic`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=66;

--
-- AUTO_INCREMENT for table `main_unit`
--
ALTER TABLE `main_unit`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `main_userprofile`
--
ALTER TABLE `main_userprofile`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

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
-- Ограничения за таблица `main_aiprompt`
--
ALTER TABLE `main_aiprompt`
  ADD CONSTRAINT `main_aiprompt_created_by_id_07047b1d_fk_auth_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `auth_user` (`id`);

--
-- Ограничения за таблица `main_appattachment`
--
ALTER TABLE `main_appattachment`
  ADD CONSTRAINT `main_appattachment_created_by_id_dac4c7d3_fk_auth_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `auth_user` (`id`);

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
-- Ограничения за таблица `main_sessionattachment`
--
ALTER TABLE `main_sessionattachment`
  ADD CONSTRAINT `main_sessionattachment_point_id_3ef7b715_fk_main_sessionpoint_id` FOREIGN KEY (`point_id`) REFERENCES `main_sessionpoint` (`id`),
  ADD CONSTRAINT `main_sessionattachment_session_id_2a327f6c_fk_main_session_id` FOREIGN KEY (`session_id`) REFERENCES `main_session` (`id`);

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

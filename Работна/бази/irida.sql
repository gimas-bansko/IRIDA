-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1
-- Време на генериране:  4 септ 2025 в 21:53
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
(48, 'Can view Пофил на потребител', 12, 'view_userprofile');

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
(1, 'pbkdf2_sha256$600000$3iNEHTkQ6rkF6v46il2Dsp$wzYrjzST0uYMRVFUzIBCXDqFWdbed8vyiQCqZ39eB9o=', '2025-09-04 19:42:36.013385', 1, 'superadmin', '', '', '', 1, 1, '2025-09-04 19:41:42.360994');

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
(4, '2025-09-04 19:51:42.581630', '1', 'Потребител #1:  ', 2, '[{\"changed\": {\"fields\": [\"\\u0421\\u043f\\u0435\\u0446\\u0438\\u0430\\u043b\\u043d\\u043e\\u0441\\u0442\"]}}]', 12, 1);

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
(8, 'main', 'klass'),
(9, 'main', 'log'),
(10, 'main', 'school'),
(11, 'main', 'specialty'),
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
(19, 'sessions', '0001_initial', '2025-09-04 19:40:44.139625');

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
('i8dhvgopzdvup3k9cmjroa9e449itvk7', '.eJxVjEsOwjAMBe-SNYqckDoNS_Y9Q2XHDi2gVOpnhbg7VOoCtm9m3sv0tK1Dvy0696OYi3Hm9Lsx5YfWHcid6m2yearrPLLdFXvQxXaT6PN6uH8HAy3Dt4aEiBoK5aAJYgNAUBiRmaMQu9SAOJdbiS76tlDwuSCKtl5SOJOa9wflkTgu:1uuFqu:VwUMGiiQYqpCXtyQzgS9JAaqaC44RvXgd6K8d-rhAS4', '2025-09-18 19:42:36.017450');

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
-- Структура на таблица `main_klass`
--

CREATE TABLE `main_klass` (
  `id` bigint(20) NOT NULL,
  `grade` smallint(5) UNSIGNED DEFAULT NULL CHECK (`grade` >= 0),
  `section` varchar(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
(1, 1, 1);

-- --------------------------------------------------------

--
-- Структура на таблица `main_specialty`
--

CREATE TABLE `main_specialty` (
  `id` bigint(20) NOT NULL,
  `specialty_num` varchar(8) NOT NULL,
  `specialty_name` varchar(100) NOT NULL,
  `plan` varchar(100) NOT NULL,
  `level` smallint(5) UNSIGNED NOT NULL CHECK (`level` >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Схема на данните от таблица `main_specialty`
--

INSERT INTO `main_specialty` (`id`, `specialty_num`, `specialty_name`, `plan`, `level`) VALUES
(1, '481030', 'Приложен програмист', 'docs/4810301-В4_IGXD6UL.xlsx', 3);

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
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Схема на данните от таблица `main_userprofile`
--

INSERT INTO `main_userprofile` (`id`, `gender`, `access_level`, `session_screen`, `school_id`, `speciality_id`, `user_id`) VALUES
(1, 1, 5, 1, 1, 1, 1);

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
-- Индекси за таблица `main_specialty`
--
ALTER TABLE `main_specialty`
  ADD PRIMARY KEY (`id`);

--
-- Индекси за таблица `main_userprofile`
--
ALTER TABLE `main_userprofile`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`),
  ADD KEY `main_userprofile_school_id_74f42cf3_fk_main_school_id` (`school_id`),
  ADD KEY `main_userprofile_speciality_id_475d0b2d_fk_main_specialty_id` (`speciality_id`);

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=49;

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `main_documents`
--
ALTER TABLE `main_documents`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `main_klass`
--
ALTER TABLE `main_klass`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

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
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `main_specialty`
--
ALTER TABLE `main_specialty`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

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
-- Ограничения за таблица `main_school_specialities`
--
ALTER TABLE `main_school_specialities`
  ADD CONSTRAINT `main_school_speciali_specialty_id_78354343_fk_main_spec` FOREIGN KEY (`specialty_id`) REFERENCES `main_specialty` (`id`),
  ADD CONSTRAINT `main_school_specialities_school_id_9588fab6_fk_main_school_id` FOREIGN KEY (`school_id`) REFERENCES `main_school` (`id`);

--
-- Ограничения за таблица `main_userprofile`
--
ALTER TABLE `main_userprofile`
  ADD CONSTRAINT `main_userprofile_school_id_74f42cf3_fk_main_school_id` FOREIGN KEY (`school_id`) REFERENCES `main_school` (`id`),
  ADD CONSTRAINT `main_userprofile_speciality_id_475d0b2d_fk_main_specialty_id` FOREIGN KEY (`speciality_id`) REFERENCES `main_specialty` (`id`),
  ADD CONSTRAINT `main_userprofile_user_id_15c416f4_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

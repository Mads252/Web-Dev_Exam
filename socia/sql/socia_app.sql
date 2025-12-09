-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Vært: mariadb
-- Genereringstid: 09. 12 2025 kl. 18:35:42
-- Serverversion: 11.8.5-MariaDB-ubu2404
-- PHP-version: 8.2.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `socia_app`
--

-- --------------------------------------------------------

--
-- Struktur-dump for tabellen `admin_logs`
--

CREATE TABLE `admin_logs` (
  `log_id` char(32) NOT NULL,
  `admin_user_id_fk` char(32) NOT NULL,
  `target_user_id_fk` char(32) DEFAULT NULL,
  `target_post_id_fk` char(32) DEFAULT NULL,
  `action_type` varchar(50) NOT NULL,
  `reason` varchar(255) DEFAULT NULL,
  `created_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Struktur-dump for tabellen `comments`
--

CREATE TABLE `comments` (
  `comment_id` char(32) NOT NULL,
  `post_id_fk` char(32) NOT NULL,
  `user_id_fk` char(32) NOT NULL,
  `content` varchar(280) NOT NULL,
  `is_blocked` tinyint(1) NOT NULL DEFAULT 0,
  `is_deleted` tinyint(1) NOT NULL DEFAULT 0,
  `created_at` int(11) NOT NULL,
  `updated_at` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Data dump for tabellen `comments`
--

INSERT INTO `comments` (`comment_id`, `post_id_fk`, `user_id_fk`, `content`, `is_blocked`, `is_deleted`, `created_at`, `updated_at`) VALUES
('081b90ceb89e4f978deb6e8e6277537e', '2a151aa6cce7494694b631cd3133c640', 'b03bfbf476824e678cd065f4ce5510a6', 'lll', 0, 0, 1764620006, NULL),
('16473bc3cdc7430293fbcc4a07e6a312', '3257a0fa7a684d3084f3d9ee4b2cf0d2', 'b03bfbf476824e678cd065f4ce5510a6', 'd', 0, 1, 1764668485, NULL),
('2e7d696dcb914dccbb93e078a7510803', '3257a0fa7a684d3084f3d9ee4b2cf0d2', 'b03bfbf476824e678cd065f4ce5510a6', 'w', 0, 1, 1764668489, NULL),
('2f0aea3896be474dbc43af7293f8764e', 'fb2385c921224bc6b6df70d186090ed2', '9b18f018e87b468a8038b5fce6ecba54', 'fr', 0, 0, 1764836190, NULL),
('3993f0b38f1d4d02b6ca2f3b19ad749e', '567d03f29c35408997dec82c78f336fa', '9b18f018e87b468a8038b5fce6ecba54', 'dsd', 0, 0, 1764841294, NULL),
('43e2ddb7fd104a13a2fc780a1fa8b5ac', 'b5686f7fc5cc403caeacd496bf21f6df', '9b18f018e87b468a8038b5fce6ecba54', 'ewe', 0, 0, 1764847432, NULL),
('44987f5812bd4fd2ad02faab2c8cc90a', 'b5686f7fc5cc403caeacd496bf21f6df', '9b18f018e87b468a8038b5fce6ecba54', 'wewe', 0, 1, 1764847437, NULL),
('5187da0c661d4fd89eb1ab26d1983f6f', '3257a0fa7a684d3084f3d9ee4b2cf0d2', 'b03bfbf476824e678cd065f4ce5510a6', '12', 0, 1, 1764669247, NULL),
('524aa44fcfe943d0b36784067ac50183', '108171a70a964fdbb0510a64cd65d59b', '9b18f018e87b468a8038b5fce6ecba54', 'weq', 0, 1, 1764841361, NULL),
('55cd58a92580416a8d50bb13470eaca7', 'f27d7760f84c48f497b80ae61e4f6d36', 'b03bfbf476824e678cd065f4ce5510a6', 'halalalalallalalallalalalalalallalalalalalallaa', 0, 0, 1764749562, NULL),
('5750e51fc04440699941a178d8746012', '33046282d0534617afd96000065ac3fa', 'b03bfbf476824e678cd065f4ce5510a6', 'lll', 0, 0, 1764619998, NULL),
('590cbe14f319487d8f3a0f4cfce3e9d4', 'f27d7760f84c48f497b80ae61e4f6d36', 'b03bfbf476824e678cd065f4ce5510a6', '20', 0, 0, 1764749547, NULL),
('5acfced76c9840a0aaa956af9e2a00e3', 'f27d7760f84c48f497b80ae61e4f6d36', 'b03bfbf476824e678cd065f4ce5510a6', 'halalalalallalalallalalalalalallalalalalalallaa', 0, 0, 1764749559, NULL),
('741d8fa2f9b94881870f1e391c78d4f2', '3257a0fa7a684d3084f3d9ee4b2cf0d2', 'b03bfbf476824e678cd065f4ce5510a6', 'wewe', 0, 0, 1764620808, NULL),
('7dfed55fac0c4f14b294f95f0a8ecea0', '3257a0fa7a684d3084f3d9ee4b2cf0d2', 'b03bfbf476824e678cd065f4ce5510a6', 'wewe', 0, 0, 1764620804, NULL),
('93369231dcd0440a9de7b01e3a96616a', '3257a0fa7a684d3084f3d9ee4b2cf0d2', 'b03bfbf476824e678cd065f4ce5510a6', 'ew', 0, 1, 1764669308, NULL),
('9e0a0dcb90f343659e3f295445bf6760', 'f2d23ec9d0884bce9ede6e6acacc5397', '9b18f018e87b468a8038b5fce6ecba54', 'kom nu lidt', 0, 0, 1764145791, NULL),
('ad6f6bcf6990443b80f63a700381f252', '260ba315c08b416ab907d9c1d6469e21', '9b18f018e87b468a8038b5fce6ecba54', 'n', 0, 0, 1764847452, NULL),
('ada85cd41dc74777aae4c7b645f82b9a', 'f27d7760f84c48f497b80ae61e4f6d36', 'b03bfbf476824e678cd065f4ce5510a6', 'halalalalallalalallalalalalalallalalalalalallaa', 0, 0, 1764749555, NULL),
('cdc7a938ed0947a58fe86ab7e62aa653', 'bdb9b94c97ad42ff89663679344eaefd', 'b03bfbf476824e678cd065f4ce5510a6', 'wf', 0, 0, 1764670132, NULL),
('d304bec6d91c4c85b3f3a8ac2bf2f449', '3257a0fa7a684d3084f3d9ee4b2cf0d2', 'b03bfbf476824e678cd065f4ce5510a6', 'wewe', 0, 1, 1764620798, NULL),
('d768e748f73049bbbcd01a78f49b5377', '108171a70a964fdbb0510a64cd65d59b', '9b18f018e87b468a8038b5fce6ecba54', 'qergqer', 0, 0, 1765037813, NULL),
('e1b9ed8eaf1c49e1a62a9b63517e96da', '33046282d0534617afd96000065ac3fa', 'b03bfbf476824e678cd065f4ce5510a6', 'lll', 0, 0, 1764619987, NULL),
('e65769cca8244915a580d7fa512d0bed', 'f27d7760f84c48f497b80ae61e4f6d36', 'b03bfbf476824e678cd065f4ce5510a6', 'halalalalallalalallalalalalalallalalalalalallaa', 0, 0, 1764749560, NULL),
('e6f9b707694c481e91e7376b3a21631d', '3257a0fa7a684d3084f3d9ee4b2cf0d2', 'b03bfbf476824e678cd065f4ce5510a6', 'e', 0, 0, 1764668483, NULL),
('ea754a8a9eb64650ad9815b7789bb8fb', 'f2d23ec9d0884bce9ede6e6acacc5397', 'b03bfbf476824e678cd065f4ce5510a6', 'hej', 0, 0, 1764320426, NULL),
('fa26cd5434d74726a9c19e37593aeb25', '3257a0fa7a684d3084f3d9ee4b2cf0d2', 'b03bfbf476824e678cd065f4ce5510a6', '23', 0, 0, 1764669195, NULL);

-- --------------------------------------------------------

--
-- Struktur-dump for tabellen `email_verifications`
--

CREATE TABLE `email_verifications` (
  `verification_id` char(32) NOT NULL,
  `user_id_fk` char(32) NOT NULL,
  `token` char(64) NOT NULL,
  `expires_at` int(11) NOT NULL,
  `verified_at` int(11) DEFAULT NULL,
  `created_at` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Data dump for tabellen `email_verifications`
--

INSERT INTO `email_verifications` (`verification_id`, `user_id_fk`, `token`, `expires_at`, `verified_at`, `created_at`) VALUES
('13cbb86c4ebb491599c6d4bd5fc8d1ae', '1ba70766edd346a6a39022d396e2742c', '92021f6ac0b748848117855292fe7dc8', 1765124261, NULL, 1765037861),
('3158183c1dbc4da991a0d96dda9a2661', 'b03bfbf476824e678cd065f4ce5510a6', '97bec5243749417da9a9673eeee5e382', 1763718836, 1763632455, 1763632436),
('3eb1a397855a4880b0fa6b38c63578b2', '283d8aec2703404caa421a42e31ba11d', 'df1cce0e86bb43f2a22117e4f7cadaaf', 1764932907, 1764846648, 1764846507),
('7f641c6945314af2b004a85128420170', '9b18f018e87b468a8038b5fce6ecba54', 'd2e137997bd84e6fb56007c0c9c8d2b8', 1763629465, 1763543471, 1763543465);

-- --------------------------------------------------------

--
-- Struktur-dump for tabellen `follows`
--

CREATE TABLE `follows` (
  `follower_user_id_fk` char(32) NOT NULL,
  `followee_user_id_fk` char(32) NOT NULL,
  `created_at` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Data dump for tabellen `follows`
--

INSERT INTO `follows` (`follower_user_id_fk`, `followee_user_id_fk`, `created_at`) VALUES
('9b18f018e87b468a8038b5fce6ecba54', 'g789h01i23c4d5e6f7g8h9i0j1k2l3m4', 1764846991),
('b03bfbf476824e678cd065f4ce5510a6', '9b18f018e87b468a8038b5fce6ecba54', 1764150006);

-- --------------------------------------------------------

--
-- Struktur-dump for tabellen `likes`
--

CREATE TABLE `likes` (
  `user_id_fk` char(32) NOT NULL,
  `post_id_fk` char(32) NOT NULL,
  `created_at` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Data dump for tabellen `likes`
--

INSERT INTO `likes` (`user_id_fk`, `post_id_fk`, `created_at`) VALUES
('9b18f018e87b468a8038b5fce6ecba54', '260ba315c08b416ab907d9c1d6469e21', 1764674764),
('9b18f018e87b468a8038b5fce6ecba54', 'b3aab0195d5546b19c348c8921b0fd4e', 1765305214),
('b03bfbf476824e678cd065f4ce5510a6', '225a5b9160d64a5f9765d0026030692b', 1764922392),
('b03bfbf476824e678cd065f4ce5510a6', '9c870760cdd743d7acdb84abf257a394', 1764327630),
('b03bfbf476824e678cd065f4ce5510a6', 'c1dbcc5bf5ed46aab6b719c508bb6965', 1764321731),
('b03bfbf476824e678cd065f4ce5510a6', 'f2d23ec9d0884bce9ede6e6acacc5397', 1764324293);

-- --------------------------------------------------------

--
-- Struktur-dump for tabellen `password_resets`
--

CREATE TABLE `password_resets` (
  `reset_id` char(32) NOT NULL,
  `user_id_fk` char(32) NOT NULL,
  `token` char(64) NOT NULL,
  `expires_at` int(11) NOT NULL,
  `used_at` int(11) DEFAULT NULL,
  `created_at` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Data dump for tabellen `password_resets`
--

INSERT INTO `password_resets` (`reset_id`, `user_id_fk`, `token`, `expires_at`, `used_at`, `created_at`) VALUES
('404dbcedc79e48d6848292524a4d5988', '9b18f018e87b468a8038b5fce6ecba54', 'd1f08d6f8e4647728c14d992964e35b0', 1763567395, 1763560304, 1763560195),
('4cdd296525ea43e9a0c36e37adb1a0eb', '9b18f018e87b468a8038b5fce6ecba54', 'bf0d6bdb688947569d9017ecf8b427ca', 1763742432, 1763735247, 1763735232),
('568c4c7194d54efdb32f35a9a1239bec', '9b18f018e87b468a8038b5fce6ecba54', 'a944be9e9599458b92b0ad80edf6eaa7', 1763567158, NULL, 1763559958),
('784e57888d0443a2a71be886045627ad', '9b18f018e87b468a8038b5fce6ecba54', 'c7a6d68cce1d4c64baa9d738fa714bf6', 1763566421, NULL, 1763559221),
('a4735fd7b773475ca2596cc85ce11f3d', '9b18f018e87b468a8038b5fce6ecba54', 'b1193dc7d2de49a9909af017b656cf2e', 1763566437, NULL, 1763559237),
('ad585b7789754e6ab73a2aa8ecbcb094', '9b18f018e87b468a8038b5fce6ecba54', '7cf1c74df084440dad97200c9f516c81', 1763566445, NULL, 1763559245),
('c44969f534634e6b8cb98c51949234e1', '9b18f018e87b468a8038b5fce6ecba54', 'b34c9a1976724a66b63ea5dcb07f4cc2', 1763567855, 1763560680, 1763560655),
('d470ae23cc8c41f4a42a0feef13e7b5f', '9b18f018e87b468a8038b5fce6ecba54', 'dd5918a94ef54858b7819d05d63ccaf4', 1763566285, NULL, 1763559085),
('e5440bae93994ba2b77a42831844feec', '9b18f018e87b468a8038b5fce6ecba54', '59e293112c0c4ad3835920c0a1f1b308', 1763567554, 1763560369, 1763560354);

-- --------------------------------------------------------

--
-- Struktur-dump for tabellen `posts`
--

CREATE TABLE `posts` (
  `post_id` char(32) NOT NULL,
  `user_id_fk` char(32) NOT NULL,
  `content` varchar(280) NOT NULL,
  `is_blocked` tinyint(1) NOT NULL DEFAULT 0,
  `is_deleted` tinyint(1) NOT NULL DEFAULT 0,
  `created_at` int(11) NOT NULL,
  `updated_at` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Data dump for tabellen `posts`
--

INSERT INTO `posts` (`post_id`, `user_id_fk`, `content`, `is_blocked`, `is_deleted`, `created_at`, `updated_at`) VALUES
('073e7fb2cdd44067a1dd93803dcc9baa', 'b03bfbf476824e678cd065f4ce5510a6', 'qwe', 0, 0, 1764671238, 1764671238),
('0899622a492647fb902b8a55db169f12', 'b03bfbf476824e678cd065f4ce5510a6', 'k', 0, 0, 1764671280, 1764671280),
('09e7b39ab8c843e68ed82051ca07cbc6', 'b03bfbf476824e678cd065f4ce5510a6', '123', 0, 0, 1764350231, 1764350231),
('0e18f9a4da86494ab9f6d3a0c3b5471b', 'b03bfbf476824e678cd065f4ce5510a6', '1234', 0, 0, 1764349360, 1764349360),
('108171a70a964fdbb0510a64cd65d59b', '9b18f018e87b468a8038b5fce6ecba54', 'I luv u Zimbabwe', 0, 1, 1764841337, 1765227365),
('1dacbebb7572424c8a1d3acb690ecc6f', 'b03bfbf476824e678cd065f4ce5510a6', '132', 0, 0, 1764349743, 1764349743),
('2212035d6e5b4ffb94837a8fa0a7cf3c', 'b03bfbf476824e678cd065f4ce5510a6', 'qergqergqerqergqergqergqerqergqergqergqerqergqergqergqerqergqergqergqerqergqergqergqerqergqergqergqerqergqergqergqerqergqergqergqerqergqergqergqerqergqergqergqerqergqergqergqerqergqergqergqerqergqergqergqerqergqergqergqerqerg', 0, 0, 1764616332, 1764616332),
('225a5b9160d64a5f9765d0026030692b', '9b18f018e87b468a8038b5fce6ecba54', 'aaaaaaaaaaadasdfaevjwnervpjwe rvpijw erpiw revipjeqr pijerijpwevpijwre pwj erg iwejgpiwegh weh g hwwegrhu heiur ghuwegi hweuhrg huiewrg hiuwerhu gwiuerg uwergu werhug huiewrg hiuweghiu ewrguiwerg uewrgu iuerg hweug iuweh giuweg ouiwerhg werhg weurighu', 0, 1, 1764845322, 1765037745),
('260ba315c08b416ab907d9c1d6469e21', 'b03bfbf476824e678cd065f4ce5510a6', '123123123', 0, 0, 1764673294, 1764673294),
('2968b0ffea744477bdec7c0c2fd8771c', 'b03bfbf476824e678cd065f4ce5510a6', '1234', 0, 0, 1764349995, 1764349995),
('2a151aa6cce7494694b631cd3133c640', 'b03bfbf476824e678cd065f4ce5510a6', '234234', 0, 0, 1764618001, 1764618001),
('2d9eb0049f194651b1bdfef87b0f6e7b', 'b03bfbf476824e678cd065f4ce5510a6', 'ew', 0, 0, 1764671498, 1764671498),
('2f14d0c2688845049503e7ec1b9fe1c9', 'b03bfbf476824e678cd065f4ce5510a6', '343443', 0, 0, 1764321846, 1764321846),
('2fc3cf198ca643d78d497be1ac421162', '9b18f018e87b468a8038b5fce6ecba54', 'r4', 0, 0, 1764836193, 1764847809),
('3257a0fa7a684d3084f3d9ee4b2cf0d2', 'b03bfbf476824e678cd065f4ce5510a6', 'ew', 0, 0, 1764620713, 1764620713),
('33046282d0534617afd96000065ac3fa', 'b03bfbf476824e678cd065f4ce5510a6', '234234', 0, 0, 1764618005, 1764618005),
('367c28df95c2412796732e237ce4d567', 'b03bfbf476824e678cd065f4ce5510a6', 'ew', 0, 0, 1764670660, 1764670660),
('3730b73fecf94e4cb66985625fc8d593', 'b03bfbf476824e678cd065f4ce5510a6', 'lllll', 0, 0, 1764616763, 1764616763),
('38d0b095c36a43eb957eb141bf8c3c95', 'b03bfbf476824e678cd065f4ce5510a6', 'halløj', 0, 0, 1764616120, 1764616120),
('3a13d420d53a41b1b20a33cd83725607', 'b03bfbf476824e678cd065f4ce5510a6', '1212', 0, 0, 1764672698, 1764672698),
('465698eedd1f4b6d8b641470b264ba51', 'b03bfbf476824e678cd065f4ce5510a6', 'hullubulu...', 0, 1, 1763739080, 1764066822),
('47c26f87a1f94748a9d75a9d8d75e43b', '9b18f018e87b468a8038b5fce6ecba54', 'hejsa', 0, 0, 1763737724, 1763737724),
('51dd58638c784f11b99a9cbe2a847fb9', 'b03bfbf476824e678cd065f4ce5510a6', '123132', 0, 0, 1764672841, 1764672841),
('54f16117220644b5868ada725d54cb17', 'b03bfbf476824e678cd065f4ce5510a6', 'wqe', 0, 0, 1764671452, 1764671452),
('567d03f29c35408997dec82c78f336fa', '9b18f018e87b468a8038b5fce6ecba54', 'eee', 0, 0, 1764839979, 1764847813),
('57f3a4f384ea45dea76a61838f9510ec', 'b03bfbf476824e678cd065f4ce5510a6', '34r34r', 0, 0, 1764321841, 1764321841),
('5a1743026bbf4843b14696caaf7c712d', 'b03bfbf476824e678cd065f4ce5510a6', 'wewe', 0, 0, 1764669412, 1764669412),
('5abfa9b66c134c0fb0890f78479a58dd', 'b03bfbf476824e678cd065f4ce5510a6', 'kk', 0, 0, 1764620472, 1764620472),
('5af7c3e3393140ed9ab5b6295750d086', 'b03bfbf476824e678cd065f4ce5510a6', '123414', 0, 0, 1764350001, 1764350001),
('5bc6b54b64b144d080dfca58d9ec9593', 'b03bfbf476824e678cd065f4ce5510a6', '2r234r23', 0, 0, 1764617804, 1764617804),
('5dda94ccdc08457294526e0111be1f9b', 'b03bfbf476824e678cd065f4ce5510a6', 'wewewe', 0, 0, 1764671839, 1764671839),
('5f94bf7552134aa8b89b86d1a7a8d12a', 'b03bfbf476824e678cd065f4ce5510a6', 'kmklmk', 0, 0, 1764616755, 1764616755),
('5fda81d4348e441395f27f6cbec155e9', 'b03bfbf476824e678cd065f4ce5510a6', 'wewe', 0, 0, 1764669414, 1764669414),
('69e6f2155f4e44ff98bdc3bbd071eaf4', 'b03bfbf476824e678cd065f4ce5510a6', 'Tusind tak for denne gang... shit jeg har brugt mange timer... GODnNAT <3', 0, 0, 1765305300, 1765305300),
('69eca6131cd0486cb3cccd2ba90638f2', '9b18f018e87b468a8038b5fce6ecba54', 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 0, 1, 1764845069, 1764845194),
('6a733724837747cdb27a5eb9e2500d42', 'b03bfbf476824e678cd065f4ce5510a6', 'halløjtaler', 0, 0, 1764617039, 1764617039),
('6d6128f572c942cdabcc3b2970c8a7f5', 'b03bfbf476824e678cd065f4ce5510a6', 'ew', 0, 0, 1764670657, 1764670657),
('7060b0fee263472bb3def5ea95a799c6', 'b03bfbf476824e678cd065f4ce5510a6', '123', 0, 0, 1764673290, 1764673290),
('709aadc38a654aeb94bcd7c0ff38f18d', 'b03bfbf476824e678cd065f4ce5510a6', 'weq', 0, 0, 1764671559, 1764671559),
('70c5017a11c942a785c0b31b5b53ebf2', '9b18f018e87b468a8038b5fce6ecba54', 'ee', 0, 1, 1764845210, 1764845214),
('7e37b8647ae74fe9a4053fb05f0e3021', 'b03bfbf476824e678cd065f4ce5510a6', '234234', 0, 0, 1764671924, 1764671924),
('8592532f5efd45bab126d9fbf68921e4', 'b03bfbf476824e678cd065f4ce5510a6', '1312123123', 0, 0, 1764673018, 1764673018),
('8c95aa010da04f1a802f4f8a34698118', 'b03bfbf476824e678cd065f4ce5510a6', 'mmm', 0, 0, 1764617590, 1764617590),
('8e452531b7a14ff0bcd0675bb11fd6e8', 'b03bfbf476824e678cd065f4ce5510a6', '1312', 0, 0, 1764673015, 1764673015),
('8ea63c03087c4c4ba8a2bc48ac66d862', '9b18f018e87b468a8038b5fce6ecba54', '44', 0, 0, 1764836133, 1764836133),
('9342d251042949fbb0f8ebaed16e05a7', 'b03bfbf476824e678cd065f4ce5510a6', '12', 0, 0, 1764351506, 1764351506),
('956d4c7975ce484b86222a700525aaaf', 'b03bfbf476824e678cd065f4ce5510a6', 'f', 0, 0, 1764350103, 1764350103),
('9bdcd81f6d27446c89a4384cd027b60b', 'b03bfbf476824e678cd065f4ce5510a6', '123', 0, 0, 1764672597, 1764672597),
('9c870760cdd743d7acdb84abf257a394', 'b03bfbf476824e678cd065f4ce5510a6', 'hello', 0, 0, 1764321434, 1764321434),
('a29b11461558404ab0ffd2d40f2cf2b2', 'b03bfbf476824e678cd065f4ce5510a6', 'kkkkk', 0, 0, 1764617404, 1764617404),
('a34101c1c90d464ead57ad3f40c96844', 'b03bfbf476824e678cd065f4ce5510a6', 'kk', 0, 0, 1764620433, 1764620433),
('a640d0549c1e48f085e1bca58ce1cb1b', 'b03bfbf476824e678cd065f4ce5510a6', 'e', 0, 0, 1764671439, 1764671439),
('a7c3016ba35c4700adb7e91c9ed2e59e', 'b03bfbf476824e678cd065f4ce5510a6', '12', 0, 0, 1764351501, 1764351501),
('aa793914f36440179be57d9d3a2b2f68', 'b03bfbf476824e678cd065f4ce5510a6', '234234', 0, 0, 1764617901, 1764617901),
('b2422a949354404da2623c73b4a11790', 'b03bfbf476824e678cd065f4ce5510a6', '123', 0, 0, 1764672018, 1764672018),
('b3aab0195d5546b19c348c8921b0fd4e', '9b18f018e87b468a8038b5fce6ecba54', 'Heyyy, im Mads! Just casually playing TFT!', 0, 0, 1765227389, 1765227389),
('b5686f7fc5cc403caeacd496bf21f6df', '9b18f018e87b468a8038b5fce6ecba54', 'wewe', 0, 1, 1764847429, 1765037742),
('b6ebfd644fd24f3ba320a158f2c4ae39', '9b18f018e87b468a8038b5fce6ecba54', 'qfqwefqwefqwefqwfwqeqfqwefqwefqwefqwfwqeqfqwefqwefqwefqwfwqeqfqwefqwefqwefqwfwqeqfqwefqwefqwefqwfwqeqfqwefqwefqwefqwfwqeqfqwefqwefqwefqwfwqeqfqwefqwefqwefqwfwqeqfqwefqwefqwefqwfwqeqfqwefqwefqwefqwfwqeqfqwefqwefqwefqwfwqe', 0, 1, 1764844671, 1764844681),
('b8485ea63c4a417984ac0f84814ffd2f', '9b18f018e87b468a8038b5fce6ecba54', '2weqw', 0, 1, 1764844511, 1764844744),
('b9a7a01aa178419cb4d1a056262d0e4c', 'b03bfbf476824e678cd065f4ce5510a6', 'qwe', 0, 0, 1764671240, 1764671240),
('bac8821c8fe247e3a48824cdea1add45', 'b03bfbf476824e678cd065f4ce5510a6', '123r13r1', 0, 0, 1764617670, 1764617670),
('bb914b33b4bd4c13891d17c12ad11375', 'b03bfbf476824e678cd065f4ce5510a6', 'wewe', 0, 0, 1764669621, 1764669621),
('bdb9b94c97ad42ff89663679344eaefd', 'b03bfbf476824e678cd065f4ce5510a6', 'wewe', 0, 0, 1764669625, 1764669625),
('bdd99f1c7bb74cfba09e2a0234cfc63a', 'b03bfbf476824e678cd065f4ce5510a6', '234243', 0, 0, 1764617872, 1764617872),
('c13efa3b716f43868aa67000e2a5c79e', 'b03bfbf476824e678cd065f4ce5510a6', 'mmmm', 0, 0, 1764617637, 1764617637),
('c1dbcc5bf5ed46aab6b719c508bb6965', '9b18f018e87b468a8038b5fce6ecba54', 'hehe', 0, 0, 1763737772, 1763737772),
('c3c9b50ce9f14439bebdbc9429b66766', 'b03bfbf476824e678cd065f4ce5510a6', 'ewwe', 0, 0, 1764676124, 1764676124),
('c463f893b19541f3bd143cc6093135f5', 'b03bfbf476824e678cd065f4ce5510a6', '234', 0, 0, 1764349803, 1764349803),
('c6a37d688c46488485cc500f1879d791', 'b03bfbf476824e678cd065f4ce5510a6', 'e', 0, 0, 1764671437, 1764671437),
('c80ea1b4a6484ba0acff564cbac3aa93', 'b03bfbf476824e678cd065f4ce5510a6', 'qwe', 0, 0, 1764671235, 1764671235),
('d04d0fe1aa4348f6a059fec579f1f46e', 'b03bfbf476824e678cd065f4ce5510a6', '4', 0, 0, 1764351273, 1764351273),
('d6f560c8d20847f9bdb16aa4c692178a', 'b03bfbf476824e678cd065f4ce5510a6', 'wewewe', 0, 0, 1764671712, 1764671712),
('de6f25473e834457b7c739e81b3e71bc', 'b03bfbf476824e678cd065f4ce5510a6', '234234', 0, 0, 1764349809, 1764349809),
('e03b6374d5ad440fbce343e137cd3de7', 'b03bfbf476824e678cd065f4ce5510a6', '234', 0, 0, 1764350168, 1764350168),
('e280cc6be703454c93ac67d6398c7edd', 'b03bfbf476824e678cd065f4ce5510a6', 'wewewew', 0, 0, 1764671835, 1764671835),
('e54fd9bd15814f8b86844a16d949dfd9', 'b03bfbf476824e678cd065f4ce5510a6', '123123', 0, 0, 1764672385, 1764672385),
('ee90a67b09b842bf8838c3b33e283698', 'b03bfbf476824e678cd065f4ce5510a6', 'm', 0, 0, 1764671283, 1764671283),
('efdaab5ac74547a1a589adfaa50e1bc6', 'b03bfbf476824e678cd065f4ce5510a6', 'qwe', 0, 0, 1764671817, 1764671817),
('f1eb317177124b86a03b73ce4c0642e0', '9b18f018e87b468a8038b5fce6ecba54', 'ååååhhhhhhh', 0, 0, 1764674776, 1764674776),
('f27d7760f84c48f497b80ae61e4f6d36', 'b03bfbf476824e678cd065f4ce5510a6', 'ws', 0, 0, 1764671445, 1764671445),
('f2d23ec9d0884bce9ede6e6acacc5397', 'b03bfbf476824e678cd065f4ce5510a6', 'hej', 0, 0, 1763738346, 1763738346),
('f56025537c9a46e58191c2015105f0a5', 'b03bfbf476824e678cd065f4ce5510a6', 'e', 0, 0, 1764620682, 1764620682),
('fb2385c921224bc6b6df70d186090ed2', '9b18f018e87b468a8038b5fce6ecba54', '44234', 0, 0, 1764836137, 1764847812);

-- --------------------------------------------------------

--
-- Struktur-dump for tabellen `post_media`
--

CREATE TABLE `post_media` (
  `media_id` char(32) NOT NULL,
  `post_id_fk` char(32) NOT NULL,
  `file_path` varchar(255) NOT NULL,
  `media_type` enum('image','video') NOT NULL,
  `created_at` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Data dump for tabellen `post_media`
--

INSERT INTO `post_media` (`media_id`, `post_id_fk`, `file_path`, `media_type`, `created_at`) VALUES
('26039f44c14b44ceb243628ed7f98de6', '69e6f2155f4e44ff98bdc3bbd071eaf4', 'static/uploads/posts/26039f44c14b44ceb243628ed7f98de6.jpg', 'image', 1765305300),
('328ec4ac840943b9a0c94e13a8ca4730', '465698eedd1f4b6d8b641470b264ba51', 'static/uploads/posts/328ec4ac840943b9a0c94e13a8ca4730.png', 'image', 1763739080),
('520736a241b04eae96e2493b8e30e82a', 'de6f25473e834457b7c739e81b3e71bc', 'static/uploads/posts/520736a241b04eae96e2493b8e30e82a.png', 'image', 1764349809),
('a6faac8d185a4d2a9f7d0bff784e6dc8', 'b3aab0195d5546b19c348c8921b0fd4e', 'static/uploads/posts/a6faac8d185a4d2a9f7d0bff784e6dc8.png', 'image', 1765227389),
('aa210d199a134607998644b6d57ddd36', '108171a70a964fdbb0510a64cd65d59b', 'static/uploads/posts/aa210d199a134607998644b6d57ddd36.png', 'image', 1764841337);

-- --------------------------------------------------------

--
-- Struktur-dump for tabellen `users`
--

CREATE TABLE `users` (
  `user_id` char(32) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `username` varchar(50) NOT NULL,
  `display_name` varchar(100) DEFAULT NULL,
  `bio` varchar(160) DEFAULT NULL,
  `avatar_filename` varchar(255) DEFAULT NULL,
  `is_admin` tinyint(1) NOT NULL DEFAULT 0,
  `is_blocked` tinyint(1) NOT NULL DEFAULT 0,
  `is_deleted` tinyint(1) NOT NULL DEFAULT 0,
  `email_verified_at` int(11) DEFAULT NULL,
  `created_at` int(11) NOT NULL,
  `updated_at` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Data dump for tabellen `users`
--

INSERT INTO `users` (`user_id`, `email`, `password_hash`, `username`, `display_name`, `bio`, `avatar_filename`, `is_admin`, `is_blocked`, `is_deleted`, `email_verified_at`, `created_at`, `updated_at`) VALUES
('1ba70766edd346a6a39022d396e2742c', 'runefink1@gmail.com', 'scrypt:32768:8:1$WbkeEyBOmcdjibEz$6a0bf76bbb30a681404d7e95b44a7c1e16eacf211b5678db7f27dd1bdc6dc8f5a262d4d4cfe8a406bb83fde9e1c3f9c7845e18a2efdaaa7528df2be2e5db6a5e', 'DJFungiz', NULL, NULL, NULL, 0, 0, 0, NULL, 1765037861, 1765037861),
('283d8aec2703404caa421a42e31ba11d', 'thebangminator@gmail.com', 'scrypt:32768:8:1$LRhrW7aPb8AVCpMD$81e4ba3d712a5c39bdd713ca7c3f78a38e24aedd62cea5e73e93e98a83a7df986817eb935d3690e1d9b942ee01a98fc282754be36bfeca8f40d38f341fc2c608', 'hola_chica', '12341234', '123412341', '283d8aec2703404caa421a42e31ba11d.png', 0, 0, 0, 1764846648, 1764846507, 1764846949),
('9b18f018e87b468a8038b5fce6ecba54', 'toftmads2@gmail.com', 'scrypt:32768:8:1$IF3UrIV7fEmjACPs$d8ab4fabab46e2b2f1bb9768d9ca9295f19f6fb469a7ad8c9fb71247e58bab2d898798bd1698a0791b2981542dde151a2b84917e5a7d12f40b1ff36c9272e202', 'mads252', 'sa', 'as', 'b03bfbf476824e678cd065f4ce5510a6.png', 1, 0, 0, 1763543471, 1763543465, 1765283233),
('a123b456c789d0e1f2a3b4c5d6e7f8g9', 'fakeuser1@example.com', 'scrypt:32768:8:1$salt1$hash1', 'GamerPro99', 'Alex Smith', 'En dedikeret gamer og softwareudvikler.', 'b03bfbf476824e678cd065f4ce5510a6.png', 0, 0, 0, 1800000005, 1800000000, 1800000005),
('b03bfbf476824e678cd065f4ce5510a6', 'mads1234@live.com', 'scrypt:32768:8:1$7lvDGhttfBx5H7KD$2fad22bf1ac51da2c44e062491fc609795a12b85ab1e122e00760e6a3b81e4ef6e384e9c2836ed76c36438eb855b49c488ce161641c8183cc55b55d687cea380', 'komnulidt', 'Bobby johnson', 'Hej jeg hedder bobbyyyyyyyyyy444', 'b03bfbf476824e678cd065f4ce5510a6.jpg', 0, 0, 0, 1763632455, 1763632436, 1765305267),
('b234c567d89e0f1a2b3c4d5e6f7g8h9i', 'jenny.d@example.com', 'scrypt:32768:8:1$salt2$hash2', 'JDoodles', 'Jenny Davis', 'Elsker at tegne og drikke kaffe.', 'b03bfbf476824e678cd065f4ce5510a6.png', 0, 0, 0, 1800000115, 1800000110, 1800000115),
('c345d678e90f1a2b3c4d5e6f7g8h9i0j', 'marko.polo@example.com', 'scrypt:32768:8:1$salt3$hash3', 'ExplorerMark', 'Mark Olesen', 'Jeg rejser verden rundt og deler mine historier.', 'b03bfbf476824e678cd065f4ce5510a6.png', 0, 0, 0, 1800000225, 1800000220, 1800000225),
('d456e789f01a2b3c4d5e6f7g8h9i0j1k', 'anna.k@example.com', 'scrypt:32768:8:1$salt4$hash4', 'bookworm_anna', 'Anna Kristensen', 'Altid med en bog i hånden.', 'b03bfbf476824e678cd065f4ce5510a6.png', 0, 0, 0, 1800000335, 1800000330, 1800000335),
('e567f89g01a2b3c4d5e6f7g8h9i0j1k2', 'chef_lars@example.com', 'scrypt:32768:8:1$salt5$hash5', 'LarsTheChef', 'Lars Jensen', 'Mad er min passion. Se mine opskrifter!', 'e567f89g01a2b3c4d5e6f7g8h9i0j1k2.png', 0, 0, 0, 1800000445, 1800000440, 1800000445),
('f678g90h12b3c4d5e6f7g8h9i0j1k2l3', 'tech_guy@example.com', 'scrypt:32768:8:1$salt6$hash6', 'CodeMaster', 'Simon Tech', 'Interesseret i AI og Machine Learning.', 'b03bfbf476824e678cd065f4ce5510a6.png', 0, 0, 0, 1800000555, 1800000550, 1800000555),
('g789h01i23c4d5e6f7g8h9i0j1k2l3m4', 'maria.s@example.com', 'scrypt:32768:8:1$salt7$hash7', 'NatureLover', 'Maria Skov', 'Vandring og fotografering er mit liv.', NULL, 0, 0, 0, 1800000665, 1800000660, 1800000665),
('h890i12j34d5e6f7g8h9i0j1k2l3m4n5', 'admin.test@example.com', 'scrypt:32768:8:1$salt8$hash8', 'TheBossAdmin', 'System Admin', 'Jeg er en test administrator.', NULL, 1, 0, 0, 1800000775, 1800000770, 1800000775),
('i901j23k45e6f7g8h9i0j1k2l3m4n5o6', 'blocked.user@example.com', 'scrypt:32768:8:1$salt9$hash9', 'TroubleMaker', 'Ben Blokk', 'Dette er en blokeret testbruger.', NULL, 0, 0, 0, 1800000885, 1800000880, 1765302910),
('j012k34l56f7g8h9i0j1k2l3m4n5o6p7', 'music.fan@example.com', 'scrypt:32768:8:1$salt10$hash10', 'TuneHunter', 'Oliver Musik', 'Jeg deler kun de bedste playlister.', 'j012k34l56f7g8h9i0j1k2l3m4n5o6p7.webp', 0, 0, 0, 1800000995, 1800000990, 1765282526);

--
-- Begrænsninger for dumpede tabeller
--

--
-- Indeks for tabel `admin_logs`
--
ALTER TABLE `admin_logs`
  ADD PRIMARY KEY (`log_id`),
  ADD KEY `idx_admin_logs_admin` (`admin_user_id_fk`),
  ADD KEY `idx_admin_logs_target_user` (`target_user_id_fk`),
  ADD KEY `idx_admin_logs_target_post` (`target_post_id_fk`);

--
-- Indeks for tabel `comments`
--
ALTER TABLE `comments`
  ADD PRIMARY KEY (`comment_id`),
  ADD KEY `idx_comments_post` (`post_id_fk`),
  ADD KEY `idx_comments_user` (`user_id_fk`);

--
-- Indeks for tabel `email_verifications`
--
ALTER TABLE `email_verifications`
  ADD PRIMARY KEY (`verification_id`),
  ADD UNIQUE KEY `uq_email_verifications_token` (`token`),
  ADD KEY `idx_email_verifications_user` (`user_id_fk`);

--
-- Indeks for tabel `follows`
--
ALTER TABLE `follows`
  ADD PRIMARY KEY (`follower_user_id_fk`,`followee_user_id_fk`),
  ADD KEY `idx_follows_followee` (`followee_user_id_fk`);

--
-- Indeks for tabel `likes`
--
ALTER TABLE `likes`
  ADD PRIMARY KEY (`user_id_fk`,`post_id_fk`),
  ADD KEY `idx_likes_post` (`post_id_fk`);

--
-- Indeks for tabel `password_resets`
--
ALTER TABLE `password_resets`
  ADD PRIMARY KEY (`reset_id`),
  ADD UNIQUE KEY `uq_password_resets_token` (`token`),
  ADD KEY `idx_password_resets_user` (`user_id_fk`);

--
-- Indeks for tabel `posts`
--
ALTER TABLE `posts`
  ADD PRIMARY KEY (`post_id`),
  ADD KEY `idx_posts_user` (`user_id_fk`),
  ADD KEY `idx_posts_created_at` (`created_at`);

--
-- Indeks for tabel `post_media`
--
ALTER TABLE `post_media`
  ADD PRIMARY KEY (`media_id`),
  ADD KEY `idx_media_post` (`post_id_fk`);

--
-- Indeks for tabel `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `uq_users_email` (`email`),
  ADD UNIQUE KEY `uq_users_username` (`username`);

--
-- Begrænsninger for dumpede tabeller
--

--
-- Begrænsninger for tabel `admin_logs`
--
ALTER TABLE `admin_logs`
  ADD CONSTRAINT `fk_admin_logs_admin_users` FOREIGN KEY (`admin_user_id_fk`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_admin_logs_target_posts` FOREIGN KEY (`target_post_id_fk`) REFERENCES `posts` (`post_id`) ON DELETE SET NULL,
  ADD CONSTRAINT `fk_admin_logs_target_users` FOREIGN KEY (`target_user_id_fk`) REFERENCES `users` (`user_id`) ON DELETE SET NULL;

--
-- Begrænsninger for tabel `comments`
--
ALTER TABLE `comments`
  ADD CONSTRAINT `fk_comments_posts` FOREIGN KEY (`post_id_fk`) REFERENCES `posts` (`post_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_comments_users` FOREIGN KEY (`user_id_fk`) REFERENCES `users` (`user_id`) ON DELETE CASCADE;

--
-- Begrænsninger for tabel `email_verifications`
--
ALTER TABLE `email_verifications`
  ADD CONSTRAINT `fk_email_verifications_users` FOREIGN KEY (`user_id_fk`) REFERENCES `users` (`user_id`) ON DELETE CASCADE;

--
-- Begrænsninger for tabel `follows`
--
ALTER TABLE `follows`
  ADD CONSTRAINT `fk_follows_followee` FOREIGN KEY (`followee_user_id_fk`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_follows_follower` FOREIGN KEY (`follower_user_id_fk`) REFERENCES `users` (`user_id`) ON DELETE CASCADE;

--
-- Begrænsninger for tabel `likes`
--
ALTER TABLE `likes`
  ADD CONSTRAINT `fk_likes_posts` FOREIGN KEY (`post_id_fk`) REFERENCES `posts` (`post_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_likes_users` FOREIGN KEY (`user_id_fk`) REFERENCES `users` (`user_id`) ON DELETE CASCADE;

--
-- Begrænsninger for tabel `password_resets`
--
ALTER TABLE `password_resets`
  ADD CONSTRAINT `fk_password_resets_users` FOREIGN KEY (`user_id_fk`) REFERENCES `users` (`user_id`) ON DELETE CASCADE;

--
-- Begrænsninger for tabel `posts`
--
ALTER TABLE `posts`
  ADD CONSTRAINT `fk_posts_users` FOREIGN KEY (`user_id_fk`) REFERENCES `users` (`user_id`) ON DELETE CASCADE;

--
-- Begrænsninger for tabel `post_media`
--
ALTER TABLE `post_media`
  ADD CONSTRAINT `fk_media_posts` FOREIGN KEY (`post_id_fk`) REFERENCES `posts` (`post_id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

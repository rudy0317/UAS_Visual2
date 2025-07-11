-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               8.0.30 - MySQL Community Server - GPL
-- Server OS:                    Win64
-- HeidiSQL Version:             12.1.0.6537
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Dumping data for table sia_rudy_2310010148.kabupaten: ~6 rows (approximately)
INSERT INTO `kabupaten` (`id_kabupaten`, `id_provinsi`, `nama_kabupaten`) VALUES
	(1, 1, 'Jakarta Selatan'),
	(2, 2, 'Bandung'),
	(4, 3, 'Banjar'),
	(5, 3, 'Batola'),
	(7, 1, 'Jepara'),
	(8, 1, 'Citayeam');

-- Dumping data for table sia_rudy_2310010148.kecamatan: ~5 rows (approximately)
INSERT INTO `kecamatan` (`id_kecamatan`, `id_kabupaten`, `nama_kecamatan`) VALUES
	(1, 1, 'Kebayoran Baru'),
	(3, 2, 'Coblong'),
	(4, 2, 'Cicendo'),
	(5, 4, 'Aluh - aluh'),
	(6, 5, 'Anjir');

-- Dumping data for table sia_rudy_2310010148.madrasah: ~10 rows (approximately)
INSERT INTO `madrasah` (`id_madrasah`, `nama_madrasah`, `jenjang`, `alamat`, `id_kecamatan`, `jumlah_guru`, `jumlah_siswa`, `tahun_berdiri`) VALUES
	(1, 'MI Usluhudin', 'MI', 'Jl. Bina Marga', 1, 15, 200, '1998'),
	(3, 'MA Darul Ulum', 'MA', 'Jl. Merdeka No.5', 3, 20, 250, '1995'),
	(6, 'MI Daruh Falah', 'MI', 'Jl. Bina Marga1 ', 3, 200, 900, '2000'),
	(12, 'MTs Nurul Mustakim', 'MTs', 'Jl. Anjir Muara', 6, 30, 200, '1995'),
	(13, 'MTs Nuruddin', 'MTs', 'Jl. Banjar Raya', 6, 30, 300, '2001'),
	(14, 'MA Negeri 3 Banjarmasin', 'MA', 'Jl. Mulawarman', 6, 20, 200, '2006'),
	(16, 'MI NegerI 1 Banjarmasin', 'MI', 'Jl. Mulawarman', 6, 30, 400, '2000'),
	(17, 'MA Negeri 1 Banjarmasin', 'MA', 'JL. Pelajar ', 6, 30, 300, '2000'),
	(18, 'MI Usluhuddin', 'MI', 'Jl. Rawa Mangun', 6, 20, 200, '1999'),
	(20, 'MTs Mulawarman', 'MTs', 'Jl. Mulawarman', 5, 30, 500, '2000');

-- Dumping data for table sia_rudy_2310010148.provinsi: ~3 rows (approximately)
INSERT INTO `provinsi` (`id_provinsi`, `nama_provinsi`) VALUES
	(1, 'DKI Jakarta'),
	(2, 'Jawa Barat'),
	(3, 'Kalimantan Selatan');

-- Dumping data for table sia_rudy_2310010148.users: ~6 rows (approximately)
INSERT INTO `users` (`id_user`, `username`, `password`, `role`, `id_madrasah`, `id_provinsi`) VALUES
	(1, 'adminpusat', 'adminpusat', 'admin_pusat', NULL, NULL),
	(2, 'adminjabar', 'adminjabar', 'admin_provinsi', NULL, 2),
	(3, 'mi_alhikmah', 'mi_alhikmah', 'madrasah', 1, NULL),
	(4, 'mts_nurulfalah', '482c811da5d5b4bc6d497ffa98491e38', 'madrasah', NULL, NULL),
	(5, 'ma_darululum', '482c811da5d5b4bc6d497ffa98491e38', 'madrasah', 3, NULL),
	(6, 'admin', 'admin', 'admin_pusat', NULL, NULL);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;

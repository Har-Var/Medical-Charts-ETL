/****** Object:  Database [MedicalChartsETL]    Script Date: 27-11-2024 16:25:58 ******/
CREATE DATABASE [MedicalChartsETL] CONTAINMENT = NONE ON PRIMARY (
	NAME = N'MedicalDataETL',
	FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL16.MSSQLSERVER\MSSQL\DATA\MedicalDataETL.mdf',
	SIZE = 139264 KB,
	MAXSIZE = UNLIMITED,
	FILEGROWTH = 65536 KB
	) LOG ON (
	NAME = N'MedicalDataETL_log',
	FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL16.MSSQLSERVER\MSSQL\DATA\MedicalDataETL_log.ldf',
	SIZE = 466944 KB,
	MAXSIZE = 2048 GB,
	FILEGROWTH = 65536 KB
	)
	WITH CATALOG_COLLATION = DATABASE_DEFAULT,
		LEDGER = OFF
GO

ALTER DATABASE [MedicalChartsETL]

SET COMPATIBILITY_LEVEL = 160
GO

IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
BEGIN
	EXEC [MedicalChartsETL].[dbo].[sp_fulltext_database] @action = 'enable'
END
GO

ALTER DATABASE [MedicalChartsETL]

SET ANSI_NULL_DEFAULT OFF
GO

ALTER DATABASE [MedicalChartsETL]

SET ANSI_NULLS OFF
GO

ALTER DATABASE [MedicalChartsETL]

SET ANSI_PADDING OFF
GO

ALTER DATABASE [MedicalChartsETL]

SET ANSI_WARNINGS OFF
GO

ALTER DATABASE [MedicalChartsETL]

SET ARITHABORT OFF
GO

ALTER DATABASE [MedicalChartsETL]

SET AUTO_CLOSE OFF
GO

ALTER DATABASE [MedicalChartsETL]

SET AUTO_SHRINK OFF
GO

ALTER DATABASE [MedicalChartsETL]

SET AUTO_UPDATE_STATISTICS ON
GO

ALTER DATABASE [MedicalChartsETL]

SET CURSOR_CLOSE_ON_COMMIT OFF
GO

ALTER DATABASE [MedicalChartsETL]

SET CURSOR_DEFAULT GLOBAL
GO

ALTER DATABASE [MedicalChartsETL]

SET CONCAT_NULL_YIELDS_NULL OFF
GO

ALTER DATABASE [MedicalChartsETL]

SET NUMERIC_ROUNDABORT OFF
GO

ALTER DATABASE [MedicalChartsETL]

SET QUOTED_IDENTIFIER OFF
GO

ALTER DATABASE [MedicalChartsETL]

SET RECURSIVE_TRIGGERS OFF
GO

ALTER DATABASE [MedicalChartsETL]

SET DISABLE_BROKER
GO

ALTER DATABASE [MedicalChartsETL]

SET AUTO_UPDATE_STATISTICS_ASYNC OFF
GO

ALTER DATABASE [MedicalChartsETL]

SET DATE_CORRELATION_OPTIMIZATION OFF
GO

ALTER DATABASE [MedicalChartsETL]

SET TRUSTWORTHY OFF
GO

ALTER DATABASE [MedicalChartsETL]

SET ALLOW_SNAPSHOT_ISOLATION OFF
GO

ALTER DATABASE [MedicalChartsETL]

SET PARAMETERIZATION SIMPLE
GO

ALTER DATABASE [MedicalChartsETL]

SET READ_COMMITTED_SNAPSHOT OFF
GO

ALTER DATABASE [MedicalChartsETL]

SET HONOR_BROKER_PRIORITY OFF
GO

ALTER DATABASE [MedicalChartsETL]

SET RECOVERY FULL
GO

ALTER DATABASE [MedicalChartsETL]

SET MULTI_USER
GO

ALTER DATABASE [MedicalChartsETL]

SET PAGE_VERIFY CHECKSUM
GO

ALTER DATABASE [MedicalChartsETL]

SET DB_CHAINING OFF
GO

ALTER DATABASE [MedicalChartsETL]

SET FILESTREAM(NON_TRANSACTED_ACCESS = OFF)
GO

ALTER DATABASE [MedicalChartsETL]

SET TARGET_RECOVERY_TIME = 60 SECONDS
GO

ALTER DATABASE [MedicalChartsETL]

SET DELAYED_DURABILITY = DISABLED
GO

ALTER DATABASE [MedicalChartsETL]

SET ACCELERATED_DATABASE_RECOVERY = OFF
GO

EXEC sys.sp_db_vardecimal_storage_format N'MedicalChartsETL',
	N'ON'
GO

ALTER DATABASE [MedicalChartsETL]

SET QUERY_STORE = ON
GO

ALTER DATABASE [MedicalChartsETL]

SET QUERY_STORE(OPERATION_MODE = READ_WRITE, CLEANUP_POLICY = (STALE_QUERY_THRESHOLD_DAYS = 30), DATA_FLUSH_INTERVAL_SECONDS = 900, INTERVAL_LENGTH_MINUTES = 60, MAX_STORAGE_SIZE_MB = 1000, QUERY_CAPTURE_MODE = AUTO, SIZE_BASED_CLEANUP_MODE = AUTO, MAX_PLANS_PER_QUERY = 200, WAIT_STATS_CAPTURE_MODE = ON)
GO

/****** Object:  Schema [Common]    Script Date: 27-11-2024 16:25:59 ******/
CREATE SCHEMA [Common]
GO

/****** Object:  Schema [Gryff]    Script Date: 27-11-2024 16:25:59 ******/
CREATE SCHEMA [Gryff]
GO

/****** Object:  Schema [Huffle]    Script Date: 27-11-2024 16:25:59 ******/
CREATE SCHEMA [Huffle]
GO

/****** Object:  Schema [Raven]    Script Date: 27-11-2024 16:25:59 ******/
CREATE SCHEMA [Raven]
GO

/****** Object:  Table [Gryff].[chartlookup]    Script Date: 27-11-2024 16:25:59 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [Gryff].[chartlookup] ([chartname] [varchar](60) NULL) ON [PRIMARY]
GO

/****** Object:  Table [Huffle].[chartlookup]    Script Date: 27-11-2024 16:25:59 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [Huffle].[chartlookup] ([chartname] [varchar](60) NULL) ON [PRIMARY]
GO

/****** Object:  Table [Raven].[chartlookup]    Script Date: 27-11-2024 16:25:59 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [Raven].[chartlookup] ([chartname] [varchar](60) NULL) ON [PRIMARY]
GO

/****** Object:  Table [Gryff].[leftcharts]    Script Date: 27-11-2024 16:25:59 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [Gryff].[leftcharts] ([chartname] [varchar](60) NULL) ON [PRIMARY]
GO

/****** Object:  Table [Huffle].[leftcharts]    Script Date: 27-11-2024 16:25:59 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [Huffle].[leftcharts] ([chartname] [varchar](60) NULL) ON [PRIMARY]
GO

/****** Object:  Table [Raven].[leftcharts]    Script Date: 27-11-2024 16:25:59 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [Raven].[leftcharts] ([chartname] [varchar](60) NULL) ON [PRIMARY]
GO

/****** Object:  View [Common].[vw_lookuptable_stats]    Script Date: 27-11-2024 16:25:59 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE VIEW [Common].[vw_lookuptable_stats]
AS
(
		SELECT 'Gryff Limited' AS Type,
			count(*) AS Count
		FROM Gryff.chartlookup
		
		UNION
		
		SELECT 'Gryff Left' AS Type,
			count(*) AS Count
		FROM Gryff.leftcharts
		
		UNION
		
		SELECT 'Huffle Limited' AS Type,
			count(*) AS Count
		FROM Huffle.chartlookup
		
		UNION
		
		SELECT 'Huffle Left' AS Type,
			count(*) AS Count
		FROM Huffle.leftcharts
		
		UNION
		
		SELECT 'Raven Limited' AS Type,
			count(*) AS Count
		FROM Raven.chartlookup
		
		UNION
		
		SELECT 'Raven Left' AS Type,
			count(*) AS Count
		FROM Raven.leftcharts
		)
GO

/****** Object:  Table [Common].[report_recon_detail]    Script Date: 27-11-2024 16:25:59 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [Common].[report_recon_detail] (
	[id] [int] IDENTITY(1, 1) NOT NULL,
	[header_id] [int] NULL,
	[chart_name] [varchar](60) NULL,
	[drop_off_ind] [bit] NULL,
	[payment_recon_ind] [bit] NULL,
	[chart_lookup_ind] [bit] NULL,
	[insert_datetime] [datetime2](0) NULL,
	[update_datetime] [datetime2](0) NULL,
	[report_name] [varchar](40) NULL,
	[exclusion_ind] [bit] NULL,
	PRIMARY KEY CLUSTERED ([id] ASC) WITH (
		PAD_INDEX = OFF,
		STATISTICS_NORECOMPUTE = OFF,
		IGNORE_DUP_KEY = OFF,
		ALLOW_ROW_LOCKS = ON,
		ALLOW_PAGE_LOCKS = ON,
		OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF
		) ON [PRIMARY]
	) ON [PRIMARY]
GO

/****** Object:  View [Common].[vw_recon_detail_tally_counts]    Script Date: 27-11-2024 16:25:59 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE VIEW [Common].[vw_recon_detail_tally_counts]
AS
(
		SELECT header_id,
			report_name,
			SUM(CAST(drop_off_ind AS INT)) AS drop_off_tally_count,
			SUM(CAST(payment_recon_ind AS INT)) AS payment_recon_tally_count,
			SUM(CAST(chart_lookup_ind AS INT)) AS chart_lookup_tally_count
		FROM common.report_recon_detail
		GROUP BY header_id,
			report_name
		)
GO

/****** Object:  Table [Common].[report_recon_header]    Script Date: 27-11-2024 16:25:59 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [Common].[report_recon_header] (
	[id] [int] IDENTITY(1, 1) NOT NULL,
	[report_push_date] [date] NULL,
	[report_file_date] [date] NULL,
	[report_name] [varchar](40) NULL,
	[vendor] [varchar](10) NULL,
	[file_count] [int] NULL,
	[unique_count] [int] NULL,
	[first_delivery] [datetime2](0) NULL,
	[last_delivery] [datetime2](0) NULL,
	[drop_off_tally_count] [int] NULL,
	[payment_recon_tally_count] [int] NULL,
	[chart_lookup_tally_count] [int] NULL,
	PRIMARY KEY CLUSTERED ([id] ASC) WITH (
		PAD_INDEX = OFF,
		STATISTICS_NORECOMPUTE = OFF,
		IGNORE_DUP_KEY = OFF,
		ALLOW_ROW_LOCKS = ON,
		ALLOW_PAGE_LOCKS = ON,
		OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF
		) ON [PRIMARY]
	) ON [PRIMARY]
GO

/****** Object:  Table [Common].[vendor_active_status]    Script Date: 27-11-2024 16:25:59 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [Common].[vendor_active_status] (
	[vendor] [varchar](10) NULL,
	[active_flag] [bit] NULL
	) ON [PRIMARY]
GO

INSERT [Common].[vendor_active_status] (
	[vendor],
	[active_flag]
	)
VALUES (
	N'Gryff',
	1
	)
GO

INSERT [Common].[vendor_active_status] (
	[vendor],
	[active_flag]
	)
VALUES (
	N'Huffle',
	1
	)
GO

INSERT [Common].[vendor_active_status] (
	[vendor],
	[active_flag]
	)
VALUES (
	N'Raven',
	1
	)
GO

INSERT [Common].[vendor_active_status] (
	[vendor],
	[active_flag]
	)
VALUES (
	N'Slyth',
	0
	)
GO

ALTER TABLE [Common].[report_recon_detail]
	WITH CHECK ADD FOREIGN KEY ([header_id]) REFERENCES [Common].[report_recon_header]([id]) ON

DELETE CASCADE
GO

/****** Object:  StoredProcedure [Common].[sp_increment_chartlookup]    Script Date: 27-11-2024 16:25:59 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [Common].[sp_increment_chartlookup] @vendor_name NVARCHAR(10), -- Vendor name as a parameter
	@batch_size INT -- Number of charts to move
AS
BEGIN
	-- Declare a variable to hold the dynamic SQL query
	DECLARE @sqlQuery NVARCHAR(MAX);

	-- Build the dynamic SQL using the vendor name and batch size parameters
	SET @sqlQuery = 'SELECT TOP(' + CAST(@batch_size AS NVARCHAR(10)) + ') chartname into #MovedCharts
            FROM [' + @vendor_name + '].leftcharts
        -- Insert the moved charts into chartlookup and delete them from leftcharts
        INSERT INTO [' + @vendor_name + '].chartlookup (chartname)
        SELECT chartname FROM #MovedCharts;

        DELETE FROM [' + @vendor_name + '].leftcharts
        WHERE chartname IN (SELECT chartname FROM #MovedCharts);
		
		Drop Table #MovedCharts;
		';

	-- Execute the entire batch in a single execution block
	EXEC sp_executesql @sqlQuery;
END
GO

/****** Object:  StoredProcedure [Common].[sp_update_chart_lookup_indicator]    Script Date: 27-11-2024 16:25:59 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [Common].[sp_update_chart_lookup_indicator]
AS
BEGIN
	-- Declare a variable to hold the dynamic SQL query
	DECLARE @sqlQuery NVARCHAR(MAX);

	-- Initialize the query to start building the union of chart names
	SET @sqlQuery = '';

	-- Iterate through active vendors and add their chartlookup table to the query
	-- The query will union chart names for all active vendors
	DECLARE @vendorName NVARCHAR(10);

	-- Cursor to get active vendors
	DECLARE vendor_cursor CURSOR
	FOR
	SELECT vendor
	FROM Common.vendor_active_status
	WHERE active_flag = 1;

	OPEN vendor_cursor;

	FETCH NEXT
	FROM vendor_cursor
	INTO @vendorName;

	WHILE @@FETCH_STATUS = 0
	BEGIN
		-- For each active vendor, append the chart names to the dynamic SQL
		SET @sqlQuery = @sqlQuery + 'SELECT chartname FROM [' + @vendorName + '].chartlookup UNION ';

		FETCH NEXT
		FROM vendor_cursor
		INTO @vendorName;
	END

	CLOSE vendor_cursor;

	DEALLOCATE vendor_cursor;

	-- Remove the last 'UNION' by trimming the trailing space
	SET @sqlQuery = LEFT(@sqlQuery, LEN(@sqlQuery) - 6);
	-- Final UPDATE query using the union of chart names
	SET @sqlQuery = '
        UPDATE common.report_recon_detail
        SET chart_lookup_ind = 1, update_datetime = GETUTCDATE()
        FROM common.report_recon_detail r
        INNER JOIN (' + @sqlQuery + ') t
        ON r.chart_name = t.chartname 
		where (r.exclusion_ind = 0 or r.exclusion_ind is NULL) 
		and (r.chart_lookup_ind = 0 or r.chart_lookup_ind is NULL)
    ';

	-- Execute the dynamic SQL query
	EXEC sp_executesql @sqlQuery;
END
GO

/****** Object:  StoredProcedure [Common].[sp_update_exclusion_indicator]    Script Date: 27-11-2024 16:25:59 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [Common].[sp_update_exclusion_indicator]
AS
UPDATE common.report_recon_detail
SET exclusion_ind = 1
WHERE drop_off_ind = 1
	AND payment_recon_ind = 1
	AND chart_lookup_ind = 1
	AND (
		exclusion_ind IS NULL
		OR exclusion_ind = 0
		)
GO

/****** Object:  StoredProcedure [Common].[sp_update_header_tally_counts]    Script Date: 27-11-2024 16:25:59 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [Common].[sp_update_header_tally_counts]
AS
UPDATE h
SET h.drop_off_tally_count = t.drop_off_tally_count,
	h.payment_recon_tally_count = t.payment_recon_tally_count,
	h.chart_lookup_tally_count = t.chart_lookup_tally_count
FROM common.report_recon_header h
INNER JOIN common.vw_recon_detail_tally_counts t ON h.id = t.header_id
	AND h.report_name = t.report_name;
GO

ALTER DATABASE [MedicalChartsETL]

SET READ_WRITE
GO



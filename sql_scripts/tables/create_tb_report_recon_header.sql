USE [MedicalChartsETL]
GO

/****** Object:  Table [Common].[report_recon_header] ******/
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



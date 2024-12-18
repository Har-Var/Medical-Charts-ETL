USE [MedicalChartsETL]
GO

/****** Object:  Table [Common].[report_recon_detail] ******/
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

ALTER TABLE [Common].[report_recon_detail]
	WITH CHECK ADD FOREIGN KEY ([header_id]) REFERENCES [Common].[report_recon_header]([id]) ON

DELETE CASCADE
GO



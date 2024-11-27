USE [MedicalChartsETL]
GO

/****** Object:  Table [Common].[vendor_active_status] ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [Common].[vendor_active_status] (
	[vendor] [varchar](10) NULL,
	[active_flag] [bit] NULL
	) ON [PRIMARY]
GO



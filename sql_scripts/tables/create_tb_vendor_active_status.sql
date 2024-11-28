USE [MedicalChartsETL]
GO
/****** Object:  Table [Common].[vendor_active_status] ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [Common].[vendor_active_status](
	[vendor] [varchar](10) NULL,
	[active_flag] [bit] NULL
) ON [PRIMARY]
GO
INSERT [Common].[vendor_active_status] ([vendor], [active_flag]) VALUES (N'Gryff', 1)
GO
INSERT [Common].[vendor_active_status] ([vendor], [active_flag]) VALUES (N'Huffle', 1)
GO
INSERT [Common].[vendor_active_status] ([vendor], [active_flag]) VALUES (N'Raven', 1)
GO
INSERT [Common].[vendor_active_status] ([vendor], [active_flag]) VALUES (N'Slyth', 0)
GO

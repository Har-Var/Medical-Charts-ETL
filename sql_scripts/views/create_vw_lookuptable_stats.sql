USE [MedicalChartsETL]
GO

/****** Object:  View [Common].[vw_lookuptable_stats] ******/
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



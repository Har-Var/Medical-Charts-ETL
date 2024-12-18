USE [MedicalChartsETL]
GO

/****** Object:  StoredProcedure [Common].[sp_update_exclusion_indicator]    Script Date: 27-11-2024 16:35:32 ******/
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



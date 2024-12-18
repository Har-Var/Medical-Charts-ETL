USE [MedicalChartsETL]
GO

/****** Object:  View [Common].[vw_recon_detail_tally_counts] ******/
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



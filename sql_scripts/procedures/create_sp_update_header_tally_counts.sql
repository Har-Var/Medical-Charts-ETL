USE [MedicalChartsETL]
GO

/****** Object:  StoredProcedure [Common].[sp_update_header_tally_counts]    Script Date: 27-11-2024 16:35:32 ******/
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



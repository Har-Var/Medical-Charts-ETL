USE [MedicalChartsETL]
GO

/****** Object:  StoredProcedure [Common].[sp_update_chart_lookup_indicator] ******/
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



USE [MedicalChartsETL]
GO

/****** Object:  StoredProcedure [Common].[sp_increment_chartlookup] ******/
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



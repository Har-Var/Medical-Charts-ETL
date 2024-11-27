USE MedicalDataETL
GO

-- For resetting the tables and restarting the ID's
DELETE
FROM common.report_recon_header;

DBCC CHECKIDENT (
		'common.report_recon_header',
		RESEED,
		0
		);

DELETE
FROM common.report_recon_detail;

DBCC CHECKIDENT (
		'common.report_recon_detail',
		RESEED,
		0
		);

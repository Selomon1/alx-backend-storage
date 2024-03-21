SELECT band_name,
	GREATEST(IFNULL(split, 2022) - formed, 0) AS lifespan
FROM metal_bands
Where style LIKE '%Glam rock%'
ORDER BY lifespan DESC;

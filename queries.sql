SELECT 
	region,
	avg(trees_cut_down) as deforestation_number
FROM
	deforestation_table
GROUP BY
	region
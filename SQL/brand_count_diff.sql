SELECT
	brand,
	count(link) AS link_count,
	count(distinct link) AS link_dist_count,
	count(page) AS page_count,
	count(distinct page) AS page_dist_count
FROM

	(SELECT
		d.page,
		d.title,
		d.price,
		d.link,
		b.brand
	FROM daily_listings d 
	LEFT JOIN brand_page_mapping b
	ON d.page=b.page)

GROUP BY 1
ORDER BY 2 DESC
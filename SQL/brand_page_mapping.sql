CREATE TABLE brand_page_mapping as
SELECT * FROM

(
SELECT
	a.page,
	b.brand
FROM
		(SELECT
			page,
			SUBSTR(page, brand_start_pos, brand_pos_diff ) as brand_url
		FROM
		-- The value "6" below removes "Brand=" from the substring results
				(SELECT
					page,
					INSTR(page, 'Brand') + 6  as brand_start_pos,
					INSTR(page, '&_sop') as brand_end_pos,
					INSTR(page, '&_sop')  - INSTR(page, 'Brand') - 6  as brand_pos_diff
				FROM daily_listings
				GROUP BY 1
				ORDER BY 3 DESC) 
		GROUP BY 1
		ORDER BY 1) a
	LEFT JOIN
		brand_mapping b ON a.brand_url = b.url_brand
)
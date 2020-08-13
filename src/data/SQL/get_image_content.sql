SELECT DISTINCT on (model_code)
	tmall_id,
	model_code,
	replace(weblabel, SUBSTRING ( weblabel, '\[.*\]' ), '') as weblabel,
	benefits,
	catchline,
	sport_practices,
	product_nature,
	tmall_keywords,
	regexp_replace((regexp_replace(tmall_subject,  '[a-zA-Z]+-?\s?[a-zA-Z]+', '', 'g')),  
		'【预售】', '', 'g') as tmall_subject
FROM
	smartdata_pro.d_product_info 
WHERE
	benefits IS NOT NULL 
	-- and universe_id not in ('9024','68','2','4')
	and universe_id = {{universe_id}}
	and tmall_keywords is not null
	AND tmall_subject IS NOT NULL 
	AND tmall_sale_status = 'onsale'
	and cube_url is not null
	and active_fg = 1
-- 	and model_code = '8372809'
	order by model_code, tmall_last_modified desc
SELECT DISTINCT
	tmall_id,
	model_code,
	replace(weblabel, SUBSTRING ( weblabel, '\[.*\]' ), '') as weblabel,
	benefits,
	catchline,
	sport_practices,
	tmall_cat_lvl3_name,
	tmall_keywords,
	tmall_subject
FROM
	smartdata_pro.d_product_info 
WHERE
	benefits IS NOT NULL 
	and universe_label_zh = '瑜伽'
	and tmall_keywords is not null
	AND tmall_subject IS NOT NULL 
	AND tmall_id IN ( SELECT DISTINCT tmall_id FROM smartdata_pro.d_product_online_rate WHERE tmall_sale_status = 'onsale' ) 
	-- and model_code in ('8484434','8484480')
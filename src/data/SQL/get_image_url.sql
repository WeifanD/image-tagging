CREATE TEMP TABLE img AS SELECT A
.tmall_id,
A.model_code,
b.img_source,
b.img_url 
FROM
	( SELECT DISTINCT tmall_id, model_code FROM smartdata_pro.d_product_info WHERE tmall_id IN ( SELECT DISTINCT tmall_id FROM smartdata_pro.d_product_online_rate WHERE tmall_sale_status = 'onsale' ) )
	A LEFT JOIN ( SELECT DISTINCT tmall_id, model_code, img_url, img_source FROM smartdata_pro.d_product_img ) b ON A.model_code = b.model_code 
	OR A.tmall_id = b.tmall_id 
GROUP BY
	1,
	2,
	3,
	4;
	
CREATE TEMP TABLE img_count AS SELECT
tmall_id,
COUNT ( DISTINCT img_url ) n_img
FROM
	img 
GROUP BY
	tmall_id;
	
TRUNCATE smartdata_pro.d_content_img;
INSERT INTO smartdata_pro.d_content_img 
SELECT
i.*,
ic.n_img
FROM
	img i
	INNER JOIN ( SELECT * FROM img_count ) ic ON i.tmall_id = ic.tmall_id;

-- only keep image url which text is ready
SELECT DISTINCT
	img_url 
FROM
	smartdata_pro.d_content_img limit 5
	-- A INNER JOIN ( SELECT DISTINCT tmall_id, model_code FROM bi."d_content" WHERE TEXT IS NOT NULL ) b ON A.tmall_id = b.tmall_id 
	-- AND A.model_code = b.model_code ; 
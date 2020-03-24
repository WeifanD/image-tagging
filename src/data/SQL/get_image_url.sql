-- only keep image url which text is ready
SELECT DISTINCT
	img_url 
FROM
	smartdata_pro.d_content_img
	A INNER JOIN ( SELECT DISTINCT tmall_id, model_code FROM bi.d_content_text WHERE TEXT IS NOT NULL ) b ON A.tmall_id = b.tmall_id 
	or A.model_code = cast(b.model_code as varchar); 

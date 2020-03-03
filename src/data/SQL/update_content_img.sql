-- alter table smartdata_pro.d_content_image drop COLUMN tags;
alter table smartdata_pro.d_content_image add COLUMN tags varchar
;


UPDATE smartdata_pro.d_content_image b
SET    tags = a.Col2
FROM   image a
WHERE  a.Col1 = b.img_url;


-- select tmall_id, string_agg(img_url, '@@') AS img_url_array
-- from img
-- group by tmall_id

-- alter table smartdata_pro.d_content add COLUMN img_str varchar
-- ;

-- UPDATE smartdata_pro.d_content b
-- SET    img_url_array = a.Col2
-- FROM   image a
-- WHERE  a.Col1 = b.img_url;
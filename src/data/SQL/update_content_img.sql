-- CREATE TABLE "smartdata_pro"."d_content_img" (
--   "tmall_id" varchar COLLATE "pg_catalog"."default",
--   "model_code" varchar COLLATE "pg_catalog"."default",
--   "img_source" varchar COLLATE "pg_catalog"."default",
--   "img_url" varchar COLLATE "pg_catalog"."default",
--   "n_img" int4
-- )
-- ;

-- alter table smartdata_pro.d_content_img drop COLUMN tags;
-- alter table smartdata_pro.d_content_img add COLUMN tags varchar
-- ;


UPDATE smartdata_pro.d_content_img b
SET    tags = a.img_url
FROM   bi.d_content_img a
WHERE  a.img_url = b.tags;


-- select tmall_id, string_agg(img_url, '@@') AS img_url_array
-- from img
-- group by tmall_id

-- alter table smartdata_pro.d_content add COLUMN img_str varchar
-- ;

-- UPDATE smartdata_pro.d_content b
-- SET    img_url_array = a.tags
-- FROM   bi.content_img a
-- WHERE  a.img_url = b.tags;

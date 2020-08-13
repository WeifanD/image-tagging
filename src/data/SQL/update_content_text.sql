drop table "bi"."d_content_text";
CREATE TABLE "bi"."d_content_text" (
  "model_code" varchar COLLATE "pg_catalog"."default",
  "product_name" text COLLATE "pg_catalog"."default",
  "title" text COLLATE "pg_catalog"."default",
	"text" text COLLATE "pg_catalog"."default"
)
;

-- create table with text and img data
-- TRUNCATE smartdata_pro.d_content;
-- INSERT INTO smartdata_pro.d_content
-- SELECT DISTINCT tmall_id, model_code FROM smartdata_pro.d_product_info WHERE benefits IS NOT NULL 
-- 	and universe_label_zh = '瑜伽'
-- 	and tmall_keywords is not null
-- 	AND tmall_subject IS NOT NULL 
-- 	AND tmall_id IN ( SELECT DISTINCT tmall_id FROM smartdata_pro.d_product_online_rate WHERE tmall_sale_status = 'onsale' )

-- alter table smartdata_pro.d_content drop COLUMN text;
-- alter table smartdata_pro.d_content add COLUMN text varchar
-- ;


-- update text data
-- UPDATE smartdata_pro.d_content b
-- SET    text = a.text, product_name = a.product_name, title = a.title
-- FROM   (select model_code, product_name, string_agg(title, '@@') as title, string_agg(text, '@@') as text from bi.d_content_text
-- group by 1,2) a
-- WHERE  cast(a.model_code as varchar)=b.model_code;
-- create table with text and img data
TRUNCATE smartdata_pro.d_content;
INSERT INTO smartdata_pro.d_content
SELECT DISTINCT tmall_id, model_code FROM smartdata_pro.d_product_info WHERE tmall_id IN ( SELECT DISTINCT tmall_id FROM smartdata_pro.d_product_online_rate WHERE tmall_sale_status = 'onsale' );

alter table smartdata_pro.d_content drop COLUMN text;
alter table smartdata_pro.d_content add COLUMN text varchar
;

-- update text data
UPDATE smartdata_pro.d_content b
SET    text = a.text
FROM   bi.d_content_text a
WHERE  a.tmall_id = b.tmall_id and cast(a.model_code as varchar)=b.model_code;
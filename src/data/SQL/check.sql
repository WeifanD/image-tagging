alter table smartdata_pro.d_product_info drop COLUMN comment_label;
alter table smartdata_pro.d_product_info add COLUMN comment_label varchar
;


UPDATE smartdata_pro.d_product_info b
SET    comment_label = a.content
FROM   image a
WHERE  a.model_code = cast(b.model_code as varchar);
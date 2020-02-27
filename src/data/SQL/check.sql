-- alter table smartdata_pro.d_product_image drop COLUMN tags;
alter table smartdata_pro.d_product_image add COLUMN tags varchar
;


UPDATE smartdata_pro.d_product_img b
SET    tags = a.Col2
FROM   image a
WHERE  a.Col1 = b.img_id;
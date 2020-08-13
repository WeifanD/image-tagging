-- update all base content for this universe

 drop table if exists img_scene;
create temp table img_scene as
SELECT distinct img_url FROM bi.d_content_img where tags like '%%face,  person%%' and img_url not in 
(select img_url from smartdata_pro.d_product_img where img_source = 'cube' and img_type like '%%content%%')
and img_url like '%%pixl%%'
;

-- 基础图片数据表(细节图中有人有脸且官网类型是场景图的设为场景图)
drop table if exists img_1;
create temp table img_1 as SELECT DISTINCT 
		a.tmall_id,
		a.model_code,
		b.dsm_code,
		a.img_url,
		a.img_source,
		a.img_type AS model_img_order,
		tmall_img_order,
		( CASE WHEN img_type like '%%content%%' or c.img_url is not null THEN TRUE ELSE FALSE END ) if_scene
	FROM
		smartdata_pro.d_product_img
		a INNER JOIN PUBLIC.d_item_universe_cube b ON a.model_code = b.model_code 
		left join img_scene c on a.img_url = c.img_url
	WHERE
		tmall_id in (SELECT DISTINCT ON ( model_code ) tmall_id 
		FROM smartdata_pro.d_product_info WHERE tmall_sale_status = 'onsale' and universe_id = {{universe_id}} ORDER BY model_code, tmall_last_modified DESC)
		and img_source = 'cube'
		order by tmall_id, model_code, model_img_order
;

 -- 自己主图不够他人来凑
 drop table if exists img;
create temp table img as
select distinct tmall_id, model_code, dsm_code, if_scene, model_img_order, img_url, model_code as img_type 
from img_1 
union all
select distinct a.tmall_id, a.model_code, a.dsm_code, b.if_scene, b.model_img_order, b.img_url, b.model_code as img_type 
from img_1 a left join img_1 b on a.tmall_id = b.tmall_id and a.model_code != b.model_code
;

-- 官网场景图/产品细节图 (all)
DROP TABLE bi.d_content_image;
CREATE TABLE bi.d_content_image (
  "tmall_id" varchar(255),
  "model_code" varchar(255),
  "img_url" varchar(1000),
  "if_scene" varchar(10),
  "rank" int4
)
;

insert into bi.d_content_image
select distinct tmall_id,cast(model_code as varchar) as model_code, img_url, if_scene, 0 as rank
from img
where if_scene = 'false' and model_code = img_type and model_img_order like '%%01%%'
;

insert into bi.d_content_image
select distinct tmall_id,cast(model_code as varchar) as model_code, img_url, if_scene,
ROW_NUMBER () OVER ( PARTITION BY tmall_id, model_code ORDER BY (select null)) AS rank
from img
where if_scene = 'false' and model_img_order not like '%%01%%'
order by tmall_id, model_code
;

insert into bi.d_content_image
select distinct tmall_id,cast(model_code as varchar) as model_code, img_url, if_scene,
ROW_NUMBER () OVER ( PARTITION BY tmall_id, model_code ORDER BY (select null)) AS rank
from img
where if_scene = 'true'
order by tmall_id, model_code
;

drop table if exists image_scene;
-- select 3 scene images
create temp table image_scene as
SELECT
tmall_id, model_code, img_url, '好在哪里' as title, 1 as type, rank
FROM bi.d_content_image
WHERE
	rank < 4 and if_scene = 'true'
;

drop table if exists image_details;
create temp table image_details as
select tmall_id, cast(model_code as varchar), img_url, '产品解析' as title, 0 as type, rank
from bi.d_content_image
where rank in (1, 3) and if_scene = 'false'
;

drop table if exists image_details2;
create temp table image_details2 as
select tmall_id, cast(model_code as varchar), img_url, '设计亮点' as title, 2  as type, rank
from bi.d_content_image
where rank in (2, 4) and if_scene = 'false'
;

-- 头图3张
drop table if exists image_details3;
create temp table image_details3 as
select tmall_id,cast(model_code as varchar) as model_code, img_url, '主图' as title, 3 as type, rank
from bi.d_content_image
where rank in (0, 5, 6) and if_scene = 'false'
;

-- combined together
drop table if exists image_all;
create temp table image_all as
	select * from image_scene
	union all 
	select * from image_details
	union all 
	select * from image_details2
	union all
	select * from image_details3
	;

-- 内容图结合
drop table if exists image_str;
create temp table image_str as
select tmall_id, model_code, title, string_agg(img_url, '@@' order by model_code, type, rank) AS img_url_array
from image_all 
where type != 3 
group by tmall_id, model_code, title
;


drop table if exists img_cover;
create temp table img_cover as
	select model_code, string_agg(img_url, '@@' order by model_code, rank) as cover_img_str
				from image_all 
				where type = 3 
				and model_code in (select model_code from image_all where type = 3 group by model_code HAVING count(distinct img_url) = 3)
				group by model_code
				;



-- 符合主图和文章要求的
truncate smartdata_pro.d_content;
insert into smartdata_pro.d_content
SELECT DISTINCT A
	.tmall_id,
	A.model_code,
	product_name,
	C.cover_img_str,
	b.title,
	TEXT,
	img_url_array AS img_str 
FROM
	image_str
	A INNER JOIN bi.d_content_text b ON A.model_code = CAST ( b.model_code AS VARCHAR ) 
	AND A.title = b.title
	INNER JOIN img_cover C ON A.model_code = CAST ( C.model_code AS VARCHAR ) 
WHERE
	A.model_code IN ( SELECT model_code FROM image_all WHERE TYPE = 3 GROUP BY model_code HAVING COUNT ( DISTINCT img_url ) = 3 ) --240
	AND A.model_code IN ( SELECT cast(model_code as varchar) FROM bi.d_content_text WHERE TEXT != 'None' GROUP BY model_code HAVING COUNT ( DISTINCT TEXT ) = 3 ) --90
	and a.model_code IN (SELECT
							model_code
						FROM
							(
							SELECT
								tmall_id,
								model_code,
								title,
								(
									LENGTH (
										string_agg ( img_url_array, '@@' )) - LENGTH (
									REPLACE ( string_agg ( img_url_array, '@@' ), '@@', '' ))) / 2 + 1 AS url_size 
							FROM
								image_str 
							GROUP BY
								tmall_id,
								model_code,
								title 
							HAVING
								(
									LENGTH (
										string_agg ( img_url_array, '@@' )) - LENGTH (
									REPLACE ( string_agg ( img_url_array, '@@' ), '@@', '' ))) / 2 + 1 >= 2 
							) tmp 
						GROUP BY
							tmall_id,
							model_code 
						HAVING
							COUNT ( DISTINCT title ) = 3
													) --80
	;

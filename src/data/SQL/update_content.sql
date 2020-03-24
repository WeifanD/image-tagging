-- 基础图片数据表
CREATE TEMP TABLE img AS SELECT distinct a.*, b.img_source, b.img_order, b.img_type, b.img_url
FROM
	( SELECT DISTINCT tmall_id, model_code FROM smartdata_pro.d_product_info WHERE tmall_id IN ( SELECT DISTINCT tmall_id FROM smartdata_pro.d_product_online_rate WHERE tmall_sale_status = 'onsale' ) )
	A LEFT JOIN ( SELECT DISTINCT tmall_id, model_code, img_url, img_source, img_type as img_order,
substring(img_type,1,1) as img_type FROM smartdata_pro.d_product_img ) b ON A.model_code = b.model_code 
	OR A.tmall_id = b.tmall_id 
;
	
CREATE TEMP TABLE img_count AS SELECT
model_code,
COUNT ( DISTINCT img_url ) n_img
FROM
	img 
where img_source = 'cube'
GROUP BY
	model_code
	;
	
-- select * from img_count where model_code = '8353392'
	
CREATE TABLE if not exists "smartdata_pro"."d_content_img" (
  "tmall_id" varchar COLLATE "pg_catalog"."default",
  "model_code" varchar COLLATE "pg_catalog"."default",
  "img_source" varchar COLLATE "pg_catalog"."default",
  "img_order" varchar COLLATE "pg_catalog"."default",
  "img_type" varchar COLLATE "pg_catalog"."default",
  "img_url" varchar COLLATE "pg_catalog"."default",
  "tags" varchar COLLATE "pg_catalog"."default",
  "n_img" int4
)
;

-- alter table smartdata_pro.d_content_img drop COLUMN tags;
-- alter table smartdata_pro.d_content_img add COLUMN tags varchar
-- ;

	
TRUNCATE smartdata_pro.d_content_img;
INSERT INTO smartdata_pro.d_content_img 
SELECT
i.*,
ic.n_img
FROM
	img i
	INNER JOIN ( SELECT * FROM img_count ) ic ON i.model_code = ic.model_code;


UPDATE smartdata_pro.d_content_img b
SET    tags = a.tags
FROM   bi.d_content_img a
WHERE  a.img_url = b.img_url;


-- 官网场景图/产品细节图 (all)
CREATE TEMP TABLE image AS 
SELECT tmall_id, model_code, img_url, if_scene,
			ROW_NUMBER () OVER ( PARTITION BY A.tmall_id, A.model_code ORDER BY if_scene desc, img_type, img_order) AS RANK_scene,
			ROW_NUMBER () OVER ( PARTITION BY A.tmall_id, A.model_code ORDER BY img_type desc, img_order) AS RANK_detail  
		FROM
			(
			SELECT
			distinct
				tmall_id,
				model_code,
				img_url,
				img_type,
				img_order,
				( CASE WHEN img_type = 'c' THEN TRUE ELSE FALSE END ) if_scene
			-- ( CASE WHEN (tags LIKE'%face%person%' and img_type = 'h') or img_type = 'c' THEN TRUE ELSE FALSE END ) if_scene
	FROM
		smartdata_pro."d_content_img" 
	WHERE
		n_img > 8 
		AND img_source = 'cube'
		)a
;


-- select 3 scene images
create temp table image_scene as
SELECT
tmall_id, model_code, img_url, '好在哪里' as title, 1 as type, RANK_scene as rank
FROM image
WHERE
	RANK_scene < 4 and if_scene is TRUE
;


create temp table image_details as
select tmall_id, cast(model_code as varchar), img_url, '产品解析' as title, 0 as type, RANK_detail as rank
from image
where RANK_detail in (2,3) and if_scene is FALSE
;

create temp table image_details2 as
select tmall_id, cast(model_code as varchar), img_url, '设计亮点' as title, 2  as type, RANK_detail as rank
from image
where RANK_detail = 4 and if_scene is FALSE
;

create temp table image_details3 as
select tmall_id,cast(model_code as varchar) as model_code, img_url, '' as title, 3 as type, RANK_detail as rank
from image
where RANK_detail in (1, 5,6) and if_scene is FALSE
;

-- combined together
create temp table image_all as
	select * from image_scene
	union all 
	select * from image_details
	union all 
	select * from image_details2
	union all
	select * from image_details3
	;

create temp table image_str as
select tmall_id, model_code, title, string_agg(img_url, '@@' order by model_code, type, rank) AS img_url_array
from image_all 
where type != 3 
group by tmall_id, model_code, title
;

truncate smartdata_pro.d_content;
insert into smartdata_pro.d_content
SELECT DISTINCT
	a.tmall_id,
	a.model_code,
	product_name,
	C.cover_img_str,
	a.title,
	TEXT,
	img_url_array AS img_str
FROM
	image_all
	A INNER JOIN bi.d_content_text b ON A.model_code = cast(b.model_code as VARCHAR) 
	AND A.title = b.title
	LEFT JOIN ( select model_code, string_agg(img_url, '@@' order by model_code, rank) as cover_img_str
				from image_all 
				where type = 3 
				group by model_code) C ON A.model_code = cast(c.model_code as VARCHAR) 
	inner JOIN image_str d ON A.model_code = cast(d.model_code as VARCHAR) and a.title = d.title
;


SELECT DISTINCT A
	.model_code,
	b.universe_id,
	b.universe_label_zh,
	A.tmall_id,
	A.product_name,
	CASE
		
		WHEN LEFT ( split_part( COALESCE ( split_part( A.img, '@@', 1 ), '0' ), 'sq/', 1 ), 12 ) = 'https://pixl' THEN
		split_part( COALESCE ( split_part( A.img, '@@', 1 ), '0' ), 'sq/', 1 ) || 'sq/.jpg' ELSE split_part( COALESCE ( split_part( A.img_str, '@@', 1 ), '0' ), 'sq/', 1 ) 
	END img01,
CASE
	
	WHEN LEFT ( split_part( COALESCE ( split_part( A.img, '@@', 2 ), '0' ), 'sq/', 1 ), 12 ) = 'https://pixl' THEN
	split_part( COALESCE ( split_part( A.img, '@@', 2 ), '0' ), 'sq/', 1 ) || 'sq/.jpg' ELSE split_part( COALESCE ( split_part( A.img_str, '@@', 2 ), '0' ), 'sq/', 1 ) 
	END img02,
CASE
	
	WHEN LEFT ( split_part( COALESCE ( split_part( A.img, '@@', 3 ), '0' ), 'sq/', 1 ), 12 ) = 'https://pixl' THEN
	split_part( COALESCE ( split_part( A.img, '@@', 3 ), '0' ), 'sq/', 1 ) || 'sq/.jpg' ELSE split_part( COALESCE ( split_part( A.img_str, '@@', 3 ), '0' ), 'sq/', 1 ) 
	END img03,
	CASE
		
		WHEN LEFT ( split_part( COALESCE ( split_part( A.img, '@@', 1 ), '0' ), 'sq/', 1 ), 12 ) = 'https://pixl' THEN
		split_part( COALESCE ( split_part( A.img, '@@', 1 ), '0' ), 'sq/', 1 ) || 'sq/.jpg' ELSE split_part( COALESCE ( split_part( A.img_str, '@@', 1 ), '0' ), 'sq/', 1 ) 
	END img01,
CASE
	
	WHEN LEFT ( split_part( COALESCE ( split_part( A.img, '@@', 2 ), '0' ), 'sq/', 1 ), 12 ) = 'https://pixl' THEN
	split_part( COALESCE ( split_part( A.img, '@@', 2 ), '0' ), 'sq/', 1 ) || 'sq/.jpg' ELSE split_part( COALESCE ( split_part( A.img_str, '@@', 2 ), '0' ), 'sq/', 1 ) 
	END img02,
CASE
	
	WHEN LEFT ( split_part( COALESCE ( split_part( A.img, '@@', 3 ), '0' ), 'sq/', 1 ), 12 ) = 'https://pixl' THEN
	split_part( COALESCE ( split_part( A.img, '@@', 3 ), '0' ), 'sq/', 1 ) || 'sq/.jpg' ELSE split_part( COALESCE ( split_part( A.img_str, '@@', 3 ), '0' ), 'sq/', 1 ) 
	END img03,
	A.title,
	A.TEXT,
CASE
		
		WHEN LEFT ( split_part( COALESCE ( split_part( A.img_str, '@@', 1 ), '0' ), 'sq/', 1 ), 12 ) = 'https://pixl' THEN
		split_part( COALESCE ( split_part( A.img_str, '@@', 1 ), '0' ), 'sq/', 1 ) || 'sq/.jpg' ELSE split_part( COALESCE ( split_part( A.img_str, '@@', 1 ), '0' ), 'sq/', 1 ) 
	END img01,
CASE
	
	WHEN LEFT ( split_part( COALESCE ( split_part( A.img_str, '@@', 2 ), '0' ), 'sq/', 1 ), 12 ) = 'https://pixl' THEN
	split_part( COALESCE ( split_part( A.img_str, '@@', 2 ), '0' ), 'sq/', 1 ) || 'sq/.jpg' ELSE split_part( COALESCE ( split_part( A.img_str, '@@', 2 ), '0' ), 'sq/', 1 ) 
	END img02,
CASE
	
	WHEN LEFT ( split_part( COALESCE ( split_part( A.img_str, '@@', 3 ), '0' ), 'sq/', 1 ), 12 ) = 'https://pixl' THEN
	split_part( COALESCE ( split_part( A.img_str, '@@', 3 ), '0' ), 'sq/', 1 ) || 'sq/.jpg' ELSE split_part( COALESCE ( split_part( A.img_str, '@@', 3 ), '0' ), 'sq/', 1 ) 
	END img03,
CASE
	
	WHEN LEFT ( split_part( COALESCE ( split_part( A.img_str, '@@', 4 ), '0' ), 'sq/', 1 ), 12 ) = 'https://pixl' THEN
	split_part( COALESCE ( split_part( A.img_str, '@@', 4 ), '0' ), 'sq/', 1 ) || 'sq/.jpg' ELSE split_part( COALESCE ( split_part( A.img_str, '@@', 4 ), '0' ), 'sq/', 1 ) 
	END img04 
FROM
	(
	SELECT
		* 
	FROM
		smartdata_pro.d_content 
	WHERE
		model_code IN (
		SELECT DISTINCT
			model_code 
		FROM
			(
			SELECT DISTINCT
				tmall_id,
				model_code,
				count(distinct text) as text_size,
				(length(string_agg(img_str, '@@')) - length(replace(string_agg(img_str, '@@'), '@@', ''))) /2 + 1 AS url_size
			FROM
				smartdata_pro.d_content 
			WHERE
				TEXT != 'None' 
			GROUP BY
				tmall_id,
				model_code 
			having
			count(distinct text) = 3 and (length(string_agg(img_str, '@@')) - length(replace(string_agg(img_str, '@@'), '@@', ''))) /2 + 1 > 3
			) A
		
	))
A LEFT JOIN d_item_universe b ON A.model_code :: INT = b.model_code 
ORDER BY
	2;







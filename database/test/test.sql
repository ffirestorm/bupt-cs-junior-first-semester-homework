delimiter //

CREATE TRIGGER your_trigger_name
AFTER INSERT
ON your_table_name
FOR EACH ROW
BEGIN
    -- 检查是否已经存在相同主键的记录
    IF EXISTS (SELECT 1 FROM your_table_name WHERE l_orderkey = NEW.l_orderkey) THEN
        -- 如果存在，执行更新或删除再插入的逻辑
        -- 例如，这里假设你有其他列需要更新
        UPDATE your_table_name
        SET column1 = NEW.column1, column2 = NEW.column2
        WHERE l_orderkey = NEW.l_orderkey;
        -- 或者，如果你希望先删除再插入
        -- DELETE FROM your_table_name WHERE l_orderkey = NEW.l_orderkey;
        -- INSERT INTO your_table_name VALUES (NEW.l_orderkey, NEW.column1, NEW.column2, ...);
    ELSE
        -- 如果不存在相同主键的记录，直接插入
        -- 例如，这里假设你有其他列需要插入
        INSERT INTO your_table_name VALUES (NEW.l_orderkey, NEW.column1, NEW.column2, ...);
    END IF;
END //
delimiter ;

DELIMITER //
CREATE TRIGGER pk_trig_before
BEFORE INSERT ON lineitemcopy1_new
FOR EACH ROW
BEGIN
    DECLARE existing_rows INT;

    SELECT COUNT(*) INTO existing_rows
    FROM lineitemcopy1_new
    WHERE l_orderkey = NEW.l_orderkey;

    IF existing_rows > 0 THEN
        -- 如果主键重复，那么就删了再插入
        DELETE FROM lineitemcopy1_new WHERE l_orderkey = NEW.l_orderkey;
        
    END IF;
END //
DELIMITER ;

INSERT INTO lineitemcopy1_new
values(13220,0,0,2,0,0,0,0, 'a', 'b', '2020-01-02', 
'2020-01-01', '2020-01-01','name3', 'name4', 'name5');

INSERT INTO lineitemcopy1_new
values(13220,1,1,3,0,0,0,0, 'a', 'b', '2020-01-02', 
'2020-01-03', '2020-01-04','name3', 'name4', 'name5');

DELIMITER //
CREATE TRIGGER pk_trig_before
BEFORE INSERT ON lineitemcopy1_new
FOR EACH ROW
BEGIN
    DECLARE existing_rows INT;
    -- 检查主键是否已经存在
    SELECT COUNT(*) INTO existing_rows
    FROM lineitemcopy1_new
    WHERE l_orderkey = NEW.l_orderkey;

    IF existing_rows > 0 THEN
        -- 如果主键已经存在，更新已有元组的属性值
        DELETE FROM lineitemcopy1_new WHERE l_orderkey = NEW.l_orderkey;
    END IF;
END //
DELIMITER ;

CREATE TABLE lineitemcopy(
    L_ORDERKEY integer NOT NULL,
    L_PARTKEY integer NOT NULL,
    L_SUPPKEY integer NOT NULL,
    L_LINENUMBER integer NOT NULL,
    L_QUANTITY DECIMAL(15,2) NOT NULL,
    L_EXTENDEDPRICE DECIMAL(15,2) NOT NULL,
    L_DISCOUNT DECIMAL(15,2) NOT NULL,
    L_TAX DECIMAL(15,2) NOT NULL,
    L_RETURNFLAG CHAR(1) NOT NULL,
    L_LINESTATUS CHAR(1) NOT NULL,
    L_SHIPDATE DATE NOT NULL,
    L_COMMITDATE DATE NOT NULL,
    L_RECEIPTDATE DATE NOT NULL,
    L_SHIPINSTRUCT CHAR(25) NOT NULL,
    L_SHIPMODE CHAR(10) NOT NULL,
    L_COMMENT VARCHAR(44) NOT NULL
);


DELIMITER #
CREATE TRIGGER insert_trig_before BEFORE INSERT ON lineitemcopy1_new 
FOR EACH ROW
BEGIN
    IF (NEW.l_shipdate <= NEW.l_commitdate AND NEW.l_shipdate <= NEW.l_receiptdate) THEN
        INSERT INTO lineitemcopy (
            L_ORDERKEY, L_PARTKEY, L_SUPPKEY, L_LINENUMBER, L_QUANTITY, L_EXTENDEDPRICE, 
            L_DISCOUNT, L_TAX, L_RETURNFLAG, L_LINESTATUS, L_SHIPDATE, L_COMMITDATE, 
            L_RECEIPTDATE, L_SHIPINSTRUCT, L_SHIPMODE, L_COMMENT
        )VALUES (
            NEW.L_ORDERKEY, NEW.L_PARTKEY, NEW.L_SUPPKEY, NEW.L_LINENUMBER, 
            NEW.L_QUANTITY, NEW.L_EXTENDEDPRICE, NEW.L_DISCOUNT, NEW.L_TAX, 
            NEW.L_RETURNFLAG, NEW.L_LINESTATUS, NEW.L_SHIPDATE, NEW.L_COMMITDATE, 
            NEW.L_RECEIPTDATE, NEW.L_SHIPINSTRUCT, NEW.L_SHIPMODE, NEW.L_COMMENT
        );
    END IF;
END #
DELIMITER ;


DROP TRIGGER  IF EXISTS insert_trig_before;

INSERT INTO lineitemcopy1_new
values(4,0,0,2,0,0,0,0, 'a', 'b', '2020-01-02', 
'2020-01-01', '2020-01-01','name3', 'name4', 'name5');

ALTER TRIGGER insert_trig_before ENABLE;


DELIMITER #
CREATE TRIGGER updata_trig_before BEFORE UPDATE ON lineitemcopy1_new
FOR EACH ROW
BEGIN
    IF (NEW.l_shipdate <= NEW.l_commitdate AND NEW.l_shipdate <= NEW.l_receiptdate) THEN
        UPDATE lineitemcopy
        SET L_SHIPDATE = NEW.L_SHIPDATE
        WHERE L_ORDERKEY = NEW.L_ORDERKEY AND L_LINENUMBER = NEW.L_LINENUMBER;
    END IF;
END #
DELIMITER ;


DELIMITER #
CREATE TRIGGER pk_insert_trig_before BEFORE INSERT ON lineitemcopy1_new 
FOR EACH ROW
BEGIN
    DECLARE existing_rows INT;

    SELECT COUNT(*) INTO existing_rows
    FROM lineitemcopy
    WHERE l_orderkey = NEW.l_orderkey;

    IF existing_rows > 0 THEN
        -- 如果主键重复，那么就删了再插入
        DELETE FROM lineitemcopy WHERE l_orderkey = NEW.l_orderkey;
        INSERT INTO lineitemcopy (
            L_ORDERKEY, L_PARTKEY, L_SUPPKEY, L_LINENUMBER, L_QUANTITY, L_EXTENDEDPRICE, 
            L_DISCOUNT, L_TAX, L_RETURNFLAG, L_LINESTATUS, L_SHIPDATE, L_COMMITDATE, 
            L_RECEIPTDATE, L_SHIPINSTRUCT, L_SHIPMODE, L_COMMENT
        )VALUES (
            NEW.L_ORDERKEY, NEW.L_PARTKEY, NEW.L_SUPPKEY, NEW.L_LINENUMBER, 
            NEW.L_QUANTITY, NEW.L_EXTENDEDPRICE, NEW.L_DISCOUNT, NEW.L_TAX, 
            NEW.L_RETURNFLAG, NEW.L_LINESTATUS, NEW.L_SHIPDATE, NEW.L_COMMITDATE, 
            NEW.L_RECEIPTDATE, NEW.L_SHIPINSTRUCT, NEW.L_SHIPMODE, NEW.L_COMMENT
        );
    END IF;
END #
DELIMITER ;

DELIMITER #
CREATE TRIGGER count_trig_before BEFORE INSERT ON orderscopy 
FOR EACH ROW
BEGIN
    DECLARE  discount INT;
    SELECT DISTINCT C_ACCTBAL INTO discount
    FROM customer join orders on customer.C_CUSTKEY=orders.O_CUSTKEY
    WHERE NEW.O_CUSTKEY=orders.O_CUSTKEY;

    IF (discount >= 50) THEN
        INSERT INTO orders (
            O_ORDERKEY, O_CUSTKEY, O_ORDERSTATUS, O_TOTALPRICE, O_ORDERDATE, 
            O_ORDERPRIORITY, O_CLERK, O_SHIPPRIORITY, O_COMMENT
        )VALUES (
            NEW.O_ORDERKEY, NEW.O_CUSTKEY, NEW.O_ORDERSTATUS, NEW.O_TOTALPRICE, NEW.O_ORDERDATE, 
            NEW.O_ORDERPRIORITY, NEW.O_CLERK, NEW.O_SHIPPRIORITY, NEW.O_COMMENT            
        );
    END IF;
END #
DELIMITER ;


CREATE TABLE orderscopy ( O_ORDERKEY INTEGER NOT NULL,
O_CUSTKEY INTEGER NOT NULL,
O_ORDERSTATUS CHAR(1) NOT NULL,
O_TOTALPRICE DECIMAL(15,2) NOT NULL,
O_ORDERDATE DATE NOT NULL,
O_ORDERPRIORITY CHAR(15) NOT NULL,
O_CLERK CHAR(15) NOT NULL,
O_SHIPPRIORITY INTEGER NOT NULL,
O_COMMENT VARCHAR(79) NOT NULL);

insert into orderscopy
values(30002, 50, 'O', 114514, '2023-12-10', '123452021211138', '123452021211138', 1,'test')

    SELECT DISTINCT C_ACCTBAL 
    FROM customer join orders on customer.C_CUSTKEY=orders.O_CUSTKEY
    WHERE orders.O_CUSTKEY=50;

SELECT  
    TABLE_NAME AS relname,  
    PARTITION_METHOD AS parttype,  
    SUBPARTITION_METHOD AS subparttype, -- Optional, if you also want the subpartitioning method  
    PARTITION_NAME AS parentid,  
    PARTITION_DESCRIPTION AS boundaries  
FROM   
    information_schema.PARTITIONS  
WHERE   
    TABLE_NAME = 'partition_orders_1';  



-- 执行计划
explain
select part.p_partkey
from part join partsupp on part.p_partkey=partsupp.ps_partkey
where partsupp.ps_suppkey=5 and part.p_retailprice<920;

explain select p.p_partkey
from part p, partsupp ps
where p.p_partkey=ps.ps_partkey and
    ps.ps_suppkey=5 and p.p_retailprice<920;

explain
select c.c_name, c.c_phone
from customer c join nation n on c.c_nationkey=n.n_nationkey
where n.n_name='ALGERIA' and c.c_acctbal < 1000;

-- 在part上建立视图
create view part_view
AS
select * from part;
-- 查询并查看执行计划
explain
select p_partkey
from part_view;
-- 通过with临时视图进行查询
explain
with part_tempview as(
    select * 
    from part
)
select p_partkey
FROM part_tempview;
-- 不用视图查询
explain
select p_partkey
from part


explain
select * 
from lineitem
where l_quantity=50;

explain
select * 
from lineitem_new
where l_quantity=50;

explain
select * 
from lineitem
where l_extendedprice = 5000;

explain
select * 
from lineitem_new
where l_extendedprice = 5000;

alter table lineitem_new drop index qte_index;
create index lineitem_index1 on lineitem_new(l_suppkey);
create index lineitem_index2 on lineitem_new(l_partkey);

EXPLAIN
select DISTINCT l_suppkey,s_phone
from lineitem, supplier
where l_suppkey=10 AND l_suppkey=supplier.s_suppkey;

EXPLAIN
select DISTINCT l_suppkey,s_phone
from lineitem_new, supplier
where l_suppkey=10 AND l_suppkey=supplier.s_suppkey;

EXPLAIN
select DISTINCT l_partkey,p_name
from lineitem, part
where l_partkey= 928 AND l_partkey=part.p_partkey;

EXPLAIN
select DISTINCT l_partkey,p_name
from lineitem_new, part
where l_partkey= 928 AND l_partkey=part.p_partkey;

explain 
select s_suppkey
from supplier;

explain 
select s_suppkey
from supplier_new;

explain 
select s_suppkey
from supplier;

explain
select distinct b.l_orderkey
from lineitem_new a, lineitem_new b
where a.l_extendedprice = 16473.51
and a.l_discount = 0.04
and abs(a.l_quantity-b.l_quantity) < 20

explain
select distinct B.l_orderkey
FROM lineitem_new A, lineitem_new B
where A.l_extendedprice = 79238.70
and A.l_discount =0.04
and B.l_quantity >A.l_quantity -20
and B.l_quantity <A.l_quantity +20;

explain
select o.o_totalprice
from orders o join customer c on o.o_custkey=c.c_custkey
where o.o_custkey = 10

explain
select o.o_totalprice
from orders as o 
where o.o_custkey in(
    select c.c_custkey
    from customer as c 
    where c.c_custkey = 10
);
explain
select *
from lineitem_new
where l_quantity=36 AND (l_tax=0.06 OR l_discount=0.09)

explain
(
    select *
    from lineitem_new
    where l_quantity=36 AND l_tax=0.06 
)
UNION
(
    select *
    from lineitem_new
    where l_quantity=36 AND l_discount=0.09
);


-- 无distinct查询
explain
select s_suppkey
from supplier
where s_nationkey = 1 and s_acctbal < 1000

-- 有distinct查询
explain
select distinct s_suppkey
from supplier
where s_nationkey = 1 and s_acctbal < 1000

-- 找出客户表和订单表的客户key并综合到一起
explain
select c_custkey from customer
UNION all
select o_custkey from orders;

explain
select distinct lineitem.l_partkey
from lineitem,part
where lineitem.l_partkey=part.p_partkey;

explain
select distinct lineitem.l_partkey
from lineitem,part,orders
where lineitem.l_partkey=part.p_partkey and lineitem.l_orderkey=orders.O_ORDERKEY;


select *
from partsupp_1
where PS_AVAILQTY<20;
update partsupp_1
set PS_AVAILQTY=PS_AVAILQTY-15
where PS_AVAILQTY<20;
select *
from partsupp_1
where PS_AVAILQTY<20;

update partsupp_2
set PS_AVAILQTY=PS_AVAILQTY-15
where PS_AVAILQTY<20;

START TRANSACTION;
select PS_PARTKEY,PS_SUPPLYCOST
from partsupp_1
where PS_PARTKEY between '2020' and '2022';
update partsupp_1
set PS_SUPPLYCOST=200
where PS_PARTKEY between '2020' and '2022';
select PS_PARTKEY,PS_SUPPLYCOST
from partsupp_1
where PS_PARTKEY between '2020' and '2022';
commit;

START TRANSACTION;
select PS_PARTKEY,PS_SUPPLYCOST
from partsupp_2
where PS_PARTKEY between '2020' and '2022';
update partsupp_2
set PS_SUPPLYCOST=200
where PS_PARTKEY between '2020' and '2022';
select PS_PARTKEY,PS_SUPPLYCOST
from partsupp_2
where PS_PARTKEY between '2020' and '2022';
rollback;

select PS_PARTKEY,PS_SUPPKEY,PS_AVAILQTY
from partsupp_1
where PS_AVAILQTY<7;
INSERT INTO partsupp_1
values(2022,2022,6,0,'comment');
delete from partsupp_1
where PS_PARTKEY='2022' and PS_SUPPKEY='2022' ;
select PS_PARTKEY,PS_SUPPKEY,PS_AVAILQTY
from partsupp_1
where PS_AVAILQTY<7;


DELETE FROM partsupp_1;
DELETE FROM partsupp_2;
DROP TABLE partsupp_1;
DROP TABLE partsupp_2;


CREATE TABLE partsupp_1(  
PS_PARTKEY integer NOT NULL,  
PS_SUPPKEY integer NOT NULL,  
PS_AVAILQTY integer NOT NULL,  
PS_SUPPLYCOST decimal(15, 2) NOT NULL,  
PS_COMMENT varchar(199) NOT NULL  
);  
insert into partsupp_1  
select *  
from partsupp;  
CREATE TABLE partsupp_2(  
PS_PARTKEY integer NOT NULL,  
PS_SUPPKEY integer NOT NULL,  
PS_AVAILQTY integer NOT NULL,  
PS_SUPPLYCOST decimal(15, 2) NOT NULL,  
PS_COMMENT varchar(199) NOT NULL  
);  
insert into partsupp_2  
select *  
from partsupp;  


START TRANSACTION;
select PS_PARTKEY,PS_SUPPKEY,PS_AVAILQTY
from partsupp_2
where PS_AVAILQTY<7;
INSERT INTO partsupp_2
values(2022,2022,6,0,'comment');
delete from partsupp_2
where PS_PARTKEY='2022' and PS_SUPPKEY='2022' ;
select PS_PARTKEY,PS_SUPPKEY,PS_AVAILQTY
from partsupp_2
where PS_AVAILQTY<7;
COMMIT;

CREATE TABLE part_1 ( 
P_PARTKEY INTEGER NOT NULL,
P_NAME VARCHAR(55) NOT NULL,
P_MFGR CHAR(25) NOT NULL,
P_BRAND CHAR(10) NOT NULL,
P_TYPE VARCHAR(25) NOT NULL,
P_SIZE INTEGER NOT NULL,
P_CONTAINER CHAR(10) NOT NULL,
P_RETAILPRICE DECIMAL(15,2) NOT NULL,
P_COMMENT VARCHAR(23) NOT NULL );


start transaction;
select p_partkey
from part_1
where p_size > 300;
insert into part_1
values(202200, 'p_name', 'pmfgr20212111382021211138', 'brand11138', 'p_type', 300, 'pcontainer',2021211138.50, 'comment');
savepoint sp;
delete from part_1
where p_partkey=202200;
rollback to sp;
commit;

select p_partkey, p_size
from part_1
where p_partkey=202200

alter table part_1
add constraint
size_check  check(p_size >=1 and p_size <=50);

start transaction;
insert into part_1
values(2023307, 'p_name', 'pmfgr20212111382021211138', 'brand11138', 'p_type', 30, 'pcontainer',2021211138.50, 'comment');
insert into part_1
values(2023138, 'p_name', 'pmfgr20212111382021211138', 'brand11138', 'p_type', 60, 'pcontainer',2021211138.50, 'comment');
commit;

select * from part_1
where p_partkey = 2023307;
select * from part_1
where p_partkey = 2023138;


select *
from partsupp_1
where PS_PARTKEY='2022' and PS_SUPPKEY between '23' and '2022';

select ps_partkey, ps_suppkey, PS_AVAILQTY
from partsupp_2
where ps_partkey='2022' and ps_suppkey='1526';

fio -filename=/data/nfs/fio_test -direct=1 -rw=randwrite -bs=2048K -size=100G -runtime=300 -group_reporting -name=mytest -ioengine=libaio -numjobs=1 -iodepth=64 -iodepth_batch=8 -iodepth_low=8 -iodepth_batch_complete=8


CREATE TENANT IF NOT EXISTS mq_t1
PRIMARY_ZONE='zone1', 
RESOURCE_POOL_LIST=('mq_pool_01')
set OB_TCP_INVITED_NODES='%';


ALTER SYSTEM RESTORE mq_t1 FROM  
'file:///home/micuks/shared,file:///home/micuks/share/log_archive' UNTIL TIME='2023-12-12  
00:00:00' WITH 'pool_list=restore_pool';

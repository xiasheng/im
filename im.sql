
#init database
drop database im;
create database im;
use im;

#create admin account
insert into myapp_user_base (phonenum, password, created_at) values('admin', '21232F297A57A5A743894A0E4A801FC3', now());

#create test account
insert into myapp_user_base (phonenum, password, created_at) values('13800000000', 'E10ADC3949BA59ABBE56E057F20F883E', now());
insert into myapp_user_base (phonenum, password, created_at) values('13800000001', 'E10ADC3949BA59ABBE56E057F20F883E', now());
insert into myapp_user_base (phonenum, password, created_at) values('13800000002', 'E10ADC3949BA59ABBE56E057F20F883E', now());
insert into myapp_user_base (phonenum, password, created_at) values('13800000003', 'E10ADC3949BA59ABBE56E057F20F883E', now());
insert into myapp_user_base (phonenum, password, created_at) values('13800000004', 'E10ADC3949BA59ABBE56E057F20F883E', now());
insert into myapp_user_base (phonenum, password, created_at) values('13800000005', 'E10ADC3949BA59ABBE56E057F20F883E', now());
insert into myapp_user_base (phonenum, password, created_at) values('13800000006', 'E10ADC3949BA59ABBE56E057F20F883E', now());
insert into myapp_user_base (phonenum, password, created_at) values('13800000007', 'E10ADC3949BA59ABBE56E057F20F883E', now());
insert into myapp_user_base (phonenum, password, created_at) values('13800000008', 'E10ADC3949BA59ABBE56E057F20F883E', now());
insert into myapp_user_base (phonenum, password, created_at) values('13800000009', 'E10ADC3949BA59ABBE56E057F20F883E', now());


#create a function to calculate distance according to lat and lng
DELIMITER $$  
DROP FUNCTION IF EXISTS `GetDistance` $$  
CREATE FUNCTION `GetDistance` (lat1 double, lng1 double, lat2 double,lng2 double) RETURNS double
BEGIN
   DECLARE  distance  double ;
   if ((lat1=0 and lng1=0) or (lat2=0 and lng2=0)) then   
       set distance=99999999.00;
   else
       SET distance= 2 * 6378.137* ASIN(SQRT(POW(SIN(PI() * (lat1-lat2) / 360),2)+COS(PI() * lat1 / 180)* COS(lat2* PI() / 180) * POW(SIN(PI() * (lng1-lng2) /360), 2)));
   end if;
   RETURN distance;
END $$
DELIMITER ;

#restart mysql
service mysql restart

#mysql character set 
SHOW VARIABLES LIKE 'character%';
SHOW VARIABLES LIKE 'collation_%';
SHOW CREATE DATABSE ddd;
SHOW CREATE TABLE ttt;

#set default utf8
#/etc/mysql/my.cnf
[client]
default-character-set=utf8

[mysqld]
character-set-server=utf8
collation-server=utf8_general_ci

[mysql]
default-character-set=utf8

#alter character    
ALTER TABLE django_content_type CONVERT TO CHARACTER SET utf8;
ALTER TABLE django_session CONVERT TO CHARACTER SET utf8;
ALTER TABLE myapp_account_thirdparty CONVERT TO CHARACTER SET utf8;
ALTER TABLE myapp_comment CONVERT TO CHARACTER SET utf8;
ALTER TABLE myapp_fans CONVERT TO CHARACTER SET utf8;
ALTER TABLE myapp_forward CONVERT TO CHARACTER SET utf8;
ALTER TABLE myapp_friends CONVERT TO CHARACTER SET utf8;
ALTER TABLE myapp_like CONVERT TO CHARACTER SET utf8;
ALTER TABLE myapp_status CONVERT TO CHARACTER SET utf8;
ALTER TABLE myapp_user_base CONVERT TO CHARACTER SET utf8;
ALTER TABLE myapp_user_detail CONVERT TO CHARACTER SET utf8;
ALTER TABLE myapp_user_history CONVERT TO CHARACTER SET utf8;
ALTER TABLE myapp_user_online CONVERT TO CHARACTER SET utf8;


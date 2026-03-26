```sql

create table SC(
	Sno char(10) not null,
	Cno char(10) not null,
	Grade int,
	
	primary key (Sno,Cno),
	foreign key (Cno) references Course(Cno),
	foreign key (Sno) references Student(Sno),
	
	check (Grade >= 0 and Grade <= 100)
);

select Sno,Sname
from Student
where Sage>19 and Sdept='计算机系' ;

update SC set Grade = least(Grade + 10,100)
where exists(
	select 1
	from Student
	where Student.Ssex='女' and SC.Sno=Student.Sno	
);
   
create view E_W(Sno,Sname,Cno,Grade) as 
select st.Sno,st.Sname,sc.Cno,sc.Grade
from Student st,SC sc
where st.Sno=sc.Sno and st.Sdept='计算机系' ;

delete from SC where Grade < 60 and exists(
	select 1
	from Student
	where Student.Sdept = 'CS' and Student.Sno = SC.Sno
);
```

简述两段锁协议；
简述并发调度正确性的标准；
如何保证并发调度的正确性；
简述数据库的三层模式，及这种结构的好处；
简述登记日志文件时必须遵循的原则；
简述关系模型的参照完整性；
简述事务的ACID特性，及其在并发控制和故障恢复中的作用；
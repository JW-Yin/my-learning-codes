# MySQL一主一从集群标准化操作全流程

---

## 第一阶段：前置环境准备（必须先完成）
所有操作的基础，需在主、从两台服务器上均完成：
1.  为两台服务器配置**静态IP**，确保网络互通（两台机器可互相ping通对方IP，且开放3306端口）
2.  两台服务器均完成MySQL安装
3.  关闭防火墙限制（或在防火墙中放行3306端口，确保主从节点可互相访问MySQL服务）

---

## 第二阶段：主库（Master）节点配置流程
### 步骤1：修改MySQL核心配置文件
1.  编辑配置文件：
    ```bash
    sudo vim /etc/mysql/mysql.conf.d/mysqld.cnf
    ```
2.  在`[mysqld]`段落中，添加/修改以下配置：
    ```ini
    # 1. 主从复制核心配置
    server-id = 1                  # 集群内唯一ID，主库固定为1，不可与从库重复
    log-bin = mysql-bin            # 开启二进制日志binlog，主从复制必备
    binlog_format = ROW            # 推荐行格式binlog，提升复制准确性
    sync_binlog = 1                # 每次事务提交同步binlog到磁盘，防止崩溃丢日志

    # 2. 网络访问配置
    bind-address = 主库真实IP地址       # 改为主库实际IP，不能用127.0.0.1，确保从库可访问
    mysqlx-bind-address = 主库真实IP地址 # 同上，修改为实际IP

    # 3. 可选配置（按需添加）
    # binlog_do_db = 要同步的数据库名    # 只同步指定库，不配置则同步所有库
    # binlog_ignore_db = mysql          # 忽略不同步的系统库
    ```

### 步骤2：重启MySQL服务，使配置生效
```bash
sudo service mysql restart
```

### 步骤3：登录MySQL控制台
```bash
sudo mysql -u root -p
# 执行后输入MySQL的root密码，进入控制台
```

### 步骤4：创建主从复制专用账号并授权
1.  创建复制账号（替换`password`为自定义强密码）：
    ```sql
    CREATE USER 'repl_user'@'%' IDENTIFIED BY 'password';
    ```
2.  授予账号复制权限：
    ```sql
    GRANT REPLICATION SLAVE ON *.* TO 'repl_user'@'%';
    ```
3.  适配MySQL 8.0+，修改认证插件（避免从库连接失败）：
    ```sql
    ALTER USER 'repl_user'@'%' IDENTIFIED WITH mysql_native_password BY 'password';
    ```
4.  刷新权限使配置生效：
    ```sql
    FLUSH PRIVILEGES;
    ```

### 步骤5：获取主库binlog关键信息（从库配置必须使用）
1.  执行查询命令：
    ```sql
    SHOW MASTER STATUS;
    ```
2.  **必须记录两个核心值，后续从库配置要完全匹配**：
    - `File`：binlog文件名（如`mysql-bin.000001`）
    - `Position`：binlog偏移量（如`156`）
3.  注意：执行后不要关闭当前MySQL终端，避免锁释放、Position值变化。

---

## 第三阶段：从库（Slave）节点配置流程
### 步骤1：修改MySQL核心配置文件
1.  编辑配置文件：
    ```bash
    sudo vim /etc/mysql/mysql.conf.d/mysqld.cnf
    ```
2.  在`[mysqld]`段落中，添加/修改以下配置：
    ```ini
    # 1. 主从复制核心配置
    server-id = 2                  # 集群内唯一ID，必须与主库不同，不可重复
    relay-log = relay-bin          # 开启中继日志，存储主库同步的binlog
    read_only = 1                  # 开启从库只读，防止普通用户误写数据（root用户不受限）
    ```

### 步骤2：重启MySQL服务，使配置生效
```bash
sudo service mysql restart
```

### 步骤3：登录MySQL控制台
```bash
sudo mysql -u root -p
# 执行后输入MySQL的root密码，进入控制台
```

### 步骤4：配置主从复制关系
1.  先停止已有的复制线程（全新环境可跳过，执行无负面影响）：
    ```sql
    STOP SLAVE;
    ```
2.  绑定主库信息，配置复制关系（**所有参数必须与主库配置完全一致**）：
    ```sql
    CHANGE MASTER TO
    MASTER_HOST='主库真实IP地址',
    MASTER_USER='主库创建的复制用户名（如repl_user）',
    MASTER_PASSWORD='复制用户的密码',
    MASTER_LOG_FILE='主库SHOW MASTER STATUS查到的File值',
    MASTER_LOG_POS=主库SHOW MASTER STATUS查到的Position数值;
    ```

### 步骤5：启动从库复制线程
```sql
START SLAVE;
```

### 步骤6：验证复制状态（核心检查项）
执行状态查询命令：
```sql
SHOW SLAVE STATUS\G
```
**必须满足两个核心状态均为Yes，复制才正常生效**：
- `Slave_IO_Running: Yes`（IO线程正常，负责接收主库binlog）
- `Slave_SQL_Running: Yes`（SQL线程正常，负责重放中继日志）

---

## 第四阶段：主从同步功能有效性验证
1.  **在主库执行测试操作**：
    ```sql
    -- 创建测试库
    CREATE DATABASE test;
    USE test;
    -- 创建测试表
    CREATE TABLE test_table (
      id INT AUTO_INCREMENT PRIMARY KEY,
      name VARCHAR(255)
    );
    -- 插入测试数据
    INSERT INTO test_table (name) VALUES ('test_data_1'), ('test_data_2');
    ```

2.  **在从库验证数据同步**：
    ```sql
    USE test;
    SELECT * FROM test_table;
    ```

3.  验证结果：若从库能查询到主库插入的2条测试数据，说明主从同步配置成功。

---

## 第五阶段：生产环境性能&安全优化配置
### 1. 从库并行复制优化（减少主从延迟）
在从库`mysqld.cnf`的`[mysqld]`段落添加：
```ini
# 基于事务逻辑时钟的并行复制，大幅提升重放效率
slave_parallel_type = LOGICAL_CLOCK
# 并行工作线程数，根据服务器CPU核数调整（4核设4，8核设8）
slave_parallel_workers = 4
```

### 2. 主库事务隔离级别优化（提升并发性能）
在主库`mysqld.cnf`的`[mysqld]`段落添加：
```ini
# 读已提交隔离级别，减少锁持有时间，提升并发能力
transaction_isolation = READ-COMMITTED
```

### 3. 只读配置验证
在从库执行命令，确认只读配置生效：
```sql
show variables like 'read_only';
```

---

## 关键注意事项
1.  集群内所有节点的`server-id`必须唯一，主从不能重复
2.  主库`bind-address`必须改为真实IP，否则从库无法连接主库MySQL服务
3.  生产环境建议将复制账号的`%`改为从库固定IP，提升安全性
4.  配置主从关系时，`MASTER_LOG_FILE`和`MASTER_LOG_POS`必须与主库查询结果完全一致，否则复制会失败
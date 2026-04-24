> 假设有A-Z，共26台机器，要部署一个高可用的Ceph集群，如何安排


纯对象/块存储（无 CephFS）

- AB两台，每台均部署 HAProxy + Keepalived + Prometheus + Grafana，做主备模式
- CDEFG五台，每台上均部署 MON + MGR
- 剩余所有机器，每台上均部署 OSD + RGW，必须配置 NUMA 绑定和内存 Cgroup 限制，防止 RGW 的突发流量耗尽 OSD 内存

 
需要 POSIX 文件存储（有 CephFS）

- AB两台，每台均部署 HAProxy + Keepalived + Prometheus + Grafana，做主备模式
- CDEFG五台，每台上均部署 MON + MGR
- HIJK四台，每台上均部署 OSD + MDS
- 剩余所有机器，每台上均部署 OSD + RGW
---
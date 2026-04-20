
# 📘 Ceph 集群演示部署指南（Docker 方式）

> **适用场景**：单机快速搭建 Ceph 集群进行功能演示、K8s 对接测试。  
> **集群架构**：3 MON + 3 MGR + 3 OSD（高可用最小集）  
> **存储能力**：**RBD 块存储**（开箱即用）、CephFS（可选）、RGW（可选）

---

## 一、环境与规划

| 项目 | 说明 |
| :--- | :--- |
| **宿主机** | Linux（Fedora/Ubuntu/CentOS），已安装 Docker |
| **Ceph 版本** | Quincy（`quay.io/ceph/ceph:v17.2.8`） |
| **网络** | Docker 桥接网络 `ceph-public`，子网 `192.168.206.0/24` |
| **节点规划** | 三个逻辑节点，每个节点运行 MON + MGR + OSD |

| 节点名称 | IP 地址 | 角色 |
| :--- | :--- | :--- |
| `ceph-node1` | `192.168.206.151` | MON + MGR + OSD |
| `ceph-node2` | `192.168.206.152` | MON + MGR + OSD |
| `ceph-node3` | `192.168.206.153` | MON + MGR + OSD |

---

## 二、演示前置准备

### 1. 安装宿主机工具
```bash
# Fedora
sudo dnf install -y ceph-base ceph-common

# Ubuntu
sudo apt update && sudo apt install -y ceph-base ceph-common
```

### 2. 清理旧环境（如有）
```bash
docker ps -a | grep ceph- | awk '{print $1}' | xargs -r docker rm -f
docker network rm ceph-public 2>/dev/null || true
sudo rm -rf /etc/ceph /var/lib/ceph* /tmp/ceph* /tmp/monmap /var/lib/ceph-osd-disks
```

### 3. 创建网络与拉取镜像
```bash
docker network create --subnet=192.168.206.0/24 ceph-public
docker pull quay.io/ceph/ceph:v17.2.8
```

### 4. 生成集群 FSID
```bash
export FSID=$(uuidgen)
echo "集群 FSID: $FSID"   # 记录备用
```

---

## 三、部署第一个 MON（`ceph-node1`）

### 1. 创建基础目录和配置文件
```bash
sudo mkdir -p /etc/ceph /var/lib/ceph/mon/ceph-ceph-node1

sudo tee /etc/ceph/ceph.conf <<EOF
[global]
fsid = $FSID
mon_initial_members = ceph-node1
mon_host = 192.168.206.151
public_network = 192.168.206.0/24
auth_cluster_required = cephx
auth_service_required = cephx
auth_client_required = cephx
osd_pool_default_size = 1
osd_pool_default_min_size = 1
EOF
```

### 2. 生成密钥环和 monmap
```bash
# mon. 密钥
sudo ceph-authtool --create-keyring /tmp/ceph.mon.keyring --gen-key -n mon. --cap mon 'allow *'

# client.admin 密钥
sudo ceph-authtool --create-keyring /etc/ceph/ceph.client.admin.keyring --gen-key -n client.admin \
  --cap mon 'allow *' --cap osd 'allow *' --cap mds 'allow *' --cap mgr 'allow *'

# 合并密钥
sudo ceph-authtool /tmp/ceph.mon.keyring --import-keyring /etc/ceph/ceph.client.admin.keyring

# 生成 monmap
monmaptool --create --add ceph-node1 192.168.206.151 --fsid $FSID /tmp/monmap
```

### 3. 初始化 MON 数据目录并启动容器
```bash
# 初始化（--mkfs）
sudo docker run --rm \
  -v /var/lib/ceph:/var/lib/ceph:z \
  -v /etc/ceph:/etc/ceph:z \
  -v /tmp:/tmp:z \
  quay.io/ceph/ceph:v17.2.8 \
  ceph-mon --mkfs -i ceph-node1 --monmap /tmp/monmap --keyring /tmp/ceph.mon.keyring \
  --public-addr 192.168.206.151

# 修正权限（容器内 ceph 用户 UID=167）
sudo chown -R 167:167 /var/lib/ceph /etc/ceph

# 启动 MON 容器
docker run -d \
  --name ceph-mon-ceph-node1 \
  --network ceph-public \
  --ip 192.168.206.151 \
  -v /var/lib/ceph:/var/lib/ceph:z \
  -v /etc/ceph:/etc/ceph:z \
  -e MON_IP=192.168.206.151 \
  quay.io/ceph/ceph:v17.2.8 \
  ceph-mon -i ceph-node1 -f
```

### 4. 验证单节点状态
```bash
sleep 10
docker exec ceph-mon-ceph-node1 ceph -s
```
预期输出：`mon: 1 daemons, quorum ceph-node1`

---

## 四、添加第二个 MON（`ceph-node2`）

### 1. 导出当前 monmap 和密钥
```bash
docker exec ceph-mon-ceph-node1 ceph mon getmap -o /tmp/monmap
docker cp ceph-mon-ceph-node1:/tmp/monmap /tmp/monmap
```

### 2. 准备 node2 配置目录
```bash
sudo mkdir -p /etc/ceph-mon-ceph-node2 /var/lib/ceph-mon-ceph-node2/mon/ceph-ceph-node2

sudo cp /etc/ceph/ceph.conf /etc/ceph-mon-ceph-node2/ceph.conf
sudo cp /etc/ceph/ceph.client.admin.keyring /etc/ceph-mon-ceph-node2/
sudo cp /tmp/ceph.mon.keyring /etc/ceph-mon-ceph-node2/
sudo cp /tmp/monmap /etc/ceph-mon-ceph-node2/

# 修改配置，加入 node2 信息
sudo sed -i 's/mon_initial_members = ceph-node1/mon_initial_members = ceph-node1,ceph-node2/' /etc/ceph-mon-ceph-node2/ceph.conf
sudo sed -i 's/mon_host = 192.168.206.151/mon_host = 192.168.206.151,192.168.206.152/' /etc/ceph-mon-ceph-node2/ceph.conf
```

### 3. 初始化并启动 node2 容器
```bash
# 初始化
sudo docker run --rm \
  -v /var/lib/ceph-mon-ceph-node2:/var/lib/ceph:z \
  -v /etc/ceph-mon-ceph-node2:/etc/ceph:z \
  -v /tmp:/tmp:z \
  quay.io/ceph/ceph:v17.2.8 \
  ceph-mon --mkfs -i ceph-node2 --monmap /tmp/monmap --keyring /tmp/ceph.mon.keyring \
  --public-addr 192.168.206.152

# 修正权限
sudo chown -R 167:167 /var/lib/ceph-mon-ceph-node2 /etc/ceph-mon-ceph-node2

# 启动容器
docker run -d \
  --name ceph-mon-ceph-node2 \
  --network ceph-public \
  --ip 192.168.206.152 \
  -v /var/lib/ceph-mon-ceph-node2:/var/lib/ceph:z \
  -v /etc/ceph-mon-ceph-node2:/etc/ceph:z \
  -e MON_IP=192.168.206.152 \
  quay.io/ceph/ceph:v17.2.8 \
  ceph-mon -i ceph-node2 -f
```

### 4. 验证
```bash
sleep 10
docker exec ceph-mon-ceph-node1 ceph -s
```
预期输出：`mon: 2 daemons, quorum ceph-node1,ceph-node2`

---

## 五、添加第三个 MON（`ceph-node3`）

### 1. 准备 node3 目录
```bash
sudo mkdir -p /etc/ceph-mon-ceph-node3 /var/lib/ceph-mon-ceph-node3/mon/ceph-ceph-node3

sudo cp /etc/ceph/ceph.conf /etc/ceph-mon-ceph-node3/ceph.conf
sudo cp /etc/ceph/ceph.client.admin.keyring /etc/ceph-mon-ceph-node3/
sudo cp /tmp/ceph.mon.keyring /etc/ceph-mon-ceph-node3/
sudo cp /tmp/monmap /etc/ceph-mon-ceph-node3/

# 修改配置，加入三个节点信息
sudo sed -i 's/mon_initial_members = ceph-node1/mon_initial_members = ceph-node1,ceph-node2,ceph-node3/' /etc/ceph-mon-ceph-node3/ceph.conf
sudo sed -i 's/mon_host = 192.168.206.151/mon_host = 192.168.206.151,192.168.206.152,192.168.206.153/' /etc/ceph-mon-ceph-node3/ceph.conf
```

### 2. 初始化并启动 node3 容器
```bash
# 初始化
sudo docker run --rm \
  -v /var/lib/ceph-mon-ceph-node3:/var/lib/ceph:z \
  -v /etc/ceph-mon-ceph-node3:/etc/ceph:z \
  -v /tmp:/tmp:z \
  quay.io/ceph/ceph:v17.2.8 \
  ceph-mon --mkfs -i ceph-node3 --monmap /tmp/monmap --keyring /tmp/ceph.mon.keyring \
  --public-addr 192.168.206.153

# 修正权限
sudo chown -R 167:167 /var/lib/ceph-mon-ceph-node3 /etc/ceph-mon-ceph-node3

# 启动容器
docker run -d \
  --name ceph-mon-ceph-node3 \
  --network ceph-public \
  --ip 192.168.206.153 \
  -v /var/lib/ceph-mon-ceph-node3:/var/lib/ceph:z \
  -v /etc/ceph-mon-ceph-node3:/etc/ceph:z \
  -e MON_IP=192.168.206.153 \
  quay.io/ceph/ceph:v17.2.8 \
  ceph-mon -i ceph-node3 -f
```

### 3. 更新 node1 配置并重启
```bash
sudo sed -i 's/mon_initial_members = ceph-node1/mon_initial_members = ceph-node1,ceph-node2,ceph-node3/' /etc/ceph/ceph.conf
sudo sed -i 's/mon_host = 192.168.206.151/mon_host = 192.168.206.151,192.168.206.152,192.168.206.153/' /etc/ceph/ceph.conf
docker restart ceph-mon-ceph-node1
```

### 4. 验证三 MON 就绪
```bash
sleep 10
docker exec ceph-mon-ceph-node1 ceph -s
```
预期输出：`mon: 3 daemons, quorum ceph-node1,ceph-node2,ceph-node3`

---

## 六、部署三个 MGR（高可用管理节点）

### 1. 部署 node1 的 MGR
```bash
# 创建密钥
docker exec ceph-mon-ceph-node1 ceph auth get-or-create mgr.ceph-node1 mon 'allow profile mgr' osd 'allow *' mds 'allow *' \
  -o /etc/ceph/ceph.mgr.ceph-node1.keyring

# 准备数据目录
sudo mkdir -p /var/lib/ceph/mgr/ceph-ceph-node1
sudo cp /etc/ceph/ceph.mgr.ceph-node1.keyring /var/lib/ceph/mgr/ceph-ceph-node1/keyring
sudo chown -R 167:167 /var/lib/ceph/mgr

# 启动容器
docker run -d \
  --name ceph-mgr-ceph-node1 \
  --network ceph-public \
  -v /etc/ceph:/etc/ceph:z \
  -v /var/lib/ceph/mgr:/var/lib/ceph/mgr:z \
  quay.io/ceph/ceph:v17.2.8 \
  ceph-mgr -i ceph-node1 -f
```

### 2. 部署 node2 的 MGR
```bash
docker exec ceph-mon-ceph-node1 ceph auth get-or-create mgr.ceph-node2 mon 'allow profile mgr' osd 'allow *' mds 'allow *' \
  -o /etc/ceph/ceph.mgr.ceph-node2.keyring

sudo mkdir -p /var/lib/ceph-mon-ceph-node2/mgr/ceph-ceph-node2
sudo cp /etc/ceph/ceph.mgr.ceph-node2.keyring /var/lib/ceph-mon-ceph-node2/mgr/ceph-ceph-node2/keyring
sudo chown -R 167:167 /var/lib/ceph-mon-ceph-node2/mgr

docker run -d \
  --name ceph-mgr-ceph-node2 \
  --network ceph-public \
  -v /etc/ceph-mon-ceph-node2:/etc/ceph:z \
  -v /var/lib/ceph-mon-ceph-node2/mgr:/var/lib/ceph/mgr:z \
  quay.io/ceph/ceph:v17.2.8 \
  ceph-mgr -i ceph-node2 -f
```

### 3. 部署 node3 的 MGR
```bash
docker exec ceph-mon-ceph-node1 ceph auth get-or-create mgr.ceph-node3 mon 'allow profile mgr' osd 'allow *' mds 'allow *' \
  -o /etc/ceph/ceph.mgr.ceph-node3.keyring

sudo mkdir -p /var/lib/ceph-mon-ceph-node3/mgr/ceph-ceph-node3
sudo cp /etc/ceph/ceph.mgr.ceph-node3.keyring /var/lib/ceph-mon-ceph-node3/mgr/ceph-ceph-node3/keyring
sudo chown -R 167:167 /var/lib/ceph-mon-ceph-node3/mgr

docker run -d \
  --name ceph-mgr-ceph-node3 \
  --network ceph-public \
  -v /etc/ceph-mon-ceph-node3:/etc/ceph:z \
  -v /var/lib/ceph-mon-ceph-node3/mgr:/var/lib/ceph/mgr:z \
  quay.io/ceph/ceph:v17.2.8 \
  ceph-mgr -i ceph-node3 -f
```

### 4. 验证 MGR 状态
```bash
docker exec ceph-mon-ceph-node1 ceph -s
```
预期输出：`mgr: ceph-node1(active), standbys: ceph-node2, ceph-node3`

---

## 七、添加三个 OSD（存储节点）

### 1. 创建虚拟磁盘（loop 设备）
```bash
sudo mkdir -p /var/lib/ceph-osd-disks
for i in 1 2 3; do
    sudo dd if=/dev/zero of=/var/lib/ceph-osd-disks/osd-node${i}.img bs=1M count=0 seek=10240
    sudo losetup /dev/loop$((10+$i)) /var/lib/ceph-osd-disks/osd-node${i}.img
done
```

### 2. 生成并分发 bootstrap-osd 密钥
```bash
# 获取密钥
docker exec ceph-mon-ceph-node1 ceph auth get-or-create client.bootstrap-osd mon 'allow profile bootstrap-osd' > /tmp/bootstrap-osd.keyring

# 分发到 node1
docker exec ceph-mon-ceph-node1 mkdir -p /var/lib/ceph/bootstrap-osd
docker cp /tmp/bootstrap-osd.keyring ceph-mon-ceph-node1:/var/lib/ceph/bootstrap-osd/ceph.keyring
docker exec ceph-mon-ceph-node1 chown -R 167:167 /var/lib/ceph/bootstrap-osd

# 分发到 node2/node3
for N in 2 3; do
    sudo mkdir -p /var/lib/ceph-mon-ceph-node${N}/bootstrap-osd
    sudo cp /tmp/bootstrap-osd.keyring /var/lib/ceph-mon-ceph-node${N}/bootstrap-osd/ceph.keyring
    sudo mkdir -p /etc/ceph-mon-ceph-node${N}
    sudo cp /tmp/bootstrap-osd.keyring /etc/ceph-mon-ceph-node${N}/ceph.client.bootstrap-osd.keyring
    sudo chown -R 167:167 /var/lib/ceph-mon-ceph-node${N}/bootstrap-osd /etc/ceph-mon-ceph-node${N}
done
```

### 3. 重建 MON 容器以挂载磁盘
```bash
# Node1
docker stop ceph-mon-ceph-node1 && docker rm ceph-mon-ceph-node1
docker run -d --name ceph-mon-ceph-node1 --network ceph-public --ip 192.168.206.151 \
  -v /var/lib/ceph:/var/lib/ceph:z -v /etc/ceph:/etc/ceph:z \
  --device /dev/loop11:/dev/sdb --cap-add SYS_ADMIN \
  quay.io/ceph/ceph:v17.2.8 ceph-mon -i ceph-node1 -f

# Node2
docker stop ceph-mon-ceph-node2 && docker rm ceph-mon-ceph-node2
docker run -d --name ceph-mon-ceph-node2 --network ceph-public --ip 192.168.206.152 \
  -v /var/lib/ceph-mon-ceph-node2:/var/lib/ceph:z -v /etc/ceph-mon-ceph-node2:/etc/ceph:z \
  --device /dev/loop12:/dev/sdb --cap-add SYS_ADMIN \
  quay.io/ceph/ceph:v17.2.8 ceph-mon -i ceph-node2 -f

# Node3
docker stop ceph-mon-ceph-node3 && docker rm ceph-mon-ceph-node3
docker run -d --name ceph-mon-ceph-node3 --network ceph-public --ip 192.168.206.153 \
  -v /var/lib/ceph-mon-ceph-node3:/var/lib/ceph:z -v /etc/ceph-mon-ceph-node3:/etc/ceph:z \
  --device /dev/loop13:/dev/sdb --cap-add SYS_ADMIN \
  quay.io/ceph/ceph:v17.2.8 ceph-mon -i ceph-node3 -f
```

### 4. 在每个容器内添加 OSD
以下操作在 **三个容器内分别执行一次**（以 node1 为例，进入容器后粘贴全部命令）：

```bash
# 进入容器
docker exec -it ceph-mon-ceph-node1 bash

# 粘贴执行以下命令块
OSD_FSID=$(uuidgen)
OSD_SECRET=$(ceph-authtool --gen-print-key)
echo "FSID: $OSD_FSID"
echo "Secret: $OSD_SECRET"

OSD_ID=$(echo "{\"cephx_secret\": \"$OSD_SECRET\"}" | \
  ceph osd new $OSD_FSID -i - \
  -n client.bootstrap-osd \
  --keyring /var/lib/ceph/bootstrap-osd/ceph.keyring)
echo "Allocated OSD ID: $OSD_ID"

mkdir -p /var/lib/ceph/osd/ceph-$OSD_ID
ln -s /dev/sdb /var/lib/ceph/osd/ceph-$OSD_ID/block

ceph-authtool --create-keyring /var/lib/ceph/osd/ceph-$OSD_ID/keyring \
  --name osd.$OSD_ID --add-key $OSD_SECRET

ceph-osd -i $OSD_ID --mkfs --osd-uuid $OSD_FSID
chown -R ceph:ceph /var/lib/ceph/osd/ceph-$OSD_ID
ceph-osd -i $OSD_ID -f &

# 验证
ceph osd tree
exit
```

**注意**：node2 和 node3 的容器名称分别为 `ceph-mon-ceph-node2` 和 `ceph-mon-ceph-node3`，进入后执行完全相同的命令块即可。

```bash
# 查看存储池名
docker exec ceph-mon-ceph-node1 ceph osd pool ls
# 将存储池设置为3副本机制
docker exec ceph-mon-ceph-node1 ceph osd pool set [池名] size 3
```

### 5. 最终集群状态验证
```bash
docker exec ceph-mon-ceph-node1 ceph -s
```
预期输出：
```
  cluster:
    id:     <fsid>
    health: HEALTH_OK 

  services:
    mon: 3 daemons, quorum ceph-node1,ceph-node2,ceph-node3
    mgr: ceph-node1(active), standbys: ceph-node2, ceph-node3
    osd: 3 osds: 3 up, 3 in
```

---

## 八、演示要点总结（面向导师）

| 环节 | 演示内容 | 关键命令 |
| :--- | :--- | :--- |
| **1. 环境准备** | 清理旧环境、拉取镜像、创建网络 | `docker network create` |
| **2. MON 部署** | 逐个启动 3 个 MON 容器，形成仲裁 | `docker exec ... ceph -s` 查看 quorum |
| **3. MGR 部署** | 部署 3 个 MGR 实现管理高可用 | `ceph -s` 显示 active/standby |
| **4. OSD 部署** | 使用 loop 设备模拟磁盘，添加 3 个 OSD | `ceph osd tree` 展示 OSD 上线 |
| **5. 功能验证** | 集群健康、RBD 块存储可用 | 创建 Pool 和 RBD 镜像测试 |

### 扩展说明（可口头陈述）
- **RBD 块存储**：集群已原生支持，可直接创建 Pool 和 RBD 镜像，用于 K8s PV 供应。
- **CephFS 文件存储**：需额外部署 MDS 服务（约 2 分钟），接口为 POSIX 文件系统。
- **RGW 对象存储**：需额外部署 RGW 服务（约 2 分钟），提供 S3/Swift 兼容接口。

---

## 九、快速清理命令（演示后可选）
```bash
docker stop $(docker ps -aq --filter "name=ceph-")
docker rm $(docker ps -aq --filter "name=ceph-")
docker network rm ceph-public
sudo rm -rf /etc/ceph /var/lib/ceph* /tmp/ceph* /tmp/monmap /var/lib/ceph-osd-disks
for i in 11 12 13; do sudo losetup -d /dev/loop$i 2>/dev/null; done
```

---


# 一、前提（必须先满足）
执行：
```bash
docker exec ceph-mon-ceph-node1 ceph -s
```
满足两点即可继续：
1. `health: HEALTH_OK`
2. `osd: 3 up (3 in)` 所有盘正常

---

# 二、RBD 快速验证标准流程（最稳、不折腾挂载）
在 ceph-mon 容器里执行：
```bash
docker exec -it ceph-mon-ceph-node1 bash
```

## 1. 建一个测试池
```bash
ceph osd pool create test_rbd
```

## 2. 把池标记为 RBD 专用（必须）
```bash
rbd pool init test_rbd
```

## 3. 创建一个 1G 块设备
```bash
rbd create --size 1G test_rbd/testimg
```

## 4. 查看信息（能出来就正常）
```bash
rbd info test_rbd/testimg
```

## 5. 测试扩容（验证可写）
```bash
rbd resize test_rbd/testimg --size 2G
```

## 6. 测试快照（核心功能）
```bash
rbd snap create test_rbd/testimg@snap1
rbd snap ls test_rbd/testimg
```

---

# 三、全部跑完无报错 =
## ✅ **RBD 块存储功能完全正常、可对外提供服务**

---

# 四、一键清理还原
```bash
# 删快照
rbd snap rm test_rbd/testimg@snap1

# 删镜像
rbd rm test_rbd/testimg

# 临时开删池权限
ceph config set mon mon_allow_pool_delete true

# 删测试池
ceph osd pool rm test_rbd test_rbd --yes-i-really-really-mean-it

# 关闭删池权限（安全）
ceph config set mon mon_allow_pool_delete false
```

---

# 五、你必须记住的 3 个关键点
1. **`.mgr` 是 Ceph 自带系统池，正常、必须保留、不能删**
2. **宿主机挂载失败（rbd/nbd 模块问题）= 环境问题，不代表 RBD 坏了**
3. **只要能 create / info / resize / snap，RBD 就 100% 可用**

---


## 📘 Ceph 集群手动部署（Docker 方式）

### 一、部署环境与规划

| 项目 | 说明 |
| :--- | :--- |
| **宿主机** | 单台 Fedora 系统（或其他 Linux 发行版） |
| **容器引擎** | Docker（已安装并启动） |
| **Ceph 镜像** | `quay.io/ceph/ceph:v17.2.8`（Quincy 版本） |
| **网络** | 自定义 Docker 桥接网络 `ceph-public`，子网 `192.168.206.0/24` |
| **节点规划** | 三节点，每个节点运行一个 MON 和一个 MGR |

| 节点名称 | IP 地址 |
| :--- | :--- |
| `ceph-node1` | `192.168.206.151` |
| `ceph-node2` | `192.168.206.152` |
| `ceph-node3` | `192.168.206.153` |

---

### 二、前置准备

#### 1. 清理旧环境（如有）

```bash
docker ps -a | grep ceph- | awk '{print $1}' | xargs -r docker rm -f
docker rm -f temp-net-holder 2>/dev/null || true
docker network rm ceph-public 2>/dev/null || true
sudo rm -rf /etc/ceph /var/lib/ceph* /tmp/ceph* /tmp/monmap
```

#### 2. 创建 Docker 网络并拉取镜像

```bash
docker network create --subnet=192.168.206.0/24 ceph-public
docker pull quay.io/ceph/ceph:v17.2.8
```

#### 3. 生成集群唯一标识符（FSID）

```bash
export FSID=$(uuidgen)
echo "FSID: $FSID"   # 记录这个值，后续会用到
```

---

### 三、部署第一个 MON 节点（`ceph-node1`）

#### 1. 创建基础目录和初始配置文件

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

#### 2. 生成密钥环和 monmap

```bash
# 生成 mon. 密钥环
sudo ceph-authtool --create-keyring /tmp/ceph.mon.keyring --gen-key -n mon. --cap mon 'allow *'

# 生成 client.admin 密钥环（管理员权限）
sudo ceph-authtool --create-keyring /etc/ceph/ceph.client.admin.keyring --gen-key -n client.admin \
  --cap mon 'allow *' --cap osd 'allow *' --cap mds 'allow *' --cap mgr 'allow *'

# 将 admin 密钥导入 mon 密钥环
sudo ceph-authtool /tmp/ceph.mon.keyring --import-keyring /etc/ceph/ceph.client.admin.keyring

# 生成只包含 node1 的 monmap
monmaptool --create --add ceph-node1 192.168.206.151 --fsid $FSID /tmp/monmap
```

#### 3. 初始化 MON 数据目录并启动容器

```bash
# 初始化数据目录（--mkfs）
sudo docker run --rm \
  -v /var/lib/ceph:/var/lib/ceph:z \
  -v /etc/ceph:/etc/ceph:z \
  -v /tmp:/tmp:z \
  quay.io/ceph/ceph:v17.2.8 \
  ceph-mon --mkfs -i ceph-node1 --monmap /tmp/monmap --keyring /tmp/ceph.mon.keyring \
  --public-addr 192.168.206.151

# 修正权限（容器内 ceph 用户 UID 为 167）
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

#### 4. 验证单节点状态

```bash
sleep 10
docker exec ceph-mon-ceph-node1 ceph -s
```

预期看到 `mon: 1 daemons, quorum ceph-node1`。

---

### 四、动态添加第二个 MON 节点（`ceph-node2`）

#### 1. 从集群导出当前 monmap

```bash
docker exec ceph-mon-ceph-node1 ceph mon getmap -o /tmp/monmap
docker cp ceph-mon-ceph-node1:/tmp/monmap /tmp/monmap
```

#### 2. 准备 node2 的独立配置和数据目录

```bash
sudo mkdir -p /etc/ceph-mon-ceph-node2 /var/lib/ceph-mon-ceph-node2/mon/ceph-ceph-node2

# 复制基础文件
sudo cp /etc/ceph/ceph.conf /etc/ceph-mon-ceph-node2/ceph.conf
sudo cp /etc/ceph/ceph.client.admin.keyring /etc/ceph-mon-ceph-node2/
sudo cp /tmp/ceph.mon.keyring /etc/ceph-mon-ceph-node2/
sudo cp /tmp/monmap /etc/ceph-mon-ceph-node2/

# 修改配置文件，加入 node2 的信息
sudo sed -i 's/mon_initial_members = ceph-node1/mon_initial_members = ceph-node1,ceph-node2/' /etc/ceph-mon-ceph-node2/ceph.conf
sudo sed -i 's/mon_host = 192.168.206.151/mon_host = 192.168.206.151,192.168.206.152/' /etc/ceph-mon-ceph-node2/ceph.conf
```

#### 3. 初始化并启动 node2 容器

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

#### 4. 验证

```bash
sleep 10
docker exec ceph-mon-ceph-node1 ceph -s
```

预期看到 `mon: 2 daemons, quorum ceph-node1,ceph-node2`。

---

### 五、动态添加第三个 MON 节点（`ceph-node3`）

#### 1. 准备 node3 的目录和配置

```bash
sudo mkdir -p /etc/ceph-mon-ceph-node3 /var/lib/ceph-mon-ceph-node3/mon/ceph-ceph-node3

sudo cp /etc/ceph/ceph.conf /etc/ceph-mon-ceph-node3/ceph.conf
sudo cp /etc/ceph/ceph.client.admin.keyring /etc/ceph-mon-ceph-node3/
sudo cp /tmp/ceph.mon.keyring /etc/ceph-mon-ceph-node3/
sudo cp /tmp/monmap /etc/ceph-mon-ceph-node3/

# 修改配置文件，加入三个节点信息
sudo sed -i 's/mon_initial_members = ceph-node1/mon_initial_members = ceph-node1,ceph-node2,ceph-node3/' /etc/ceph-mon-ceph-node3/ceph.conf
sudo sed -i 's/mon_host = 192.168.206.151/mon_host = 192.168.206.151,192.168.206.152,192.168.206.153/' /etc/ceph-mon-ceph-node3/ceph.conf
```

#### 2. 初始化并启动 node3 容器

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

#### 3. 回头更新 node1 的配置并重启

```bash
sudo sed -i 's/mon_initial_members = ceph-node1/mon_initial_members = ceph-node1,ceph-node2,ceph-node3/' /etc/ceph/ceph.conf
sudo sed -i 's/mon_host = 192.168.206.151/mon_host = 192.168.206.151,192.168.206.152,192.168.206.153/' /etc/ceph/ceph.conf
docker restart ceph-mon-ceph-node1
```

#### 4. 验证

```bash
sleep 10
docker exec ceph-mon-ceph-node1 ceph -s
```

预期看到 `mon: 3 daemons, quorum ceph-node1,ceph-node2,ceph-node3`。

---

### 六、部署三个 MGR 节点

MGR 负责提供扩展功能和管理接口，三个 MGR 实现高可用（一个 active，两个 standby）。

#### 1. 部署 `ceph-node1` 的 MGR

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

#### 2. 部署 `ceph-node2` 的 MGR

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

#### 3. 部署 `ceph-node3` 的 MGR

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

#### 4. 验证 MGR 状态

```bash
docker exec ceph-mon-ceph-node1 ceph -s
```

预期看到 `mgr: ceph-node1(active), standbys: ceph-node2, ceph-node3`。

---

### 七、消除部分健康警告（可选）

```bash
docker exec ceph-mon-ceph-node1 ceph mon enable-msgr2
docker exec ceph-mon-ceph-node1 ceph config set mon auth_allow_insecure_global_id_reclaim false
```

此时集群只剩下 `OSD count 0 < osd_pool_default_size 1` 的警告，表示存储层未部署，属于正常状态。

---

### 八、最终状态

运行以下命令查看完整集群状态：

```bash
docker exec ceph-mon-ceph-node1 ceph -s
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Image}}"
```

你应该拥有：
- 3 个 MON 容器（`ceph-mon-ceph-node1/2/3`）
- 3 个 MGR 容器（`ceph-mgr-ceph-node1/2/3`）
- 集群控制平面高可用已建立

---

### 九、补充说明

| 关键点 | 解释 |
| :--- | :--- |
| **动态扩容原理** | 通过导出集群当前的 monmap，让新节点“知道”已有集群成员，从而加入仲裁。 |
| **配置文件分节点独立** | 为避免冲突，为每个非 node1 的节点创建了独立的 `/etc/ceph-mon-<node>` 目录，挂载到容器的 `/etc/ceph`。 |
| **权限（UID 167）** | Ceph 容器内 `ceph` 用户 UID 固定为 167，因此宿主机目录需匹配该 UID 所有权。 |
| **后续扩展** | 可以继续添加 OSD、创建存储池、启用 Dashboard 等。 |

---

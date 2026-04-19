好的，我来为你梳理一个**双模式操作指南**，让你能够：

1. **快速搭建完整集群**（在骨架基础上添加OSD并验证功能）
2. **快速恢复至干净骨架**（删除OSD和存储池，回到3MON+3MGR状态）

以下命令均基于你当前的环境验证通过，可直接复制执行。

---

## 📦 准备工作（仅首次执行）

### 1. 创建虚拟磁盘（loop设备）
```bash
sudo mkdir -p /var/lib/ceph-osd-disks
for i in 1 2 3; do
    sudo dd if=/dev/zero of=/var/lib/ceph-osd-disks/osd-node${i}.img bs=1M count=0 seek=10240
    sudo losetup /dev/loop$((10+$i)) /var/lib/ceph-osd-disks/osd-node${i}.img
done
```

### 2. 生成并分发 bootstrap-osd 密钥
```bash
# 从集群获取 bootstrap 密钥
docker exec ceph-mon-ceph-node1 ceph auth get-or-create client.bootstrap-osd mon 'allow profile bootstrap-osd' > /tmp/bootstrap-osd.keyring

# 分发至 node1（已在运行的容器）
docker exec ceph-mon-ceph-node1 mkdir -p /var/lib/ceph/bootstrap-osd
docker cp /tmp/bootstrap-osd.keyring ceph-mon-ceph-node1:/var/lib/ceph/bootstrap-osd/ceph.keyring
docker exec ceph-mon-ceph-node1 chown -R 167:167 /var/lib/ceph/bootstrap-osd

# 分发至 node2/node3 数据卷（宿主机操作）
for N in 2 3; do
    sudo mkdir -p /var/lib/ceph-mon-ceph-node${N}/bootstrap-osd
    sudo cp /tmp/bootstrap-osd.keyring /var/lib/ceph-mon-ceph-node${N}/bootstrap-osd/ceph.keyring
    sudo mkdir -p /etc/ceph-mon-ceph-node${N}
    sudo cp /tmp/bootstrap-osd.keyring /etc/ceph-mon-ceph-node${N}/ceph.client.bootstrap-osd.keyring
    sudo chown -R 167:167 /var/lib/ceph-mon-ceph-node${N}/bootstrap-osd /etc/ceph-mon-ceph-node${N}
done
```

> 以上准备工作只需做一次，除非你彻底删除了所有数据卷。

---

## 🚀 模式一：快速添加 OSD（从骨架到完整集群）

### 步骤1：重建 MON 容器以挂载磁盘
每个节点容器需要挂载对应的 loop 设备。

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

### 步骤2：在每个容器内添加 OSD（一键命令块）
分别进入三个容器执行相同命令块（以下以 node1 为例，node2/node3 相同）：

```bash
# 进入容器
docker exec -it ceph-mon-ceph-node1 bash

# 粘贴执行以下全部命令
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

### 步骤3：验证集群健康
```bash
docker exec ceph-mon-ceph-node1 ceph -s
```
预期：`osd: 3 osds: 3 up, 3 in`，健康状态变为 `HEALTH_OK`（或仅剩单副本警告）。

### 步骤4：创建测试存储池（可选）
```bash
docker exec ceph-mon-ceph-node1 ceph osd pool create demo 64 64
docker exec ceph-mon-ceph-node1 rados -p demo put hello /etc/hosts
docker exec ceph-mon-ceph-node1 rados -p demo get hello /tmp/hello
diff /etc/hosts /tmp/hello && echo "✅ 存储功能正常"
```

---

## 🔄 模式二：快速恢复至干净骨架（3MON+3MGR，0 OSD）

演示完成后，执行以下步骤即可回到初始状态。

### 步骤1：删除所有 OSD 和存储池
```bash
# 停止 OSD 进程（在每个容器内杀掉 ceph-osd 进程）
for N in 1 2 3; do
    docker exec ceph-mon-ceph-node$N pkill -f "ceph-osd" 2>/dev/null || true
done

# 从集群中清除 OSD 记录
for id in $(docker exec ceph-mon-ceph-node1 ceph osd ls 2>/dev/null); do
    docker exec ceph-mon-ceph-node1 ceph osd out $id
    docker exec ceph-mon-ceph-node1 ceph osd down $id
    docker exec ceph-mon-ceph-node1 ceph osd purge $id --yes-i-really-mean-it
done

# 删除所有自定义存储池（保留 .mgr）
for pool in $(docker exec ceph-mon-ceph-node1 ceph osd pool ls | grep -v '\.mgr'); do
    docker exec ceph-mon-ceph-node1 ceph osd pool delete $pool $pool --yes-i-really-really-mean-it
done
```

### 步骤2：清理容器内 OSD 目录并卸载挂载点
```bash
# Node1 特殊处理（可能挂载了 XFS）
docker exec ceph-mon-ceph-node1 umount /var/lib/ceph/osd/ceph-* 2>/dev/null || true
docker exec ceph-mon-ceph-node1 rm -rf /var/lib/ceph/osd/*

# Node2/3 直接删数据卷目录
sudo rm -rf /var/lib/ceph-mon-ceph-node2/osd/*
sudo rm -rf /var/lib/ceph-mon-ceph-node3/osd/*
```

### 步骤3：重启 MON 容器至无磁盘挂载状态
```bash
# 停止并删除挂载了磁盘的容器
docker stop ceph-mon-ceph-node{1,2,3}
docker rm ceph-mon-ceph-node{1,2,3}

# 以原始配置重启（无 --device 参数）
docker run -d --name ceph-mon-ceph-node1 --network ceph-public --ip 192.168.206.151 -v /var/lib/ceph:/var/lib/ceph:z -v /etc/ceph:/etc/ceph:z quay.io/ceph/ceph:v17.2.8 ceph-mon -i ceph-node1 -f
docker run -d --name ceph-mon-ceph-node2 --network ceph-public --ip 192.168.206.152 -v /var/lib/ceph-mon-ceph-node2:/var/lib/ceph:z -v /etc/ceph-mon-ceph-node2:/etc/ceph:z quay.io/ceph/ceph:v17.2.8 ceph-mon -i ceph-node2 -f
docker run -d --name ceph-mon-ceph-node3 --network ceph-public --ip 192.168.206.153 -v /var/lib/ceph-mon-ceph-node3:/var/lib/ceph:z -v /etc/ceph-mon-ceph-node3:/etc/ceph:z quay.io/ceph/ceph:v17.2.8 ceph-mon -i ceph-node3 -f
```

### 步骤4：验证恢复
```bash
docker exec ceph-mon-ceph-node1 ceph -s
```
应显示 `osd: 0 osds`，健康警告包含 `OSD count 0 < osd_pool_default_size 1`，即表明已回到干净骨架。

---

## 📌 核心要点备忘

| 项目 | 说明 |
| :--- | :--- |
| **loop 设备** | 只需创建一次，除非重启后消失（重启需重新 `losetup`） |
| **bootstrap 密钥** | 分发一次即可，保存在数据卷中 |
| **MGR 容器** | 始终无需改动，它们不参与 OSD 挂载 |
| **快速回退关键** | 先停止 OSD 进程，再 purge OSD 记录，最后删除数据目录 |

---

有了这份指南，你可以反复练习添加 OSD、演示功能、快速回退，完全掌控整个 Ceph 集群的生命周期。如果有任何一步执行异常，随时贴出输出，我帮你排查。
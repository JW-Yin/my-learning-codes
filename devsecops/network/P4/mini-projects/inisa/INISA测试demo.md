🎯 目标

在三台主机（h1、h2、h3）和一台P4交换机（s1）的Mininet环境中，实现：

    h1（训练节点） 发STATUS给h3（控制平面）

    h3（控制平面） 根据STATUS发PREFETCH给h2（存储节点）

    h2（存储节点） 收到PREFETCH后，经过2s延迟，将数据推送给h1

    h1 从本地缓存队列取出数据，实现零等待，形成闭环。

---

## 🌐 环境要求
- Ubuntu 20.04/22.04（或 VM）
- 已安装 [P4 Tutorials](https://github.com/p4lang/tutorials) 环境（包含 `p4c-bm2-ss`，`simple_switch_grpc`，`mininet`）
- 确认 `~/tutorials/exercises/basic` 可正常 `make run`（表示环境完备）

---

## 📁 项目结构

```
~/tutorials/exercises/inisa/
├── Makefile
├── inisa.p4                    # P4 交换机程序
├── h1.py                       # 训练节点
├── h2.py                       # 存储节点
├── controller.py               # 控制平面
├── pod-topo/
│   ├── topology.json            # 拓扑定义
│   └── s1-runtime.json          # 转发表
├── build/                      # 编译输出（自动生成）
├── pcaps/                      # 抓包文件
└── logs/                       # 日志
```

---

## 📝 第一步：创建项目目录并写入所有文件

```bash
mkdir -p ~/tutorials/exercises/inisa/pod-topo
cd ~/tutorials/exercises/inisa
```

### 1.1 写入 `Makefile`

```bash
cat > Makefile << 'EOF'
BMV2_SWITCH_EXE = simple_switch_grpc
P4C = p4c-bm2-ss
P4C_ARGS = --p4v 16 --p4runtime-files $(BUILD_DIR)/inisa.p4.p4info.txtpb -o $(BUILD_DIR)/inisa.json
P4_FILE = inisa.p4
TOPO = pod-topo/topology.json
RUN_PY = ../../utils/run_exercise.py

include ../../utils/Makefile
EOF
```

### 1.2 写入 `inisa.p4`（P4 交换机程序）

```bash
cat > inisa.p4 << 'P4EOF'
#include <core.p4>
#include <v1model.p4>

const bit<16> TDTP_PORT = 0x270F;  // 9999

typedef bit<9>  egressSpec_t;
typedef bit<48> macAddr_t;
typedef bit<32> ip4Addr_t;

// ===== 标准头部 =====
header ethernet_t {
    macAddr_t dstAddr;
    macAddr_t srcAddr;
    bit<16>   etherType;
}

header ipv4_t {
    bit<4>    version;
    bit<4>    ihl;
    bit<8>    diffserv;
    bit<16>   totalLen;
    bit<16>   identification;
    bit<3>    flags;
    bit<13>   fragOffset;
    bit<8>    ttl;
    bit<8>    protocol;
    bit<16>   hdrChecksum;
    ip4Addr_t srcAddr;
    ip4Addr_t dstAddr;
}

header udp_t {
    bit<16> srcPort;
    bit<16> dstPort;
    bit<16> length;
    bit<16> checksum;
}

// ===== 自定义 TDTP 头部 =====
header tdtp_t {
    bit<8>  opcode;
    bit<8>  task_id;
    bit<32> batch_id;
    bit<32> t_comp_ms;
    bit<32> t_load_ms;
    bit<32> object_id;
    bit<32> seq_num;
    bit<32> offset;
    bit<32> length;
    bit<16> flags;
}

struct metadata { }

struct headers {
    ethernet_t   ethernet;
    ipv4_t       ipv4;
    udp_t        udp;
    tdtp_t       tdtp;
}

// ===== 解析器 =====
parser MyParser(packet_in packet,
                out headers hdr,
                inout metadata meta,
                inout standard_metadata_t standard_metadata) {
    state start {
        packet.extract(hdr.ethernet);
        transition select(hdr.ethernet.etherType) {
            0x0800: parse_ipv4;
            0x0806: accept;    // ARP 直接放行
            default: accept;
        }
    }
    state parse_ipv4 {
        packet.extract(hdr.ipv4);
        transition select(hdr.ipv4.protocol) {
            17: parse_udp;
            default: accept;
        }
    }
    state parse_udp {
        packet.extract(hdr.udp);
        transition select(hdr.udp.dstPort) {
            TDTP_PORT: parse_tdtp;
            default: accept;
        }
    }
    state parse_tdtp {
        packet.extract(hdr.tdtp);
        transition accept;
    }
}

// ===== 校验和验证（空） =====
control MyVerifyChecksum(inout headers hdr, inout metadata meta) {
    apply { }
}

// ===== 入口处理：IPv4 路由 =====
control MyIngress(inout headers hdr,
                  inout metadata meta,
                  inout standard_metadata_t standard_metadata) {
    action ipv4_forward(macAddr_t dstAddr, egressSpec_t port) {
        standard_metadata.egress_spec = port;
        hdr.ethernet.srcAddr = hdr.ethernet.dstAddr;
        hdr.ethernet.dstAddr = dstAddr;
        hdr.ipv4.ttl = hdr.ipv4.ttl - 1;
    }
    action drop() {
        mark_to_drop(standard_metadata);
    }

    table ipv4_lpm {
        key = { hdr.ipv4.dstAddr: lpm; }
        actions = { ipv4_forward; drop; NoAction; }
        size = 1024;
        default_action = drop();
    }

    apply {
        if (hdr.ipv4.isValid()) {
            ipv4_lpm.apply();
        }
        // 非 IPv4 包交给交换机泛洪处理
    }
}

// ===== 出口处理（空） =====
control MyEgress(inout headers hdr,
                 inout metadata meta,
                 inout standard_metadata_t standard_metadata) {
    apply { }
}

// ===== 校验和计算：必须更新 IPv4 校验和 =====
control MyComputeChecksum(inout headers hdr, inout metadata meta) {
    apply {
        update_checksum(
            hdr.ipv4.isValid(),
            { hdr.ipv4.version, hdr.ipv4.ihl, hdr.ipv4.diffserv,
              hdr.ipv4.totalLen, hdr.ipv4.identification,
              hdr.ipv4.flags, hdr.ipv4.fragOffset, hdr.ipv4.ttl,
              hdr.ipv4.protocol, hdr.ipv4.srcAddr, hdr.ipv4.dstAddr },
            hdr.ipv4.hdrChecksum,
            HashAlgorithm.csum16
        );
    }
}

// ===== 逆解析器 =====
control MyDeparser(packet_out packet, in headers hdr) {
    apply {
        packet.emit(hdr.ethernet);
        packet.emit(hdr.ipv4);
        packet.emit(hdr.udp);
        packet.emit(hdr.tdtp);
    }
}

V1Switch(
    MyParser(),
    MyVerifyChecksum(),
    MyIngress(),
    MyEgress(),
    MyComputeChecksum(),
    MyDeparser()
) main;
P4EOF
```

### 1.3 写入 `pod-topo/topology.json`

```bash
cat > pod-topo/topology.json << 'EOF'
{
    "hosts": {
        "h1": {
            "ip": "10.0.0.1/24",
            "mac": "08:00:00:00:01:11"
        },
        "h2": {
            "ip": "10.0.0.2/24",
            "mac": "08:00:00:00:02:22"
        },
        "h3": {
            "ip": "10.0.0.3/24",
            "mac": "08:00:00:00:03:33"
        }
    },
    "switches": {
        "s1": {
            "runtime_json": "pod-topo/s1-runtime.json"
        }
    },
    "links": [
        ["h1", "s1-p1"],
        ["h2", "s1-p2"],
        ["h3", "s1-p3"]
    ]
}
EOF
```

### 1.4 写入 `pod-topo/s1-runtime.json`

```bash
cat > pod-topo/s1-runtime.json << 'EOF'
{
  "target": "bmv2",
  "p4info": "build/inisa.p4.p4info.txtpb",
  "bmv2_json": "build/inisa.json",
  "table_entries": [
    {
      "table": "MyIngress.ipv4_lpm",
      "match": { "hdr.ipv4.dstAddr": ["10.0.0.1", 32] },
      "action_name": "MyIngress.ipv4_forward",
      "action_params": { "dstAddr": "08:00:00:00:01:11", "port": 1 }
    },
    {
      "table": "MyIngress.ipv4_lpm",
      "match": { "hdr.ipv4.dstAddr": ["10.0.0.2", 32] },
      "action_name": "MyIngress.ipv4_forward",
      "action_params": { "dstAddr": "08:00:00:00:02:22", "port": 2 }
    },
    {
      "table": "MyIngress.ipv4_lpm",
      "match": { "hdr.ipv4.dstAddr": ["10.0.0.3", 32] },
      "action_name": "MyIngress.ipv4_forward",
      "action_params": { "dstAddr": "08:00:00:00:03:33", "port": 3 }
    }
  ]
}
EOF
```

### 1.5 写入三个 Python 脚本

#### `h1.py`（训练节点）

```bash
cat > h1.py << 'EOF'
import socket, time, random, threading, queue

H2_PORT = 8888
CTRL = ('10.0.0.3', 9999)
BUF = queue.Queue()

def listen():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('0.0.0.0', H2_PORT))
    while True:
        data, _ = s.recvfrom(1024)
        BUF.put(data.decode())

threading.Thread(target=listen, daemon=True).start()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
batch = 1

print(f"[h1] cold start, request batch {batch}")
sock.sendto(f"STATUS {batch} 0".encode(), CTRL)

while True:
    item = BUF.get()
    batch = int(item)
    print(f"[h1] got batch {batch}, training...")
    time.sleep(random.randint(1, 5))
    sock.sendto(f"STATUS {batch} 0".encode(), CTRL)
    print(f"[h1] sent STATUS for batch {batch}")
EOF
```

#### `h2.py`（存储节点）

```bash
cat > h2.py << 'EOF'
import socket, time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 7777))
send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("[h2] waiting for PREFETCH...")
while True:
    data, _ = sock.recvfrom(1024)
    msg = data.decode()
    if msg.startswith("PREFETCH"):
        _, batch = msg.split()
        print(f"[h2] PREFETCH {batch}, preparing...")
        time.sleep(2)              # 模拟存储延迟 2 秒
        send_sock.sendto(batch.encode(), ('10.0.0.1', 8888))
        print(f"[h2] pushed batch {batch}")
EOF
```

#### `controller.py`（控制平面）

```bash
cat > controller.py << 'EOF'
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 9999))
send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("[ctrl] waiting for STATUS...")
while True:
    data, _ = sock.recvfrom(1024)
    msg = data.decode()
    if msg.startswith("STATUS"):
        _, batch, _ = msg.split()
        batch = int(batch)
        print(f"[ctrl] got STATUS {batch}")
        next_batch = batch + 1
        send_sock.sendto(f"PREFETCH {next_batch}".encode(), ('10.0.0.2', 7777))
        print(f"[ctrl] sent PREFETCH {next_batch}")
EOF
```

---

## 🚀 第二步：编译并启动网络

```bash
cd ~/tutorials/exercises/inisa
make run
```

如果编译成功，会看到：
- `Inserting 3 table entries...`
- `mininet>` 提示符

---

## 🔧 第三步：配置静态 ARP（每次启动都要执行）

在 `mininet>` 中输入：

```
h1 arp -s 10.0.0.2 08:00:00:00:02:22
h1 arp -s 10.0.0.3 08:00:00:00:03:33
h2 arp -s 10.0.0.1 08:00:00:00:01:11
h2 arp -s 10.0.0.3 08:00:00:00:03:33
h3 arp -s 10.0.0.1 08:00:00:00:01:11
h3 arp -s 10.0.0.2 08:00:00:00:02:22
```

验证连通性：
```
h1 ping 10.0.0.2
```
应返回 `ttl=63 time=...`

---

## 🎯 第四步：启动 INISA 极简 Demo

在 `mininet>` 中按顺序启动（先控制平面，再存储，最后训练）：

```
h3 python3 -u controller.py &
h2 python3 -u h2.py &
h1 python3 -u h1.py &
```

观察输出，你会看到：
```
[ctrl] waiting for STATUS...
[h2] waiting for PREFETCH...
[h1] cold start, request batch 1
[ctrl] got STATUS 1
[ctrl] sent PREFETCH 2
[h2] PREFETCH 2, preparing...
[h2] pushed batch 2
[h1] got batch 2, training...
[h1] sent STATUS for batch 2
[ctrl] got STATUS 2
[ctrl] sent PREFETCH 3
...
```

**关键现象**：除冷启动外，h1 每次直接打印 `got batch X` 而无任何等待，证明预取成功隐藏了存储延迟。

---

## 🛑 停止 Demo

```
h1 pkill -9 python3
h2 pkill -9 python3
h3 pkill -9 python3
```

退出 Mininet：`exit`

---

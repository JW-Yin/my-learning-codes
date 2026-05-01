🎯 目标

在三台主机（h1、h2、h3）和一台P4交换机（s1）的Mininet环境中，实现：

    h1（训练节点） 发STATUS给h3（控制平面）

    h3（控制平面） 根据STATUS发PREFETCH给h2（存储节点）

    h2（存储节点） 收到PREFETCH后，经过2s延迟，将数据推送给h1

    h1 从本地缓存队列取出数据，实现零等待，形成闭环。

📁 项目目录结构
text

~/tutorials/exercises/inisa/
├── inisa.p4
├── Makefile
├── pod-topo/
│   ├── topology.json
│   └── s1-runtime.json
├── h1.py
├── h2.py
├── controller.py
├── build/
├── pcaps/
└── logs/

🚀 完整搭建步骤（复制粘贴即可）
1. 进入教程目录并创建项目文件夹
bash

cd ~/tutorials/exercises
mkdir inisa
cd inisa
mkdir -p build pcaps logs pod-topo
cp ../basic/Makefile .

2. 编写 P4 程序 inisa.p4
bash

cat > inisa.p4 << 'EOF'
#include <core.p4>
#include <v1model.p4>

const bit<16> TDTP_PORT = 0x270F;

typedef bit<9>  egressSpec_t;
typedef bit<48> macAddr_t;
typedef bit<32> ip4Addr_t;

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

parser MyParser(packet_in packet,
                out headers hdr,
                inout metadata meta,
                inout standard_metadata_t standard_metadata) {
    state start {
        packet.extract(hdr.ethernet);
        transition select(hdr.ethernet.etherType) {
            0x0800: parse_ipv4;
            0x0806: accept;
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

control MyVerifyChecksum(inout headers hdr, inout metadata meta) {
    apply { }
}

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
    }
}

control MyEgress(inout headers hdr,
                 inout metadata meta,
                 inout standard_metadata_t standard_metadata) {
    apply { }
}

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
EOF

3. 编写拓扑文件 pod-topo/topology.json
bash

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

4. 编写运行时配置 pod-topo/s1-runtime.json
bash

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

5. 修改 Makefile
bash

cat > Makefile << 'EOF'
BMV2_SWITCH_EXE = simple_switch_grpc
P4C = p4c-bm2-ss
P4C_ARGS = --p4v 16 --p4runtime-files $(BUILD_DIR)/inisa.p4.p4info.txtpb -o $(BUILD_DIR)/inisa.json
P4_FILE = inisa.p4
TOPO = pod-topo/topology.json
RUN_PY = ../../utils/run_exercise.py

include ../../utils/Makefile
EOF

6. 编写主机脚本
h1.py (训练节点)
bash

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

h2.py (存储节点)
bash

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
        time.sleep(2)
        send_sock.sendto(batch.encode(), ('10.0.0.1', 8888))
        print(f"[h2] pushed batch {batch}")
EOF

controller.py (控制平面)
bash

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

🏃 启动与运行
1. 编译并启动Mininet
bash

cd ~/tutorials/exercises/inisa
make run

看到 mininet> 提示符后，配置静态ARP（必须）：
text

h1 arp -s 10.0.0.2 08:00:00:00:02:22
h1 arp -s 10.0.0.3 08:00:00:00:03:33
h2 arp -s 10.0.0.1 08:00:00:00:01:11
h2 arp -s 10.0.0.3 08:00:00:00:03:33
h3 arp -s 10.0.0.1 08:00:00:00:01:11
h3 arp -s 10.0.0.2 08:00:00:00:02:22

测试网络：
text

h1 ping 10.0.0.2

应该通。
2. 启动INISA脚本

在 mininet> 中依次执行（先控制平面，再存储，后训练）：
text

h3 python3 -u controller.py > /tmp/ctrl.log 2>&1 &
h2 python3 -u h2.py > /tmp/h2.log 2>&1 &
h1 python3 -u h1.py > /tmp/h1.log 2>&1 &

3. 查看运行日志

等待几秒后，查看输出：
text

h3 cat /tmp/ctrl.log
h2 cat /tmp/h2.log
h1 cat /tmp/h1.log

（也可以用 tail -f 实时观察）
📖 预期输出

    controller.log：[ctrl] got STATUS 1 → [ctrl] sent PREFETCH 2 → got STATUS 2 → PREFETCH 3… 连续不断。

    h2.log：[h2] PREFETCH 2, preparing... → 2秒后 [h2] pushed batch 2 → PREFETCH 3…

    h1.log：[h1] cold start... → [h1] got batch 2, training... → sent STATUS for batch 2 → got batch 3… 始终无阻塞。

🔧 停止和清理
bash

h1 pkill -9 python3
h2 pkill -9 python3
h3 pkill -9 python3
exit  # 退出mininet
make clean

这就完成了！ 整个Demo仅需复制粘贴上述命令，即可在任何P4教程VM上零基础复现INISA的推送预取逻辑。
#!/bin/bash
set -euo pipefail

# ============================================
# Ceph 集群一键部署脚本 (Docker 方式)
# 支持任意数量 MON 和 MGR 节点
# ============================================

# ---------- 可配置参数 ----------
CEPH_IMAGE="quay.io/ceph/ceph:v17.2.8"
NETWORK_NAME="ceph-public"
SUBNET="192.168.206.0/24"

# 定义 MON 节点列表，格式："名称:IP地址"
MON_NODES=(
    "ceph-node1:192.168.206.151"
    "ceph-node2:192.168.206.152"
    "ceph-node3:192.168.206.153"
)

# ---------- 颜色输出 ----------
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

info()  { echo -e "${GREEN}[INFO]${NC} $1"; }
warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

# ---------- 辅助函数 ----------
get_node_count() { echo ${#MON_NODES[@]}; }
get_node_name()  { echo "${MON_NODES[$1]}" | cut -d: -f1; }
get_node_ip()    { echo "${MON_NODES[$1]}" | cut -d: -f2; }

get_conf_dir() {
    local idx=$1
    local name=$(get_node_name $idx)
    if [ $idx -eq 0 ]; then echo "/etc/ceph"; else echo "/etc/ceph-mon-$name"; fi
}

get_data_dir() {
    local idx=$1
    local name=$(get_node_name $idx)
    if [ $idx -eq 0 ]; then echo "/var/lib/ceph"; else echo "/var/lib/ceph-mon-$name"; fi
}

# ---------- 依赖检查 ----------
check_deps() {
    info "检查依赖..."
    command -v docker >/dev/null 2>&1 || error "Docker 未安装"
    command -v uuidgen >/dev/null 2>&1 || error "uuidgen 未安装"
    if ! command -v ceph-authtool >/dev/null 2>&1; then
        warn "安装 ceph-base 和 ceph-common..."
        dnf install -y ceph-base ceph-common || error "安装失败"
    fi
}

# ---------- 清理 ----------
cleanup() {
    info "清理旧容器、网络和数据..."
    docker ps -a --filter "name=ceph-" --format '{{.Names}}' | xargs -r docker rm -f || true
    docker network rm "$NETWORK_NAME" 2>/dev/null || true
    rm -rf /etc/ceph /var/lib/ceph* /tmp/ceph* /tmp/monmap 2>/dev/null || true
}

# ---------- 准备 ----------
prepare() {
    info "创建网络 $NETWORK_NAME ($SUBNET)"
    docker network create --subnet="$SUBNET" "$NETWORK_NAME" || error "网络创建失败"
    info "拉取镜像 $CEPH_IMAGE"
    docker pull "$CEPH_IMAGE" || error "拉取失败"
}

export FSID=$(uuidgen)
info "FSID: $FSID"

# ---------- 生成引导文件 ----------
generate_bootstrap_files() {
    local first_name=$(get_node_name 0)
    local first_ip=$(get_node_ip 0)
    local conf_dir=$(get_conf_dir 0)
    local data_dir=$(get_data_dir 0)

    mkdir -p "$conf_dir" "$data_dir/mon/ceph-$first_name"

    cat > "$conf_dir/ceph.conf" <<EOF
[global]
fsid = $FSID
mon_initial_members = $first_name
mon_host = $first_ip
public_network = $SUBNET
auth_cluster_required = cephx
auth_service_required = cephx
auth_client_required = cephx
osd_pool_default_size = 1
osd_pool_default_min_size = 1
EOF

    ceph-authtool --create-keyring /tmp/ceph.mon.keyring --gen-key -n mon. --cap mon 'allow *'
    ceph-authtool --create-keyring "$conf_dir/ceph.client.admin.keyring" --gen-key -n client.admin \
        --cap mon 'allow *' --cap osd 'allow *' --cap mds 'allow *' --cap mgr 'allow *'
    ceph-authtool /tmp/ceph.mon.keyring --import-keyring "$conf_dir/ceph.client.admin.keyring"
    monmaptool --create --add "$first_name" "$first_ip" --fsid "$FSID" /tmp/monmap
}

# ---------- 更新所有 MON 配置 ----------
update_all_mon_configs() {
    local deployed_count=$1
    local member_list=""
    local host_list=""
    local i

    for ((i=0; i<deployed_count; i++)); do
        local name=$(get_node_name $i)
        local ip=$(get_node_ip $i)
        if [ $i -eq 0 ]; then
            member_list="$name"
            host_list="$ip"
        else
            member_list="$member_list,$name"
            host_list="$host_list,$ip"
        fi
    done

    local new_conf="[global]
fsid = $FSID
mon_initial_members = $member_list
mon_host = $host_list
public_network = $SUBNET
auth_cluster_required = cephx
auth_service_required = cephx
auth_client_required = cephx
osd_pool_default_size = 1
osd_pool_default_min_size = 1
"

    info "同步配置到所有 MON 节点 (成员: $member_list)"
    for ((i=0; i<deployed_count; i++)); do
        local conf_dir=$(get_conf_dir $i)
        echo "$new_conf" > "$conf_dir/ceph.conf"
        info "  -> $conf_dir/ceph.conf"
    done
}

# ---------- 添加单个 MON ----------
add_mon_node() {
    local idx=$1
    local name=$(get_node_name $idx)
    local ip=$(get_node_ip $idx)
    local conf_dir=$(get_conf_dir $idx)
    local data_dir=$(get_data_dir $idx)

    info ">>> 添加 MON 节点 $name ($ip) [索引 $idx]"

    if [ $idx -eq 0 ]; then
        info "使用引导阶段生成的 monmap"
    else
        local first_name=$(get_node_name 0)
        docker exec "ceph-mon-$first_name" ceph mon getmap -o /tmp/monmap
        docker cp "ceph-mon-$first_name":/tmp/monmap /tmp/monmap
    fi

    mkdir -p "$conf_dir" "$data_dir/mon/ceph-$name"

    if [ $idx -ne 0 ]; then
        cp /etc/ceph/ceph.client.admin.keyring "$conf_dir/"
        cp /tmp/ceph.mon.keyring "$conf_dir/"
        cp /tmp/monmap "$conf_dir/"
    fi

    update_all_mon_configs $((idx + 1))

    docker run --rm \
        -v "$data_dir:/var/lib/ceph:z" \
        -v "$conf_dir:/etc/ceph:z" \
        -v /tmp:/tmp:z \
        "$CEPH_IMAGE" \
        ceph-mon --mkfs -i "$name" --monmap /tmp/monmap --keyring /tmp/ceph.mon.keyring \
        --public-addr "$ip"

    chown -R 167:167 "$data_dir" "$conf_dir"

    docker run -d \
        --name "ceph-mon-$name" \
        --network "$NETWORK_NAME" \
        --ip "$ip" \
        -v "$data_dir:/var/lib/ceph:z" \
        -v "$conf_dir:/etc/ceph:z" \
        -e MON_IP="$ip" \
        "$CEPH_IMAGE" \
        ceph-mon -i "$name" -f

    sleep 10

    local quorum=$(docker exec "ceph-mon-$(get_node_name 0)" ceph -s 2>/dev/null | grep "mon:" || echo "等待集群稳定...")
    info "$quorum"
}

# ---------- 部署所有 MON ----------
deploy_all_mons() {
    local node_count=$(get_node_count)
    local i
    info "计划部署 $node_count 个 MON 节点"
    generate_bootstrap_files

    for ((i=0; i<node_count; i++)); do
        add_mon_node $i
    done

    # info "重启所有 MON 容器以应用最新配置(可选)"
    # for ((i=0; i<node_count; i++)); do
    #     local container_name="ceph-mon-$(get_node_name $i)"
    #     if docker ps -a --format '{{.Names}}' | grep -q "^$container_name$"; then
    #         docker restart "$container_name" >/dev/null
    #     else
    #         warn "容器 $container_name 不存在，跳过重启"
    #     fi
    # done
    # sleep 20

    info "最终 MON 集群状态:"
    docker exec "ceph-mon-$(get_node_name 0)" ceph -s | grep "mon:"
}

# ---------- 部署单个 MGR ----------
deploy_mgr() {
    local idx=$1
    local name=$(get_node_name $idx)
    local conf_dir=$(get_conf_dir $idx)
    local data_dir=$(get_data_dir $idx)

    info "部署 MGR: $name"

    local first_name=$(get_node_name 0)
    docker exec "ceph-mon-$first_name" ceph auth get-or-create mgr.$name \
        mon 'allow profile mgr' osd 'allow *' mds 'allow *' \
        -o "/etc/ceph/ceph.mgr.$name.keyring"

    if [ $idx -ne 0 ]; then
        cp "/etc/ceph/ceph.mgr.$name.keyring" "$conf_dir/"
    fi

    mkdir -p "$data_dir/mgr/ceph-$name"
    cp "$conf_dir/ceph.mgr.$name.keyring" "$data_dir/mgr/ceph-$name/keyring"
    chown -R 167:167 "$data_dir/mgr"

    docker run -d \
        --name "ceph-mgr-$name" \
        --network "$NETWORK_NAME" \
        -v "$conf_dir:/etc/ceph:z" \
        -v "$data_dir/mgr:/var/lib/ceph/mgr:z" \
        "$CEPH_IMAGE" \
        ceph-mgr -i "$name" -f
}

# ---------- 部署所有 MGR ----------
deploy_all_mgrs() {
    local node_count=$(get_node_count)
    local i
    info "部署 $node_count 个 MGR 节点"
    for ((i=0; i<node_count; i++)); do
        deploy_mgr $i
    done
    sleep 15
    docker exec "ceph-mon-$(get_node_name 0)" ceph -s | grep "mgr:"
}

# ---------- 健康优化 ----------
post_config() {
    info "执行健康优化配置"
    local first_name=$(get_node_name 0)
    docker exec "ceph-mon-$first_name" ceph mon enable-msgr2 || true
    docker exec "ceph-mon-$first_name" ceph config set mon auth_allow_insecure_global_id_reclaim false || true
}

# ---------- 展示最终状态 ----------
show_status() {
    echo "========================================="
    info "Ceph 集群部署完成！"
    echo "========================================="
    docker exec "ceph-mon-$(get_node_name 0)" ceph -s
    echo ""
    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Image}}"
}

# ---------- 主流程 ----------
main() {
    if [ "$EUID" -ne 0 ]; then error "请使用 root 或 sudo 执行"; fi

    check_deps
    cleanup
    prepare
    deploy_all_mons
    deploy_all_mgrs
    post_config
    show_status
}

main "$@"
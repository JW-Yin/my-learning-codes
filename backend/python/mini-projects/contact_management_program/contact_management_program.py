import os
import json

pwd = os.path.dirname(os.path.abspath(__file__))
file_path = pwd + '/contacts.json'

def load_contacts():
    """加载联系人列表"""
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
    
def save_contacts(contacts):
    """保存联系人列表"""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(contacts, f, ensure_ascii=False, indent=2)

def add_contact(name, phone):
    """添加联系人"""
    contacts = load_contacts()
    contacts.append({"姓名": name, "电话": phone})
    save_contacts(contacts)
    print(f"已添加联系人：{name}，电话：{phone}")

def view_contacts():
    """查看所有联系人"""
    contacts = load_contacts()
    if not contacts:
        print("联系人列表为空。")
        return
    print("联系人列表：")
    for idx, contact in enumerate(contacts, st2art=1):
        print(f"{idx}. 姓名：{contact['姓名']}，电话：{contact['电话']}")

def delete_contact(index):
    """删除联系人"""
    contacts = load_contacts()
    if 0 <= index < len(contacts):
        removed = contacts.pop(index)
        save_contacts(contacts)
        print(f"已删除联系人：{removed['姓名']}，电话：{removed['电话']}")
    else:
        print("无效的联系人索引。")

def modify_contact(index, new_name, new_phone):
    """修改联系人"""
    contacts = load_contacts()
    if 0 <= index < len(contacts):
        if new_name:
            contacts[index]['姓名'] = new_name
        if new_phone:
            contacts[index]['电话'] = new_phone
        save_contacts(contacts)
        print(f"已修改联系人：{contacts[index]['姓名']}，电话：{contacts[index]['电话']}")
    else:
        print("无效的联系人索引。")

def find_contact(name):
    """查找联系人电话"""
    contacts = load_contacts()
    for contact in contacts:
        if name.upper() in contact['姓名'].upper():
            print(f"找到联系人：{contact['姓名']}，电话：{contact['电话']}")
            return
    print(f"未找到相关联系人：{name}")


def main():
    while True:
        print("\n联系人管理程序")
        print("1. 添加联系人")
        print("2. 查找联系人")
        print("3. 查看所有联系人")
        print("4. 修改联系人")
        print("5. 删除联系人")
        print("其他任意键退出")
        choice = input("请选择操作：")
        
        if choice == '1':
            name = input("请输入姓名：")
            phone = input("请输入电话：")
            add_contact(name, phone)
        elif choice == '3':
            view_contacts()
        elif choice == '5':
            view_contacts()
            index = int(input("请输入要删除的联系人索引（从1开始）：")) - 1
            delete_contact(index)
        elif choice == '4':
            view_contacts()
            index = int(input("请输入要修改的联系人索引（从1开始）：")) - 1
            new_name = input("请输入新的姓名(无需修改直接回车)：")
            new_phone = input("请输入新的电话(无需修改直接回车)：")
            modify_contact(index, new_name, new_phone)
        elif choice == '2':
            name = input("请输入要查找的姓名：")
            find_contact(name)
        else:
            print("已退出程序。")
            break

if __name__ == "__main__":
    main()
安装 Git
	sudo apt update && sudo apt install git

安装 VS Code
	wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
	sudo install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/trusted.gpg.d/packages.microsoft.gpg
	echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/trusted.gpg.d/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" | sudo tee /etc/apt/sources.list.d/vscode.list > /dev/null
	sudo apt update && sudo apt install code

配置 Git 与 Gitee 交互
	git config --global user.name "你的Gitee用户名"
	git config --global user.email "你的Gitee绑定邮箱"
	ssh-keygen -t ed25519 -C "你的Gitee绑定邮箱"
	cat ~/.ssh/id_ed25519.pub
	chmod 600 ~/.ssh/id_ed25519
	chmod 644 ~/.ssh/id_ed25519.pub
	建立本地仓库
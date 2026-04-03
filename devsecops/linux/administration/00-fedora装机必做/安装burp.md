# 从官网下载burp.jar软件本体、JDK21、BurpLoaderKeygen.jar

- 软件本体：`https://portswigger.net/burp/releases/professional-community-2026-2-4`
- JDK21：`https://www.oracle.com/java/technologies/javase/jdk21-archive-downloads.html`
- 寻找并下载BurpLoaderKeygen.jar
- 装好JDK21
- 将BurpLoaderKeygen.jar与软件本体放在同级目录下

# 启动BurpLoaderKeygen.jar激活burp.jar软件本体


# 将启动命令加入/usr/local/bin

将下面脚本写入`sudo nano /usr/local/bin/burp`，并赋予权限`sudo chmod +x /usr/local/bin/burp`，直接在终端输入`burp`，就能自动启动 BurpSuite！

```bash
#!/bin/bash
/usr/lib/jvm/jdk-21.0.9-oracle-x64/bin/java \
--add-opens=java.desktop/javax.swing=ALL-UNNAMED \
--add-opens=java.base/java.lang=ALL-UNNAMED \
--add-opens=java.base/jdk.internal.org.objectweb.asm=ALL-UNNAMED \
--add-opens=java.base/jdk.internal.org.objectweb.asm.tree=ALL-UNNAMED \
--add-opens=java.base/jdk.internal.org.objectweb.asm.Opcodes=ALL-UNNAMED \
-javaagent:/home/jw-yin/burpsuit/BurpLoaderKeygen.jar \
-noverify \
-jar /home/jw-yin/burpsuit/burpsuite_pro_v2026.2.4.jar
```
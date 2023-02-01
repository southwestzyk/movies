# 简介
抓取互联网上目前电影热映排行榜(只取前十名)
数据源地址：猫眼电影[https://m.maoyan.com/asgard/board/1]
# 安装
将movies文件夹放入HA的/custom_components/目录
# 配置
在config/configutration.yaml文件下写入：
```
sensor: 
  - platform: movies
    name: hotmovie
```
即可在开发者工具部分查找到该实体，可集成到前端
# 更新
前端页面已集成到frontend-UI.md中，可以新建markdown卡片复制粘贴即可。
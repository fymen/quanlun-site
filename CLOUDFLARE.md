# Cloudflare Pages · GitHub 自动部署

- GitHub：https://github.com/fymen/quanlun-site
- Cloudflare 项目：`quanlun-site`
- 生产分支：`main`
- 网站入口：https://quanlun-site.pages.dev/

## 发布流程

提交网站修改并推送 `main` 后，Cloudflare 从 GitHub 拉取对应提交，执行 Hugo 构建并发布。其他分支自动生成预览。初次发布及后续发布均应以 Cloudflare 构建结果为准。

## 已配置的构建参数

- 构建命令：`bash scripts/build.sh`
- 输出目录：`public`
- 根目录：仓库根目录
- `HUGO_VERSION=0.162.1`
- `HUGO_ENV=production`（预览环境为 `preview`）
- `TZ=Asia/Shanghai`

构建脚本使用 Cloudflare 的 `CF_PAGES_URL` 设置当前部署网址；`hugo.toml` 中的正式域名保留。非 `main` 分支设置预览环境并通过 robots 禁止抓取。`static/_headers` 提供响应头配置，`wrangler.jsonc` 声明 Pages 静态输出。

## 原测试站

`buzhengjingquanlun-test` 项目采用直接上传，入口 https://buzhengjingquanlun-test.pages.dev/ ，目前保留。它不能原地切换为 Git 集成，因此另建了当前的 `quanlun-site` 项目。

## 正式域名

正式域名暂未绑定到新项目。绑定完成后，应按正式域名调整生产构建网址，并检查 canonical、分享图片及站点地图。

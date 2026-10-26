# Cloudflare Pages 测试部署

当前项目适合静态部署，不需要 Pages Functions。

## 本地直接上传

```sh
hugo --minify --baseURL https://YOUR-PROJECT.pages.dev/
npx wrangler@4 login --scopes account:read user:read pages:write
npx wrangler@4 pages project create YOUR-PROJECT --production-branch main --force
npx wrangler@4 pages deploy public --project-name YOUR-PROJECT --branch main --commit-dirty=true
```

仅上传构建目录 `public/`；不要上传仓库或 `themes/`。站点仍未配备支付与完整版下载。测试时不修改 `hugo.toml` 中作者已配置的正式域名。

## 后续 Git 自动部署

Cloudflare Pages 控制台导入 Git 仓库，构建命令设置 `bash scripts/build.sh`，输出目录 `public`；环境变量设置 `HUGO_VERSION=0.162.1`、`HUGO_ENV=production`、`TZ=Asia/Shanghai`。脚本读取平台 `CF_PAGES_URL`；非 main 分支自动设置预览抓取策略。若生产分支改名，应同步脚本中的分支判定。

Cloudflare 的直接上传项目不能就地切换成 Git 集成项目。测试使用单独项目，正式自动部署可以另建项目，域名绑定后应重新核对 canonical 与分享图片地址。

`static/_headers` 提供 Cloudflare Pages 的响应头，Netlify 配置继续保留。切换托管不会改变书稿源文件。

## 当前测试项目

项目名称：`buzhengjingquanlun-test`。测试入口：https://buzhengjingquanlun-test.pages.dev/ 。实际部署结果以 Cloudflare 返回及访问验证为准。

新版 Wrangler 创建项目时可能自动转到 Workers，因此创建直接上传项目使用 `--force`；已有 Pages 项目正常上传无需该参数。`wrangler.jsonc` 已明确配置为 Pages 静态输出，避免误用 `npx hugo` 自动构建。

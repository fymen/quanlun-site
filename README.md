# 不正经拳论 · 书籍网站

基于 Hugo 与 PaperMod 的独立网站。包含定制书籍宣传首页、三篇精选试读、全书导读、作者介绍、站内搜索与 Netlify 配置。Cloudflare Pages 已连接 GitHub：`fymen/quanlun-site`，生产分支 `main`，入口 https://quanlun-site.pages.dev/ 。源码托管于 https://github.com/fymen/quanlun-site ，未部署到 Netlify。

## 本地使用

要求 Hugo **0.162.1**（本地已验证版本；PaperMod 上游要求至少 0.158.0）。主题已随仓库保存，无需 npm，也无需再下载主题。

```sh
hugo server --bind 127.0.0.1
```

浏览器访问终端显示的地址，通常为 http://localhost:1313/ 。

构建：

```sh
bash scripts/build.sh
# 按实际生产域名构建：
bash scripts/build.sh --baseURL https://your-domain.example/
```

生成目录 `public/` 不纳入 Git。默认 `baseURL` 为本地地址；部署时必须传入真实网址，Netlify 构建脚本会自动处理。

## 目录与编辑位置

- `layouts/home.html`：Hugo 当前版本使用的定制宣传首页。
- `assets/css/extended/book.css`：站点与手机排版样式。
- `hugo.toml`：标题、描述、导航、主题设置。
- `content/read/`：精选试读，优先由书稿同步，直接修改会被覆盖。
- `content/book.md`：全书导读、版本及获取说明。
- `content/about.md`：作者介绍。只使用书稿已有信息，没有编造师承、年限和推荐语。
- `content/articles/`：后续研习札记，当前没有预置假文章。
- `static/images/`：网站使用的封面、Logo 和试读插图。
- `themes/PaperMod/`：固定版本的上游主题，出处见 `THEME.md`。

网页只发布明确选定的三篇试读，不携带全书 PDF、EPUB 或视频工程。网站完整构建不依赖书稿仓库；只有重新同步试读时才需要书稿和 Pandoc。

## 从 Org 书稿同步

要求 Python 3 与 Pandoc。默认书稿位于同级 `../martial_art/`，也可明确指定：

```sh
python3 scripts/sync-samples.py --book-root ../martial_art
bash scripts/build.sh
```

Pandoc 不在 PATH 时，使用 `PANDOC=/path/to/pandoc python3 scripts/sync-samples.py`。同步脚本只处理明确列出的三篇：空空静静、中和之道、自动平衡；保留正文与脚注，移除印刷专用指令并复制用到的图片。每次同步后应检查脚注、图片及正文是否与书稿一致。

首页引用与导读为编辑文案，不会自动覆盖；书稿有重大变更时应人工复核这些文案。封面取自建立网站时本书 PDF 的第一页；书封变更后需单独更新。

## 在 Netlify 发布

1. 将本网站仓库推送到你自己的 Git 远程仓库。
2. 在 Netlify 导入该仓库。构建命令 `bash scripts/build.sh`，发布目录 `public`，仓库自带 `netlify.toml`。
3. 生产构建使用 Netlify 的 `URL`，预览构建使用 `DEPLOY_PRIME_URL`。绑定自定义域名后重新构建，检查 canonical、站点地图与分享图片地址。
4. 部署预览和分支预览会在 robots 中禁止抓取；这不是访问权限控制。
5. 实际测试微信内访问、手机布局、图片和试读速度，检查 Netlify 账号配额。

销售入口、联系方式和视频目录尚未配置。确认真实信息后再添加；不要把付费完整版放进 `static/` 或公开仓库。

## 内容和许可

PaperMod 依 MIT 许可使用，许可证保留于 `themes/PaperMod/LICENSE`。书稿、Logo、封面与插图不因主题的 MIT 授权而自动转为 MIT，仍按各自权利归属处理。

## Cloudflare Pages

Git 自动部署入口：https://quanlun-site.pages.dev/ 。配置与更新方法见 `CLOUDFLARE.md`。原直接上传测试站 https://buzhengjingquanlun-test.pages.dev/ 保留，`deployment-cloudflare.json` 是该旧测试站的检查记录。正式域名配置保留，目前尚未绑定。

## 源码仓库

https://github.com/fymen/quanlun-site ，主分支为 `main`。Cloudflare Pages 的 `quanlun-site` 项目已连接此仓库；推送 `main` 将自动构建并部署，其他分支生成预览。

# 口播剪辑工作台 · talking-edit

可安装的 Agent Skill。把真人口播视频交给 Agent，在随包本地页面选择步骤 Skill、校正字幕、确认剪切和动态包装，最后导出视频与可恢复项目。无需独立桌面程序，也无需用户启动前端开发环境。

首版源码试用：Windows、Python 3.11+、FFmpeg/ffprobe；本地 ASR 建议用 Python 3.12 创建隔离环境。动态包装需 Node.js/npm、对应 FredTalk 组件源码及 Remotion 依赖。所有运行数据、依赖、模型和 Key 均保存到包外。

安装时把 [Skill 安装地址](https://github.com/zhangyanhua0913/talking-edit/tree/main/skills/talking-edit) 交给 Agent，安装整个目录，然后说：

> 使用 talking-edit 剪辑我的口播视频，先打开页面导入素材，已有字幕先复用，不调用付费接口。

首次 Agent 执行 `python SKILL_DIR/scripts/cli.py doctor`，按提示配置媒体程序，创建项目并启动 review。静态页面随包提供，无前端 dev server。默认不上传录音；本地 Whisper 首次需下载 small 模型。FredTalk 为可选依赖，固定版本放包外；不是把作者私人环境和会员素材打进包。

支持：视频＋SRT导入、流程适配器选择、逐句字幕、候选剪切、原段/接缝试听、恢复/撤销/重做、同步剪切、速度调整、FredTalk Agent 制作简报与组件检索、真实关键帧/包装视频采纳、本地导出、版本冲突和恢复。v0.1.2 增加固定底部确认栏、按阶段显示确认按钮、可配置包装位置与淡入淡出、多段一次合成、版本化配乐与人声侧链避让；页面标明当前／历史输出及有无动画、配乐。新增 Skill 先由 Agent 审阅适配，再出现在对应步骤。

当前千问3.1转写按 Token 计费，无法证明费用上界，**新提交关闭**；配置 Key 不代表可以付费。不会套旧每秒价或自动换其他模型。云端真实付费、真人接缝听感及全部 FredTalk 组件的兼容性分别验收，不将免费合成样例当作通过。

开发验证：`python -m unittest discover -s tests -v`；`python tests/verify_local.py --workdir ABS_OUTSIDE_REPO --open-review` 只使用合成测试画面和音轨，不调用付费服务。

原始素材、旧版本保留。项目可能含私人音视频及临时接口数据，不上传公共仓库。关闭页面不是确认，暂停不取消已提交上游任务。首版不承诺自动唤醒已结束 Agent、多机位、数字人、剪映草稿或自动发布。

原创整合代码 MIT；FredTalk 原创与第三方素材须分别遵守其许可，参见 THIRD_PARTY_NOTICES.md。验证详情见 VALIDATION.md。

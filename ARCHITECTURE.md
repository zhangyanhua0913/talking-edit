# 口播剪辑Skill架构

GitHub分发源码，Agent对话启动、编排和处理异常；静态页面与Python脚本随Skill安装，运行环境和业务项目放包外。当前v0.2.0为Windows源码试用版，支持范围见README和VALIDATION。

- scripts/core.py：SQLite权威项目/版本/确认/任务；project.json为可读镜像，旧产物保留。
- scripts/cli.py：JSON统一入口、依赖准备、交互请求、认证保活等待、执行与恢复。
- scripts/web.py与assets：回环HTTP服务、会话校验、六区工作台及批量处理；页面不冒充Agent。
- scripts/registry.py：转写、粗剪、包装、合成适配器及真实依赖状态。第三方Agent指令需审阅并绑定摘要。
- scripts/media.py与fred_bridge.py：共用时间映射、原声/视频同步剪切、字幕、变速、动画与可选配乐合成。
- scripts/batch.py：主项目范围的持久化串行队列，每视频独立项目，显式自动模式与手动模式分开。
- scripts/auto_gold.py：自动模式的暗金标题模板链；不承担语义图解创作。
- templates/gold-motion及evidence-motion：独立模板及锁文件，资料讲解整片组合由Agent制作为独立审看片。
- scripts/providers.py与vault.py：本地Whisper、受限云适配、Windows DPAPI；云新提交当前关闭。

交互绑定project_id/request_id/revision/stage，草稿不授权，旧版本拒绝覆盖；wait向服务认证保活。暂停只阻止尚未执行步骤，未知上游任务只查原单，不自动重建。自动模式需用户显式选定支持的范围，最终听看确认单独记录。

依赖、模型、用户媒体、凭据及运行数据库不随源码发布。升级只替换Skill，保留包外项目。完整命令与范围见skills/talking-edit/references。

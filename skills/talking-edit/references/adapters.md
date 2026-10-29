# 新增步骤 Skill

用户给出 GitHub 地址或本地路径后，先读取实际 SKILL.md、许可、运行脚本、输入输出与依赖。不要通过网页直接执行陌生地址。确认它承担粗剪还是包装；准备依赖并用隔离样例验证，再注册。

首版第三方扩展采用 Agent 执行：工作台返回该适配器的指令路径，由当前 Agent 完成，产物仍通过统一项目命令导入和人审。新增脚本执行器需改适配代码并增加行为测试，注册清单不能包含任意 shell 命令。

示例注册清单（路径换成实际已审阅文件）：

```json
{"id":"custom-packaging","name":"自定义包装方案","stages":["packaging"],"execution":"agent","input":"reviewed-timeline","output":"remotion-clips","version":"1","dependency":null,"instructions":"ABSOLUTE_PATH_TO_SKILL_MD","source_revision":"REVIEWED_COMMIT"}
```

register 保存指令文件 SHA-256；文件变化时 step 拒绝继续，必须重新审阅。项目保存选择的 adapter ID，已有结果保留，切换相关步骤使后续确认失效。新适配器也必须遵循本项目版本、暂停、付费和原单规则。带私人 Key 的配置仍只能经凭据页，不放入注册信息。

FredTalk 固定提交由 registry.py 维护，完整仓库在包外保留。目录检索只提供候选；Agent 必须核对实际源码、素材来源、锁文件和对应门禁，不能把所有预览都列为已可用组件。上游音频原声处理环境不随公开包分发，本适配遵照当前用户要求默认原速与零额外增益。

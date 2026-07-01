# Agent Workflow Hub

中文 | [English](./README.md)

面向 Codex 多 worktree / 多 thread 开发的 Agent 工作流层。Agent Workflow Hub 通过本地 sidecar 帮助 Codex 协调 project hub、execution thread、worktree、task、handoff、validation、safety rules 和 recommended actions。

Agent Workflow Hub 是 workflow state layer，不是原生模型 memory/context 的替代品。即使 Codex、Claude Code、Cursor、Windsurf 等 agent 的内置记忆继续增强，多 worktree 开发仍然需要一个显式、可审计的协议来回答：哪个 task 正在进行、对应哪个 worktree、验证过什么、哪些内容 stale、哪些未知、下一步应该由哪个 thread 执行。减少重复扫描和降低 context rebuild 成本是收益，不是产品契约。

日常入口是自然语言：

```text
Use $agent-workflow-hub to resume this worktree.
```

主 skill 自带 Python sidecar CLI，位于 `skills/agent-workflow-hub/scripts/`。兼容 skill 位于 `skills/context-handoff/`，使用同一套 CLI 和 sidecar 数据。用户安装 skill 后，不需要知道 CLI 在哪里。

## 兼容性

V2.7 起默认入口是 `$agent-workflow-hub`。`$context-handoff` 仍作为 legacy compatibility entrypoint 保留，并使用同一套本地 sidecar 数据、CLI 文件名和 JSON schema。已有 `%USERPROFILE%\.codex\projects\<project-id>\` 状态不会迁移。

## 产品定位

### 如果 agent 已经有 memory/context，为什么还需要它

原生 agent memory 更适合记住用户偏好、近期对话和宽泛上下文。Agent Workflow Hub 关注的是显式项目工作流状态：task 身份、worktree 映射、handoff facts、inferences、unknowns、validation、safety rules、stale detection，以及 project hub 级 recommended actions。

### 它不替代什么

它不替代代码理解、测试、PR review、issue tracking、项目管理工具，也不替代 agent 自己的调查判断。`resume-feature` 和 `resume-query` 恢复的是已记录的 workflow state，不证明代码正确。

### agent 继续变强后它仍然有价值的地方

当工作跨多个 worktree、多个 execution thread、多个 agent 或长期 branch 时，状态需要独立于任意单个聊天记录，并且可见、可检查、可交接。sidecar 是可审计的项目状态，不是聊天记录库，也不是模型思维链存储。

长版产品定位见 [docs/product/workflow-value-positioning.md](./docs/product/workflow-value-positioning.md)。

## 解决什么问题

- 新 execution thread 需要明确的 task/worktree 路由。
- feature branch、worktree、thread 之间丢失任务状态。
- 多 worktree 项目被拆成多个不相关的本地 projectId。
- handoff、完成归档、audit、周报输出不一致。
- project hub thread 把 sidecar 已登记任务误当成完整 worktree 全貌。
- agent 对什么时候开 hub、execution thread、side chat、subagent 或 worktree 给出不稳定建议。
- 动态 agent 状态误写进目标仓库文档或 feature PR。

## 安装

clone 本仓库后运行：

```powershell
python install.py
```

它会把两个完整 skill 包复制到：

```text
%USERPROFILE%\.codex\skills\agent-workflow-hub\
%USERPROFILE%\.codex\skills\context-handoff\
```

如果 Codex 没有立刻刷新 skill 列表，请重启或刷新 Codex。

安装器只复制两个 skill 包，不会安装 GitHub CLI，不会登录账号，也不会修改全局 Codex 配置。

## 使用

在任意 git 项目或 worktree 中，对 Codex 说：

```text
Use $agent-workflow-hub to run doctor/setup for this project.
```

然后可以自然对话：

```text
Use $agent-workflow-hub to start this feature. Goal: improve the dashboard UI.
```

```text
Use $agent-workflow-hub to resume this worktree and tell me the immediate next step.
```

```text
Use $agent-workflow-hub to 接手 markerless.
```

```text
Use $agent-workflow-hub to 你是 markerless 的执行进程.
```

```text
Use $agent-workflow-hub to save a handoff before I stop today.
```

```text
Use $agent-workflow-hub to audit this context before another agent takes over.
```

```text
Use $agent-workflow-hub to audit this project hub across all worktrees.
```

```text
Use $agent-workflow-hub to draft a dogfood issue for this problem.
```

```text
Use $agent-workflow-hub to finish this feature and generate PR text.
```

```text
Use $agent-workflow-hub to generate this week's eval report.
```

## 多 Thread Workflow Playbook

Agent Workflow Hub 把不同 thread 固化为 workflow 角色，把 sidecar 作为它们之间的共享状态层。默认心智模型是 `Hub -> Discussion/Research -> Execution`。这只是文档和 agent 指南，不要求 UI/MCP 支持。

用户主要需要记住 4 个 core roles：

- `hub`：全局状态、任务地图、路由、优先级、摘要、rebaseline、报告和项目级 prompt。
- `discussion`：工程路线、产品方向、架构取舍、任务塑形和实现准备度。
- `research`：面向外部证据的 thread，用于外部知识、学术/产品/生态研究、related work、市场对比、prior art、novelty、baseline、实验和基于证据的方向判断。
- `primary-execution`：实现、bugfix、本地验证、task handoff、finish/archive 和 PR 文案。

Support roles 仍保留给结构化 sidecar/UI/audit 状态，但默认工作流不要求用户记住：`review`、`validation`、`dogfood`、`explainer`。

默认拓扑：

- 一个项目默认一个 Project Hub Thread，负责项目全局状态、任务路由、worktree inventory，以及周期性的 `audit-project` / `weekly-report` 汇总。
- 一个 active worktree/task 默认一个 Primary Execution Thread，负责实现、验证、handoff、finish/archive 和 PR 文案。
- 当任务需要隔离 branch、并行实现或不同 base 时，创建新 worktree；继续同一任务或很小的一次性草稿时，复用当前 worktree。
- 模糊但确定会落到某个 repo/worktree 的 task，可以直接开 execution thread，在里面先 plan 再实现。
- 模糊且产品方向不确定的 task，留在 hub 或开短期 Discussion Thread，直到它变成可执行任务。
- 研究型问题进入 Research Thread，尤其是产出外部证据、prior art、市场/生态对比、论文 story、novelty、related work 方向、baseline、实验设计或可行性判断，而不是立即实现时。
- Side chat 用于短问题、草稿措辞、一次性推敲；只把稳定决策复制回 hub 或 execution thread。
- Subagent 用于临时 review、调查、对比或验证；它只回传 findings，不作为长期 task owner。
- Explainer Thread 用于深入项目讲解或 onboarding，避免把 hub 变成长教程。
- Dogfood/QA Thread 用于真实项目测试反馈、复现信息和 issue draft。
- `sidecar`、`handoff` 和 `audit-project` 是这些 thread 之间的共享状态层。

路由建议：

- 用户问“整个项目现在到哪了”、需要所有 worktree 或任务路由时，用或创建 Project Hub Thread。
- 用户要 build、fix、refactor、validate 或 finish 某个 branch/worktree task 时，用或创建 Primary Execution Thread。
- 只有隔离、并行工作或独立 branch/base 有价值时，才建议新 worktree；否则继续当前 worktree。
- task 还模糊但明显属于某个 repo/worktree 时，直接开 execution thread，并先在里面 plan。
- task 仍在讨论产品方向、优先级或是否值得做时，留在 hub 或 Discussion Thread。
- task 关注外部证据、学术/产品/生态研究、市场对比、prior art、论文潜力、novelty、related work、baseline、实验、ablation、审稿预期、可行性或投稿准备度时，用 Research Thread，并记录 `threadRole: research`。
- 小问题且不需要长期记忆时，用 side chat。
- 需要独立 review、调查或验证时，用 subagent，并给它窄问题和只返回 findings 的要求。
- 需要讲清架构、历史或 onboarding 时，用 Explainer Thread。
- dogfood/QA 反馈用 Dogfood/QA Thread；默认优先 `draft-issue`，除非用户明确要求创建 issue。

状态规则：

- Hub 负责地图、inventory、路由决策和紧凑摘要，不负责每个实现细节。
- Execution thread 按需用 `start-feature`、`resume-feature`、`handoff`、`audit-context` 和 `finish-feature` 更新 sidecar。
- Discussion、side chat、explainer、dogfood 和 subagent 的结果，只有复制进 hub、相关 execution thread 或 sidecar handoff/audit 输出后才算持久状态。
- 不要把 `project-status` 当成完整项目 inventory；hub 级状态必须用 `audit-project`。

推荐 prompt templates：

新 execution thread：

```text
You are the Primary Execution Thread for <project>/<task>. Repo/worktree: <path>. Use $agent-workflow-hub first: run resume-feature if a task already exists, otherwise start-feature with this goal: <goal>. Plan briefly inside this thread, then implement. Keep dynamic state in sidecar/handoffs, not tracked repo docs. Before stopping, run the relevant validation, audit-context if useful, and save a handoff with facts, inferences, unknowns, safety rules, validation, blockers, and next step.
```

Execution thread completion handoff：

```text
Task complete for <project>/<task>. Please update $agent-workflow-hub: run audit-context, then finish-feature or handoff as appropriate. Report back to the Project Hub with: branch, worktree, summary of changes, validation commands/results, PR URL or generated PR title/body, remaining risks, sidecar handoff/archive path, and whether the worktree is clean.
```

Dogfood feedback：

```text
This is a Dogfood/QA Thread for <project>. Feedback: <observed behavior>. Expected: <expected behavior>. Repo/worktree if known: <path>. Use $agent-workflow-hub to draft a dogfood issue. Keep Facts, Inferences, Unknowns, Reproduction, Suggested Fix, and Priority separate. Do not create a GitHub issue unless I explicitly ask or dogfood issue mode is enabled.
```

Project hub migration：

```text
You are the Project Hub Thread for <project>. Canonical repo/worktree: <path>. Use $agent-workflow-hub to run audit-project with the expected project id/base branch. Build the hub view from real git worktrees plus sidecar active tasks. Summarize active execution threads, missing sidecar coverage, stale handoffs, validation gaps, and concrete backfill prompts. Do not treat project-status as the full inventory.
```

Explainer thread：

```text
You are an Explainer Thread for <project>. Repo/worktree: <path>. Explain <topic> for onboarding. Use stable repo docs and current code. Keep the hub clean: produce a concise explanation, glossary, key files, and open questions, then tell the hub only the durable takeaways or docs that should be updated.
```

## 人类可读输出本地化

机器 JSON keys、CLI action names、status enum、event names、路径、branch 名和 Git 输出始终保持英文或原始值。给人读的 Markdown、摘要、warnings、findings message 和 backfill prompts 可以输出英文或简体中文。

默认语言是英文。对于单次命令，agent 可以给会产出人类可读文本的 action 传 `--language zh-CN` 或 `--language en`，包括 `handoff`、`resume-feature`、`audit-context`、`audit-project`、`weekly-report`、`draft-issue` 和 `create-issue`。

如果要把偏好持久化到本地 sidecar config：

```text
Use $agent-workflow-hub to set human-facing output language to zh-CN.
```

这只会把 `preferredLanguage` 写到 `%USERPROFILE%\.codex\projects\<project-id>\config.json`，不会修改目标项目仓库。

## 自然语言任务路由

V2.8 增加确定性的自然语言 task routing。用户只说 `continue markerless clean`、`接手 markerless`、`继续 markerless`、`恢复 markerless`、`你是 markerless 的执行进程` 或 `作为 markerless execution thread` 时，agent 应优先用 `resume-query --query "markerless"` 或 `resolve-task --query "markerless"`，从本地 sidecar 解析到正确 task/worktree，再执行 sidecar-first resume。

只有用户明确说 `当前 worktree`、`this worktree` 或明显指向已经选中的 Git worktree 时，才优先使用 `resume-feature`。

这不是替代 agent 的代码理解、测试或 PR review。它只是一个稳定、可审计、低摩擦的 workflow routing layer：恢复最近记录的 workflow state，并给出 branch、worktree、HEAD、dirty status、nextStep、blocker、validation、safetyRules 和 startThreadSummary。

解析完全本地确定性执行：字符串归一化、token overlap 和 `difflib`，不使用 LLM、embedding、向量库、UI、MCP 或 thread API。高置信时 `resume-query` 自动 resume；低置信或多个候选相近时只返回候选和一句消歧问题，不猜。

Task alias 支持：

- `start-feature --alias "markerless clean"` 和 `handoff --alias "markerless clean"` 会持久化用户确认过的 alias。
- `alias-task --alias "markerless clean"` 添加 alias。
- `alias-task --remove-alias "markerless clean"` 删除 alias。
- 程序生成的 alias 会参与匹配，但不会污染 task 的持久化 `aliases`。

`start-feature` 和 `handoff` 默认会拒绝在非 Git 路径上创建或更新 sidecar task/handoff，并返回 guidance，建议使用 `resume-query` 或提供真实 worktree path。只有用户明确要记录非 Git 目录时，才使用 `--allow-non-git-worktree`。

V3.5 增加 route guard 和 thread attachment metadata。写入型 action 会检查请求内容里明确出现的 task、branch、worktree hints；如果这些 hints 和当前 cwd 冲突，CLI 会返回 `routingStatus: "mismatch"` 或 `"ambiguous"`，不会静默写进当前 branch task。对于 agent 推断出的关系，sidecar 会记录 `routingStatus`、`routingConfidence`、`routingEvidence` 和 `routingNeedsReview`，方便 hub UI 显示“推断路由待确认”。

Task 支持轻量 parent/child 关系：子任务只保存 `parentTaskId`，children 由扫描所有 task 推导；sidecar 不保存 `childrenTaskIds`，也暂不支持 dependencies 或多 parent。可选 `phase`、`threadRole`、`threadLabel` 和 `threadPurpose` 用来描述 follow-up、validation、review、dogfood 或 explainer thread。

## 新 Thread 自我定位

当新 thread 以角色和主题开场时，先用 `orient-thread`：

```text
Use $agent-workflow-hub, you are a research thread about external skills for Agent Workflow Hub roles.
```

`orient-thread` 默认只报告，不写 sidecar。它会识别可能的 project、canonical `threadRole`、role boundary、task route、建议下一步、handoff 要求和可选 companion skills。只有用 `--attach` 重新运行时才会写入 sidecar。

当主题是整个项目、全局方向、项目 roadmap、研究路线或 hub/discussion/research 的 project-level 问题时，使用 `orient-thread --scope project-level`。project-level orientation 只把 canonical repo/project 路径当作 `storageAnchor`，把匹配到的 feature worktree 放进 `relatedCandidates`，除非用户明确选择某个 feature scope，否则不能把 thread 绑定到 feature worktree。

如果 route 是 inferred、ambiguous、mismatch，或来自非 Git 路径，`--attach` 必须同时使用 `--confirm-route`。建议的 external skills 只是 advisory metadata，不是必需依赖，也不会自动安装。

## Sidecar 状态
动态状态只保存在本机，不进入目标仓库：

```text
%USERPROFILE%\.codex\projects\<project-id>\
  config.json
  active-tasks.json
  project-state.json
  handoffs\
  archive\
  reports\
  events.jsonl
```

`project-state.json` 是给 agent 读的紧凑机器状态。handoff 和 weekly report 是给人读的 Markdown。稳定仓库事实仍然可以放在受版本控制的 `docs/agent/` 中。

projectId 在多个 worktree 之间保持稳定。解析顺序是：

- `--project-id`
- `CONTEXT_HANDOFF_PROJECT_ID`
- 已存在的本地 sidecar `config.json`
- Git remote URL 或 common Git directory
- repo root 名称兜底

base branch 可以用 `--base-branch dev` 覆盖；该值会持久化到本地 sidecar config，后续 action 会继续使用。

## 主要动作

- `doctor`：检查 Python、Git、sidecar、可选 GitHub CLI 是否就绪。
- `setup`：创建本地 sidecar 结构。
- `start-feature`：把当前 branch/worktree 记录为 active task。
- `attach-thread`：把 thread role、label、purpose、parent task、phase 和 routing review metadata 记录到 sidecar task。
- `orient-thread`：用 role 和简短 query 给新 thread 做自我定位。默认只报告；会建议 project/task route、role boundary、下一条 CLI 命令、handoff 要求和可选 companion skills。
- `resume-feature`：恢复紧凑上下文、stale detection，并输出 `startThreadSummary`。
- `handoff`：保存未完成工作、下一步、facts、inferences、unknowns、validation 和 safety rules。
- `audit-context`：报告当前 worktree 缺 handoff、stale git 状态、缺 validation、缺 safetyRules、dirty worktree 和 backfill prompts。
- `audit-project`：审计所有 Git worktree，对比真实 worktree 与 sidecar active tasks，并生成按 branch/worktree 分组的 backfill prompts、recommended actions、execution-thread prompts 和 cleanup prompts。
- `finish-feature`：归档任务并生成 PR 标题/正文；只有用户明确要求且 GitHub CLI 就绪时才创建 PR。
- `project-status`：汇总紧凑 sidecar 项目状态。它不是完整 Git worktree inventory。
- `weekly-report`：在 sidecar 的 `reports/` 目录生成给人看的 Markdown 周报。
- `eval-report`：在 sidecar 的 `reports/` 目录生成轻量 workflow evaluation Markdown 和 JSON 报告。它报告 workflow proxy metrics，不报告精确 token savings，也不证明代码正确。
- `visualize-project`：在 sidecar 的 `reports/` 目录生成 Markdown + Mermaid 项目关系图、配套 JSON 和静态 HTML dashboard。用户要求“可视化项目”或“显示项目图”时使用。
- `hygiene-dogfood`：报告已有后续通过证据的 stale dogfood/smoke sidecar 记录；只有显式传 `--confirm-archive --task-id <id>` 时才归档单个合格记录。
- `draft-issue`：生成 dogfood/debug issue draft，不需要 GitHub CLI。
- `create-issue`：仅在用户明确要求、内容安全、GitHub CLI 已登录且未发现明显重复时创建 dogfood/debug issue。
- `enable-dogfood-issue-mode` / `disable-dogfood-issue-mode`：把 dogfood issue 创建权限保存到本地 sidecar config。
- `set-language`：把人类可读输出语言偏好保存到本地 sidecar config。
- `snapshot`：输出当前 worktree 的 Git facts，用于轻量 backfill。

V1 的 `worktree-intake` 和 `worktree-handoff` 已合并进 Agent Workflow Hub，分别对应 `resume-feature` 和 `handoff`。旧 `$context-handoff` 入口仍作为兼容入口保留。

## Project Hub Inventory

`project-status` 只报告 sidecar 已登记的 active tasks。它不会枚举每个 Git worktree。对于 project hub thread 或多 worktree 状态，请使用：

```text
Use $agent-workflow-hub to audit this project hub across all worktrees. Project id: my_project. Base branch: dev.
```

skill 会运行 `audit-project`，它使用 `git worktree list --porcelain` 枚举所有 worktree，逐个审计，并返回：

- Git worktree 总数与 sidecar active task 总数。
- 已登记和未登记的 worktree。
- dirty、stale、缺 handoff、缺 validation、缺 safety rule 的 worktree。
- sidecar 中记录了 task 但对应 worktree 已不存在的条目。
- 按 branch/worktree 分组的 backfill prompts。
- 可复制给旧 thread 或新 execution thread 的 recommended actions。
- 针对 worktree 已不存在的 sidecar task 的 cleanup prompts。

`sidecarHit: false` 的行表示不存在真实 sidecar task，因此 `taskStatus` 会是 `"missing"`。这类行可能包含 `provisionalTaskStatus`，它只是 audit 生成的临时 fallback，不代表 sidecar 状态。

如果请求的 projectId 被规范化，例如 `paus_robot_lab_host` 变成 `paus-robot-lab-host`，输出会显式提示这次 canonicalization。

如果旧 execution thread 仍存在，优先把 `oldThreadBackfillPrompt` 发给旧 thread，因为它可能仍有 Git 无法恢复的语义上下文。没有旧 thread 时，再用 `newExecutionThreadPrompt` 开新的 Primary Execution Thread。新 thread 必须恢复或初始化 sidecar 状态，区分 facts/inferences/unknowns，补 validation/safety/nextStep，保存 handoff，并回执 Project Hub。

这些 prompt 用来标准化协作产物，而不是微管理 agent 的调查路径。Agent 可以按需使用 sidecar 状态、handoff Markdown、Git facts、touched files、recent commits、PR、issue、测试或 targeted search。

## 项目可视化

当用户说 `可视化项目`、`显示项目图`、`项目关系图`、`看一下项目全局`、`visualize project` 或 `show project graph` 时，使用：

```text
使用 $agent-workflow-hub 可视化当前项目。
```

skill 会运行 `visualize-project`，在本机 sidecar 的 `reports/` 目录写入 Markdown、JSON 和静态 HTML dashboard 报告。默认回复只贴 Mermaid 图、Legend、详情表、needs-attention 摘要和报告路径，不贴完整 JSON。HTML 默认只生成路径，不自动打开浏览器。

默认图只展示主链路 `Project -> Task -> Worktree -> Thread Role`。HTML dashboard 把 Project 保持为页面上下文，task/worktree/thread 支持 route spotlight；dependency 和 `th-project-hub` audit/routing 入口不进入 ownership 图；risk、nextStep、validation、handoff 放在详情面板，不画成主图节点。状态和健康度通过文本 badge 与视觉 class 表达。可视化详情会把 canonical `threadRole` 和人类可读 `threadLabel` 分开展示。归档任务默认隐藏，并显示 `Archived hidden: N`；只有需要查看归档上下文时才传 `--include-archive`。

## 可信 handoff

Git 历史可以恢复客观事实，例如 branch、commit、改动文件和触达目录。它不能可靠恢复目标、设计决策、阻塞点、验证状态或正确下一步。

`touchedFiles` 表示当前 Git dirty/touched files。它只是上下文不足时的定位线索之一，不要求 agent 固定先看 touched files，也不要求做全量扫描。

V2.2 handoff 会强制区分：

- `facts`：观察到或用户提供的事实。
- `inferences`：agent 的推断，必须可检查。
- `unknowns`：缺失上下文，不应被猜测填补。
- `safetyRules`：后续 agent 必须遵守的一等约束。
- `validation`：命令、结果、备注和验证时间。

sidecar 也会记录 `headSha`、`upstream`、`dirtyFiles` 和 `dirtyFingerprint`。当 HEAD 或 dirty files 与记录的 task snapshot 不一致时，`resume-feature` 和 `audit-context` 会标记 stale。

## Dogfood Issue Mode

Dogfood issue 默认只生成 draft。agent 可以用 `draft-issue` 产出可复制的标题和正文，不需要 GitHub CLI。Issue body 必须区分：

- Facts
- Inferences
- Unknowns
- Reproduction
- Suggested Fix
- Priority

只有当用户明确要求创建 issue，或为本地 sidecar project 启用 `dogfoodIssueMode` 后，CLI 才允许自动创建 issue。自动创建的 issue 会带有 `agent-reported` 和 `needs-triage` labels。创建前会检查 `gh auth status`，尽量搜索相似 open issue，并在检测到敏感内容、密钥、本地隐私路径或过长日志时阻止创建并返回 draft。`dogfoodIssueMode` 只写入本机 sidecar config，不写入目标仓库。

## Dogfood Smoke Hygiene

`hygiene-dogfood` 是一个很窄的安全阀，用来处理已经被后续通过结果覆盖的旧 dogfood/smoke 记录，例如 pre-reinstall 失败、stale environment blocker。默认只报告候选项，并在 hub 输出里通过 `dogfoodHygiene` 和 `archive-stale-dogfood-record` recommendation 暴露。

它不会批量归档、不会删除 worktree，也不会清理普通 execution task。要归档一个合格记录，必须显式确认：

```text
hygiene-dogfood --confirm-archive --task-id <id>
```

## GitHub PR 行为

GitHub CLI 是可选能力。没有 PR URL 时，`finish-feature` 也能正常完成和归档。如果本机已安装并登录 `gh`，且用户明确要求创建 PR，skill 才会尝试创建 PR。否则它只生成 PR 标题/正文，并记录本地完成状态。

任何非 0 的 `gh auth status` 结果、traceback、`TypeError` 或 exception-like 输出都会被视为未认证。

## 研究说明

`events.jsonl` 会记录轻量生命周期事件，方便以后评估效果。它本身不是完整 benchmark。后续对照实验设计见 [docs/research/agent-workflow-hub-v2-benchmark.md](./docs/research/context-handoff-v2-benchmark.md)。

`weekly-report` 面向项目进展汇报。`eval-report` 面向 Agent Workflow Hub 工具效果：usage counts、recovery health、routing health、coverage 和 proxy efficiency metrics。它刻意不声明精确 token 节省。

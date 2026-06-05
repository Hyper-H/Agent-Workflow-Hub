# context-handoff

中文 | [English](./README.md)

`context-handoff` 是一个自包含的 Codex 本地项目上下文层，面向多 worktree 的 AI 辅助开发。它帮助 agent 恢复 feature 上下文、审计 project hub 状态，并在 branch、worktree、thread 之间协调任务状态，减少重复扫描和重复解释。

日常入口是自然语言：

```text
Use $context-handoff to resume this worktree.
```

skill 自带 Python sidecar CLI，位于 `skills/context-handoff/scripts/`。用户安装 skill 后，不需要知道 CLI 在哪里。

## 解决什么问题

- 新 agent thread 反复扫描同一个仓库。
- feature branch、worktree、thread 之间丢失任务状态。
- 多 worktree 项目被拆成多个不相关的本地 projectId。
- handoff、完成归档、audit、周报输出不一致。
- project hub thread 把 sidecar 已登记任务误当成完整 worktree 全貌。
- 动态 agent 状态误写进目标仓库文档或 feature PR。

## 安装

clone 本仓库后运行：

```powershell
python install.py
```

它会把完整 skill 包复制到：

```text
%USERPROFILE%\.codex\skills\context-handoff\
```

如果 Codex 没有立刻刷新 skill 列表，请重启或刷新 Codex。

安装器只复制 skill 包，不会安装 GitHub CLI，不会登录账号，也不会修改全局 Codex 配置。

## 使用

在任意 git 项目或 worktree 中，对 Codex 说：

```text
Use $context-handoff to run doctor/setup for this project.
```

然后可以自然对话：

```text
Use $context-handoff to start this feature. Goal: improve the dashboard UI.
```

```text
Use $context-handoff to resume this worktree and tell me the immediate next step.
```

```text
Use $context-handoff to save a handoff before I stop today.
```

```text
Use $context-handoff to audit this context before another agent takes over.
```

```text
Use $context-handoff to audit this project hub across all worktrees.
```

```text
Use $context-handoff to draft a dogfood issue for this problem.
```

```text
Use $context-handoff to finish this feature and generate PR text.
```

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
- `resume-feature`：恢复紧凑上下文、stale detection，并输出 `startThreadSummary`。
- `handoff`：保存未完成工作、下一步、facts、inferences、unknowns、validation 和 safety rules。
- `audit-context`：报告当前 worktree 缺 handoff、stale git 状态、缺 validation、缺 safetyRules、dirty worktree 和 backfill prompts。
- `audit-project`：审计所有 Git worktree，对比真实 worktree 与 sidecar active tasks，并生成按 branch/worktree 分组的 backfill prompts。
- `finish-feature`：归档任务并生成 PR 标题/正文；只有用户明确要求且 GitHub CLI 就绪时才创建 PR。
- `project-status`：汇总紧凑 sidecar 项目状态。它不是完整 Git worktree inventory。
- `weekly-report`：在 sidecar 的 `reports/` 目录生成给人看的 Markdown 周报。
- `draft-issue`：生成 dogfood/debug issue draft，不需要 GitHub CLI。
- `create-issue`：仅在用户明确要求、内容安全、GitHub CLI 已登录且未发现明显重复时创建 dogfood/debug issue。
- `enable-dogfood-issue-mode` / `disable-dogfood-issue-mode`：把 dogfood issue 创建权限保存到本地 sidecar config。
- `snapshot`：输出当前 worktree 的 Git facts，用于轻量 backfill。

V1 的 `worktree-intake` 和 `worktree-handoff` 已合并进统一的 `context-handoff` skill，分别对应 `resume-feature` 和 `handoff`。

## Project Hub Inventory

`project-status` 只报告 sidecar 已登记的 active tasks。它不会枚举每个 Git worktree。对于 project hub thread 或多 worktree 状态，请使用：

```text
Use $context-handoff to audit this project hub across all worktrees. Project id: my_project. Base branch: dev.
```

skill 会运行 `audit-project`，它使用 `git worktree list --porcelain` 枚举所有 worktree，逐个审计，并返回：

- Git worktree 总数与 sidecar active task 总数。
- 已登记和未登记的 worktree。
- dirty、stale、缺 handoff、缺 validation、缺 safety rule 的 worktree。
- sidecar 中记录了 task 但对应 worktree 已不存在的条目。
- 按 branch/worktree 分组的 backfill prompts。

如果请求的 projectId 被规范化，例如 `paus_robot_lab_host` 变成 `paus-robot-lab-host`，输出会显式提示这次 canonicalization。

## 可信 handoff

Git 历史可以恢复客观事实，例如 branch、commit、改动文件和触达目录。它不能可靠恢复目标、设计决策、阻塞点、验证状态或正确下一步。

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

## GitHub PR 行为

GitHub CLI 是可选能力。没有 PR URL 时，`finish-feature` 也能正常完成和归档。如果本机已安装并登录 `gh`，且用户明确要求创建 PR，skill 才会尝试创建 PR。否则它只生成 PR 标题/正文，并记录本地完成状态。

任何非 0 的 `gh auth status` 结果、traceback、`TypeError` 或 exception-like 输出都会被视为未认证。

## 研究说明

`events.jsonl` 会记录轻量生命周期事件，方便以后评估效果。它本身不是完整 benchmark。后续对照实验设计见 [docs/research/context-handoff-v2-benchmark.md](./docs/research/context-handoff-v2-benchmark.md)。

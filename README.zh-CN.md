# context-handoff

中文 | [English](./README.md)

`context-handoff` 是一套轻量的上下文复用与交接工作流，用来降低多 worktree、多 thread 的 feature/PR 开发中的上下文重建成本。它由仓库内稳定事实、本机 sidecar 状态层，以及 intake/handoff skills 组成。

## 它解决什么问题

- 新 thread 反复重扫同一个仓库
- 多个 worktree 和 agent thread 之间容易丢失任务状态
- feature 或 PR 的交接噪声大、不稳定、成本高

## 核心思路

把项目上下文拆成三层：

- `docs/agent/`
  放入版本控制的稳定仓库事实
- local sidecar
  不进入 feature PR 的动态任务状态
- `worktree-intake` / `worktree-handoff`
  用自然语言触发的 skill 入口，用来恢复和保存当前任务上下文

## 实际应该怎么用

这套方案的主要入口应该是对话，而不是手动敲命令。

理想中的实际使用方式应该像这样：

- `接手这个 worktree，告诉我现在做到哪了`
- `继续这个 feature，恢复一下当前上下文`
- `我准备提 PR，先同步一下当前状态并做 handoff`
- `结束这轮开发，把 next step 和记交接都存一下`
- `这个任务做完了，归档当前任务状态`

也就是说，skill 应该在后台自动同步 sidecar。Python 脚本是 skill 背后的实现层，同时也保留为测试和调试时的备用入口。

## 仓库结构

```text
docs/
  agent/
    project-map.md
    conventions.md
    common-commands.md
skills/
  worktree-intake/
  worktree-handoff/
tools/
  worktree-context-reuse-v1/
    context_sidecar.py
    templates/
specs/
  multi-worktree-thread-handoff-v1.md
worktree-context-reuse-v1-usage.md
```

## 本机 Sidecar 结构

工具默认把本机状态写到：

```text
%USERPROFILE%\.codex\projects\<project-id>\
  active-tasks.json
  handoffs\
  archive\
  events.jsonl
```

这些状态是本机私有的，不应该进 feature PR。

## 对话优先的快速开始

1. 先补齐 `docs/agent/` 下的稳定事实文档
2. 把两个 skill 安装或复制到本机 Codex skill 目录
3. 在真实 git worktree 里，优先直接对 agent 说：
   - `Use $worktree-intake to recover the current worktree context and tell me the next step.`
4. 每轮工作结束前，对 agent 说：
   - `Use $worktree-handoff to save the current worktree status and prepare the next agent handoff.`
5. 任务彻底完成后，让 agent 归档当前任务

## Skill 用法

本地安装后，可以直接这样对 Codex 说：

- `Use $worktree-intake to recover the current worktree context and tell me the next step.`
- `Use $worktree-handoff to save the current worktree status and prepare the next agent handoff.`

也可以直接说更自然的话，比如：

- `接手当前 worktree，恢复一下上下文`
- `继续这个分支，告诉我下一步做什么`
- `提 PR 前先帮我同步当前状态`
- `结束今天这轮，给下一个 agent 留个交接`
- `这个任务结束了，归档掉当前状态`

## 底层 CLI

仓库里仍然保留了 Python CLI，方便测试、调试和非 skill 集成：

```powershell
python tools\worktree-context-reuse-v1\context_sidecar.py init
python tools\worktree-context-reuse-v1\context_sidecar.py snapshot
python tools\worktree-context-reuse-v1\context_sidecar.py intake
python tools\worktree-context-reuse-v1\context_sidecar.py handoff ...
python tools\worktree-context-reuse-v1\context_sidecar.py archive
```

## 当前验证状态

这个仓库里的 v1 实现目前已经验证过：

- 非 git 回退场景
- 一个临时真实 git 仓库中的 smoke test：
  - `snapshot`
  - `handoff`
  - `intake`
  - `archive`

## 说明

- 这个项目在 v1 明确不优先做自定义 MCP
- 当前设计优先服务个人工作流，之后再考虑共享或实验评估
- `events.jsonl` 只是轻量实验留痕，不是正式 benchmark

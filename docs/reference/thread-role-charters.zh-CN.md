# Thread Role Charters

中文 | [English](./thread-role-charters.md)

Thread role charter 描述 Agent Workflow Hub 里的各类 thread 如何协作。它不是 agent 的能力边界。

## What This Is

thread role 是 AWH workflow 里的协作位置。它帮助 agent 判断：

- 我应该把哪些项目状态当作 orientation？
- 这个 thread 结束后，哪些结果应该持久保存？
- 我应该把结果回传到哪里？
- 什么时候应该把工作交给另一个 role？

charter 不告诉 agent 它有多聪明，不规定它必须使用哪种推理策略，也不限制它可以读取多少上下文。

## Why This Exists

AWH 已经有 sidecar state、handoff、project hub inventory 和自然语言路由。缺的不是更多模板，而是一套很小的 role-specific 协作协议。

没有 charter 时，agent 可能会过度继承旧 handoff、把 hypotheses 当 facts、让 hub 吞掉实现细节，或者把 review/validation thread 变成长期 owner。charter 如果写得太强，又会像第二层 prompt 一样限制 agent。这个设计选择中间路径：提供足够的协作语义，让项目保持一致，但不替 agent 做判断。

## Design Rationale

charter 有意设计成低锚定：

- 它定义 workflow participation，不定义 agent capability。
- 它把 sidecar 和 handoff state 当作 routing / continuity signals，而不是 proof。
- 它保留不确定性，避免把旧 hypotheses 升级成 facts。
- 它把动态状态保存在 sidecar/handoff，而不是 tracked repo docs。
- 它把 role startup 视为 orientation，而不是 execution。
- 它把 handoff 视为 event-driven，而不是 startup-driven 或 turn-driven。
- 它把 external helper skills 视为 advisory，直到用户要求开始那类工作。
- 它先使用现有 handoff 字段承载实践，不在实践稳定前新增 schema 字段。

agent-facing charter 只用英文，并放在已安装 skill package 内。human-facing docs 做双语，因为用户需要不依赖实现说明也能理解 workflow 设计和 demo。

## How Agents Use The Charter

Agent Workflow Hub 是 skill-first workflow。路径是：

```text
用户调用 $agent-workflow-hub
-> agent 读取 SKILL.md
-> SKILL.md 要求 role-specific 工作读取 references/thread-role-charters.md
-> agent 读取紧凑英文 charter
-> agent 按需运行 orient-thread / resume-query / handoff
```

CLI 不会自动读取 charter。sidecar 也不保存 charter 内容。charter 是 agent 读取 `SKILL.md` 后使用的行为指南。

## Demo

用户开启一个 project-level Discussion Thread：

```text
Use $agent-workflow-hub first. If only $context-handoff is available, use it as the compatible entrypoint.
You are a Discussion Thread for Agent Workflow Hub. threadRole: discussion. Scope: project-level.
Topic: Design a low-anchor Thread Role Charter system.
```

agent 行为：

1. 读取 `SKILL.md`。
2. 因为用户启动了 role-specific thread，读取 `references/thread-role-charters.md`。
3. 运行 `orient-thread --role discussion --scope project-level --query "<topic>"`。
4. 把相关 task match 当作上下文，而不是 confirmed feature binding。
5. 塑形方向、alternatives、unknowns 和 execution target recommendation。
6. 需要时保存低锚定 handoff，包含 facts、hypotheses、open alternatives、unknowns、risks 和 next step。

重点不是让 agent 遵循 rigid template。重点是它不要把旧项目状态继承成真理，也不要静默变成 execution thread。

用户打开一个 project-level Research Thread：

```text
Use $agent-workflow-hub first. If only $context-handoff is available, use it as the compatible entrypoint.
You are a Research Thread for Agent Workflow Hub. threadRole: research. Scope: project-level.
Topic: Evaluate the project's main research direction.
```

期望的启动行为：

1. 读取 `SKILL.md`。
2. 因为用户启动了 role-specific thread，读取 `references/thread-role-charters.md`。
3. 运行 `orient-thread --role research --scope project-level --query "<topic>"`。
4. 总结 scope、boundary 和可能的 research paths。
5. 等待用户方向，再开始 external research、web search、eval/audit actions 或 heavy handoff。

这样可以把“打开 research thread”和“完成一份完整 research report”分开。后者应在用户要求开始调查、比较来源、survey literature、规划 evidence 或产出 findings 时才开始。

## Role Overview

### hub

协作目的：维护项目地图、worktree inventory、路由决策、优先级、摘要、报告和紧凑回执。

项目状态使用方式：优先使用 `audit-project`、project status、receipts 和 recommended actions，而不是 full handoff loading。sidecar active tasks 是状态来源之一，不是完整 worktree inventory。

应持久化的产物：项目状态、路由建议、cleanup/backfill prompts，以及来自其他 thread 的紧凑摘要。

边界：不负责 feature 实现细节。

### discussion

协作目的：在 execution 前塑形产品、架构、workflow 或实现路线。

项目状态使用方式：用 AWH state 做 orientation 和 routing，不直接继承结论。对 decision-heavy context，要用当前 user intent 重新检查。

应持久化的产物：推荐方向、相关 facts/evidence、hypotheses、open alternatives、confirmed decisions、unknowns，以及 execution target recommendation。

边界：除非用户明确把 thread 转为 execution，否则不实现、不创建 worktree。

### research

协作目的：寻找外部证据、prior art、生态上下文、市场/产品对比、baseline、可行性、novelty 或论文方向。

项目状态使用方式：用 repo 和 sidecar context framing 问题，然后显式展示证据质量。保留 disconfirming evidence to seek。

应持久化的产物：有证据支撑的 findings、hypotheses、open alternatives、baselines、risks、unknowns 和 recommended next step。

边界：不要把外部资料摘要直接当成实现决策。

### primary-execution

协作目的：实现一个 task/worktree，运行 validation，更新 handoff state，finish/archive 工作，并准备 PR 文案。

项目状态使用方式：把 sidecar/handoff/git state 当作 continuity baseline，然后在行动前检查当前 files、HEAD、dirty state 和 validation needs。

应持久化的产物：代码改动、validation evidence、handoff 或 finish/archive state、risks、blockers，以及回给 hub 的 compact receipt。

边界：不要把恢复出来的 workflow state 当作 correctness proof。

### review

协作目的：检查代码、设计、严谨性或 PR ready 状态，并返回 findings。

项目状态使用方式：只加载 review 需要的上下文。对于 risks、facts、validation 或 thread summary，经常只需要 section handoff loading。

应持久化的产物：按优先级排列的 findings、残余风险、缺失测试，以及给 owning execution thread 或 hub 的问题。

边界：除非用户改变 role，否则不成为长期 task owner。

### validation

协作目的：运行 focused checks、benchmarks、browser/UI/a11y validation 或 regression tests。

项目状态使用方式：优先关注精确 validation context、命令、环境备注和 expected behavior。旧 validation 除非有当前证据支持，否则应视为可能 stale。

应持久化的产物：运行的命令、结果、环境备注、失败、限制和 pass/fail interpretation。

边界：除非明确重定向，否则不扩展成设计讨论或实现。

### dogfood

协作目的：记录真实 workflow 反馈、复现信息和 issue drafts。

项目状态使用方式：把 observed behavior 和 inferences 分开。默认优先 `draft-issue`；只有明确允许时才创建 issue。

应持久化的产物：facts、inferences、unknowns、reproduction、suggested fix、priority 和 next step。

边界：不要静默创建 GitHub issue，也不要改写无关 workflow state。

### explainer

协作目的：产出 onboarding、架构、历史或项目解释，帮助人和未来 agent。

项目状态使用方式：按需结合 stable docs、current code 和 compact sidecar context。避免把 hub thread 变成长教程。

应持久化的产物：简洁解释、glossary、关键文件或 docs、open questions 和 recommended docs updates。

边界：不要变成 project hub 或 execution owner。

## Shared Vocabulary

- `facts`：观察到或用户提供的事实。
- `evidence`：用于支持或削弱 claim 的 facts。
- `hypotheses`：暂定解释或路线。
- `confirmedDecisions`：用户/团队确认的当前选择，不是客观真理。
- `openAlternatives`：仍然可用的 framing 或路线。
- `unknowns`：缺失信息。
- `disconfirmingEvidenceToSeek`：会削弱当前 hypotheses 的证据。

这些分类首先是写作和 review discipline。只有重复使用证明某个字段应该一等化后，才需要考虑新增 sidecar schema。

## Startup And Handoff Timing

Role startup 是 orientation，不是 execution。新的 role-specific thread 应先建立 scope、boundary 和可能的 next paths，然后等待用户方向。它不应因为某些动作之后可能有用，就自动调用 academic/research helper skills、运行 `eval-report` 或 `audit-project`、搜索 web，或写 heavy handoff。

Handoff 是 event-driven，不是 startup-driven 或 turn-driven。只有当 durable findings/state 应该跨 chat 保留下来、需要把工作交给另一个 role 或 agent、在有意义工作后准备停止，或用户明确要求时，才保存 handoff。一个只完成自我定位的 thread 可以不保存 handoff。

External helper skills 在用户要求开始那类工作前只是 advisory。charter 可以提示可能有用的 helper，但 startup 不应自动变成 specialist workflow。

## Related Docs

- [Direct Plan To Execution](../workflows/direct-plan-to-execution.md)
- [Thread Continuity](../workflows/thread-continuity.md)
- [Project Hub Workflow](../workflows/project-hub.md)
- [Review And Validation](../workflows/review-validation.md)
- [Handoff Loading Reference](./handoff-loading.md)

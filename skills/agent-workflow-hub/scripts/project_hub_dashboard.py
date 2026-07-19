from __future__ import annotations

import json
from typing import Any


def _json_for_script(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def build_visual_project_html(report: dict[str, Any]) -> str:
    payload = dict(report)
    payload["dashboardVersion"] = "v3.4"
    data = _json_for_script(payload)
    html = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Agent Workflow Hub - Project Hub</title>
  <style>
    :root {
      --bg: #f6f4ee;
      --surface: #fffef9;
      --surface-2: #efede4;
      --surface-3: #e4dfd2;
      --ink: #20211d;
      --muted: #67645c;
      --line: #d3ccbd;
      --line-strong: #9d9586;
      --focus: #1f5f78;
      --accent: #28665d;
      --attention: #946017;
      --blocked: #96312b;
      --healthy: #2f6849;
      --archived: #6f6c64;
      --shadow: 0 18px 46px rgba(42, 36, 27, .12);
      --mono: Consolas, "SFMono-Regular", "Liberation Mono", monospace;
      --sans: "Microsoft YaHei UI", "Segoe UI", system-ui, sans-serif;
    }

    * { box-sizing: border-box; }

    body {
      margin: 0;
      min-height: 100vh;
      color: var(--ink);
      background:
        linear-gradient(90deg, rgba(32, 33, 29, .045) 1px, transparent 1px) 0 0 / 36px 36px,
        linear-gradient(0deg, rgba(32, 33, 29, .03) 1px, transparent 1px) 0 0 / 36px 36px,
        var(--bg);
      font-family: var(--sans);
      letter-spacing: 0;
    }

    button,
    input {
      font: inherit;
    }

    button {
      border: 0;
    }

    .app {
      display: grid;
      grid-template-columns: 72px minmax(0, 1fr);
      min-height: 100vh;
    }

    .rail {
      position: sticky;
      top: 0;
      z-index: 5;
      height: 100vh;
      padding: 16px 12px;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 12px;
      border-right: 1px solid var(--line);
      background: rgba(255, 254, 249, .78);
      backdrop-filter: blur(14px);
    }

    .mark {
      width: 42px;
      height: 42px;
      display: grid;
      place-items: center;
      background: var(--ink);
      color: var(--surface);
      border: 1px solid var(--ink);
      font-weight: 850;
    }

    .rail button {
      width: 42px;
      height: 42px;
      display: grid;
      place-items: center;
      background: transparent;
      color: var(--muted);
      border: 1px solid transparent;
      cursor: pointer;
      font-weight: 850;
    }

    .rail button.active,
    .rail button:hover {
      background: var(--surface);
      color: var(--ink);
      border-color: var(--line);
    }

    .shell {
      min-width: 0;
      display: grid;
      grid-template-rows: auto 1fr;
    }

    .topbar {
      position: sticky;
      top: 0;
      z-index: 4;
      display: grid;
      grid-template-columns: minmax(260px, 1fr) minmax(260px, 420px);
      gap: 18px;
      align-items: center;
      padding: 16px 24px;
      border-bottom: 1px solid var(--line);
      background: rgba(246, 244, 238, .88);
      backdrop-filter: blur(16px);
    }

    .eyebrow {
      margin: 0 0 5px;
      color: var(--muted);
      font-size: 12px;
      font-weight: 850;
      text-transform: uppercase;
    }

    h1 {
      margin: 0;
      font-size: 34px;
      line-height: 1.05;
    }

    .subtitle {
      margin: 7px 0 0;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.45;
      overflow-wrap: anywhere;
    }

    .toolbar {
      display: grid;
      gap: 10px;
      justify-items: end;
      min-width: 0;
    }

    .search {
      width: 100%;
      min-height: 40px;
      padding: 0 12px;
      border: 1px solid var(--line);
      background: var(--surface);
      color: var(--ink);
      outline: 0;
    }

    .search:focus {
      border-color: var(--focus);
      box-shadow: 0 0 0 3px rgba(31, 95, 120, .15);
    }

    .mode-switch {
      display: inline-flex;
      width: fit-content;
      gap: 2px;
      padding: 2px;
      border: 1px solid var(--line);
      background: var(--surface-2);
    }

    .mode-switch button {
      min-height: 30px;
      padding: 0 10px;
      background: transparent;
      color: var(--muted);
      cursor: pointer;
      font-size: 12px;
      font-weight: 850;
      white-space: nowrap;
    }

    .mode-switch button.active {
      background: var(--surface);
      color: var(--ink);
      box-shadow: 0 1px 0 rgba(0, 0, 0, .07);
    }

    .content {
      display: grid;
      grid-template-columns: minmax(0, 1fr) 382px;
      gap: 20px;
      padding: 20px 24px 26px;
      min-width: 0;
    }

    .workspace,
    .side {
      display: grid;
      gap: 16px;
      align-content: start;
      min-width: 0;
    }

    .summary-grid {
      display: grid;
      grid-template-columns: minmax(280px, 1.45fr) repeat(4, minmax(112px, .55fr));
      gap: 10px;
    }

    .summary,
    .metric,
    .panel {
      background: rgba(255, 254, 249, .92);
      border: 1px solid var(--line);
      box-shadow: 0 1px 0 rgba(255, 255, 255, .72) inset;
    }

    .summary {
      min-height: 126px;
      padding: 16px;
      display: grid;
      gap: 10px;
      align-content: space-between;
    }

    .summary h2 {
      margin: 0;
      font-size: 17px;
    }

    .summary p {
      margin: 0;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.5;
    }

    .metric {
      min-height: 126px;
      padding: 14px;
      display: grid;
      align-content: space-between;
      gap: 8px;
    }

    .metric span {
      color: var(--muted);
      font-size: 12px;
      font-weight: 850;
      text-transform: uppercase;
    }

    .metric b {
      font-size: 31px;
      line-height: 1;
    }

    .panel-head {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 14px;
      padding: 14px 16px;
      border-bottom: 1px solid var(--line);
    }

    .panel-head h2,
    .detail-title {
      margin: 0;
      font-size: 15px;
    }

    .map-wrap {
      position: relative;
      min-height: 548px;
      overflow: hidden;
      background:
        linear-gradient(90deg, rgba(40, 102, 93, .07) 0 33.33%, transparent 33.33% 66.66%, rgba(148, 96, 23, .06) 66.66%),
        var(--surface);
    }

    .context-band {
      margin: 14px;
      min-height: 68px;
      padding: 12px 14px;
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 14px;
      align-items: center;
      border: 1px solid var(--line);
      background: rgba(255, 254, 249, .88);
    }

    .context-band b {
      display: block;
      margin-bottom: 4px;
      font-size: 14px;
      overflow-wrap: anywhere;
    }

    .context-band span {
      color: var(--muted);
      font-size: 12px;
      line-height: 1.4;
    }

    .map-stage {
      position: relative;
      min-height: 438px;
      padding: 0 14px 18px;
    }

    .map-svg {
      position: absolute;
      inset: 0 14px 18px;
      width: calc(100% - 28px);
      height: calc(100% - 18px);
      pointer-events: none;
      z-index: 0;
    }

    .map-lanes {
      position: relative;
      z-index: 1;
      display: grid;
      grid-template-columns: repeat(3, minmax(190px, 1fr));
      gap: 16px;
      height: 100%;
      min-height: 438px;
    }

    .lane {
      min-width: 0;
      display: grid;
      grid-template-rows: auto 1fr;
      gap: 10px;
    }

    .lane-title {
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      gap: 12px;
      color: var(--muted);
      font-size: 12px;
      font-weight: 850;
      text-transform: uppercase;
    }

    .node-stack {
      display: flex;
      flex-direction: column;
      gap: 10px;
    }

    .node {
      width: 100%;
      min-height: 80px;
      padding: 11px;
      display: grid;
      gap: 7px;
      text-align: left;
      color: var(--ink);
      background: rgba(255, 254, 249, .94);
      border: 1px solid var(--line);
      box-shadow: 0 1px 0 rgba(255, 255, 255, .72) inset;
      cursor: pointer;
      transition: transform .16s ease, border-color .16s ease, box-shadow .16s ease, opacity .16s ease, background .16s ease;
    }

    .node:hover {
      transform: translateY(-1px);
      border-color: var(--line-strong);
      box-shadow: 0 12px 28px rgba(42, 36, 27, .1);
    }

    .node.selected {
      border-color: var(--focus);
      background: #fffffc;
      box-shadow: 0 0 0 3px rgba(31, 95, 120, .18), 0 13px 30px rgba(42, 36, 27, .1);
    }

    .node.related {
      border-color: var(--ink);
    }

    .node.dimmed {
      opacity: .36;
    }

    .node-type {
      color: var(--muted);
      font-size: 11px;
      font-weight: 850;
      text-transform: uppercase;
    }

    .node-main {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 9px;
      min-width: 0;
    }

    .node-name {
      min-width: 0;
      font-size: 14px;
      font-weight: 850;
      line-height: 1.2;
      overflow-wrap: anywhere;
    }

    .node-meta {
      color: var(--muted);
      font-size: 12px;
      line-height: 1.35;
      overflow-wrap: anywhere;
    }

    .node-foot {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }

    .status-pill,
    .chip {
      display: inline-flex;
      align-items: center;
      min-height: 24px;
      max-width: 100%;
      padding: 4px 8px;
      border: 1px solid currentColor;
      background: var(--surface);
      color: var(--muted);
      font-size: 12px;
      line-height: 1.1;
      font-weight: 850;
      white-space: nowrap;
    }

    .status-pill::before {
      content: "";
      width: 7px;
      height: 7px;
      margin-right: 6px;
      display: inline-block;
      background: currentColor;
      border: 1px solid currentColor;
    }

    .status-healthy { color: var(--healthy); }
    .status-attention { color: var(--attention); }
    .status-blocked { color: var(--blocked); }
    .status-archived { color: var(--archived); }
    .status-missing { color: var(--blocked); }

    .chip {
      color: var(--accent);
      background: rgba(40, 102, 93, .08);
      border-color: rgba(40, 102, 93, .35);
      white-space: normal;
      overflow-wrap: anywhere;
    }

    .route-edge {
      fill: none;
      stroke: rgba(32, 33, 29, .22);
      stroke-width: 1.5;
      vector-effect: non-scaling-stroke;
    }

    .route-edge.active {
      stroke: var(--focus);
      stroke-width: 3;
    }

    .route-edge.dimmed {
      stroke: rgba(32, 33, 29, .075);
    }

    .mobile-routes {
      display: none;
      padding: 12px;
      gap: 10px;
      background: var(--surface);
    }

    .route-card {
      width: 100%;
      display: grid;
      gap: 8px;
      padding: 12px;
      text-align: left;
      color: var(--ink);
      background: var(--surface);
      border: 1px solid var(--line);
      cursor: pointer;
    }

    .route-card.selected {
      border-color: var(--focus);
      box-shadow: 0 0 0 3px rgba(31, 95, 120, .16);
    }

    .route-card span {
      color: var(--muted);
      font-size: 12px;
      line-height: 1.4;
      overflow-wrap: anywhere;
    }

    .matrix-wrap,
    .timeline-wrap {
      display: none;
      padding: 14px;
      overflow-x: auto;
      background: var(--surface);
    }

    .matrix {
      width: 100%;
      min-width: 780px;
      border-collapse: collapse;
      font-size: 12px;
    }

    .matrix th,
    .matrix td {
      border: 1px solid var(--line);
      padding: 9px;
      text-align: left;
      vertical-align: top;
    }

    .matrix th {
      color: var(--muted);
      background: var(--surface-2);
      font-size: 11px;
      text-transform: uppercase;
    }

    .matrix .hit {
      background: rgba(40, 102, 93, .09);
      font-weight: 850;
    }

    .timeline-list {
      display: grid;
      gap: 10px;
    }

    .timeline-item {
      display: grid;
      grid-template-columns: 96px minmax(0, 1fr);
      gap: 12px;
      padding: 12px;
      border: 1px solid var(--line);
      background: var(--surface);
    }

    .timeline-item b {
      font-size: 13px;
    }

    .timeline-item p {
      margin: 4px 0 0;
      color: var(--muted);
      font-size: 12px;
      line-height: 1.45;
      overflow-wrap: anywhere;
    }

    .secondary-list {
      display: grid;
      gap: 10px;
      padding: 14px;
      background: var(--surface);
    }

    .secondary-item {
      min-width: 0;
      padding: 12px;
      display: grid;
      gap: 7px;
      text-align: left;
      color: var(--ink);
      border: 1px dashed var(--line-strong);
      background: rgba(239, 237, 228, .68);
      cursor: pointer;
    }

    .secondary-item.selected {
      border-style: solid;
      border-color: var(--attention);
      box-shadow: 0 0 0 3px rgba(148, 96, 23, .14);
    }

    .secondary-item b {
      overflow-wrap: anywhere;
      font-size: 13px;
    }

    .secondary-item span {
      color: var(--muted);
      font-size: 12px;
      line-height: 1.4;
      overflow-wrap: anywhere;
    }

    .side {
      position: sticky;
      top: 92px;
      align-self: start;
    }

    .detail-body,
    .action-body {
      padding: 15px;
      display: grid;
      gap: 12px;
      min-width: 0;
    }

    .detail-heading {
      display: grid;
      gap: 8px;
      min-width: 0;
    }

    .detail-heading h3 {
      margin: 0;
      font-size: 22px;
      line-height: 1.1;
      overflow-wrap: anywhere;
    }

    .detail-heading p {
      margin: 0;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.45;
      overflow-wrap: anywhere;
    }

    .evidence-block {
      min-width: 0;
      padding: 12px;
      border: 1px solid var(--line);
      background: var(--surface-2);
    }

    .evidence-block h4 {
      margin: 0 0 8px;
      color: var(--muted);
      font-size: 12px;
      text-transform: uppercase;
    }

    .field-grid {
      display: grid;
      gap: 6px;
    }

    .field-row {
      display: grid;
      grid-template-columns: 112px minmax(0, 1fr);
      gap: 8px;
      align-items: start;
      font-size: 12px;
      line-height: 1.35;
    }

    .field-row b {
      color: var(--muted);
      font-family: var(--mono);
      font-weight: 700;
      overflow-wrap: anywhere;
    }

    .field-row span {
      overflow-wrap: anywhere;
    }

    .evidence-list {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin: 0;
      padding: 0;
      list-style: none;
    }

    .evidence-list li,
    .copy-value {
      min-width: 0;
      padding: 6px 8px;
      border: 1px solid var(--line);
      background: var(--surface);
      font-size: 12px;
      line-height: 1.35;
      overflow-wrap: anywhere;
    }

    .copy-value {
      font-family: var(--mono);
    }

    .copy-row {
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 8px;
    }

    .btn {
      min-height: 38px;
      padding: 0 12px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      border: 1px solid var(--ink);
      background: var(--ink);
      color: var(--surface);
      cursor: pointer;
      font-size: 12px;
      font-weight: 850;
      text-transform: uppercase;
      white-space: nowrap;
    }

    .btn:hover {
      background: var(--focus);
      border-color: var(--focus);
    }

    .btn.secondary {
      color: var(--ink);
      background: var(--surface);
      border-color: var(--line);
    }

    .btn.secondary:hover {
      border-color: var(--ink);
      background: var(--surface-2);
    }

    .audit-entry {
      display: grid;
      gap: 8px;
      padding: 12px;
      border: 1px solid var(--line);
      background: var(--surface);
    }

    .toast {
      position: fixed;
      right: 22px;
      bottom: 22px;
      z-index: 20;
      padding: 10px 12px;
      color: var(--surface);
      background: var(--ink);
      box-shadow: var(--shadow);
      font-size: 13px;
      opacity: 0;
      transform: translateY(16px);
      pointer-events: none;
      transition: opacity .18s ease, transform .18s ease;
    }

    .toast.show {
      opacity: 1;
      transform: translateY(0);
    }

    @media (max-width: 1240px) {
      .summary-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }

      .summary {
        grid-column: 1 / -1;
      }

      .content {
        grid-template-columns: minmax(0, 1fr);
      }

      .side {
        position: static;
        grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
      }
    }

    @media (max-width: 860px) {
      .app {
        grid-template-columns: 1fr;
      }

      .rail {
        display: none;
      }

      .topbar {
        grid-template-columns: 1fr;
        padding: 15px;
      }

      h1 {
        font-size: 28px;
      }

      .toolbar {
        justify-items: stretch;
      }

      .content {
        padding: 14px;
        gap: 14px;
      }

      .summary-grid {
        grid-template-columns: 1fr 1fr;
      }

      .summary,
      .metric {
        min-height: auto;
      }

      .map-stage,
      .map-svg,
      .map-lanes {
        display: none;
      }

      .map-wrap {
        min-height: auto;
      }

      .context-band {
        grid-template-columns: 1fr;
      }

      .mobile-routes {
        display: grid;
      }

      .side {
        grid-template-columns: 1fr;
      }

      .copy-row,
      .field-row {
        grid-template-columns: 1fr;
      }

      .panel-head {
        flex-direction: column;
      }
    }

    @media (max-width: 540px) {
      .summary-grid {
        grid-template-columns: 1fr;
      }

      h1 {
        font-size: 24px;
      }

      .mode-switch {
        width: 100%;
      }

      .mode-switch button {
        flex: 1;
      }

      .timeline-item {
        grid-template-columns: 1fr;
      }
    }
  </style>
</head>
<body>
  <div class="app">
    <aside class="rail" aria-label="Project Hub navigation">
      <div class="mark" aria-label="Agent Workflow Hub">AW</div>
      <button class="active" type="button" title="Project Hub">H</button>
      <button type="button" title="Tasks">T</button>
      <button type="button" title="Environments">E</button>
      <button type="button" title="Audit">A</button>
    </aside>

    <div class="shell">
      <header class="topbar">
        <div>
          <p id="dashboardEyebrow" class="eyebrow">Project Hub / V3.4 Static Dashboard</p>
          <h1 id="projectTitle"></h1>
          <p id="projectSubtitle" class="subtitle"></p>
        </div>
        <div class="toolbar">
          <input id="search" class="search" type="search" placeholder="筛选 taskId / branch / environment / thread role / status" aria-label="筛选项目关系">
          <div class="mode-switch" aria-label="视图切换">
            <button id="mapMode" class="active" type="button">关系图 / Map</button>
            <button id="matrixMode" type="button">矩阵 / Matrix</button>
            <button id="timelineMode" type="button">时间线 / Activity</button>
          </div>
          <div class="mode-switch" aria-label="Language">
            <button id="zhMode" class="active" type="button">中文</button>
            <button id="enMode" type="button">English</button>
          </div>
        </div>
      </header>

      <main class="content">
        <section class="workspace" aria-label="Project Hub dashboard">
          <div id="summaryGrid" class="summary-grid"></div>

          <section class="panel" aria-labelledby="mapTitle">
            <div class="panel-head">
              <div>
                <p id="mapEyebrow" class="eyebrow">关系图 / Map</p>
                <h2 id="mapTitle">Task -> Thread -> Environment</h2>
              </div>
              <span id="mapNote" class="chip">Project 是页面上下文，dependency 不进入 ownership 图</span>
            </div>
            <div id="mapView" class="map-wrap">
              <div id="contextBand" class="context-band"></div>
              <div class="map-stage">
                <svg id="mapSvg" class="map-svg" aria-hidden="true"></svg>
                <div class="map-lanes">
                  <div class="lane">
                    <div class="lane-title"><span id="taskLaneTitle">Task</span><span id="taskCount"></span></div>
                    <div id="taskLane" class="node-stack"></div>
                  </div>
                  <div class="lane">
                    <div class="lane-title"><span id="threadLaneTitle">Thread</span><span id="threadCount"></span></div>
                    <div id="threadLane" class="node-stack"></div>
                  </div>
                  <div class="lane">
                    <div class="lane-title"><span id="environmentLaneTitle">Environment</span><span id="worktreeCount"></span></div>
                    <div id="worktreeLane" class="node-stack"></div>
                  </div>
                </div>
              </div>
              <div id="mobileRoutes" class="mobile-routes"></div>
            </div>
            <div id="matrixView" class="matrix-wrap" aria-label="Relationship matrix"></div>
            <div id="timelineView" class="timeline-wrap" aria-label="Timeline secondary view"></div>
          </section>

          <section class="panel" aria-labelledby="secondaryTitle">
            <div class="panel-head">
              <div>
                <p id="needsEyebrow" class="eyebrow">Needs Attention / 待处理</p>
                <h2 id="needsTitle">需要处理的事项</h2>
              </div>
            </div>
            <div id="needsList" class="secondary-list"></div>
          </section>

          <section class="panel" aria-labelledby="secondaryTitle">
            <div class="panel-head">
              <div>
                <p id="routingEyebrow" class="eyebrow">Routing Notes / 路由说明</p>
                <h2 id="secondaryTitle">辅助判断，不作为 ownership</h2>
              </div>
            </div>
            <div id="secondaryList" class="secondary-list"></div>
          </section>
        </section>

        <aside class="side" aria-label="Detail and actions">
          <section class="panel">
            <div class="panel-head">
              <div>
                <p id="detailEyebrow" class="eyebrow">Detail / Evidence</p>
                <h2 id="detailTitle" class="detail-title">选中路线</h2>
              </div>
              <span id="detailStatus" class="status-pill"></span>
            </div>
            <div id="detailBody" class="detail-body"></div>
          </section>

          <section class="panel">
            <div class="panel-head">
              <div>
                <p id="legendEyebrow" class="eyebrow">Health Legend / 状态图例</p>
                <h2 id="legendTitle" class="detail-title">状态含义</h2>
              </div>
            </div>
            <div id="legendBody" class="action-body"></div>
          </section>

          <section class="panel">
            <div class="panel-head">
              <div>
                <p id="actionEyebrow" class="eyebrow">Sidecar Actions / 操作</p>
                <h2 id="actionTitle" class="detail-title">可复制动作</h2>
              </div>
            </div>
            <div id="actionBody" class="action-body"></div>
          </section>
        </aside>
      </main>
    </div>
  </div>
  <div id="toast" class="toast" role="status" aria-live="polite"></div>
  <script id="visualPayload" type="application/json">__PAYLOAD__</script>
  <script>
    const payload = JSON.parse(document.getElementById("visualPayload").textContent);
    const rows = payload.taskRows || [];
    const archiveSummary = payload.archiveSummary || {};
    const summaryCounts = payload.summaryCounts || {};
    const recommendedActions = payload.recommendedActions || [];
    const cleanupPrompts = payload.cleanupPrompts || [];
    const needsAttention = payload.needsAttention || [];
    const threadDiscoveryAudit = payload.threadDiscoveryAudit || {};
    const warnings = payload.warnings || [];
    const activeRows = rows.filter((row) => !row.archived);

    const state = {
      selectedKey: "",
      selectedType: "task",
      mode: "map",
      query: "",
      lang: (payload.language || "zh-CN").startsWith("zh") ? "zh-CN" : "en"
    };

    const i18n = {
      "zh-CN": {
        dashboardEyebrow: "Project Hub / V3.4 静态 Dashboard",
        searchPlaceholder: "筛选 taskId / branch / environment / threadRole / status",
        mapTab: "关系图 / Map",
        matrixTab: "矩阵 / Matrix",
        timelineTab: "时间线 / Activity",
        mapEyebrow: "关系图 / Map",
        mapNote: "Project 是页面上下文，dependency 不进入 ownership 图",
        needsEyebrow: "Needs Attention / 待处理",
        needsTitle: "需要处理的事项",
        routingEyebrow: "Routing Notes / 路由说明",
        routingTitle: "辅助判断，不作为 ownership",
        detailEyebrow: "Detail / Evidence",
        detailTitle: "选中路线",
        legendEyebrow: "Health Legend / 状态图例",
        legendTitle: "状态含义",
        actionEyebrow: "Sidecar Actions / 操作",
        actionTitle: "可复制动作",
        summaryText: "Project 是页面上下文。主关系固定为 Task -> Thread -> Environment(optional)；状态、risk、nextStep、validation、handoff 在详情和矩阵中呈现。",
        baseBranch: "Base branch",
        generated: "Generated",
        tasks: "Tasks",
        threads: "Threads",
        environments: "Environments",
        archive: "Archive",
        blocked: "blocked",
        auditErrors: "worktree audit errors",
        discoveryItems: "discovery audit items",
        hiddenByDefault: "hidden by default",
        projectContext: "Project context",
        contextText: "当前视图不把 Project 画成地图节点。Archived 默认隐藏",
        contextHub: "th-project-hub 保留在 audit / routing 区域",
        routeRows: "route rows",
        none: "none",
        projectLevelNone: "project-level / none",
        taskRoute: "task route",
        taskRoutes: "task routes",
        whyStatus: "为什么是这个状态",
        machineFields: "route fields",
        nodeDetail: "详情承载状态证据，不把 risk / validation / handoff 画成主图节点。",
        recommendedAction: "recommended action",
        noSelection: "没有选中项。",
        noActivity: "暂无足够活动记录",
        noActivityDetail: "payload 中没有足够的 sidecar event、handoff、validation 或 archive 时间。",
        noRouting: "暂无路由说明。主图只表达 Task -> Thread -> Environment(optional)。",
        noNeeds: "暂无需要处理的事项。",
        promptSource: "source: sidecar action",
        copy: "Copy",
        copied: "copied",
        copyBlocked: "复制被浏览器阻止，请手动选择文本",
        warnings: "warnings",
        noActions: "没有 payload 提供的可复制 prompt。",
        sidecarOnly: "只显示 sidecar payload 已提供的 action prompt。"
      },
      en: {
        dashboardEyebrow: "Project Hub / V3.4 Static Dashboard",
        searchPlaceholder: "Filter taskId / branch / environment / threadRole / status",
        mapTab: "关系图 / Map",
        matrixTab: "矩阵 / Matrix",
        timelineTab: "时间线 / Activity",
        mapEyebrow: "关系图 / Map",
        mapNote: "Project is page context; dependencies stay outside the ownership graph",
        needsEyebrow: "Needs Attention / 待处理",
        needsTitle: "Items to handle",
        routingEyebrow: "Routing Notes / 路由说明",
        routingTitle: "Supporting evidence, not ownership",
        detailEyebrow: "Detail / Evidence",
        detailTitle: "Selected route",
        legendEyebrow: "Health Legend / 状态图例",
        legendTitle: "Status meaning",
        actionEyebrow: "Sidecar Actions / 操作",
        actionTitle: "Copyable actions",
        summaryText: "Project is page context. The main chain is Task -> Thread -> Environment(optional); status, risk, nextStep, validation, and handoff live in details and matrix.",
        baseBranch: "Base branch",
        generated: "Generated",
        tasks: "Tasks",
        threads: "Threads",
        environments: "Environments",
        archive: "Archive",
        blocked: "blocked",
        auditErrors: "worktree audit errors",
        discoveryItems: "discovery audit items",
        hiddenByDefault: "hidden by default",
        projectContext: "Project context",
        contextText: "Project is not drawn as a map node. Archived tasks are hidden by default",
        contextHub: "th-project-hub stays in audit / routing areas",
        routeRows: "route rows",
        none: "none",
        projectLevelNone: "project-level / none",
        taskRoute: "task route",
        taskRoutes: "task routes",
        whyStatus: "Why this status",
        machineFields: "route fields",
        nodeDetail: "Details carry evidence; risk / validation / handoff are not graph nodes.",
        recommendedAction: "recommended action",
        noSelection: "No selection.",
        noActivity: "No activity records yet",
        noActivityDetail: "The payload does not have enough sidecar event, handoff, validation, or archive timestamps.",
        noRouting: "No routing notes. The main graph only expresses Task -> Thread -> Environment(optional).",
        noNeeds: "No needs-attention items.",
        promptSource: "source: sidecar action",
        copy: "Copy",
        copied: "copied",
        copyBlocked: "Clipboard access was blocked; select the text manually.",
        warnings: "warnings",
        noActions: "No copyable prompt was provided by the payload.",
        sidecarOnly: "Only action prompts already provided by the sidecar payload are shown."
      }
    };

    function t(key) {
      return (i18n[state.lang] && i18n[state.lang][key]) || i18n.en[key] || key;
    }

    const graph = buildGraph(activeRows);
    state.selectedKey = graph.tasks[0]?.key || graph.threads[0]?.key || graph.worktrees[0]?.key || "";
    state.selectedType = graph.tasks[0] ? "task" : graph.threads[0] ? "thread" : "worktree";

    function escapeHtml(value) {
      return String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#39;");
    }

    function escapeAttr(value) {
      return escapeHtml(value).replaceAll("`", "&#96;");
    }

    function unique(values) {
      return Array.from(new Set(values.filter((value) => String(value || "").trim()).map(String)));
    }

    function nodeKey(type, value) {
      return `${type}:${value || "unknown"}`;
    }

    function rowTaskKey(row, index) {
      return row.taskId || row.branch || `task-${index + 1}`;
    }

    function rowThreadKey(row, index) {
      return row.threadId || `${rowTaskKey(row, index)}:${rowThreadLabel(row)}`;
    }

    function rowThreadLabel(row) {
      return row.threadDisplayLabel || row.threadLabel || row.threadRole || "primary-execution";
    }

    function buildGraph(sourceRows) {
      const taskMap = new Map();
      const worktreeMap = new Map();
      const threadMap = new Map();
      const edgeMap = new Map();

      sourceRows.forEach((row, index) => {
        const taskId = rowTaskKey(row, index);
        const threadId = rowThreadKey(row, index);
        const worktreeId = row.worktreePath || "";
        const taskKey = nodeKey("task", taskId);
        const threadKey = nodeKey("thread", threadId);
        const worktreeKey = worktreeId ? nodeKey("environment", worktreeId) : "";

        if (!taskMap.has(taskKey)) {
          taskMap.set(taskKey, {
            type: "task",
            key: taskKey,
            label: taskId,
            health: row.health || "attention",
            status: row.taskStatus || row.health || "missing",
            rows: []
          });
        }
        taskMap.get(taskKey).rows.push(row);

        if (worktreeKey && !worktreeMap.has(worktreeKey)) {
          worktreeMap.set(worktreeKey, {
            type: "environment",
            key: worktreeKey,
            label: shortPath(row.worktreePath),
            health: row.health || "attention",
            status: row.dirty ? "dirty" : row.stale ? "stale" : row.health || "attention",
            rows: []
          });
        }
        if (worktreeKey) worktreeMap.get(worktreeKey).rows.push(row);

        if (!threadMap.has(threadKey)) {
          threadMap.set(threadKey, {
            type: "thread",
            key: threadKey,
            label: rowThreadLabel(row),
            health: row.health || "attention",
            status: row.health || "attention",
            rows: []
          });
        }
        threadMap.get(threadKey).rows.push(row);

        edgeMap.set(`${taskKey}->${threadKey}`, { from: taskKey, to: threadKey });
        if (worktreeKey) {
          edgeMap.set(`${threadKey}->${worktreeKey}`, { from: threadKey, to: worktreeKey });
        }
      });

      return {
        tasks: Array.from(taskMap.values()),
        worktrees: Array.from(worktreeMap.values()),
        threads: Array.from(threadMap.values()),
        nodesByKey: new Map([...taskMap, ...worktreeMap, ...threadMap]),
        edges: Array.from(edgeMap.values())
      };
    }

    function shortPath(value) {
      const text = String(value || "");
      const parts = text.split(/[\\\\/]+/).filter(Boolean);
      return parts.slice(-2).join("/") || text || "project-level / none";
    }

    function statusClass(status) {
      const value = String(status || "missing");
      if (["healthy", "active", "review"].includes(value)) return "status-healthy";
      if (["blocked", "missing"].includes(value)) return "status-blocked";
      if (["archived"].includes(value)) return "status-archived";
      return "status-attention";
    }

    function healthForNode(node) {
      if (!node) return "missing";
      if (node.rows.some((row) => row.health === "blocked")) return "blocked";
      if (node.rows.some((row) => row.health === "attention")) return "attention";
      if (node.rows.some((row) => row.health === "archived")) return "archived";
      return node.health || "healthy";
    }

    function matchesQuery(node) {
      const query = state.query.trim().toLowerCase();
      if (!query) return true;
      return JSON.stringify(node).toLowerCase().includes(query);
    }

    function getRelated(selectedKey) {
      const related = new Set([selectedKey]);
      let changed = true;
      while (changed) {
        changed = false;
        graph.edges.forEach((edge) => {
          if (related.has(edge.from) && !related.has(edge.to)) {
            related.add(edge.to);
            changed = true;
          }
          if (related.has(edge.to) && !related.has(edge.from)) {
            related.add(edge.from);
            changed = true;
          }
        });
      }
      return related;
    }

    function renderSummary() {
      const projectHealth = summaryCounts.blocked ? "blocked" : summaryCounts.attention ? "attention" : "healthy";
      document.getElementById("summaryGrid").innerHTML = `
        <article class="summary">
          <div>
            <h2>${escapeHtml(payload.projectId || "project")}</h2>
            <p>${escapeHtml(t("summaryText"))}</p>
          </div>
          <span class="status-pill ${statusClass(projectHealth)}">${escapeHtml(projectHealth)}</span>
        </article>
        <article class="metric"><span>${escapeHtml(t("tasks"))}</span><b>${summaryCounts.visibleTasks || graph.tasks.length}</b><span>${summaryCounts.blocked || 0} ${escapeHtml(t("blocked"))}</span></article>
        <article class="metric"><span>${escapeHtml(t("environments"))}</span><b>${summaryCounts.visibleEnvironments || graph.worktrees.length}</b><span>${summaryCounts.worktreeAuditErrors || 0} ${escapeHtml(t("auditErrors"))}</span></article>
        <article class="metric"><span>${escapeHtml(t("threads"))}</span><b>${summaryCounts.visibleThreads || graph.threads.length}</b><span>${summaryCounts.threadDiscoveryAttention || 0} ${escapeHtml(t("discoveryItems"))}</span></article>
        <article class="metric"><span>${escapeHtml(t("archive"))}</span><b>${archiveSummary.archivedHidden || 0}</b><span>${escapeHtml(t("hiddenByDefault"))}</span></article>
      `;
    }

    function renderChrome() {
      document.documentElement.lang = state.lang;
      document.getElementById("projectTitle").textContent = payload.projectId || "Agent Workflow Hub";
      document.getElementById("projectSubtitle").textContent = `${t("baseBranch")}: ${payload.baseBranch || "unknown"}. ${t("generated")}: ${payload.generatedAt || "unknown"}.`;
      document.getElementById("dashboardEyebrow").textContent = t("dashboardEyebrow");
      document.getElementById("search").placeholder = t("searchPlaceholder");
      document.getElementById("search").setAttribute("aria-label", t("searchPlaceholder"));
      document.getElementById("mapMode").textContent = t("mapTab");
      document.getElementById("matrixMode").textContent = t("matrixTab");
      document.getElementById("timelineMode").textContent = t("timelineTab");
      document.getElementById("zhMode").classList.toggle("active", state.lang === "zh-CN");
      document.getElementById("enMode").classList.toggle("active", state.lang === "en");
      document.getElementById("mapEyebrow").textContent = t("mapEyebrow");
      document.getElementById("mapNote").textContent = t("mapNote");
      document.getElementById("taskLaneTitle").textContent = "Task";
      document.getElementById("threadLaneTitle").textContent = "Thread";
      document.getElementById("environmentLaneTitle").textContent = "Environment";
      document.getElementById("needsEyebrow").textContent = t("needsEyebrow");
      document.getElementById("needsTitle").textContent = t("needsTitle");
      document.getElementById("routingEyebrow").textContent = t("routingEyebrow");
      document.getElementById("secondaryTitle").textContent = t("routingTitle");
      document.getElementById("detailEyebrow").textContent = t("detailEyebrow");
      document.getElementById("detailTitle").textContent = t("detailTitle");
      document.getElementById("legendEyebrow").textContent = t("legendEyebrow");
      document.getElementById("legendTitle").textContent = t("legendTitle");
      document.getElementById("actionEyebrow").textContent = t("actionEyebrow");
      document.getElementById("actionTitle").textContent = t("actionTitle");
    }

    function renderContextBand() {
      const hidden = archiveSummary.archivedHidden || 0;
      document.getElementById("contextBand").innerHTML = `
        <div>
          <b>${escapeHtml(payload.projectId || "Project")} / ${escapeHtml(t("projectContext"))}</b>
          <span>${escapeHtml(t("contextText"))}${hidden ? `: ${hidden}` : ""}.</span>
        </div>
        <span class="chip">${escapeHtml(t("contextHub"))}</span>
      `;
    }

    function renderLane(nodes, elementId, countId) {
      const related = getRelated(state.selectedKey);
      const visible = nodes.filter(matchesQuery);
      document.getElementById(countId).textContent = String(nodes.length);
      document.getElementById(elementId).innerHTML = visible.map((node) => {
        const selected = state.selectedKey === node.key;
        const isRelated = related.has(node.key);
        const dimmed = related.size > 1 && !selected && !isRelated;
        const health = healthForNode(node);
        const meta = metaForNode(node);
        return `
          <button class="node ${selected ? "selected" : ""} ${isRelated ? "related" : ""} ${dimmed ? "dimmed" : ""}"
            type="button"
            data-key="${escapeAttr(node.key)}"
            data-type="${escapeAttr(node.type)}">
            <span class="node-type">${escapeHtml(node.type)}</span>
            <span class="node-main">
              <span class="node-name">${escapeHtml(node.label)}</span>
              <span class="status-pill ${statusClass(health)}">${escapeHtml(health)}</span>
            </span>
            <span class="node-meta">${escapeHtml(meta)}</span>
            <span class="node-foot">${chipsForNode(node)}</span>
          </button>
        `;
      }).join("");
      document.querySelectorAll(`#${elementId} .node`).forEach((node) => {
        node.addEventListener("click", () => selectNode(node.dataset.type, node.dataset.key));
      });
    }

    function metaForNode(node) {
      if (node.type === "task") {
        const branches = unique(node.rows.map((row) => row.branch));
        return branches.join(" / ") || `${node.rows.length} ${t("routeRows")}`;
      }
      if (node.type === "environment") {
        const path = node.rows[0]?.worktreePath || "";
        return path || t("projectLevelNone");
      }
      const tasks = unique(node.rows.map((row) => row.taskId));
      return `${node.label} / ${tasks.length} ${tasks.length === 1 ? t("taskRoute") : t("taskRoutes")}`;
    }

    function chipsForNode(node) {
      if (node.type === "task") return `<span class="chip">taskId</span><span class="chip">branch</span>`;
      if (node.type === "environment") return `<span class="chip">environment</span><span class="chip">dirty/stale</span>`;
      return `<span class="chip">thread role</span><span class="chip">routing</span>`;
    }

    function renderMap() {
      renderContextBand();
      renderLane(graph.tasks, "taskLane", "taskCount");
      renderLane(graph.threads, "threadLane", "threadCount");
      renderLane(graph.worktrees, "worktreeLane", "worktreeCount");
      requestAnimationFrame(drawEdges);
      renderMobileRoutes();
    }

    function drawEdges() {
      const svg = document.getElementById("mapSvg");
      const stage = document.querySelector(".map-stage");
      if (!svg || !stage || getComputedStyle(stage).display === "none") return;
      const rect = stage.getBoundingClientRect();
      svg.setAttribute("viewBox", `0 0 ${rect.width} ${rect.height}`);
      const related = getRelated(state.selectedKey);
      const nodeMap = Object.fromEntries(Array.from(document.querySelectorAll(".node")).map((node) => [node.dataset.key, node]));
      svg.innerHTML = graph.edges.map((edge) => {
        const from = nodeMap[edge.from];
        const to = nodeMap[edge.to];
        if (!from || !to) return "";
        const a = from.getBoundingClientRect();
        const b = to.getBoundingClientRect();
        const x1 = a.right - rect.left;
        const y1 = a.top + a.height / 2 - rect.top;
        const x2 = b.left - rect.left;
        const y2 = b.top + b.height / 2 - rect.top;
        const bend = Math.max(42, (x2 - x1) * .42);
        const active = related.has(edge.from) && related.has(edge.to);
        const dimmed = related.size > 1 && !active;
        return `<path class="route-edge ${active ? "active" : ""} ${dimmed ? "dimmed" : ""}" d="M ${x1} ${y1} C ${x1 + bend} ${y1}, ${x2 - bend} ${y2}, ${x2} ${y2}"></path>`;
      }).join("");
    }

    function renderMobileRoutes() {
      const related = getRelated(state.selectedKey);
      document.getElementById("mobileRoutes").innerHTML = graph.tasks.filter(matchesQuery).map((node) => {
        const selected = state.selectedKey === node.key;
        const dimmed = related.size > 1 && !related.has(node.key);
        const worktrees = unique(node.rows.map((row) => row.worktreePath || t("projectLevelNone"))).map(shortPath).join(" / ");
        const threads = unique(node.rows.map((row) => row.threadRole || "primary-execution")).join(" / ");
        const threadLabels = unique(node.rows.map(rowThreadLabel)).join(" / ");
        return `
          <button class="route-card ${selected ? "selected" : ""} ${dimmed ? "dimmed" : ""}" type="button" data-type="task" data-key="${escapeAttr(node.key)}">
            <span class="node-main"><b>${escapeHtml(node.label)}</b><span class="status-pill ${statusClass(healthForNode(node))}">${escapeHtml(healthForNode(node))}</span></span>
            <span>threadLabel: ${escapeHtml(threadLabels || t("none"))}</span>
            <span>threadRole: ${escapeHtml(threads || t("none"))}</span>
            <span>environment: ${escapeHtml(worktrees || t("projectLevelNone"))}</span>
          </button>
        `;
      }).join("");
      document.querySelectorAll(".route-card").forEach((node) => {
        node.addEventListener("click", () => selectNode(node.dataset.type, node.dataset.key));
      });
    }

    function renderMatrix() {
      const worktrees = graph.worktrees;
      const threads = graph.threads;
      const rowsHtml = graph.tasks.map((task) => {
        const threadCells = threads.map((thread) => {
          const hit = task.rows.some((row) => thread.rows.includes(row));
          return `<td class="${hit ? "hit" : ""}">${hit ? escapeHtml(thread.label) : ""}</td>`;
        }).join("");
        const worktreeCells = worktrees.map((worktree) => {
          const hit = task.rows.some((row) => worktree.rows.includes(row));
          return `<td class="${hit ? "hit" : ""}">${hit ? escapeHtml(worktree.label) : ""}</td>`;
        }).join("");
        return `
          <tr>
            <th>${escapeHtml(task.label)}<br><span class="status-pill ${statusClass(healthForNode(task))}">${escapeHtml(healthForNode(task))}</span></th>
            ${threadCells}
            ${worktreeCells}
          </tr>
        `;
      }).join("");
      document.getElementById("matrixView").innerHTML = `
        <table class="matrix">
          <thead>
            <tr>
              <th>taskId</th>
              ${threads.map((thread) => `<th>threadRole<br>${escapeHtml(thread.label)}</th>`).join("")}
              ${worktrees.map((worktree) => `<th>environment<br>${escapeHtml(worktree.label)}</th>`).join("")}
            </tr>
          </thead>
          <tbody>${rowsHtml}</tbody>
        </table>
      `;
    }

    function renderTimeline() {
      const items = payload.activityEvents || [];
      if (!items.length) {
        document.getElementById("timelineView").innerHTML = `
          <div class="timeline-list">
            <div class="timeline-item">
              <span class="chip">${escapeHtml(t("noActivity"))}</span>
              <div><b>${escapeHtml(t("noActivity"))}</b><p>${escapeHtml(t("noActivityDetail"))}</p></div>
            </div>
          </div>
        `;
        return;
      }
      document.getElementById("timelineView").innerHTML = `<div class="timeline-list">${items.map((item) => `
        <div class="timeline-item">
          <span class="chip">${escapeHtml(item.kind || "activity")}</span>
          <div>
            <b>${escapeHtml(item.timestamp || item.title || "activity")}</b>
            <p>${escapeHtml([item.title, item.taskId, item.threadLabel, item.detail].filter(Boolean).join(" / "))}</p>
          </div>
        </div>
      `).join("")}</div>`;
    }

    function actionPromptHtml(prompt, label) {
      if (!prompt) return "";
      return `
        <div class="copy-row">
          <div class="copy-value">${escapeHtml(t("promptSource"))}: ${escapeHtml(prompt)}</div>
          <button class="btn" type="button" data-copy="${escapeAttr(prompt)}" data-label="${escapeAttr(label || t("promptSource"))}">${escapeHtml(t("copy"))}</button>
        </div>
      `;
    }

    function renderNeedsAttention() {
      const items = needsAttention.slice(0, 12);
      document.getElementById("needsList").innerHTML = items.length ? items.map((item) => `
        <div class="secondary-item">
          <span class="status-pill ${statusClass(item.health)}">${escapeHtml(item.health || "attention")}</span>
          <b>${escapeHtml(item.taskId || item.branch || item.threadLabel || item.worktreePath || "needs attention")}</b>
          <span>${escapeHtml(item.reason || "needs review")}</span>
          <span>threadRole: ${escapeHtml(item.threadRole || t("none"))}; threadLabel: ${escapeHtml(item.threadLabel || t("none"))}; environment: ${escapeHtml(item.worktreePath || t("projectLevelNone"))}</span>
        </div>
      `).join("") : `<span class="chip">${escapeHtml(t("noNeeds"))}</span>`;
    }

    function renderSecondary() {
      const actionItems = recommendedActions.map((item, index) => ({
        id: `action-${index}`,
        title: item.taskId || item.branch || item.worktreePath || "recommended action",
        status: item.recommendedActionType || "attention",
        body: item.reason || "recommended action",
        prompt: item.oldThreadBackfillPrompt || item.newExecutionThreadPrompt || ""
      }));
      const cleanupItems = cleanupPrompts.map((item, index) => ({
        id: `cleanup-${index}`,
        title: item.taskId || item.branch || "cleanup prompt",
        status: "attention",
        body: item.reason || "cleanup",
        prompt: item.prompt || ""
      }));
      const discoveryItems = [
        ...(threadDiscoveryAudit.unregisteredCodexThreads || []).map((item, index) => ({
          id: `thread-unregistered-${index}`,
          title: item.codexThreadId || "unregistered Codex thread",
          status: "attention",
          body: item.reason || "seen in Codex storage but not registered in sidecar",
          prompt: (threadDiscoveryAudit.refreshRequests || []).find((request) => request.codexThreadId === item.codexThreadId)?.prompt || ""
        })),
        ...(threadDiscoveryAudit.staleRegisteredThreads || []).map((item, index) => ({
          id: `thread-stale-${index}`,
          title: item.threadLabel || item.taskId || item.codexThreadId || "stale registered thread",
          status: "attention",
          body: item.reason || "Codex thread changed after sidecar registration",
          prompt: (threadDiscoveryAudit.refreshRequests || []).find((request) => request.codexThreadId === item.codexThreadId)?.prompt || ""
        })),
        ...(threadDiscoveryAudit.registeredButNotSeen || []).map((item, index) => ({
          id: `thread-not-seen-${index}`,
          title: item.threadLabel || item.taskId || item.codexThreadId || "registered thread not seen",
          status: "attention",
          body: item.reason || "registered in sidecar but not seen in Codex storage",
          prompt: ""
        }))
      ];
      const items = [...discoveryItems, ...actionItems, ...cleanupItems].slice(0, 12);
      document.getElementById("secondaryList").innerHTML = items.length ? items.map((item) => `
        <div class="secondary-item">
          <span class="status-pill ${statusClass(item.status)}">${escapeHtml(item.status)}</span>
          <b>${escapeHtml(item.title)}</b>
          <span>${escapeHtml(item.body)}</span>
          ${actionPromptHtml(item.prompt, item.title)}
        </div>
      `).join("") : `<span class="chip">${escapeHtml(t("noRouting"))}</span>`;
      document.querySelectorAll("#secondaryList [data-copy]").forEach((button) => {
        button.addEventListener("click", () => copyText(button.dataset.copy, button.dataset.label));
      });
    }

    function selectedNode() {
      return graph.nodesByKey.get(state.selectedKey);
    }

    function fieldRows(fields) {
      return `<div class="field-grid">${fields.map(([key, value]) => `
        <div class="field-row"><b>${escapeHtml(key)}</b><span>${escapeHtml(value || "none")}</span></div>
      `).join("")}</div>`;
    }

    function evidenceBlock(title, content) {
      return `<div class="evidence-block"><h4>${escapeHtml(title)}</h4>${content}</div>`;
    }

    function listBlock(title, values) {
      const items = values.length ? values : ["none"];
      return evidenceBlock(title, `<ul class="evidence-list">${items.map((value) => `<li>${escapeHtml(value)}</li>`).join("")}</ul>`);
    }

    function copyBlock(label, value) {
      return `
        <div class="evidence-block">
          <h4>${escapeHtml(label)}</h4>
          <div class="copy-row">
            <div class="copy-value">${escapeHtml(value)}</div>
            <button class="btn" type="button" data-copy="${escapeAttr(value)}" data-label="${escapeAttr(label)}">${escapeHtml(t("copy"))}</button>
          </div>
        </div>
      `;
    }

    function boolText(value) {
      return value ? "true" : "false";
    }

    function statusReasonsForRows(rows) {
      const reasons = [];
      if (rows.some((row) => row.taskStatus === "blocked")) reasons.push("taskStatus=blocked");
      if (rows.some((row) => row.blocker)) reasons.push("blocker");
      if (rows.some((row) => row.stale)) reasons.push("stale");
      if (rows.some((row) => row.dirty)) reasons.push("dirty worktree");
      if (rows.some((row) => !row.handoffAvailable)) reasons.push("missing handoff");
      if (rows.some((row) => !row.validationPresent)) reasons.push("missing validation");
      if (rows.some((row) => !row.safetyRulesPresent)) reasons.push("missing safety");
      if (rows.some((row) => row.routingNeedsReview)) reasons.push("routing needs review");
      if (rows.some((row) => row.recommendedAction)) reasons.push("recommended action");
      if (!reasons.length) reasons.push("all required evidence is present");
      return unique(reasons);
    }

    function renderDetail() {
      const node = selectedNode();
      const health = healthForNode(node);
      const status = document.getElementById("detailStatus");
      status.className = `status-pill ${statusClass(health)}`;
      status.textContent = health;
      if (!node) {
        document.getElementById("detailBody").innerHTML = `<p class="subtitle">${escapeHtml(t("noSelection"))}</p>`;
        return;
      }
      const branches = unique(node.rows.map((row) => row.branch));
      const worktreePaths = unique(node.rows.map((row) => row.worktreePath || t("projectLevelNone")));
      const threadRoles = unique(node.rows.map((row) => row.threadRole));
      const threadLabels = unique(node.rows.map((row) => row.threadLabel));
      const threadDisplayLabels = unique(node.rows.map(rowThreadLabel));
      const nextSteps = unique(node.rows.map((row) => row.nextStep));
      const blockers = unique(node.rows.map((row) => row.blocker));
      const actions = unique(node.rows.map((row) => row.recommendedAction));
      const dirty = node.rows.some((row) => row.dirty);
      const stale = node.rows.some((row) => row.stale);
      const handoff = node.rows.every((row) => row.handoffAvailable);
      const validation = node.rows.every((row) => row.validationPresent);
      const safety = node.rows.every((row) => row.safetyRulesPresent);
      document.getElementById("detailBody").innerHTML = `
        <div class="detail-heading">
          <h3>${escapeHtml(node.label)}</h3>
          <p>${escapeHtml(node.type)} selection. ${escapeHtml(t("nodeDetail"))}</p>
        </div>
        ${listBlock(t("whyStatus"), statusReasonsForRows(node.rows))}
        ${evidenceBlock(t("machineFields"), fieldRows([
          ["taskId", unique(node.rows.map((row) => row.taskId)).join(" / ")],
          ["branch", branches.join(" / ")],
          ["worktreePath", worktreePaths.join(" / ")],
          ["threadRole", threadRoles.join(" / ")],
          ["threadLabel", threadLabels.join(" / ") || threadDisplayLabels.join(" / ")],
          ["codexThreadId", unique(node.rows.map((row) => row.codexThreadId)).join(" / ")],
          ["dirty/stale", `dirty=${boolText(dirty)}, stale=${boolText(stale)}`],
          ["handoff", boolText(handoff)],
          ["validation", boolText(validation)],
          ["safety rules", boolText(safety)]
        ]))}
        ${listBlock("nextStep", nextSteps)}
        ${listBlock("blocker", blockers)}
        ${listBlock(t("recommendedAction"), actions)}
      `;
    }

    function renderLegend() {
      const legend = payload.legend || {};
      const fallback = {
        healthy: "handoff, validation, safety rules, clean worktree, current snapshot, and no blocker",
        attention: "dirty worktree, routing review, missing alias, or recommended action",
        blocked: "blocked status, blocker, stale snapshot, or missing handoff/validation/safety rules",
        archived: "archived sidecar task"
      };
      const items = ["healthy", "attention", "blocked", "archived"].map((key) => ({
        key,
        text: legend[key] || fallback[key]
      }));
      document.getElementById("legendBody").innerHTML = items.map((item) => `
        <div class="audit-entry">
          <span class="status-pill ${statusClass(item.key)}">${escapeHtml(item.key)}</span>
          <span class="subtitle">${escapeHtml(item.text)}</span>
        </div>
      `).join("");
    }

    function collectSidecarPrompts() {
      const prompts = [];
      recommendedActions.forEach((item, index) => {
        const prompt = item.oldThreadBackfillPrompt || item.newExecutionThreadPrompt || "";
        if (prompt) prompts.push({ id: `recommended-${index}`, title: item.taskId || item.branch || item.recommendedActionType || "recommended action", prompt });
      });
      cleanupPrompts.forEach((item, index) => {
        if (item.prompt) prompts.push({ id: `cleanup-${index}`, title: item.taskId || item.branch || "cleanup prompt", prompt: item.prompt });
      });
      (threadDiscoveryAudit.refreshRequests || []).forEach((item, index) => {
        if (item.prompt) prompts.push({ id: `refresh-${index}`, title: item.threadLabel || item.taskId || item.codexThreadId || "thread refresh", prompt: item.prompt });
      });
      return prompts.slice(0, 8);
    }

    function renderActions() {
      const prompts = collectSidecarPrompts();
      document.getElementById("actionBody").innerHTML = `
        <div class="audit-entry">
          <span class="status-pill status-attention">sidecar action</span>
          <b>${escapeHtml(t("actionTitle"))}</b>
          <span class="subtitle">${escapeHtml(t("sidecarOnly"))}</span>
        </div>
        ${prompts.length ? prompts.map((item) => copyBlock(`${t("promptSource")} / ${item.title}`, item.prompt)).join("") : `<span class="chip">${escapeHtml(t("noActions"))}</span>`}
        ${warnings.length ? listBlock(t("warnings"), warnings) : ""}
      `;
      document.querySelectorAll("#actionBody [data-copy]").forEach((button) => {
        button.addEventListener("click", () => copyText(button.dataset.copy, button.dataset.label));
      });
    }

    async function copyText(text, label) {
      try {
        await navigator.clipboard.writeText(text);
        showToast(`${label} ${t("copied")}`);
      } catch (error) {
        showToast(t("copyBlocked"));
      }
    }

    function showToast(message) {
      const toast = document.getElementById("toast");
      toast.textContent = message;
      toast.classList.add("show");
      clearTimeout(showToast.timer);
      showToast.timer = setTimeout(() => toast.classList.remove("show"), 1800);
    }

    function selectNode(type, key) {
      state.selectedType = type;
      state.selectedKey = key;
      renderAll();
    }

    function setMode(mode) {
      state.mode = mode;
      document.getElementById("mapMode").classList.toggle("active", mode === "map");
      document.getElementById("matrixMode").classList.toggle("active", mode === "matrix");
      document.getElementById("timelineMode").classList.toggle("active", mode === "timeline");
      document.getElementById("mapView").style.display = mode === "map" ? "block" : "none";
      document.getElementById("matrixView").style.display = mode === "matrix" ? "block" : "none";
      document.getElementById("timelineView").style.display = mode === "timeline" ? "block" : "none";
      if (mode === "map") requestAnimationFrame(drawEdges);
    }

    function renderAll() {
      renderChrome();
      renderSummary();
      renderMap();
      renderMatrix();
      renderTimeline();
      renderNeedsAttention();
      renderSecondary();
      renderDetail();
      renderLegend();
      renderActions();
      setMode(state.mode);
    }

    document.getElementById("search").addEventListener("input", (event) => {
      state.query = event.target.value;
      renderMap();
    });
    document.getElementById("mapMode").addEventListener("click", () => setMode("map"));
    document.getElementById("matrixMode").addEventListener("click", () => setMode("matrix"));
    document.getElementById("timelineMode").addEventListener("click", () => setMode("timeline"));
    document.getElementById("zhMode").addEventListener("click", () => {
      state.lang = "zh-CN";
      renderAll();
    });
    document.getElementById("enMode").addEventListener("click", () => {
      state.lang = "en";
      renderAll();
    });
    window.addEventListener("resize", () => requestAnimationFrame(drawEdges));
    renderAll();
  </script>
</body>
</html>
"""
    return html.replace("__PAYLOAD__", data)

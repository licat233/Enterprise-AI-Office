# ARMOR Enterprise AI Office

企业 AI 办公系统的产品设计、总体架构与长期运维规范。

本仓库的定位是**设计基线**，用于明确 ARMOR Enterprise AI Office 的系统边界、组件职责、安全模型、用户体验方向和未来实施规范；它不是当前阶段的生产代码仓库，也不代表系统已经完成部署。

## 项目定位

ARMOR Enterprise AI Office 旨在设计一个统一的企业 AI 工作入口，使员工能够：

```text
提出工作问题
    ↓
AI Agent 理解任务
    ↓
查询企业知识
    ↓
调用适当工具
    ↓
必要时执行任务
    ↓
返回可追溯的结果
```

第一版优先建立稳定、可治理、可演进的基础架构，再根据真实业务使用情况持续迭代。

## v1 核心架构

| 能力层 | 设计组件 | 主要职责 |
| --- | --- | --- |
| Knowledge | WeKnora | 企业知识库、解析、检索、重排与引用 |
| Agent Runtime | Hermes Agent | 任务理解、Profile、Skills、Tools、Memory 与 MCP 编排 |
| Employee Access | Open WebUI | 员工 Web 入口、用户、分组与资源权限 |
| Admin Control | hermes-webui | Hermes 管理与控制 |
| Specialized Execution | Codex + Claude Code | 编程、仓库修改、测试与软件工程任务 |
| Task Orchestration | Hermes Kanban | AI 工作任务的持久化编排 |
| Automation | Hermes Cron | 定时任务与自动化执行 |
| Operations | `armor-ai-office` repository | 配置、部署状态、备份、升级和变更记录 |

总体架构采用：

```text
员工入口
  → Hermes Agent / Profiles
  → WeKnora / 企业知识
  → Codex、Claude Code 或其他授权工具
```

## 设计原则

- 以真实业务需求推动版本演进，而不是堆叠技术功能。
- 优先采用成熟的官方能力、官方扩展机制和薄适配层。
- 不为了“先进”增加组件，也不为了“简单”删除必要的生产基础设施。
- 明确 Source of Truth，避免多个系统争夺同一种事实的权威。
- Profile、用户、知识、工具和长期记忆之间必须保持清晰的安全边界。
- 遵循最小权限、默认拒绝和可验证的权限模型。
- 除非有明确需求，不主动 fork 核心上游项目。

## Source of Truth

| 内容 | 权威系统 |
| --- | --- |
| 企业知识 | WeKnora |
| Agent 行为与角色配置 | Hermes Profiles、SOUL、Skills、Tools、MCP |
| 用户身份与 Web 权限 | Open WebUI |
| AI 工作任务状态 | Hermes Kanban |
| 实际部署状态与运维记录 | `armor-ai-office` repository、`DEPLOYMENT-STATE.md` |
| 现有 ARMOR Memory | 独立运行，v1 不自动同步、不双写 |

## 当前设计文档

- [ARMOR Enterprise AI Office v1：总体架构、部署蓝图与长期运维规范](<ARMOR Enterprise AI Office v1 — 总体架构、部署蓝图与长期运维规范.md>)

该文档定义 v1 的技术选型、六层职责模型、Profile 体系、知识库集成、权限与记忆隔离、部署顺序、验收标准、备份恢复和长期运维规范。

## 当前阶段

| 项目 | 状态 |
| --- | --- |
| v1 总体架构 | `approved-design` |
| 产品与用户场景设计 | 持续完善 |
| 信息架构与交互流程 | 待设计 |
| MVP 范围与优先级 | 待确定 |
| 生产部署 | 不属于当前设计阶段 |

后续设计工作将重点完善：

1. 目标用户、部门角色与核心工作场景
2. 员工端与管理端的信息架构
3. AI Agent 交互流程和异常处理流程
4. MVP 功能边界与版本路线图
5. 权限、审计、安全和治理模型
6. 设计决策记录与可验证的验收指标

## 仓库边界

本仓库用于沉淀：

- 产品与系统设计
- 架构决策
- 组件职责与集成边界
- 部署与运维蓝图
- 安全、权限与治理规范
- 验收标准和长期演进规则

除非另有明确说明，后续实施代码、基础设施配置和生产部署应在独立的实施仓库或明确的实施阶段中进行。

## 变更原则

涉及以下内容的变更，需要单独记录并进行架构评审：

- 核心组件替换
- Source of Truth 调整
- 用户、Profile 或工具权限边界调整
- 知识与记忆隔离策略调整
- 生产部署模型调整

实现细节可以随上游版本变化进行兼容调整，但不得未经评审改变既定的架构意图和安全边界。

# xclabel 新功能设计文档

## 1. 项目现状

xclabel 是一款开源的样本管理与模型训练平台，支持多人协作。
现阶段主要功能包括：
- 样本导入与管理
- 样本标注
- 模型训练、测试与管理
- 文件存储访问

项目基于 Python+Django 开发，默认使用 SQLite 存储。

### 1.1 现有数据模型

- `Task`：描述标注任务及其元数据（名称、类型、标签数量等）。
- `TaskSample`：任务样本及标注信息。
- `TaskTrain`：训练任务及运行状态。
- `TaskTrainTest`：训练模型的测试记录。

### 1.2 主要接口

| 功能 | 接口路径 |
|------|----------|
| 用户登录 | `POST /login` |
| 用户管理 | `/user/index`, `/user/add`, `/user/edit`, `/user/postDel` |
| 任务管理 | `/task/index`, `/task/add`, `/task/edit`, `/task/sync`, `/task/postDel` |
| 样本管理 | `/sample/index`, `/sample/getInfo`, `/sample/postSaveAnnotation`, `/sample/postDelAnnotation`, `/sample/getIndex`, `/sample/postAdd`, `/sample/postDel` |
| 训练管理 | `/train/index`, `/train/add`, `/train/manage`, `/train/postDel`, `/train/postTaskCreateDatasets`, `/train/postTaskStartTrain`, `/train/postTaskStopTrain`, `/train/getTrainLog` |
| 模型测试 | `/trainTest/postAdd`, `/trainTest/postDel`, `/trainTest/getIndex` |
| 文件存储 | `/storage/download`, `/storage/access` |

## 2. 新功能需求

1. **模型推理能力**：在现有标注功能基础上，提供模型推理（Inference）服务。
2. **多大模型接入**：支持 DeepSeek API、OpenAI API、火山引擎 API、vLLM、Ollama 以及阿里云百炼平台 API，允许通过配置选择使用的模型服务。
3. **多模态能力**：用户可选择接入的大模型进行文本对话、图片生成、视频生成、图像/视频分析等任务。
4. **大模型 Agent**：引入 Agent 概念，支持聊天 Agent、工作流 Agent 等，参考 MaxKB 与 Dify 的实现。
5. **前端重构**：采用 `Vue3 + Vite + Element Plus` 重写前端界面。
6. **自动标注与调优**：在现有标注模块上提供自动标注功能，可结合大模型以及 YOLO、DINO 等视觉模型，对标准图片、视频、文本等多模态数据进行标注，并对标注流程进行优化。

## 3. 设计方案

### 3.1 技术架构

- **后端**：继续使用 Django，新增 `llm` 应用负责大模型相关逻辑。
- **前端**：使用 Vue3/Vite/Element Plus 独立构建，前后端通过 RESTful API 交互。
- **存储**：保留现有 SQLite/MySQL 选项，新增与大模型相关的配置表。
- **异步任务**：可结合 Celery 或 Django-Q 处理耗时推理与自动标注任务。

### 3.2 模型推理与大模型接入

#### 3.2.1 Provider 抽象

设计统一的 `LLMProvider` 抽象类，定义：
- `chat(messages, model, **kwargs)`
- `generate_image(prompt, **kwargs)`
- `generate_video(prompt, **kwargs)`
- `analyze_media(file, task, **kwargs)`

不同厂商实现各自的 Provider：`OpenAIProvider`、`DeepSeekProvider`、`VolcanoProvider`、`VLLMProvider`、`OllamaProvider`、`BailianProvider`。

#### 3.2.2 配置

新增 `llm_provider` 配置表，包含：
- `name`、`type`、`base_url`、`api_key`、`extra` 等字段。
支持在管理界面增加/编辑/禁用 Provider。

#### 3.2.3 API 设计

| 功能 | 方法与路径 | 请求参数 | 响应 |
|------|------------|----------|------|
| 文本对话 | `POST /api/llm/chat` | `provider_id`, `model`, `messages` | 模型回复内容 |
| 图片生成 | `POST /api/llm/image` | `provider_id`, `model`, `prompt`, `size` | 图片 URL/数据 |
| 视频生成 | `POST /api/llm/video` | `provider_id`, `model`, `prompt`, `duration` | 视频 URL/数据 |
| 媒体分析 | `POST /api/llm/analyze` | `provider_id`, `model`, `task`, `file` | 分析结果 |

所有接口均支持可选的 `stream` 参数用于流式输出。

### 3.3 Agent 体系

- **Agent 定义**：在数据库中新增 `Agent` 表，记录 Agent 类型（聊天/工作流）、使用的 Provider/模型、工具链配置等。
- **聊天 Agent**：维护对话上下文，可结合知识库（参考 MaxKB）。
- **工作流 Agent**：支持节点式流程，节点可调用工具（外部 API、脚本等）。
- **接口**：
  - `POST /api/agent/chat`：与指定聊天 Agent 交互。
  - `POST /api/agent/workflow/execute`：触发工作流 Agent。

### 3.4 自动标注

- 提供 `POST /api/auto_label/start` 接口，接收任务编号、待标注样本集合及所用模型。
- 根据样本类型自动选择模型：
  - 文本样本可调用大语言模型生成标签或摘要；
  - 图片/视频样本可调用目标检测、分割模型（如 YOLO、DINO 等）生成边界框或语义标签；
  - 允许接入第三方模型服务以扩展能力。
- 后端触发异步任务执行推理，将标注结果写入 `TaskSample.annotation_*` 字段，并记录使用的模型与参数。
- 前端可通过 `GET /api/auto_label/progress` 接口查询自动标注进度，支持人工校正和重新标注。

### 3.5 前端方案

- 使用 `Vue3 + Vite + Element Plus` 重新构建 SPA：
  - 登录与用户管理
  - 任务、样本、标注界面
  - 模型推理与 Agent 交互界面
  - Provider 与 Agent 配置界面
- 通过 axios 调用后端 RESTful API。

### 3.6 权限与安全

- 用户角色管理：管理员、标注员、访客等。
- Provider/Agent 的 API Key 采用加密存储。
- 接口鉴权可继续使用 Django session / JWT。

## 4. 开发计划

1. **阶段一：基础架构**
   - 新增 `llm` 应用和 Provider 抽象。
   - 实现 OpenAI/DeepSeek/火山引擎等 Provider。
   - 编写 `/api/llm/*` 接口。
2. **阶段二：Agent 支持**
   - 设计数据库与 API。
   - 实现聊天 Agent、工作流 Agent。
3. **阶段三：自动标注模块**
   - 接入指定模型进行样本自动标注。
   - 提供任务进度管理。
4. **阶段四：前端重构**
   - 基于 Vue3/Vite/Element Plus 开发 SPA。
   - 对接新的后端接口。
5. **阶段五：优化与文档**
   - 完善测试、部署脚本、使用文档。


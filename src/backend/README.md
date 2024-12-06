# Credit Insight Backend

Credit Insight 的后端服务是整个系统的核心，负责数据处理、业务逻辑和与前端的交互。它基于现代 Python 架构设计，模块化清晰、职责明确，能够支持高效开发与扩展。

## 项目结构

```
backend/
├── analyzer/           # 风险评估模块
├── api/                # API 路由层
├── collector/          # 数据采集模块
├── database/           # 数据访问层
├── services/           # 服务层，封装业务逻辑
├── utils/              # 工具库
├── main.py             # 后端主入口
└── README.md           # 说明
```

### **模块功能介绍**

#### **1. `analyzer/` - 风险评估模型**
- **作用：**
  包含用于分析和预测的核心算法模块，支持风险评估、信用分数计算等复杂逻辑。

---

#### **2. `api/` - API 路由层**
- **作用：**
  提供 RESTful API，用于处理前端的 HTTP 请求，负责将请求转发给服务层并返回响应。
- **主要文件：**
  - `accounts.py`: 用户账户相关接口。
  - `admin.py`: 管理员接口。
  - `monitor.py`: 数据监控接口。
  - `reports.py`: 报表生成接口。
  - `static.py`: 静态文件处理（托管前端构建资源）。

---

#### **3. `collector/` - 数据采集器**
- **作用：**
  负责从外部来源抓取和解析数据，如网站、PDF 文件等。
- **主要文件：**
  - `main.py`: 数据采集主程序。
  - `decaptcha.py`: 验证码处理。
  - `scrape_data.py`: 数据爬取逻辑。
  - `scrape_pdf.py`: PDF 清单爬取。
  - `pdf_parser.py`: PDF 清单解析。

---

#### **4. `database/` - 数据访问层**
- **作用：**
  封装数据库操作，包括数据模型定义、数据库连接管理、具体的数据操作。
- **子目录与主要文件：**
  - **`link.py`**: 数据库连接管理。
    - 数据库引擎配置和会话管理。
    - 连接字符串和配置加载。
  - **`models/`**: 数据模型定义。
    - `user.py`: 用户模型。
    - `enterprise.py`: 企业模型。
    - `financial_status.py`: 财务状况模型。
    - `credit_report.py`: 信用报告模型。
    - `monitoring_subscription.py`: 监控订阅模型。
    - `decision_report.py`: 决策报告模型。
    - `disclosure_info.py`: 信息披露模型。
    - `overdue_aging_analysis.py`: 逾期账龄分析模型。
  - **`crud/`**: 数据操作封装。
    - `user_crud.py`: 用户数据操作。
    - `enterprise_crud.py`: 企业数据操作。
    - `financialstatus_crud.py`: 财务状况操作。
    - `credit_report_crud.py`: 信用报告操作。
    - `monitoringsubscriptions_crud.py`: 监控订阅操作。
    - `decisionreports_crud.py`: 决策报告操作。
    - `disclosureinfo_crud.py`: 信息披露操作。
    - `overdueaginganalysis_crud.py`: 逾期账龄分析操作。

---

#### **5. `services/` - 服务层**
- **作用：**
  实现核心业务逻辑，作为路由层和数据层之间的桥梁，确保模块职责分离。
- **主要文件：**
  - `accounts.py`: 用户账户管理逻辑。
  - `admin.py`: 管理员控制逻辑。
  - `monitor.py`: 数据监控逻辑。
  - `reports.py`: 数据报告逻辑。
  - `analyzer.py`: 风险评估模型连接器。
  - `collector.py`: 数据采集器连接器。
  - `permissions.py`: 访问权限控制。
  - `maintenance.py`: 系统维护。

---

#### **6. `utils/` - 工具库**
- **作用：**
  提供后端运行所需的通用工具和模块。

---

## 快速开始（此处仅为示例）

### **环境要求**
- Python 3.12。
- 数据库。

### **运行项目**
1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
2. 启动后端服务：
   ```bash
   python main.py
   ```

### **项目目录约定**
- **配置文件：** 位于项目根目录的 `conf` 目录中，包含环境变量和默认配置。
- **日志文件：** 默认存储在项目根目录的 `log` 目录中。

# 🧠 AI Agent Workshops

***13 Feb 2025, University of Wollongong, GiftCity, Gandhinagar***

---

## 📌 Table of Contents

#### **🔹Part 1: Building Blocks – The Augmented LLM**

- **Basic LLM Calls** – Sending requests and processing responses
- **Structured Output** – Formatting responses in structured formats
- **Tool Use** – Integrating external tools with the LLM
- **Retrieval** – Using memory and external sources for better responses

#### 🔹**Part 2: Workflow Patterns for AI Systems**

- **Prompt Chaining** – Structuring multi-step AI tasks
- **Routing** – Directing requests to specialized handlers
- **Parallelization** – Running multiple AI processes simultaneously

#### 🔹Part 3: Introduction to Agentic Framework (CrewAI)

- **CrewAI Framework Step by Step**
- **Agent  :** Finance Agent App

#### 🔹Part 4: Introduction to Agentic Framework(SmolAgent)

- **SmolAgent Framework Step by Step**
- **Agent** : AI News Agent App

---

## 🔄Part 2: Workflow Patterns for AI Systems

### 🏗️ Prompt Chaining

Prompt chaining **breaks down complex AI tasks** into smaller, more manageable steps. Each step **processes** and **validates** the output from the previous step, improving **control and reliability**.

#### 📅 Calendar Assistant Example

```mermaid
graph LR
    A[User Input] --> B[LLM 1: Extract]
    B --> C{Gate Check}
    C -->|Pass| D[LLM 2: Parse Details]
    C -->|Fail| E[Exit]
    D --> F[LLM 3: Generate Confirmation]
    F --> G[Final Output]
```

**📝 Step Breakdown:**

| **Step**                             | **Description**                                                                                                                                   |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **✅ Step 1: Extract & Validate**    | - Detects if input is a valid**calendar request**  <br />- Assigns a **confidence score** <br />- Filters out **irrelevant requests** |
| **✅ Step 2: Parse Details**         | - Extracts structured information (**date, time, participants**) <br />- Converts **natural language** into a structured format             |
| **✅ Step 3: Generate Confirmation** | - Creates a**user-friendly response** <br />- Generates calendar links if necessary                                                               |

---

### 🔀 Routing

Routing is a pattern that directs different types of requests to specialized **handlers**, allowing for **clean separation of concerns** and **optimized processing**.

#### 📅 Calendar Assistant Example

```mermaid
graph LR
    A[User Input] --> B[LLM Router]
    B --> C{Route}
    C -->|New Event| D[New Event Handler]
    C -->|Modify Event| E[Modify Event Handler]
    C -->|Other| F[Exit]
    D --> G[Response]
    E --> G
```

**📝 Step Breakdown:**

| **Component**               | **Description**                                                                                                 |
| --------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| **✅ Router**               | - Classifies requests into**new event** or **modification** <br />- Provides **confidence scoring** |
| **✅ Specialized Handlers** | -**New Event Handler:** Creates calendar events<br />- **Modify Event Handler:** Updates existing events  |

---

### ⚡ Parallelization

Parallelization improves **efficiency** by running multiple LLM calls **simultaneously** to analyze different aspects of a request in parallel.

#### 📅 Calendar Assistant Example

```mermaid
graph LR
    A[User Input] --> B[Calendar Check]
    A --> C[Security Check]
    B --> D{Aggregate}
    C --> D
    D -->|Valid| E[Continue]
    D -->|Invalid| F[Exit]
```

**📝 Step Breakdown:**

| **Component**            | **Description**                                                                                                      |
| ------------------------------ | -------------------------------------------------------------------------------------------------------------------------- |
| **✅ Parallel Checks**   | **- Calendar Validation:** Ensures a valid request <br />**- Security Check** : Screens for prompt injection |
| **✅ Aggregation Layer** | - Merges results from parallel checks<br />- Makes the**final validation decision**                                  |

---

### 🎭 Orchestrator-Workers

The **orchestrator-workers** pattern uses a **central LLM** to dynamically **analyze, coordinate, and synthesize** responses from specialized workers. This is useful for tasks requiring structured content generation.

#### 📝 Blog Writing Example

```mermaid
graph LR
    A[Topic Input] --> B[Orchestrator]
    B --> C[Planning Phase]
    C --> D[Writing Phase]
    D --> E[Review Phase]
    style D fill:#f9f,stroke:#333,stroke-width:2px
```

**📝 Step Breakdown:**

| 🛠️**Orchestrator**                                     | 📝**Planning Phase**                                 | ✍️**Writing Phase**                           | 🔍**Review Phase**                        |
| -------------------------------------------------------------- | ---------------------------------------------------------- | ----------------------------------------------------- | ----------------------------------------------- |
| 🔎 Analyzes the**blog topic** and **requirements** | 📌 Breaks content into**sections**                   | 🏗️ Assigns sections to**specialized writers** | ✅ Evaluates**content flow and cohesion** |
| 🏗️ Generates a**structured content plan**              | 📏 Defines**word count** and **writing style** | 🔗 Maintains**context and consistency**         | ✨ Suggests**improvements**               |
| 🔄 Oversees**content cohesion**                          | -                                                          | -                                                     | 🏆 Produces a**polished final version**   |

---

## 🔄Part 3: Introduction to Agentic Framework 🤖

This section introduces additional architectures for building AI agents, providing a structured overview of their workflows and modular designs.

##### CrewAIAgent

**CrewAI** follows a modular, step-by-step approach that includes:

![](images/CrewAI.png)

**Example:** **Finance Agent App**

![](images/aiagentfinanceanalysis.gif)

> **Workflow**

```mermaid
graph TD
    A[Start] --> B[Initialize Streamlit App]
    B --> C[Set Up API Keys & Load Environment Variables]
    C --> D[User Inputs Company Name]
    D --> E{Start Analysis Button Clicked?}
  
    E -- Yes --> F[Display Progress & Setup Agents]
    F --> G[Create Financial Analyst Agent]
    G --> H[Create Investment Strategy Reviewer Agent]
    H --> I[Initialize Stock Market Scraper Tool]
    I --> J[Define Stock Market Analysis Task]
    J --> K[Define Investment Review Task]
    K --> L[Create Financial Analysis Crew]
  
    L --> M[Run AI Analysis Crew Process]
    M --> N[Generate Financial Report]
    N --> O[Display Final Financial Analysis Report]
  
    E -- No --> P[Wait for User Action]

    style A fill:#ffcc00,stroke:#333,stroke-width:2px
    style O fill:#ffcc00,stroke:#333,stroke-width:2px
    style M fill:#00ccff,stroke:#333,stroke-width:2px
    style J fill:#00ccff,stroke:#333,stroke-width:2px

```

## 🔄Part 4: Introduction to Agentic Framework(SmolAgent)

##### **SmalAgent**

**SmolAgent** provides a live coding guide for building lightweight agents. Key highlights include:

- **Streamlit App:** Running using Colab as the backend server
- **AI News Agent App**

![](images/ainewsagent.gif)

> **Workflow**

```mermaid
graph TD
    A[Start] --> B[Initialize Streamlit App]
    B --> C[Initialize LLM and Search Tool]
    C --> D[User Inputs News Topic]
    D --> E[Set Search Depth and Analysis Type]
    E --> F{Analyze News Button Clicked?}
  
    F -- Yes --> G[Perform DuckDuckGo Search]
    G --> H{Results Found?}
  
    H -- Yes --> I[Create Analysis Prompt]
    I --> J[Generate Analysis Using LLM]
    J --> K[Display Analysis Results]
    K --> L[Log Activity]
  
    H -- No --> M[Show No Results/Error Message]
  
    F -- No --> N[Wait for User Action]
  
    K --> O[Show Tips for Better Results]
    M --> O
    O --> P[End]

    style A fill:#ffcc00,stroke:#333,stroke-width:2px
    style P fill:#ffcc00,stroke:#333,stroke-width:2px
    style G fill:#00ccff,stroke:#333,stroke-width:2px
    style J fill:#00ccff,stroke:#333,stroke-width:2px
```

> **Running live in Colab**

```mermaid
graph TD
    SA[SmolAgent]
    SA --> SC[Step-by-Step Live Coding]
    SC --> S[Streamlit App via Colab]
    SC --> N[AI News Agent App]
```

---

## 🤝 Contributing

Contributions are welcome! To get started:

1. **Fork** the repository
2. **Create a branch** (`feature-new-pattern`)
3. **Commit your changes**
4. **Push to GitHub** and **open a PR**

For detailed guidelines, check [CONTRIBUTING.md](CONTRIBUTING.md).

---

## 📜 License

This project is licensed under the **MIT License** – see [LICENSE](LICENSE) for details.

---

## 📬 Contact

For questions or collaborations, feel free to reach out:

📧 **Email:** ashishpatel.ce.2011@gmail.com

---

_🎯 Happy Coding! 🚀_

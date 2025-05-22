# 🧠💼 IntelliManage - AI-Powered Management Assistant

<div align="center">

![IntelliManage Logo](https://img.shields.io/badge/IntelliManage-AI%20Management-purple?style=for-the-badge&logo=brain&logoColor=white)

**Repository:** `intellimanage-ai-assistant`

*🚀 Streamlining user and project management through intelligent automation*

[![Python](https://img.shields.io/badge/Python-3.12+-blue?style=flat-square&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Framework-green?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![OpenAI](https://img.shields.io/badge/OpenAI-AI%20Powered-orange?style=flat-square&logo=openai)](https://openai.com)

</div>

---

## 🌟 What is IntelliManage?

**IntelliManage** *(Intelligence + Management)* is a revolutionary AI-powered assistant that transforms how organizations handle user and project management. By combining natural language processing with intelligent automation, IntelliManage eliminates the complexity of traditional management systems, supporting both REST API and WebSocket connections for flexible real-time integration.

🎯 **Perfect for:** Team leads, project managers, HR departments, and any organization seeking to automate administrative tasks through conversational AI with real-time capabilities.

---

## ✨ Key Features

<table>
<tr>
<td align="center">

### 🔍 **Smart Query Processing**
Natural language understanding powered by OpenAI Assistant for intuitive interactions

</td>
<td align="center">

### 👥 **User Management**
Create, pause, unpause users with simple voice commands

</td>
</tr>
<tr>
<td align="center">

### 📁 **Project Control**
Seamless project assignment and unassignment capabilities

</td>
<td align="center">

### 🔐 **Secure Authentication**
Enterprise-grade security with comprehensive auth verification

</td>
</tr>
<tr>
<td align="center">

### ⚡ **Dual Connectivity**
Both REST API and WebSocket support for flexible integration

</td>
<td align="center">

### 🔧 **Modular Architecture**
Clean, maintainable codebase designed for easy extension

</td>
</tr>
</table>

---

## 🚀 Quick Start

### 📋 Prerequisites

```bash
# Ensure Python 3.12+ is installed
python --version
```

### 🔧 Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/intellimanage-ai-assistant.git
   cd intellimanage-ai-assistant
   ```

2. **Set Up Virtual Environment**
   ```bash
   python -m venv venv
   
   # Linux/Mac
   source venv/bin/activate
   
   # Windows
   venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   Create a `.env` file in the root directory:
   ```env
   ORGANIZATION=your-organization-name
   OPENAI_KEY=your-openai-api-key
   ```

### 🎬 Launch Application

```bash
uvicorn manage:app --reload
```

🌐 **REST API Documentation:** `http://localhost:8000/docs`
🔄 **WebSocket Connection:** `ws://localhost:8000/manage/`

---

## 🔌 API Reference

### 🎯 REST API Endpoint

#### `POST /manage/`

**Description:** Process natural language management queries via REST API

**Request:**
```json
{
  "user_query": "Create a new user named John Doe"
}
```

**Response Examples:**
```json
// Success (200)
{
  "status": "success",
  "message": "User John Doe created successfully",
  "action_performed": "user_creation"
}

// Authentication Error (401)
{
  "detail": "Authentication failed"
}

// Processing Error (500)
{
  "detail": "Query processing failed"
}
```

### 🔄 WebSocket Endpoint

#### `WebSocket /manage/`

**Description:** Real-time management queries with persistent connection

**Connection Parameters:**
```javascript
// WebSocket connection with query parameters
ws://localhost:8000/manage/?authorization_header=Bearer_token&thread=thread_id
```

**Message Format:**
```json
{
  "user_query": "Pause user account for John Doe"
}
```

**Real-time Response:**
```json
{
  "status": "success",
  "message": "User John Doe paused successfully",
  "action_performed": "user_pause",
  "timestamp": "2025-05-18T10:30:00Z"
}
```

**Benefits of WebSocket:**
- 🔄 **Real-time Communication:** Instant bidirectional messaging
- ⚡ **Low Latency:** Persistent connection eliminates handshake overhead
- 📊 **Live Updates:** Receive status updates and notifications in real-time
- 🔐 **Thread Management:** Maintain conversation context with thread IDs

---

## 🏗️ Architecture Overview

```
User Query → Authentication → AI Processing → Action Execution → Response
```

### 📁 Project Structure

| 📄 File | 🎯 Purpose | 📝 Description |
|---------|-----------|---------------|
| `manage.py` | 🚀 **API Gateway** | FastAPI app initialization and endpoint definition |
| `helper.py` | 🔐 **Security Layer** | Authentication verification and data fetching |
| `assistant.py` | 🧠 **AI Brain** | OpenAI Assistant integration and query processing |
| `assistant_functionality.py` | ⚙️ **Function Registry** | OpenAI function definitions for management tasks |
| `user_management_tools.py` | 🛠️ **Action Executor** | API-based user and project management tools |

---

## 💡 Example Queries

IntelliManage understands natural language commands like:

- 👤 *"Create a new user named Sarah with admin privileges"*
- ⏸️ *"Pause the user account for John Doe"*
- ▶️ *"Reactivate Mary's account"*
- 📁 *"Assign the Phoenix project to the development team"*
- 🔄 *"Remove Alice from the Marketing project"*

---

## 🔒 Security & Best Practices

### 🛡️ Security Features
- ✅ Environment variable protection for sensitive data
- ✅ Comprehensive authentication verification
- ✅ Detailed error logging with user privacy protection
- ✅ Secure API endpoint protection

### 📋 Best Practices
- 🔐 Never commit `.env` files to version control
- 📊 Monitor API usage and implement rate limiting
- 🧪 Write comprehensive tests for all endpoints
- 📝 Keep dependencies updated and secure

---

## 🚀 Extensibility

### 🔧 Adding New Functions

IntelliManage is designed for easy extension:

1. **Define Function** in `assistant_functionality.py`
2. **Implement Logic** in `user_management_tools.py`
3. **Register Handler** in `assistant.py`

### 🔌 Custom API Integration

```python
# Example: Adding custom project management API
def integrate_custom_api():
    # Your custom integration logic here
    pass
```

---

## 🛠️ Built With

<div align="center">

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![WebSocket](https://img.shields.io/badge/WebSocket-Real--time-green?style=for-the-badge&logo=websocket)](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)
[![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai)](https://openai.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)

</div>

---

## 🤝 Contributing

We welcome contributions to make IntelliManage even better!

### 🔄 Contribution Workflow

1. 🍴 **Fork** the repository
2. 🌟 **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. 💻 **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. 📤 **Push** to the branch (`git push origin feature/amazing-feature`)
5. 📝 **Open** a Pull Request

### 🎨 Development Guidelines

- Follow PEP 8 style guidelines
- Write clear, concise commit messages
- Include tests for new features
- Update documentation as needed



*🌟 Built with ❤️ for modern management teams*

### 🔗 Connect With Us
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?style=social&logo=github)](https://github.com/PrimeRoxy)

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=social&logo=linkedin)](https://linkedin.com/in/ismart-vipulray)

</div>

# Portfolio Chatbot System

A sophisticated chatbot system for portfolio websites with message classification, session-based memory, and dynamic UI components.

## 🚀 Features

### Message Classification
- **Projects**: Questions about portfolio projects
- **Skills**: Technical skills and technologies
- **Education**: Academic background and certifications
- **Experience**: Work experience and professional background
- **Achievements**: Awards, recognition, and accomplishments
- **Contact**: Contact information requests
- **Personal**: General personal information
- **Other**: General conversation and greetings

### Dynamic UI Components
- **Text Responses**: Normal conversational chat bubbles
- **Projects List**: Interactive project cards with links and tech stacks
- **Skills Grid**: Categorized skill display with proficiency levels
- **Education Timeline**: Academic history with details
- **Experience Cards**: Work experience with technologies used
- **Contact Info**: Contact details with clickable links

### Memory System
- **Session-based**: Maintains context within chat sessions
- **Automatic Cleanup**: Sessions expire after 1 hour
- **Conversation History**: Remembers previous messages for context

## 🏗️ Architecture

### Backend Pipeline
```
User Message → Classification → Data Retrieval → Response Generation → UI Type Selection
```

1. **Message Intake**: Receives user message and session ID
2. **Classification Chain**: Uses OpenAI GPT-4 to classify message intent
3. **Routing Logic**: Determines response type and data requirements
4. **Data Retrieval**: Fetches relevant portfolio data
5. **Response Generation**: Creates personalized response as Arif Foysal
6. **UI Selection**: Chooses appropriate frontend component type

### Tech Stack
- **Backend**: FastAPI + OpenAI API + Pydantic
- **Frontend**: Nuxt 3 + Vue.js + Tailwind CSS
- **Memory**: In-memory storage (Redis recommended for production)
- **API**: RESTful JSON responses with structured data

## 📚 API Documentation

### Chat Endpoint
```http
POST /chat/
```

**Request Body:**
```json
{
  "message": "Show me all your projects",
  "session_id": "optional-session-id"
}
```

**Response Examples:**

#### Text Response
```json
{
  "type": "text",
  "data": "I'm passionate about building innovative solutions...",
  "session_id": "session_123"
}
```

#### Projects List Response
```json
{
  "type": "projects_list",
  "data": [
    {
      "name": "Skin Disease Detection System",
      "description": "AI-powered mobile application...",
      "technologies": ["Python", "TensorFlow", "Flutter"],
      "link": "https://example.com",
      "github_link": "https://github.com/...",
      "image": "/projects/skin-detection.jpg"
    }
  ],
  "session_id": "session_123"
}
```

#### Skills List Response
```json
{
  "type": "skills_list",
  "data": [
    {
      "category": "Frontend Development",
      "skills": ["React", "Vue.js", "Nuxt.js"],
      "proficiency": "Advanced"
    }
  ],
  "session_id": "session_123"
}
```

### Health Check
```http
GET /chat/health
```

## 🛠️ Setup Instructions

### 1. Backend Setup

#### Install Dependencies
```bash
cd backend/
uv add langchain langchain-openai langchain-community python-dotenv openai
```

#### Environment Variables
Create `.env` file:
```env
OPENAI_API_KEY=your_openai_api_key_here
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

#### Run Backend
```bash
uv run uvicorn main:app --reload
```

### 2. Frontend Integration

#### Install Component
Copy `ChatBot.vue` to your components directory.

#### Usage in Nuxt Page
```vue
<template>
  <div>
    <ChatBot />
  </div>
</template>

<script setup>
// Component will be auto-imported in Nuxt 3
</script>
```

#### Update API URL
In `ChatBot.vue`, update the API base URL:
```javascript
const API_BASE_URL = 'https://your-backend-domain.com'
```

## 🎯 Usage Examples

### Example Queries and Expected Behaviors

1. **"Show me all your projects"**
   - Type: `projects_list`
   - UI: Project cards grid with images, descriptions, tech stacks, and links

2. **"What skills do you have?"**
   - Type: `skills_list`
   - UI: Categorized skill grid with proficiency levels

3. **"Tell me about your skin disease detection project"**
   - Type: `text`
   - Response: Detailed explanation about the specific project

4. **"How can I contact you?"**
   - Type: `contact_info`
   - UI: Contact card with email, LinkedIn, GitHub links

5. **"What's your educational background?"**
   - Type: `education_list`
   - UI: Education timeline with degrees and institutions

6. **"What programming languages did you use for that project?"**
   - Type: `text`
   - Response: Conversational answer referencing previous context

## 🔧 Customization

### Adding New Categories
1. Update `MessageType` enum in `models.py`
2. Add classification logic in `classify_message()`
3. Create data retrieval method in `portfolio_data.py`
4. Add UI component in `ChatBot.vue`

### Modifying Portfolio Data
Edit the data in `services/portfolio_data.py`:
- Update project information
- Add new skills and categories
- Modify education and experience details
- Change contact information

### Customizing Personality
Modify the system prompts in `services/chatbot.py`:
- Update personality traits
- Change response style
- Add domain-specific knowledge
- Adjust conversation tone

## 🚀 Production Deployment

### Environment Setup
1. Set OpenAI API key in production environment
2. Configure CORS origins for your domain
3. Set up Redis for session storage (recommended)
4. Configure logging and monitoring

### Scaling Considerations
- Use Redis for distributed memory storage
- Implement rate limiting for API calls
- Add caching for frequently requested data
- Monitor OpenAI API usage and costs

### Security
- Validate and sanitize all user inputs
- Implement proper error handling
- Use environment variables for sensitive data
- Add authentication if needed for admin features

## 📊 Response Types Summary

| Type | Description | UI Component |
|------|-------------|--------------|
| `text` | Normal conversation | Chat bubble |
| `projects_list` | All projects overview | Project grid |
| `skills_list` | Skills categorized | Skills grid |
| `education_list` | Academic background | Education timeline |
| `experience_list` | Work experience | Experience cards |
| `achievements_list` | Awards and recognition | Achievement list |
| `contact_info` | Contact details | Contact card |

This system provides a flexible foundation for creating engaging, intelligent chatbots that can represent portfolio owners professionally while providing rich, interactive user experiences.

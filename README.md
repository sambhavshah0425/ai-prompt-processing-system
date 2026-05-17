# Project Overview
The AI Prompt Processing System is a complete, scalable backend solution designed to manage, process, and track AI prompt generations. Built with Python, Flask, and MongoDB, the system dynamically injects user inputs into predefined prompt templates, interfaces with AI services (like OpenAI), and safely stores both the requests and responses. The project also features a fully-functional modern "glassmorphism" frontend dashboard to effortlessly test single and batch processing capabilities.

# Features
- **Dynamic Prompt Templates**: Prompts are stored in a NoSQL database with injectable placeholders (e.g., `{{userInput}}`).
- **Single Response Generation**: API endpoint to instantly process a single prompt and receive an AI response.
- **Asynchronous Batch Processing**: Process multiple prompts concurrently using Python's `asyncio` without blocking the main execution flow. 
- **Robust Request/Response History**: Every API call (including batch items) is permanently logged in a MongoDB history collection for audit and review.
- **Frontend Dashboard**: A sleek, responsive user interface built with Vanilla HTML/JS/CSS to interact with all API endpoints seamlessly.
- **Clean Architecture**: Highly modular structure separating Routes, Services, Models, and Configurations.

# Tech Stack
- **Backend Framework**: Python (Flask)
- **Database**: MongoDB (PyMongo)
- **Asynchronous Processing**: `asyncio`
- **Frontend**: Vanilla HTML5, CSS3, JavaScript (Glassmorphism UI)
- **Environment Management**: `python-dotenv`

# Architecture
The application follows a clean, modular pattern separating concerns:
```
Project/
│
├── app.py                # Main Flask application entry point
├── config.py             # Configuration and environment variables
├── requirements.txt      # Project dependencies
├── seed.py               # Database initialization script
├── README.md             # Project documentation
├── .env.example          # Sample environment variables
│
├── database/             # Database connection logic
│   └── mongo.py
├── models/               # MongoDB schema representations
│   ├── history_model.py
│   └── prompt_model.py
├── routes/               # API endpoints
│   └── generate.py
├── services/             # Core business logic
│   ├── ai_service.py     # AI Integration (Mock/OpenAI)
│   ├── history_service.py# Request logging logic
│   └── prompt_service.py # Template injection logic
├── utils/                # Helper functions
│   └── helpers.py        # MongoDB JSON Encoder
│
├── templates/            # Frontend HTML
│   └── index.html
└── static/               # Frontend Assets
    ├── css/
    │   └── styles.css
    └── js/
        └── app.js
```

# MongoDB Collections
1. **prompts**: Stores the base templates for prompt generation.
   - Example Schema: `{ "_id": "Education_Prompt", "template": "You are an expert... {{userInput}}", "createdAt": "timestamp" }`
2. **history**: Logs all requests and AI responses.
   - Example Schema: `{ "_id": ObjectId, "requestType": "single/batch", "userInput": "...", "finalPrompt": "...", "response": "...", "batchId": "optional", "timestamp": "timestamp" }`

# API Endpoints
- `GET /` - Renders the web dashboard.
- `GET /health` - Health check endpoint.
- `GET /history` - Retrieves all stored historical prompts and responses.
- `POST /generate` - Accepts a `userInput`, processes it via the prompt template, and returns a single AI response.
- `POST /generate-batch` - Accepts a list of `inputs`, processes them asynchronously, and returns an ordered list of responses.

# Async Processing
For the batch endpoint (`/generate-batch`), the system leverages `asyncio.gather()` to make concurrent calls to the AI service. This architecture guarantees that even if a single batch contains hundreds of inputs, the operations execute in parallel rather than sequentially, vastly improving response times and avoiding long-running blocking requests.

# Setup Instructions
1. Ensure you have **Python 3.9+** and **MongoDB** installed on your system.
2. Clone or extract the project.
3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Create an environment file based on the example:
   - Copy `.env.example` to `.env`
   - Adjust `MONGO_URI` to point to your local or cloud MongoDB instance (default is `mongodb://localhost:27017`).

# Run Instructions
1. **Seed the Database**: Before running the app, inject the default `Education_Prompt` into your MongoDB instance.
   ```bash
   python seed.py
   ```
2. **Start the Flask Server**:
   ```bash
   python app.py
   ```
3. Open your web browser and navigate to `http://localhost:5000` to interact with the dashboard.

# Sample Requests

### Single Generation
**Request**
```bash
curl -X POST http://localhost:5000/generate \
-H "Content-Type: application/json" \
-d '{"userInput": "How much should I score in each subject to pass CA final?"}'
```
**Response**
```json
{
  "response": "Mocked AI response for: 'You are an expert in education domain. Answer the following: How much should I score in each subject to pass CA final?'"
}
```

### Batch Generation
**Request**
```bash
curl -X POST http://localhost:5000/generate-batch \
-H "Content-Type: application/json" \
-d '{
  "inputs": [
    "How to pass CA final?",
    "How to prepare for CAT?",
    "Best way to study AI?"
  ]
}'
```
**Response**
```json
{
  "responses": [
    "Mocked AI response for: '... How to pass CA final?'",
    "Mocked AI response for: '... How to prepare for CAT?'",
    "Mocked AI response for: '... Best way to study AI?'"
  ]
}
```

# Future Improvements
- **Real OpenAI Integration**: The current `ai_service.py` is configured with a stable Mock. Swap out the `asyncio.sleep` with real `aiohttp` or `openai` client requests for production.
- **Dockerization**: Include a `Dockerfile` and `docker-compose.yml` for effortless environment orchestration.
- **Authentication**: Secure the endpoints using JWT (JSON Web Tokens).
- **Task Queue**: Move heavy AI processing to background workers like Celery + Redis for ultimate scalability.
- Authentication and user-based authorization can be implemented in future versions.
- JWT-based secure APIs can be added.
- User-specific history tracking can be implemented.
- Rate limiting and caching can be added for scalability.

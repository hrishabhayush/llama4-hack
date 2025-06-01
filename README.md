# Llama on Fly

Welcome to the Llama On Fly project! This project is part of Meta's Llama Hackathon 2025, held during NYC Tech Week (June 2-8).

## Project Overview

Llama on Fly aims to revolutionize the way we interact with text and writing tools. 

While there exists a lot of tool for pair coding, there doesn't exist anything that helps with pair writing and developing ideas on a topic with you. We are creating bubble maps (that finds contrast and synthesis among different topics from different sources). With Llama on Fly we help college students develop ideas for their papers quickly, fine tune our models through the liking of the user to tip the result towards the liking of the user. Most importantly, the bubble maps keeps them engaged to how the AI model is reasoning and what are the underlying thoughts and three main ideas that it uses, for instance to write a philosophy or history paper!

## Features
- Intuitive text editing for writing and creative reasoning
- Bubble Map to help in the creation and discovery of novel ideas
- Implementation of Meta's Llama API for long context application

## Getting Started

To get started with the Llama on Fly, follow these steps:

# Clone the repository:
   ```bash
   git clone <repository-url>
   cd llama4-hack
   ```
   
# Backend Setup

We use FastAPI to power our backend.

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Install the necessary dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the backend server
   ```bash
   cd ..
   uvicorn api:app --reload --host 0.0.0.0 --port 8000
   ```
# Fronend Setup

We use Next.js for the frontend, managed via `npm`.

1. Navigate to the frontend directory
```bash
cd frontend
```

2. Install dependencies
```bash
npm install
```

3. Start the development server:

```bash
npm run dev
```
The frontend should now be live at http://localhost:3000.


## License

This project is licensed under the MIT License.

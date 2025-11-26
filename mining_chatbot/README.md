# Mining Data Analytics Chatbot

A professional, multi-agent AI system for intelligent mining data exploration and analysis.

## Architecture

### Multi-Agent System
1. **Query Analyzer Agent** - Understands user questions and determines required analysis
2. **Code Generator Agent** - Dynamically generates pandas code for data analysis
3. **Execution Agent** - Safely executes code and captures results
4. **Domain Expert Agent** - Provides mining-specific insights and context
5. **Response Synthesizer Agent** - Combines everything into professional responses

### Tech Stack
- **Frontend**: Next.js 14, TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python 3.10+
- **AI**: OpenAI GPT-4o
- **Data**: Pandas for CSV analysis
- **Visualization**: Plotly (interactive charts)

## Setup Instructions

### Prerequisites
- Python 3.10 or higher
- Node.js 18 or higher
- npm or yarn

### Backend Setup

1. Navigate to backend directory:
```bash
cd mining_chatbot/backend
```

2. Create virtual environment:
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Update the DATA_PATH in `main.py` (line 38):
```python
DATA_PATH = "path/to/your/Untitled spreadsheet - opencast_15points_12flights_dataset.csv"
```

5. Start the backend server:
```bash
python main.py
```

Backend will run on: `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd mining_chatbot/frontend
```

2. Install dependencies:
```bash
npm install
# or
yarn install
```

3. Start the development server:
```bash
npm run dev
# or
yarn dev
```

Frontend will run on: `http://localhost:3000`

## Usage

1. Open your browser and navigate to `http://localhost:3000`

2. Ask questions about the mining data:
   - "Why is NOx the dominant pollutant at most locations?"
   - "What is the trend of Fire Risk Score over time?"
   - "Which monitoring points have the highest AQI values?"
   - "Why is the O2 percentage lower at certain points?"
   - "Is the working environment safe based on current data?"
   - "What mitigation strategies are recommended for high NOx levels?"

3. The chatbot will:
   - Analyze your question
   - Generate and execute pandas code
   - Provide data-driven answers with citations
   - Show visualizations when relevant
   - Offer mining-specific insights and recommendations

## Features

- **Intelligent Data Analysis**: Dynamically generates pandas code based on user questions
- **Professional UI**: Clean, modern interface with no emojis
- **Code Transparency**: View the generated analysis code
- **Interactive Visualizations**: Plotly charts for data insights
- **Domain Expertise**: Mining-specific context and safety assessments
- **Data Citations**: All answers backed by actual data
- **Mitigation Strategies**: Recommendations for problematic conditions

## API Endpoints

### POST /query
Process user questions through the multi-agent system.

**Request:**
```json
{
  "question": "Why is NOx the dominant pollutant?"
}
```

**Response:**
```json
{
  "answer": "Professional answer with data citations",
  "code": "# Generated pandas code",
  "visualization": "Plotly JSON (if applicable)",
  "statistics": {"analyzed_rows": 65700},
  "citations": ["Data points analyzed: 65700"]
}
```

### GET /dataset-info
Returns basic dataset information.

### GET /health
Health check endpoint.

## Dataset

The system analyzes a comprehensive mining dataset with:
- **65,700 rows** (one full year of data)
- **27 columns** including:
  - Pollutant concentrations (PM10, PM2.5, CO, CO2, SO2, NOx, CH4)
  - AQI values
  - Temperature, O2 percentage
  - Graham's Ratio (GR)
  - Fire Risk Score (FRS)
  - Dominant pollutant
- **15 monitoring points**
- **12 flights per day**

## Security Note

The code execution environment is sandboxed to only allow pandas operations on the dataset. No file system access or external imports are permitted.

## Troubleshooting

### Backend issues:
- Ensure the CSV file path is correct in `main.py`
- Check that port 8000 is not in use
- Verify OpenAI API key is valid

### Frontend issues:
- Ensure backend is running on port 8000
- Check that port 3000 is not in use
- Clear browser cache if UI doesn't update

### CORS issues:
- The backend is configured to allow requests from `http://localhost:3000`
- If using a different port, update the CORS settings in `main.py`

## Development

To modify the system:

1. **Add new agent capabilities**: Edit agent classes in `backend/main.py`
2. **Customize UI**: Modify `frontend/app/page.tsx`
3. **Add new visualizations**: Update `VisualizationAgent` class
4. **Extend domain knowledge**: Enhance `DomainExpertAgent` prompts

## Production Deployment

### Backend:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Frontend:
```bash
npm run build
npm start
```

## License

Proprietary - Internal use only

## Support

For issues or questions, contact the development team.


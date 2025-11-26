# Quick Start Guide

## Fast Setup (5 minutes)

### Step 1: Backend Setup
```bash
cd mining_chatbot/backend
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
```

**IMPORTANT**: Edit `main.py` line 38 to point to your CSV file:
```python
DATA_PATH = "../../Untitled spreadsheet - opencast_15points_12flights_dataset.csv"
```

Start backend:
```bash
python main.py
```

### Step 2: Frontend Setup (in new terminal)
```bash
cd mining_chatbot/frontend
npm install
npm run dev
```

### Step 3: Open Browser
Navigate to: `http://localhost:3000`

## Test Questions

Try these to see the system in action:

1. **Dominant Pollutant Analysis**:
   "Why is NOx the dominant pollutant at most locations?"

2. **Fire Risk Assessment**:
   "What is the maximum Fire Risk Score at each monitoring point?"

3. **Oxygen Levels**:
   "Which points have the lowest O2 percentage and why?"

4. **Safety Assessment**:
   "Is the working environment safe based on the AQI values?"

5. **Trends**:
   "Show me the monthly trend of dominant pollutants."

6. **Mitigation**:
   "What strategies can reduce NOx levels in the mine?"

## How It Works

1. **You ask** a question
2. **Query Analyzer** understands what you need
3. **Code Generator** writes pandas code
4. **Execution Agent** runs the analysis
5. **Domain Expert** adds mining context
6. **Synthesizer** creates the final answer
7. **You see**: Answer + Code + Visualization (if applicable)

## Troubleshooting

**Backend not starting?**
- Check CSV file path is correct
- Ensure Python 3.10+ is installed
- Verify port 8000 is free

**Frontend not loading?**
- Ensure backend is running first
- Check port 3000 is free
- Clear browser cache

**No response from chatbot?**
- Check backend terminal for errors
- Verify OpenAI API key is valid
- Check network requests in browser DevTools

## Features to Explore

- Click "Show" on generated code to see pandas analysis
- View interactive Plotly visualizations
- See data citations and statistics
- Try different question types (trends, comparisons, explanations)

## Architecture Highlights

**Multi-Agent System:**
- 5 specialized AI agents work together
- Each agent has a specific role
- Agents communicate through structured data
- Final response is synthesized from all agents

**Professional Design:**
- Clean, minimal UI
- No emojis (as requested)
- Data-driven responses
- Code transparency
- Mining domain expertise

Enjoy exploring your mining data!


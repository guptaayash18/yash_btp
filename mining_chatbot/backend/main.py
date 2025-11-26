"""
FastAPI Backend for Mining Data Chatbot
Multi-Agent System for Intelligent Data Analysis
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import pandas as pd
import numpy as np
import os
import json
import base64
from io import BytesIO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from openai import OpenAI

# Initialize FastAPI
app = FastAPI(title="Mining Data Chatbot API")

# CORS middleware for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3005", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI client
OPENAI_API_KEY = "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"
client = OpenAI(api_key=OPENAI_API_KEY)

# Load dataset
DATA_PATH = "../../Untitled spreadsheet - opencast_15points_12flights_dataset.csv"
df = None

def load_data():
    global df
    try:
        df = pd.read_csv(DATA_PATH)
        print(f"Data loaded: {len(df)} rows, {len(df.columns)} columns")
        return True
    except Exception as e:
        print(f"Error loading data: {e}")
        return False

# Load data on startup
load_data()

# Request/Response models
class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    code: Optional[str] = None
    visualization: Optional[str] = None
    statistics: Optional[Dict[str, Any]] = None
    citations: Optional[List[str]] = None

# ==============================================================================
# MULTI-AGENT SYSTEM
# ==============================================================================

class QueryAnalyzerAgent:
    """Agent 1: Analyzes user query and determines required analysis"""
    
    @staticmethod
    def analyze(question: str) -> Dict[str, Any]:
        prompt = f"""You are a query analyzer for a mining data analysis system.

Dataset columns available:
- flight_id, timestamp, point_id
- Pollutants: PM10_ug_m3, PM2.5_ug_m3, CO_ug_m3, CO2_ug_m3, SO2_ug_m3, NOx_ug_m3, CH4_ug_m3
- AQI values: PM10_AQI, PM2.5_AQI, CO_AQI, NOx_AQI, SO2_AQI
- Other: Temperature (°C), O2_percentage, CO_percentage, GR, FRS, Dominant_Pollutant

User question: "{question}"

Analyze and return JSON:
{{
    "analysis_type": "trend|comparison|explanation|statistics|prediction",
    "relevant_columns": ["list", "of", "columns"],
    "needs_visualization": true/false,
    "time_range": "specific|full_year|monthly",
    "spatial_scope": "specific_point|all_points|comparison"
}}"""

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)


class CodeGeneratorAgent:
    """Agent 2: Generates pandas code for analysis"""
    
    @staticmethod
    def generate_code(question: str, analysis: Dict[str, Any]) -> str:
        prompt = f"""You are a pandas code generator for mining data analysis.

Dataset info:
- Variable name: df
- Shape: 65,700 rows, 27 columns
- Date range: Nov 2024 - Nov 2025
- 15 monitoring points, 12 flights per day

User question: "{question}"
Analysis requirements: {json.dumps(analysis, indent=2)}

Generate Python pandas code that:
1. Performs the required analysis
2. Stores results in a variable called 'result'
3. Is safe (no file operations, no imports)
4. Includes proper error handling

Return ONLY the Python code, no explanations."""

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.choices[0].message.content.strip()


class ExecutionAgent:
    """Agent 3: Executes code and captures results"""
    
    @staticmethod
    def execute(code: str) -> Dict[str, Any]:
        try:
            # Clean code
            code = code.replace("```python", "").replace("```", "").strip()
            
            # Create safe execution environment
            local_vars = {"df": df, "pd": pd, "np": np}
            safe_builtins = {
                "Exception": Exception,
                "len": len,
                "range": range,
                "min": min,
                "max": max,
                "sum": sum,
                "abs": abs,
                "round": round,
                "print": print,
                "str": str,
                "int": int,
                "float": float,
                "dict": dict,
                "list": list,
                "tuple": tuple,
                "set": set,
                "bool": bool,
            }
            
            # Execute code
            exec(code, {"__builtins__": safe_builtins}, local_vars)
            
            # Extract result
            result = local_vars.get("result", None)
            
            return {
                "success": True,
                "result": result,
                "error": None
            }
            
        except Exception as e:
            return {
                "success": False,
                "result": None,
                "error": str(e)
            }


class DomainExpertAgent:
    """Agent 4: Provides mining-specific context and insights"""
    
    @staticmethod
    def get_insights(question: str, result: Any, analysis: Dict[str, Any]) -> str:
        result_str = str(result)[:2000] if result is not None else "No data"
        
        prompt = f"""You are a mining safety and environmental expert.

User question: "{question}"
Data analysis result: {result_str}

Provide professional insights including:
1. What the data means in mining context
2. Safety implications (if any)
3. Possible reasons for these readings in an opencast mine
4. Mitigation strategies (if problematic)
5. Trend interpretation (rising=problematic, stable=normal, falling=improving)

Be concise, professional, NO emojis. Include specific numbers from the data."""

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.choices[0].message.content


class ResponseSynthesizerAgent:
    """Agent 5: Combines everything into final response"""
    
    @staticmethod
    def synthesize(question: str, result: Any, insights: str, code: str) -> str:
        result_str = str(result)[:1500] if result is not None else "No data available"
        
        prompt = f"""Create a professional response combining data analysis and expert insights.

Question: "{question}"
Analysis Result: {result_str}
Expert Insights: {insights}

Format response as:
1. Direct answer with specific numbers (cite the data)
2. Context and interpretation
3. Safety/operational implications
4. Recommendations if applicable

Be professional, clear, data-driven. NO emojis."""

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.choices[0].message.content


class VisualizationAgent:
    """Generates visualizations when needed"""
    
    @staticmethod
    def create_viz(question: str, result: Any, analysis: Dict[str, Any]) -> Optional[str]:
        if not analysis.get("needs_visualization", False):
            return None
        
        try:
            # Determine chart type
            if isinstance(result, pd.DataFrame):
                if len(result) <= 20 and len(result.columns) <= 3:
                    # Bar chart
                    fig = px.bar(result, x=result.columns[0], y=result.columns[1] if len(result.columns) > 1 else result.columns[0])
                elif len(result.columns) >= 2:
                    # Line chart for trends
                    fig = px.line(result, x=result.columns[0], y=result.columns[1:])
                else:
                    return None
                    
                fig.update_layout(
                    template="plotly_white",
                    font=dict(family="Arial, sans-serif", size=12),
                    margin=dict(l=50, r=50, t=50, b=50)
                )
                
                return fig.to_json()
            
            elif isinstance(result, pd.Series):
                # Pie or bar chart
                fig = px.bar(x=result.index, y=result.values)
                fig.update_layout(template="plotly_white")
                return fig.to_json()
                
        except Exception as e:
            print(f"Visualization error: {e}")
            return None


# ==============================================================================
# API ENDPOINTS
# ==============================================================================

@app.get("/")
async def root():
    return {"message": "Mining Data Chatbot API", "status": "running"}


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "data_loaded": df is not None,
        "data_rows": len(df) if df is not None else 0
    }


@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """Main endpoint - processes user query through multi-agent system"""
    
    try:
        question = request.question.strip()
        
        if not question:
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        # Agent 1: Analyze query
        analysis = QueryAnalyzerAgent.analyze(question)
        print(f"Analysis: {analysis}")
        
        # Agent 2: Generate code
        code = CodeGeneratorAgent.generate_code(question, analysis)
        print(f"Generated code:\n{code}")
        
        # Agent 3: Execute code
        execution_result = ExecutionAgent.execute(code)
        
        if not execution_result["success"]:
            raise HTTPException(status_code=500, detail=f"Code execution failed: {execution_result['error']}")
        
        result = execution_result["result"]
        
        # Agent 4: Get domain insights
        insights = DomainExpertAgent.get_insights(question, result, analysis)
        
        # Agent 5: Synthesize response
        final_answer = ResponseSynthesizerAgent.synthesize(question, result, insights, code)
        
        # Generate visualization if needed
        visualization = VisualizationAgent.create_viz(question, result, analysis)
        
        # Extract citations from result
        citations = []
        if isinstance(result, (pd.DataFrame, pd.Series)):
            citations.append(f"Data points analyzed: {len(result)}")
        
        return QueryResponse(
            answer=final_answer,
            code=code,
            visualization=visualization,
            statistics={"analyzed_rows": len(result) if hasattr(result, '__len__') else 1},
            citations=citations
        )
        
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/dataset-info")
async def dataset_info():
    """Returns basic dataset information"""
    if df is None:
        raise HTTPException(status_code=500, detail="Dataset not loaded")
    
    return {
        "rows": len(df),
        "columns": list(df.columns),
        "date_range": {
            "start": df['timestamp'].min(),
            "end": df['timestamp'].max()
        },
        "monitoring_points": int(df['point_id'].nunique()),
        "flights_per_day": int(df['flight_id'].nunique())
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)


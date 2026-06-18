import streamlit as st
import pandas as pd
import google.generativeai as genai
import io
import plotly.express as px
import plotly.graph_objects as go
import traceback
import time

# ==========================================
# 1. PAGE CONFIGURATION & INITIALIZATION
# ==========================================
st.set_page_config(
    page_title="GemSight", 
    page_icon="✨", 
    layout="wide",
    initial_sidebar_state="expanded" 
)

# Customizing the look: Spotify Dark Theme + Neon Blue Accents
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* App Background (Spotify Dark) */
    .stApp {
        background-color: #121212;
        color: #b3b3b3;
    }
    
    /* Headers */
    .main-header { 
        font-size: 3.5rem; 
        font-weight: 800; 
        color: #ffffff;
        margin-bottom: 0px; 
        letter-spacing: -1px;
    }
    .main-header span {
        color: #38bdf8; /* Neon Blue Accent */
    }
    .sub-header { 
        font-size: 1.1rem; 
        color: #b3b3b3; 
        margin-top: 5px;
        margin-bottom: 40px; 
        font-weight: 400;
    }
    
    /* Premium Pill Buttons */
    .stButton > button {
        background-color: #38bdf8 !important;
        color: #121212 !important;
        border: none !important;
        padding: 0.75rem 2rem !important;
        border-radius: 50px !important; /* Pill shape */
        font-weight: 700 !important;
        letter-spacing: 0.5px !important;
        transition: transform 0.2s ease, filter 0.2s ease !important;
    }
    .stButton > button:hover {
        transform: scale(1.04) !important;
        filter: brightness(1.1) !important;
        box-shadow: 0 4px 20px 0 rgba(56, 189, 248, 0.4) !important;
    }
    
    /* Flat Dark Metrics */
    [data-testid="stMetric"] {
        background-color: #181818 !important;
        padding: 20px !important;
        border-radius: 8px !important;
        transition: background-color 0.3s ease;
    }
    [data-testid="stMetric"]:hover {
        background-color: #282828 !important;
    }
    [data-testid="stMetricLabel"] > div {
        color: #b3b3b3 !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    [data-testid="stMetricValue"] {
        color: #38bdf8 !important;
        font-size: 2.5rem !important;
        font-weight: 800 !important;
    }
    
    /* Tabs Customization */
    .stTabs [data-baseweb="tab-list"] {
        gap: 30px;
        background-color: transparent;
        border-bottom: 1px solid #282828;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent !important;
        border-radius: 0;
        padding: 10px 0px;
        font-size: 1rem;
        font-weight: 700;
        color: #b3b3b3 !important;
        border: none !important;
    }
    .stTabs [aria-selected="true"] {
        color: #ffffff !important;
        border-bottom: 3px solid #38bdf8 !important;
    }
    
    /* Enhanced Chat Bubbles */
    [data-testid="stChatMessage"] {
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Assistant Message */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
        background-color: #181818;
        border-left: 4px solid #38bdf8;
    }
    
    /* User Message */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        background-color: rgba(56, 189, 248, 0.05);
        border-right: 4px solid #38bdf8;
    }
    
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
        color: #e2e8f0;
        font-size: 1.05rem;
        line-height: 1.6;
    }
    
    /* Enhanced Chat Input */
    [data-testid="stChatInput"] {
        border-radius: 50px !important;
        border: 2px solid #282828 !important;
        background-color: #181818 !important;
        transition: border-color 0.3s ease, box-shadow 0.3s ease !important;
        padding: 0px !important;
        overflow: hidden !important;
    }
    [data-testid="stChatInput"]:focus-within {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.3) !important;
    }
    [data-testid="stChatInput"] div {
        border-radius: 50px !important;
        background-color: transparent !important;
    }
    [data-testid="stChatInput"] textarea {
        color: #fff !important;
        background-color: transparent !important;
        border-radius: 50px !important;
    }
    
    /* Send Button inside Chat Input */
    [data-testid="stChatInputSubmitButton"] {
        background-color: #38bdf8 !important;
        border-radius: 50% !important;
        color: #121212 !important;
        transition: transform 0.2s ease !important;
    }
    [data-testid="stChatInputSubmitButton"]:hover {
        transform: scale(1.1) !important;
    }
    
    /* File Uploader styling */
    [data-testid="stFileUploadDropzone"] {
        background-color: #181818 !important;
        border: 2px dashed #282828 !important;
        border-radius: 12px !important;
        transition: border-color 0.3s ease !important;
    }
    [data-testid="stFileUploadDropzone"]:hover {
        border-color: #38bdf8 !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #181818 !important;
        border-radius: 8px !important;
        color: #fff !important;
        font-weight: 600 !important;
    }
    
    </style>
""", unsafe_allow_html=True)

# Securely configure the Gemini API
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    st.error(f"Failed to connect to Gemini. Check your .streamlit/secrets.toml file. Error: {e}")

# ==========================================
# 2. HELPER FUNCTIONS
# ==========================================
@st.cache_data 
def load_data(file):
    filename = file.name
    if filename.endswith('.csv'):
        return pd.read_csv(file)
    elif filename.endswith(('.xls', '.xlsx')):
        return pd.read_excel(file)
    return None

def get_df_schema(df):
    """Returns a concise summary of the dataframe to save token space. Optimized for large datasets."""
    schema_info = []
    for col in df.columns:
        dtype = df[col].dtype
        missing = df[col].isna().sum()
        # Sample top 100 non-null values for speed on massive datasets
        unique_vals = df[col].dropna().head(100).unique()[:3]
        schema_info.append(f"- {col} (Type: {dtype}, Missing: {missing}): e.g., {list(unique_vals)}")
    return "\n".join(schema_info)

def safe_exec(code_str, df_context):
    """Executes AI generated code with restricted globals/locals and returns locals."""
    restricted_globals = {
        "pd": pd,
        "px": px,
        "go": go,
        "__builtins__": __builtins__
    }
    local_vars = {"df": df_context, "fig1": None, "fig2": None, "fig3": None, "fig4": None, "fig": None}
    
    exec(code_str, restricted_globals, local_vars)
    return local_vars

# ==========================================
# 3. SIDEBAR
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/8653/8653200.png", width=60)
    st.title("Data Settings")
    st.markdown("---")
    
    st.subheader("Upload Dataset")
    uploaded_file = st.file_uploader("Drop a CSV or Excel file here", type=['csv', 'xlsx'])

# ==========================================
# 4. MAIN WORKSPACE
# ==========================================
st.markdown('<p class="main-header">Gem<span>Sight</span></p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Interactive EDA, Actionable Cleaning, and Chat-Driven Plotly Visualizations</p>', unsafe_allow_html=True)

# Create the tabs
tab1, tab2, tab3 = st.tabs(["📊 Interactive Grid", "🧹 Smart Cleaning", "💬 Chat with Data"])

# ==========================================
# 5. CORE LOGIC & TAB ROUTING
# ==========================================
if uploaded_file is not None:
    # Use session state to store the working dataframe so cleaning steps persist
    if "working_df" not in st.session_state or st.session_state.get("current_file") != uploaded_file.name:
        st.session_state.working_df = load_data(uploaded_file)
        st.session_state.current_file = uploaded_file.name
        st.session_state.eda_figs = None
        st.session_state.cleaning_code = None
        st.session_state.messages = [{"role": "assistant", "content": "Hello! I have analyzed your dataset. What would you like to know or see plotted?", "code": None}]
    
    df = st.session_state.working_df
    
    if df is not None:
        schema_summary = get_df_schema(df)
        
        # --- TAB 1: Interactive Grid ---
        with tab1:
            st.subheader("Dataset Overview")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Rows", f"{df.shape[0]:,}")
            col2.metric("Total Columns", df.shape[1])
            col3.metric("Total Missing Values", f"{df.isna().sum().sum():,}")
                
            with st.expander("View Raw Data"):
                st.dataframe(df.head(10), use_container_width=True)

            st.markdown("---")
            st.markdown("### 📊 AI Generated Analysis Grid")
            
            if st.session_state.eda_figs is None:
                with st.spinner("AI is generating a grid of the best visualizations for this data..."):
                    prompt = f"""
                    You are an expert Data Scientist. I have a pandas DataFrame named 'df'.
                    Schema:
                    {schema_summary}
                    
                    Write Python code using `plotly.express` (as `px`) to generate exactly FOUR highly insightful, distinct, and beautiful interactive plots for EDA.
                    
                    STRICT RULES:
                    1. Use Plotly Express (`px`). 
                    2. Use the 'plotly_dark' template for all figures.
                    3. You MUST assign the four Plotly figure objects to variables named exactly `fig1`, `fig2`, `fig3`, and `fig4`.
                    4. Output ONLY raw, executable Python code. No explanations, NO ```python tags.
                    5. Assume `pandas as pd`, `plotly.express as px` are already imported.
                    6. The dataframe is already loaded as `df`. Do NOT re-import data.
                    7. If the dataset has more than 5000 rows, use `df.sample(5000)` inside the plotting functions to prevent freezing.
                    """
                    
                    for attempt in range(2):
                        try:
                            response = model.generate_content(prompt)
                            generated_code = response.text.replace("```python", "").replace("```", "").strip()
                            
                            # Execute safely with a DEEP COPY of df to prevent accidental data mutation
                            local_vars = safe_exec(generated_code, df.copy())
                            
                            if all(f in local_vars and local_vars[f] is not None for f in ["fig1", "fig2", "fig3", "fig4"]):
                                st.session_state.eda_figs = [local_vars["fig1"], local_vars["fig2"], local_vars["fig3"], local_vars["fig4"]]
                                break
                            else:
                                prompt += "\n\nERROR: You failed to assign all four plots to 'fig1', 'fig2', 'fig3', and 'fig4'. Try again."
                        except Exception as e:
                            prompt += f"\n\nERROR executing code:\n{e}\nRewrite code to fix."
                            time.sleep(3)  # Rate limit protection
            
            if st.session_state.eda_figs:
                # Render 2x2 Grid
                r1_col1, r1_col2 = st.columns(2)
                r1_col1.plotly_chart(st.session_state.eda_figs[0], use_container_width=True)
                r1_col2.plotly_chart(st.session_state.eda_figs[1], use_container_width=True)
                
                r2_col1, r2_col2 = st.columns(2)
                r2_col1.plotly_chart(st.session_state.eda_figs[2], use_container_width=True)
                r2_col2.plotly_chart(st.session_state.eda_figs[3], use_container_width=True)
            else:
                st.error("Failed to generate EDA visualizations after multiple attempts.")

        # --- TAB 2: Actionable Cleaning ---
        with tab2:
            st.subheader("AI Cleaning Agent")
            st.write("Let the AI write Pandas code to clean your data (e.g., drop NA, fill missing, fix types).")
            
            if st.button("Generate Cleaning Steps", type="primary"):
                with st.spinner("Analyzing schema to find dirty data..."):
                    prompt = f"""
                    You are an expert Data Engineer. Analyze the schema below.
                    Identify missing values, wrong types, or messy columns.
                    
                    Schema:
                    {schema_summary}
                    
                    Write Python code to clean this DataFrame.
                    
                    STRICT RULES:
                    1. The original dataframe is `df`.
                    2. Modify `df` in place OR reassign to `df`. 
                    3. Output ONLY valid, executable Python code. NO ```python tags. NO text explanations.
                    4. Assume `pandas as pd` is imported.
                    """
                    try:
                        response = model.generate_content(prompt)
                        st.session_state.cleaning_code = response.text.replace("```python", "").replace("```", "").strip()
                    except Exception as e:
                        st.error(f"Gemini API Error: {e}")
                        
            if st.session_state.cleaning_code:
                st.markdown("### Suggested Cleaning Code:")
                st.code(st.session_state.cleaning_code, language="python")
                
                if st.button("Apply Cleaning Code to Dataset", type="secondary"):
                    try:
                        # For cleaning, we pass the actual df reference so it can be mutated/reassigned
                        local_vars = safe_exec(st.session_state.cleaning_code, df)
                        if "df" in local_vars:
                            st.session_state.working_df = local_vars["df"]
                            st.success("Cleaning applied successfully! The main dataset has been updated.")
                            # Reset EDA figs so it recalculates with clean data
                            st.session_state.eda_figs = None
                            st.session_state.cleaning_code = None
                            st.rerun()
                    except Exception as e:
                        st.error(f"Error applying cleaning code: {e}")

        # --- TAB 3: Agentic Chat with Data ---
        with tab3:
            st.subheader("💬 Chat with your Data")
            st.write("Ask questions. The AI will remember the context and use Plotly for visuals.")
            
            chat_container = st.container(height=500)
            
            with chat_container:
                for msg in st.session_state.messages:
                    with st.chat_message(msg["role"]):
                        st.markdown(msg["content"])
                        if msg.get("fig"):
                            st.plotly_chart(msg["fig"], use_container_width=True)

            if user_query := st.chat_input("E.g., 'Show me a scatter plot of X vs Y'"):
                
                st.session_state.messages.append({"role": "user", "content": user_query})
                
                with chat_container:
                    with st.chat_message("user"):
                        st.markdown(user_query)
                    
                    with st.chat_message("assistant"):
                        with st.spinner("Analyzing and plotting..."):
                            
                            # Format conversation history (Sliding window: last 5 pairs)
                            history = ""
                            recent_messages = st.session_state.messages[-6:-1] 
                            for m in recent_messages: 
                                history += f"{m['role'].capitalize()}: {m['content']}\n"
                                
                            prompt = f"""
                            You are an advanced Data Science Assistant. I have a pandas DataFrame named 'df'.
                            Schema: {schema_summary}
                            
                            Recent Conversation History:
                            {history}
                            
                            The user just asked: "{user_query}"
                            
                            Write Python code to answer this. 
                            - If the user wants a chart, use `plotly.express` (as `px`) and assign it to a variable exactly named `fig`. Use `template='plotly_dark'`.
                            - If it is a conceptual question or data calculation, assign the text answer (as a string) to a variable exactly named `answer_text`.
                            - You can do both (assign `fig` and `answer_text`) if needed.
                            
                            STRICT RULES:
                            1. Output ONLY executable Python code. No raw text, NO ```python tags.
                            2. Assume `pandas as pd`, `plotly.express as px` are imported.
                            3. The dataframe is already loaded as `df`.
                            4. Do NOT use `st.markdown` or `st.plotly_chart`. Just assign the variables.
                            """
                            
                            final_fig = None
                            final_text = None
                            success = False
                            
                            for attempt in range(2):
                                try:
                                    response = model.generate_content(prompt)
                                    generated_code = response.text.replace("```python", "").replace("```", "").strip()
                                    
                                    # Execute safely with a DEEP COPY to protect the main state
                                    local_vars = safe_exec(generated_code, df.copy())
                                    
                                    if "fig" in local_vars and local_vars["fig"] is not None:
                                        final_fig = local_vars["fig"]
                                        success = True
                                        
                                    if "answer_text" in local_vars and local_vars["answer_text"] is not None:
                                        final_text = local_vars["answer_text"]
                                        success = True
                                        
                                    if success:
                                        break
                                    else:
                                        prompt += "\n\nERROR: You must assign either 'fig' or 'answer_text'. Try again."
                                        
                                except Exception as e:
                                    prompt += f"\n\nERROR: {e}\nRewrite code to fix."
                                    time.sleep(3)  # Rate limit protection
                            
                            if success:
                                response_content = final_text if final_text else "Here is the visual you requested:"
                                st.markdown(response_content)
                                if final_fig:
                                    st.plotly_chart(final_fig, use_container_width=True)
                                    
                                st.session_state.messages.append({
                                    "role": "assistant", 
                                    "content": response_content, 
                                    "fig": final_fig
                                })
                            else:
                                error_msg = "**Execution Failed.** I couldn't write valid code for that request."
                                st.markdown(error_msg)
                                st.session_state.messages.append({
                                    "role": "assistant", 
                                    "content": error_msg,
                                    "fig": None
                                })
                st.rerun()

    else:
        st.error("Could not load the dataset. Please ensure it is a valid CSV or Excel file.")

else:
    with tab1:
        st.info("👈 Please upload a dataset from the sidebar to begin Automated EDA.")
    with tab2:
        st.info("👈 Please upload a dataset from the sidebar to generate Cleaning Suggestions.")
    with tab3:
        st.info("👈 Please upload a dataset from the sidebar to Chat with your Data.")

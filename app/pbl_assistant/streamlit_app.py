import os
import sys
import uuid
import asyncio
import logging
from datetime import datetime

import streamlit as st
from langgraph.types import Command

# ────────────────────────────────────────────────────────────
# Make the repo root importable so we can import pbl_agent_graph
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
    )
)

from app.pbl_assistant.localization import get_preset
from app.pbl_assistant.agent_graph import pbl_agent_graph
# ────────────────────────────────────────────────────────────

# Optional: use PyMongo (sync) for read-only listing of saved docs
try:
    from pymongo import MongoClient
except Exception:
    MongoClient = None  # handle gracefully if not installed

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("pbl_ui")

# === MongoDB (READ-ONLY in UI) ===============================================
ATLAS_URI = os.getenv("ATLAS_URI", "mongodb+srv://erandDevbd:oPDTDscngZ6geaAX@cluster0-ea24.kwhgj0v.mongodb.net/")
ATLAS_DB = os.getenv("ATLAS_DB", "erandiapp")
ATLAS_COLLECTION = os.getenv("ATLAS_COLLECTION", "project_templates")

mongo_client = None
mongo_col = None
if ATLAS_URI and MongoClient:
    try:
        mongo_client = MongoClient(ATLAS_URI, connectTimeoutMS=4000, serverSelectionTimeoutMS=4000)
        mongo_db = mongo_client[ATLAS_DB]
        mongo_col = mongo_db[ATLAS_COLLECTION]
    except Exception as e:
        log.warning("Could not connect to MongoDB for UI listing: %s", e)

# === Streamlit Page Config ====================================================
st.set_page_config(page_title="🎓 PBL Agent", layout="wide")

# === Session State Defaults ===================================================
def _ss_default(key, value):
    if key not in st.session_state:
        st.session_state[key] = value

_ss_default("language", "English")
_ss_default("class_profile", "")
_ss_default("chat_history", [])
_ss_default("first_message", True)
_ss_default("thread_id", None)
_ss_default("teacher_session_id", str(uuid.uuid4()))
_ss_default("selected_saved_id", None)

lang = st.session_state.language

# === Sidebar =================================================================
st.sidebar.header(get_preset("settings_header", lang))

# 1) Language selector
st.session_state.language = st.sidebar.selectbox(
    get_preset("language_label", lang),
    ["English", "Spanish", "French"],
    index=["English", "Spanish", "French"].index(st.session_state.language),
)

# 2) Classroom profile
st.session_state.class_profile = st.sidebar.text_area(
    get_preset("classroom_profile_label", st.session_state.language),
    st.session_state.get("class_profile", st.session_state.class_profile),
    height=120,
)

# 3) Teacher Session ID (used to group saved projects)
sid_col1, sid_col2 = st.sidebar.columns([0.7, 0.3])
with sid_col1:
    st.session_state.teacher_session_id = st.text_input(
        "Teacher Session ID",
        st.session_state.teacher_session_id,
        help="Use this ID to view your saved project templates."
    )
with sid_col2:
    if st.button("New ID"):
        st.session_state.teacher_session_id = str(uuid.uuid4())

# 4) Start / reset conversation
if st.sidebar.button(get_preset("start_conversation_button", st.session_state.language)):
    st.session_state.chat_history = []
    st.session_state.first_message = True
    st.session_state.thread_id = None

st.sidebar.markdown("---")

# === Utility: Load saved projects for this session_id =========================
def load_saved_projects(session_id: str):
    """Read-only listing of saved projects created by the agent graph."""
    if mongo_col is None or not session_id:
        return []
    try:
        cur = mongo_col.find({"session_id": session_id}).sort("created_at", -1)
        docs = list(cur)
        return docs
    except Exception as e:
        log.warning("Mongo read failed: %s", e)
        return []

def label_for_doc(doc: dict) -> str:
    proj = (doc or {}).get("selected_option", {}) or {}
    title = proj.get("title") or proj.get("template_name") or "(Untitled)"
    when = doc.get("created_at")
    if isinstance(when, datetime):
        ts = when.strftime("%Y-%m-%d %H:%M")
    else:
        ts = ""
    return f"{title} • {ts}"

def render_project_preview(doc: dict):
    if not doc:
        st.info("Select a saved project on the right to preview.")
        return
    proj = doc.get("selected_option", {}) or {}

    st.markdown(f"### {proj.get('title') or proj.get('template_name') or 'Project Preview'}")
    st.write(f"**Template:** {proj.get('template_name', '—')}")
    st.write(f"**Rationale:** {proj.get('template_rationale', '—')}")
    st.write(f"**Driving Question:** {proj.get('driving_question', '—')}")
    st.write(f"**End Product:** {proj.get('end_product', '—')}")

    ks = proj.get("key_skills") or []
    st.write("**Key Skills:** " + (", ".join(ks) if ks else "—"))

    los = proj.get("learning_objectives") or []
    st.write("**Learning Objectives:**")
    if los:
        for lo in los:
            st.write(f"- {lo}")
    else:
        st.write("—")

    st.write(f"**Assessment:** {proj.get('assessment_summary', '—')}")

    when = doc.get("created_at")
    if isinstance(when, datetime):
        st.caption(f"Saved: {when.strftime('%Y-%m-%d %H:%M')}")
    else:
        st.caption("Saved: —")

    with st.expander("Raw document"):
        st.json(doc)

# === Layout: two columns (Chat | Saved + Preview) =============================
left, right = st.columns([0.60, 0.40])

# ====================== LEFT: Chat ============================================
with left:
    st.markdown("## Chat")
    
    # Create a container for the chat messages
    chat_container = st.container()
    
    # Create a container for the input at the bottom
    input_container = st.container()
    
    # Place the input at the bottom
    with input_container:
        user_input = st.chat_input(get_preset("chat_input_placeholder", st.session_state.language))
    
    # Render existing chat in the chat container
    with chat_container:
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                st.caption(msg["timestamp"])
    if user_input:
        ts = datetime.now().strftime("%I:%M %p")

        # Show & save user's message
        with chat_container:
            with st.chat_message("user"):
                st.markdown(user_input)
                st.caption(ts)
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input,
            "timestamp": ts
        })

        # Stream the assistant's reply
        with chat_container:
            with st.chat_message("assistant"):
                placeholder = st.empty()
                full_response: list[str] = []

            async def stream_agent():
                # Ensure thread_id
                if not st.session_state.thread_id:
                    st.session_state.thread_id = str(uuid.uuid4())

                cfg = {"configurable": {"thread_id": st.session_state.thread_id}}

                # Build initial vs. resume state
                if st.session_state.first_message:
                    init_state = {
                        "user_input": user_input,
                        "class_profile": st.session_state.class_profile,
                        "language": st.session_state.language,
                        "project_details": {},
                        "standards_result": {},
                        "knowledge_graph_result": {},
                        "project_options": {},
                        "messages": [],
                        # IMPORTANT: pass session_id to graph (it will handle saving)
                        "session_id": st.session_state.teacher_session_id,
                    }
                    stream = pbl_agent_graph.astream(init_state, cfg, stream_mode="custom")
                else:
                    # Check if the input might be a numeric option selection
                    if user_input.strip().isdigit():
                        # If it's a number, send it as a structured payload
                        choice_int = int(user_input.strip())
                        stream = pbl_agent_graph.astream(
                            Command(resume={"selected_id": choice_int}),
                            cfg,
                            stream_mode="custom"
                        )
                    else:
                        # Otherwise send as regular text
                        stream = pbl_agent_graph.astream(
                            Command(resume=user_input),
                            cfg,
                            stream_mode="custom"
                        )

                # Pull and display chunks
                async for chunk in stream:
                    if isinstance(chunk, str):
                        full_response.append(chunk)
                        placeholder.markdown("".join(full_response))

                # Save the assistant's full reply
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": "".join(full_response),
                    "timestamp": datetime.now().strftime("%I:%M %p")
                })
                st.session_state.first_message = False

            # Execute the async function
            loop = asyncio.new_event_loop()
            try:
                loop.run_until_complete(stream_agent())
            finally:
                loop.close()

# ====================== RIGHT: Saved Projects + Preview ========================
with right:
    st.markdown("## Saved Projects")

    if mongo_col is None:
        st.info("Saved projects listing is unavailable (no MongoDB connection in UI).")
    else:
        # Controls
        r1, r2 = st.columns([0.75, 0.25])
        with r1:
            st.text_input("Filter by Session ID", st.session_state.teacher_session_id, key="filter_sid")
        with r2:
            refresh = st.button("Refresh")

        session_to_query = st.session_state.filter_sid.strip() or st.session_state.teacher_session_id
        docs = load_saved_projects(session_to_query) if (session_to_query and (refresh or True)) else []

        if not docs:
            st.write("No saved projects yet for this session.")
        else:
            # Build radio options
            options = [str(d.get("_id")) for d in docs]
            labels = [label_for_doc(d) for d in docs]

            # Keep selection stable
            default_index = 0
            if st.session_state.selected_saved_id in options:
                default_index = options.index(st.session_state.selected_saved_id)

            selected = st.radio(
                "Your saved projects",
                options=options,
                index=default_index if options else 0,
                format_func=lambda oid: labels[options.index(oid)],
            )
            st.session_state.selected_saved_id = selected

            # Find selected doc and render
            chosen = next((d for d in docs if str(d.get("_id")) == selected), None)
            render_project_preview(chosen)
import os
import sys
import uuid
import asyncio
import threading
import logging
from datetime import datetime, timezone
import streamlit as st
from langgraph.types import Command
import certifi

# Get certifi CA bundle path
CA = certifi.where()

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
from app.pbl_assistant.refine_graph import refine_project_option
# ────────────────────────────────────────────────────────────

# Optional: use PyMongo (sync) for read-only listing of saved docs
try:
    from pymongo import MongoClient
    from bson import ObjectId
except Exception:
    MongoClient = None  # handle gracefully if not installed
    ObjectId = None

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
        mongo_client = MongoClient(
            ATLAS_URI,
            tlsCAFile=CA,
            connectTimeoutMS=10000,
            serverSelectionTimeoutMS=10000,
        )
        mongo_db = mongo_client[ATLAS_DB]
        mongo_col = mongo_db[ATLAS_COLLECTION]
        # Force a quick ping to fail-fast
        mongo_db.command("ping")
        log.info("MongoDB connection successful")
    except Exception as e:
        log.warning("Could not connect to MongoDB for UI listing: %s", e)
        mongo_client = None
        mongo_col = None

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
_ss_default("filter_sid", "")
_ss_default("refine_mode", False)
_ss_default("last_refine_doc_id", None)
_ss_default("thread_id", None)
_ss_default("selected_saved_id", None)
_ss_default("teacher_session_id", str(uuid.uuid4()))

lang = st.session_state.get("language", "English")

# === Utility: Async runner that works in Streamlit ============================
# Global (per process) persistent loop + thread
# Initialize these first before any async operations
_ss_default("_async_loop", asyncio.new_event_loop())
if "_async_thread" not in st.session_state:
    st.session_state._async_thread = threading.Thread(
        target=st.session_state._async_loop.run_forever, daemon=True
    )
    st.session_state._async_thread.start()

def run_coro_sync(coro):
    """
    Submit a coroutine to the persistent background loop and wait for result
    without closing/replacing the loop (Motor-safe).
    """
    loop = st.session_state._async_loop
    return asyncio.run_coroutine_threadsafe(coro, loop).result()

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

def fetch_doc_by_id(doc_id: str):
    if (mongo_col is None) or (not doc_id) or (ObjectId is None):
        return None
    try:
        return mongo_col.find_one({"_id": ObjectId(doc_id)})
    except Exception as e:
        log.warning("Mongo fetch by id failed: %s", e)
        return None

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

# === Layout: two columns (Chat | Saved + Preview) =============================
left, right = st.columns([0.60, 0.40])

# ====================== RIGHT: Saved Projects + Preview ========================
with right:
    st.markdown("## Saved Projects")

    if mongo_col is None:
        st.info("Saved projects listing is unavailable (no MongoDB connection in UI).")
        chosen = None
    else:
        # Controls
        r1, r2 = st.columns([0.75, 0.25])
        with r1:
            st.text_input("Filter by Session ID", st.session_state.teacher_session_id, key="filter_sid")
        with r2:
            st.button("Refresh")  # the page reruns on every interaction anyway

        filter_sid = st.session_state.get("filter_sid", "")
        filter_sid_str = filter_sid if isinstance(filter_sid, str) else ""
        session_to_query = filter_sid_str.strip() or st.session_state.get("teacher_session_id", "")
        # Always load docs (keeps preview fresh after refine)
        docs = load_saved_projects(session_to_query) if session_to_query else []

        if not docs:
            st.write("No saved projects yet for this session.")
            chosen = None
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

    st.markdown("---")
    st.checkbox("Refine selected project via chat", key="refine_mode")
    if st.session_state.get("refine_mode", False):
        st.caption("Type changes on the left (e.g., “Focus the driving question on Mars and add a telescope activity”).")

# ====================== LEFT: Chat ============================================
with left:
    st.markdown("## Chat")

    # Dynamic placeholder based on mode/selection
    refine_mode = st.session_state.get("refine_mode", False)
    selected_saved_id = st.session_state.get("selected_saved_id", None)
    if refine_mode and selected_saved_id:
        placeholder_text = "Describe the change you want (e.g., “Focus on Mars and add a telescope-building activity”)."
    elif refine_mode and not selected_saved_id:
        placeholder_text = "Select a saved project on the right, then describe your change."
    else:
        placeholder_text = get_preset("chat_input_placeholder", st.session_state.language)

    # Create a container for the chat messages
    chat_container = st.container()

    # Create a container for the input at the bottom
    input_container = st.container()

    # Place the input at the bottom
    with input_container:
        user_input = st.chat_input(placeholder_text)

    # Render existing chat in the chat container
    with chat_container:
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                st.caption(msg["timestamp"])

    # ────────────────────────────────────────────────────────────────────────
    # Pure async helpers (NO access to st.session_state inside)
    # ────────────────────────────────────────────────────────────────────────
    async def run_creation_stream_async(
        *,
        user_input: str,
        thread_id: str,
        first_message: bool,
        class_profile: str,
        language: str,
        teacher_session_id: str,
    ) -> dict:
        cfg = {"configurable": {"thread_id": thread_id}}

        if first_message:
            init_state = {
                "user_input": user_input,
                "class_profile": class_profile,
                "language": language,
                "project_details": {},
                "standards_result": {},
                "knowledge_graph_result": {},
                "project_options": {},
                "messages": [],
                "session_id": teacher_session_id,  # for backend persistence
            }
            stream = pbl_agent_graph.astream(init_state, cfg, stream_mode="custom")
        else:
            # numeric selection vs free text
            if user_input.strip().isdigit():
                choice_int = int(user_input.strip())
                payload = Command(resume={"selected_id": choice_int})
            else:
                payload = Command(resume=user_input)
            stream = pbl_agent_graph.astream(payload, cfg, stream_mode="custom")

        full_chunks: list[str] = []
        async for chunk in stream:
            if isinstance(chunk, str):
                full_chunks.append(chunk)

        return {
            "text": "".join(full_chunks),
            "thread_id": thread_id,
            "first_message": False,
        }

    async def run_refine_once_async(
        *,
        selected_id: str,
        selected_doc: dict | None,
        user_input: str,
        language: str,
        class_profile: str,
        teacher_session_id: str,
        idem_key: str,
    ) -> dict:
        result = await refine_project_option(
            source_doc_id=selected_id,
            change_request=user_input,
            session_id=teacher_session_id,
            language=language,
            class_profile=class_profile,
            selected_option=(selected_doc or {}).get("selected_option") if selected_doc else None,
            standards_result=(selected_doc or {}).get("standards_result") if selected_doc else None,
            knowledge_graph_result=(selected_doc or {}).get("knowledge_graph_result") if selected_doc else None,
            strict=False,
            idempotency_key=idem_key,
            thread_id=f"refine_{selected_id}",
        )

        refine_result = result.get("refine_result", {}) or {}
        updated_id = result.get("updated_doc_id")
        affected = refine_result.get("affected_fields") or []
        warnings = refine_result.get("warnings") or []
        change_summary = refine_result.get("change_summary") or "Refinement completed."

        parts = [f"**Refinement summary:** {change_summary}"]
        if affected:
            parts.append(f"**Affected fields:** {', '.join(affected)}")
        if warnings:
            parts.append(f"**Warnings:** {', '.join(warnings)}")
        if updated_id:
            parts.append(f"**Saved new version:** `{updated_id}`")

        return {
            "text": "\n\n".join(parts),
            "updated_id": updated_id,
            "refine_result": refine_result,
        }

    # ────────────────────────────────────────────────────────────────────────
    # Handle a new user message
    # ────────────────────────────────────────────────────────────────────────
    if user_input:
        ts = datetime.now().strftime("%I:%M %p")

        # Show & save user's message (main thread)
        with chat_container:
            with st.chat_message("user"):
                st.markdown(user_input)
                st.caption(ts)
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input,
            "timestamp": ts
        })

        # Assistant reply container
        with chat_container:
            with st.chat_message("assistant"):
                placeholder = st.empty()

        # Snapshot all state needed for async work (so we don't touch session_state inside)
        first_message = bool(st.session_state.get("first_message", True))
        thread_id = st.session_state.get("thread_id") or str(uuid.uuid4())
        class_profile = st.session_state.get("class_profile", "")
        language = st.session_state.get("language", "English")
        teacher_session_id = st.session_state.get("teacher_session_id", "")
        refine_mode_now = bool(st.session_state.get("refine_mode", False))
        selected_saved_id_now = st.session_state.get("selected_saved_id", None)

        # Preload selected doc synchronously if refining
        selected_doc = fetch_doc_by_id(selected_saved_id_now) if (refine_mode_now and selected_saved_id_now) else None

        # Build coroutine without touching session_state inside
        async def orchestrate_async():
            if refine_mode_now:
                if not selected_saved_id_now:
                    return {"text": "Please select a saved project on the right before refining."}
                idem_key = f"{selected_saved_id_now}:{hash(user_input)}:{datetime.now(timezone.utc).strftime('%Y%m%d%H%M')}"
                return await run_refine_once_async(
                    selected_id=selected_saved_id_now,
                    selected_doc=selected_doc,
                    user_input=user_input,
                    language=language,
                    class_profile=class_profile,
                    teacher_session_id=teacher_session_id,
                    idem_key=idem_key,
                )
            else:
                return await run_creation_stream_async(
                    user_input=user_input,
                    thread_id=thread_id,
                    first_message=first_message,
                    class_profile=class_profile,
                    language=language,
                    teacher_session_id=teacher_session_id,
                )

        # Execute the async function in background loop and get the result
        try:
            result_dict = run_coro_sync(orchestrate_async())
        except Exception as e:
            logging.exception("Async orchestration failed")
            err_text = f"Sorry, something went wrong.\n\n```text\n{e}\n```"
            placeholder.markdown(err_text)
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": err_text,
                "timestamp": datetime.now().strftime("%I:%M %p")
            })
        else:
            # Update UI and session_state on main thread
            response_text = result_dict.get("text", "")
            placeholder.markdown(response_text)

            # Persist thread_id and first_message if we were in creation mode
            if not refine_mode_now:
                st.session_state.thread_id = thread_id
                st.session_state.first_message = False

            # If refine produced a new doc, switch selection to it so preview updates
            updated_id = result_dict.get("updated_id")
            if updated_id:
                st.session_state.last_refine_doc_id = updated_id
                st.session_state.selected_saved_id = updated_id

            # Save to chat history
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": response_text,
                "timestamp": datetime.now().strftime("%I:%M %p")
            })

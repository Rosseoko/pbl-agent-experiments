# pbl_assistant/localization.py

import boto3

# ─── Language code map ────────────────────────────────────────────────────────
# Map UI language names (from your streamlit/CLI) → AWS Translate codes
LANG_CODE_MAP = {
    "English": "en",
    "Spanish": "es",
    "French":  "fr",
}

# Shared AWS Translate client
_translate_client = boto3.client("translate", region_name="us-east-1")


# ─── Low-level dynamic translate helper ───────────────────────────────────────
def translate_text(text: str, source: str, target: str) -> str:
    """
    Call AWS Translate from `source`→`target`. On failure, return original text.
    """
    try:
        resp = _translate_client.translate_text(
            Text=text,
            SourceLanguageCode=source,
            TargetLanguageCode=target
        )
        return resp.get("TranslatedText", text)
    except Exception:
        return text


# ─── Canonical English originals for all fixed UI strings ────────────────────
PRESET_STRINGS = {
    # Info-gathering node
    "need_more_info":        "I need more information to help you create your project.",
    "provide_missing_slots": "Could you please provide the {slots}?",
    "all_info_received":     "Great! I have all the information I need.",

    # Standards node
    "get_standards_header":    "\n#### Getting standards recommendations...\n",
    "recommended_standards":   "\n🔖 **Recommended Standards:**\n",
    "prerequisites_prefix":    "\n📌 **Prerequisites:** ",
    "cross_curricular_prefix": "\n🔗 **Cross-Curricular Connections:** ",

    # Knowledge-Graph node
    "get_kg_header":        "\n#### Getting knowledge-graph insights…\n",
    "kg_insights_header":   "\n🔍 **Knowledge-Graph Insights:**\n",
    "kg_standard_prefix":   "> **Working from standard**: ",
    "kg_retry":             "\n⏳ Retrying knowledge-graph call...\n",
    "kg_fallback":          "\n⚠️ Using fallback Knowledge-Graph insights.\n",
    "project_topics_header":"\n📚 **Project Topics:**\n",
    "cross_subjects_header":"🔗 **Cross-Subject Connections:**\n",
    "real_world_header":    "🌎 **Real-World Applications:**\n",
    "resources_header":     "📘 **Curriculum Resources:**\n",
    "implementation_header":"💡 **Implementation Ideas:**\n",
    "confidence_prefix":    "✅ **Relevance Confidence:** ",

    # Project-options node
    "creating_options_header": "\n####Creating Project Options…\n",
    "project_options_header":    "\n=== PROJECT OPTIONS ===\n",
    "fallback_options":          "\n⚠️ Could not parse structured options; here’s what we got:\n",
    "option_label":              "Option",
    "rationale_label":           "• Rationale",
    "driving_question_label":    "• Driving Question",
    "end_product_label":         "• End Product",
    "key_skills_label":          "• Key Skills",
    "learning_objectives_label": "• Learning Objectives",
    "assessment_summary_label":  "• Assessment Summary",
    "choice_prompt":             "Please choose 1, 2, or 3.",
    "invalid_choice":            "Please select an option between 1 and {max}.",
    "full_details_header":       "\n🔎 **Full project details:**",
    "project_ready":             "\n🎉 Your project is ready.",

    # Streamlit app
    "settings_header":           "⚙️ Settings",
    "language_label":            "Choose your language",
    "classroom_profile_label":   "Classroom profile",
    "start_conversation_button": "🗣️ Start Conversation",
    "chat_input_placeholder":    "Type your message here…",
}


# ─── Per-language overrides, by the same keys above ────────────────────────────
PRESET_TRANSLATIONS = {
    "es": {
        "need_more_info":        "Necesito más información para ayudarte a crear tu proyecto.",
        "provide_missing_slots": "Por favor proporciona {slots}",
        "all_info_received":     "¡Genial! Tengo toda la información que necesito.",

        "get_standards_header":    "\n#### Obteniendo recomendaciones de estándares...\n",
        "recommended_standards":   "\n🔖 **Estándares recomendados:**\n",
        "prerequisites_prefix":    "\n📌 **Prerrequisitos:** ",
        "cross_curricular_prefix": "\n🔗 **Conexiones interdisciplinarias:** ",

        "get_kg_header":        "\n#### Obteniendo ideas del grafo de conocimientos…\n",
        "kg_insights_header":   "\n🔍 **Ideas del grafo de conocimientos:**\n",
        "kg_standard_prefix":   "> **Trabajando desde estándar**: ",
        "kg_retry":             "\n⏳ Reintentando llamada del grafo de conocimientos...\n",
        "kg_fallback":          "\n⚠️ Usando ideas del grafo de conocimientos de respaldo.\n",
        "project_topics_header":"\n📚 **Temas del proyecto:**\n",
        "cross_subjects_header":"\n🔗 **Conexiones entre materias:**\n",
        "real_world_header":    "\n🌎 **Aplicaciones en el mundo real:**\n",
        "resources_header":     "\n📘 **Recursos curriculares:**\n",
        "implementation_header":"\n💡 **Ideas de implementación:**\n",
        "confidence_prefix":    "\n✅ **Confianza de relevancia:** ",

        # Project-options node
        "creating_options_header": "\n#### Creando ideas de proyectos…\n",
        "project_options_header":    "\n=== OPCIONES DE PROYECTO ===\n",
        "fallback_options":          "\n⚠️ No pude parsear las opciones; esto es lo que obtuve:\n",
        "option_label":              "\nOpción",
        "rationale_label":           "\n• Justificación",
        "driving_question_label":    "\n• Pregunta impulsora",
        "end_product_label":         "\n• Producto final",
        "key_skills_label":          "\n• Habilidades clave",
        "learning_objectives_label": "\n• Objetivos de aprendizaje",
        "assessment_summary_label":  "\n• Resumen de evaluación",
        "choice_prompt":             "Por favor elige 1, 2 o 3.",
        "invalid_choice":            "Por favor selecciona una opción entre 1 y {max}.",
        "full_details_header":       "\n🔎 **Detalles completos de tu proyecto:**",
        "project_ready":             "\n🎉 Tu proyecto está listo.",

        # Streamlit app
        "settings_header":           "⚙️ Configuración",
        "language_label":            "Elige tu idioma",
        "classroom_profile_label":   "Perfil del aula",
        "start_conversation_button": "🗣️ Iniciar conversación",
        "chat_input_placeholder":    "Escribe tu mensaje aquí…",

    },
    "fr": {
        "need_more_info":        "J’ai besoin d’informations supplémentaires pour t’aider à créer ton projet.",
        "provide_missing_slots": "Peux-tu me fournir {slots} ?",
        "all_info_received":     "Génial ! J’ai toutes les informations dont j’ai besoin.",

        "get_standards_header":    "\n#### Récupération des recommandations de normes…\n",
        "recommended_standards":   "\n🔖 **Normes recommandées :**\n",
        "prerequisites_prefix":    "\n📌 **Prérequis :** ",
        "cross_curricular_prefix": "\n🔗 **Connexions interdisciplinaires :** ",

        "get_kg_header":        "\n#### Récupération des insights du graphe de connaissances…\n",
        "kg_insights_header":   "\n🔍 **Insights du graphe de connaissances :**\n",
        "kg_standard_prefix":   "\n> **Travail à partir de la norme**: ",
        "kg_retry":             "\n⏳ Nouvelle tentative de l’appel au graphe de connaissances…\n",
        "kg_fallback":          "\n⚠️ Utilisation des insights de secours du graphe de connaissances.\n",
        "project_topics_header":"\n📚 **Sujets du projet :**\n",
        "cross_subjects_header":"\n🔗 **Connexions entre disciplines :**\n",
        "real_world_header":    "\n🌎 **Applications concrètes :**\n",
        "resources_header":     "\n📘 **Ressources pédagogiques :**\n",
        "implementation_header":"\n💡 **Idées de mise en œuvre :**\n",
        "confidence_prefix":    "\n✅ **Confiance de pertinence :** ",

        # Project-options node
        "creating_options_header":   "\n####En cours de création des options de projet…\n",
        "project_options_header":    "\n=== OPTIONS DE PROJET ===\n",
        "fallback_options":          "\n⚠️ Impossible d’analyser les options ; voici ce que j’ai obtenu :\n",
        "option_label":              "Option",
        "rationale_label":           "\n• Justification",
        "driving_question_label":    "\n• Question directrice",
        "end_product_label":         "\n• Produit final",
        "key_skills_label":          "\n• Compétences clés",
        "learning_objectives_label": "\n• Objectifs d’apprentissage",
        "assessment_summary_label":  "\n• Résumé de l’évaluation",
        "choice_prompt":             "Veuillez choisir 1, 2 ou 3.",
        "invalid_choice":            "Veuillez sélectionner une option entre 1 et {max}.",
        "full_details_header":       "\n🔎 **Détails complets du projet :**",
        "project_ready":             "🎉 Votre projet est prêt.",

        # Streamlit app
        "settings_header":           "⚙️ Paramètres",
        "language_label":            "Choisissez votre langue",
        "classroom_profile_label":   "Profil de la classe",
        "start_conversation_button": "🗣️ Démarrer la conversation",
        "chat_input_placeholder":    "Tapez votre message ici…",

    },
}


# ─── Lookup helper for all fixed strings ──────────────────────────────────────
def get_preset(key: str, lang_name: str) -> str:
    """
    Return the localized version of PRESET_STRINGS[key]
    for the given UI language name. Falls back to English.
    """
    code = LANG_CODE_MAP.get(lang_name, "en")
    return PRESET_TRANSLATIONS.get(code, {}).get(key, PRESET_STRINGS.get(key, ""))


def localize(text: str, src: str, tgt: str) -> str:
    """
    1) If tgt==src or text empty → return text.
    2) If text exactly matches one of our PRESET_STRINGS, return the preset.
    3) Else fallback to AWS Translate.
    """
    if tgt == src or not text.strip():
        return text
    # exact-match preset lookup
    presets = PRESET_TRANSLATIONS.get(tgt, {})
    if text in presets:
        return presets[text]
    # otherwise real-time translation
    return translate_text(text, src, tgt)


__all__ = [
    "LANG_CODE_MAP",
    "translate_text",
    "get_preset",
    "PRESET_STRINGS",
]

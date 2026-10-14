"""
EGFR-DrugDiscovery-XAI — Centralized Semantic Design Tokens
Design System: HERBARIUM ALPINUM — The Edelweiss Folio
Reference: https://ui.oiloil.org/works/herbarium/live/index.html
"""

from typing import Dict, Any

# ==============================================================================
# 1. FOUNDATION TOKENS
# ==============================================================================

TYPOGRAPHY_FOUNDATIONS = {
    "family": {
        "primary": "Inter",
        "mono": "'JetBrains Mono', 'IBM Plex Mono', 'Courier New', monospace",
        "display": "'Anton', 'Impact', 'Inter', sans-serif",
        "stack": "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
    },
    "scale": {
        "xs": "9px",
        "sm": "10px",
        "md": "11px",
        "lg": "12px",
        "xl": "13px",
        "2xl": "14px",  # base font size
        "3xl": "18px",
        "4xl": "19px",
        "display_sm": "24px",
        "display_md": "32px",
        "display_lg": "42px"
    },
    "weight": {
        "light": 300,
        "base": 400,
        "medium": 500,
        "semibold": 600,
        "bold": 700
    },
    "lineHeight": {
        "tight": "1.1",
        "snug": "1.3",
        "base": "21px",  # 1.5 at 14px
        "relaxed": "1.65"
    }
}

COLOR_FOUNDATIONS = {
    "text": {
        "primary": "#e6e9d9",      # chalk / pale botanical text
        "secondary": "#9ba793",    # muted sage green
        "tertiary": "#080e0a",     # deep forest near-black (for light parchment mounts)
        "inverse": "#99ff00"       # fluorescent chartreuse
    },
    "surface": {
        "base": "#000000",         # pure near-black viewport surface
        "forest": "#080e0a",       # deep botanical forest floor
        "muted": "#101811",        # card and drawer panel surface
        "elevated": "#151f16",     # elevated interactive containers
        "parchment": "#d4dac1"     # botanical specimen voucher label
    },
    "border": {
        "strong": "#35402f",       # botanical bounding lines
        "subtle": "#1e291b",       # secondary divider rules
        "highlight": "#99ff00"     # active focus and selection borders
    },
    "accent": {
        "chartreuse": "#99ff00",   # primary interactive highlight
        "crimson": "#ff5555",      # penalty / unfavorable SHAP / inactive
        "amber": "#e0b034",        # warning / borderline
        "teal": "#70a9a1"          # informational secondary series
    }
}

SPACING_FOUNDATIONS = {
    "space.1": "1px",
    "space.2": "6px",
    "space.3": "7px",
    "space.4": "8px",
    "space.5": "9px",
    "space.6": "10px",
    "space.7": "12px",
    "space.8": "13px"
}

MOTION_FOUNDATIONS = {
    "duration": {
        "instant": "180ms",
        "paper": "380ms"
    },
    "easing": {
        "settle": "cubic-bezier(0.16, 0.78, 0.22, 1)"
    }
}

# ==============================================================================
# 2. SEMANTIC TOKEN ALIASES (WCAG 2.2 AA COMPLIANT)
# ==============================================================================

SEMANTIC_TOKENS = {
    "color": {
        # Foreground Text Aliases (minimum 4.5:1 contrast against #080e0a / #101811)
        "text_primary": COLOR_FOUNDATIONS["text"]["primary"],          # 12.3:1 contrast
        "text_secondary": COLOR_FOUNDATIONS["text"]["secondary"],      # 6.4:1 contrast
        "text_muted_tertiary": "#85937d",                              # 5.1:1 contrast (WCAG AA compliant dark surface alias)
        "text_label_dark": COLOR_FOUNDATIONS["text"]["tertiary"],      # For use on parchment surfaces (#d4dac1)
        "text_inverse": COLOR_FOUNDATIONS["text"]["inverse"],          # #99ff00
        "text_disabled": "#4a5843",

        # Surfaces
        "surface_page": COLOR_FOUNDATIONS["surface"]["base"],
        "surface_card": COLOR_FOUNDATIONS["surface"]["muted"],
        "surface_elevated": COLOR_FOUNDATIONS["surface"]["elevated"],
        "surface_voucher": COLOR_FOUNDATIONS["surface"]["parchment"],
        "surface_selected": "#192815",

        # Borders
        "border_primary": COLOR_FOUNDATIONS["border"]["strong"],
        "border_subtle": COLOR_FOUNDATIONS["border"]["subtle"],
        "border_active": COLOR_FOUNDATIONS["accent"]["chartreuse"],

        # Interactive Actions
        "action_primary_bg": COLOR_FOUNDATIONS["accent"]["chartreuse"],
        "action_primary_text": "#080e0a",
        "action_primary_hover": "#b3ff33",
        "action_secondary_bg": "#142013",
        "action_secondary_text": COLOR_FOUNDATIONS["text"]["primary"],
        "action_secondary_border": COLOR_FOUNDATIONS["border"]["strong"],

        # Status / Feedback
        "status_success": COLOR_FOUNDATIONS["accent"]["chartreuse"],
        "status_error": COLOR_FOUNDATIONS["accent"]["crimson"],
        "status_warning": COLOR_FOUNDATIONS["accent"]["amber"],
        "status_info": COLOR_FOUNDATIONS["text"]["secondary"],

        # Molecular Attribution & Scientific Plotting
        "xai_favorable": "#99ff00",       # Binding anchor (+SHAP)
        "xai_unfavorable": "#ff5555",     # Clash / steric penalty (-SHAP)
        "xai_neutral": "#687760"
    },
    "layout": {
        "radius": "2px",                  # Technical, editorial, restrained
        "border_width": "1px",
        "grid_pattern_size": "48px"
    }
}


# ==============================================================================
# 3. PLOTLY SCIENTIFIC THEME BUILDER
# ==============================================================================

def get_herbarium_plotly_layout(height: int = 380, title: str = "") -> Dict[str, Any]:
    """
    Returns a unified layout dictionary for Plotly charts matching
    Herbarium Alpinum dark technical editorial tokens.
    """
    layout = dict(
        height=height,
        paper_bgcolor=SEMANTIC_TOKENS["color"]["surface_card"],
        plot_bgcolor=SEMANTIC_TOKENS["color"]["surface_card"],
        font=dict(
            family=TYPOGRAPHY_FOUNDATIONS["family"]["stack"],
            size=11,
            color=SEMANTIC_TOKENS["color"]["text_secondary"]
        ),
        margin=dict(l=40, r=30, t=40 if title else 20, b=40),
        xaxis=dict(
            gridcolor=SEMANTIC_TOKENS["color"]["border_subtle"],
            linecolor=SEMANTIC_TOKENS["color"]["border_primary"],
            tickcolor=SEMANTIC_TOKENS["color"]["border_primary"],
            tickfont=dict(size=10, color=SEMANTIC_TOKENS["color"]["text_secondary"]),
            zerolinecolor=SEMANTIC_TOKENS["color"]["border_primary"]
        ),
        yaxis=dict(
            gridcolor=SEMANTIC_TOKENS["color"]["border_subtle"],
            linecolor=SEMANTIC_TOKENS["color"]["border_primary"],
            tickcolor=SEMANTIC_TOKENS["color"]["border_primary"],
            tickfont=dict(size=10, color=SEMANTIC_TOKENS["color"]["text_secondary"]),
            zerolinecolor=SEMANTIC_TOKENS["color"]["border_primary"]
        ),
        legend=dict(
            font=dict(size=10, color=SEMANTIC_TOKENS["color"]["text_primary"]),
            bgcolor="rgba(16, 24, 17, 0.8)",
            bordercolor=SEMANTIC_TOKENS["color"]["border_primary"],
            borderwidth=1
        )
    )
    if title:
        layout["title"] = dict(
            text=f"<span style='color:{SEMANTIC_TOKENS['color']['text_primary']}; font-size:13px; font-weight:600; letter-spacing:0.04em;'>{title.upper()}</span>",
            x=0.02,
            y=0.96
        )
    return layout


# ==============================================================================
# 4. GLOBAL CSS STYLESHEET GENERATOR
# ==============================================================================

def get_herbarium_css() -> str:
    """
    Generates the complete CSS stylesheet implementing Herbarium Alpinum
    editorial dark design language inside Streamlit.
    """
    return f"""
<style>
    /* Google Fonts: Inter & JetBrains Mono */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

    :root {{
        --forest: {COLOR_FOUNDATIONS["surface"]["forest"]};
        --surface: {COLOR_FOUNDATIONS["surface"]["muted"]};
        --elevated: {COLOR_FOUNDATIONS["surface"]["elevated"]};
        --accent: {COLOR_FOUNDATIONS["accent"]["chartreuse"]};
        --chalk: {COLOR_FOUNDATIONS["text"]["primary"]};
        --muted: {COLOR_FOUNDATIONS["text"]["secondary"]};
        --muted-dark: {SEMANTIC_TOKENS["color"]["text_muted_tertiary"]};
        --line: {COLOR_FOUNDATIONS["border"]["strong"]};
        --line-subtle: {COLOR_FOUNDATIONS["border"]["subtle"]};
        --label: {COLOR_FOUNDATIONS["surface"]["parchment"]};
        --crimson: {COLOR_FOUNDATIONS["accent"]["crimson"]};
        --fast: {MOTION_FOUNDATIONS["duration"]["instant"]};
        --font-body: {TYPOGRAPHY_FOUNDATIONS["family"]["stack"]};
        --font-mono: {TYPOGRAPHY_FOUNDATIONS["family"]["mono"]};
    }}

    /* Global Body and Viewport */
    html, body, [data-testid="stAppViewContainer"] {{
        background-color: var(--forest) !important;
        color: var(--chalk) !important;
        font-family: var(--font-body) !important;
        font-size: {TYPOGRAPHY_FOUNDATIONS["scale"]["2xl"]} !important;
        line-height: {TYPOGRAPHY_FOUNDATIONS["lineHeight"]["base"]} !important;
        letter-spacing: -0.01em;
    }}

    /* Subtle technical grid texture on main content area */
    [data-testid="stMain"] {{
        background-image: 
            linear-gradient(90deg, transparent calc(100% - 1px), rgba(53, 64, 47, 0.15) 1px),
            linear-gradient(transparent calc(100% - 1px), rgba(53, 64, 47, 0.15) 1px);
        background-size: 48px 48px;
        background-color: var(--forest) !important;
    }}

    /* Hide extraneous Streamlit elements */
    #MainMenu, header, footer, .stDeployButton,
    div[data-testid="stToolbar"], div[data-testid="stDecoration"],
    div[data-testid="stStatusWidget"] {{
        visibility: hidden !important;
        display: none !important;
    }}

    /* Typography Foundations */
    h1, h2, h3, h4, h5, h6 {{
        color: var(--chalk) !important;
        font-family: var(--font-body) !important;
        font-weight: 500 !important;
        letter-spacing: -0.02em;
    }}

    .mono {{
        font-family: var(--font-mono) !important;
        font-size: {TYPOGRAPHY_FOUNDATIONS["scale"]["md"]};
        letter-spacing: 0.04em;
        line-height: 1.5;
    }}

    .eyebrow {{
        font-family: var(--font-mono) !important;
        font-size: {TYPOGRAPHY_FOUNDATIONS["scale"]["sm"]};
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: var(--muted) !important;
        display: block;
        margin-bottom: 6px;
    }}

    /* Editorial Section Rule */
    .section-rule {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-top: 1px solid var(--line);
        padding-top: 10px;
        padding-bottom: 12px;
        margin-top: 24px;
        margin-bottom: 16px;
        font-family: var(--font-mono);
        font-size: {TYPOGRAPHY_FOUNDATIONS["scale"]["sm"]};
        color: var(--muted);
        letter-spacing: 0.08em;
    }}

    .section-rule span:last-child {{
        color: var(--accent);
    }}

    /* Herbarium Technical Banner */
    .specimen-header {{
        border: 1px solid var(--line);
        background: var(--surface);
        padding: 20px 24px;
        margin-bottom: 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: relative;
    }}

    .specimen-header::before {{
        content: "";
        position: absolute;
        top: 0; left: 0; bottom: 0;
        width: 3px;
        background: var(--accent);
    }}

    .specimen-header-title {{
        font-size: 22px;
        font-weight: 600;
        letter-spacing: -0.02em;
        color: var(--chalk);
        margin: 0;
    }}

    .specimen-header-sub {{
        font-size: {TYPOGRAPHY_FOUNDATIONS["scale"]["lg"]};
        color: var(--muted);
        margin-top: 4px;
    }}

    .specimen-accession {{
        font-family: var(--font-mono);
        font-size: {TYPOGRAPHY_FOUNDATIONS["scale"]["sm"]};
        color: var(--accent);
        text-align: right;
        border-left: 1px solid var(--line);
        padding-left: 20px;
    }}

    /* Specimen Label / Voucher (Botanical Archive Mount) */
    .specimen-voucher {{
        background: var(--label);
        color: #080e0a !important;
        padding: 18px 20px;
        border: 1px solid #1a2414;
        position: relative;
        font-family: var(--font-body);
        margin-bottom: 16px;
    }}

    .specimen-voucher::before {{
        content: "";
        position: absolute;
        inset: 4px;
        border: 1px solid rgba(8, 14, 10, 0.25);
        pointer-events: none;
    }}

    .specimen-voucher * {{
        color: #080e0a !important;
    }}

    .voucher-head {{
        display: flex;
        justify-content: space-between;
        border-bottom: 1px solid rgba(8, 14, 10, 0.4);
        padding-bottom: 6px;
        margin-bottom: 8px;
        font-family: var(--font-mono);
        font-size: {TYPOGRAPHY_FOUNDATIONS["scale"]["xs"]};
        letter-spacing: 0.1em;
        font-weight: 600;
    }}

    .voucher-title {{
        font-size: 18px;
        font-weight: 700;
        line-height: 1.2;
        margin: 4px 0 6px 0;
    }}

    .voucher-barcode {{
        height: 14px;
        width: 52px;
        background: repeating-linear-gradient(90deg, #080e0a 0 1px, transparent 1px 3px, #080e0a 3px 5px, transparent 5px 7px, #080e0a 7px 8px);
        opacity: 0.8;
    }}

    /* Card Panels & Containers */
    .herb-card {{
        background: var(--surface);
        border: 1px solid var(--line);
        padding: 16px 20px;
        margin-bottom: 16px;
        position: relative;
    }}

    .herb-card-title {{
        font-family: var(--font-mono);
        font-size: {TYPOGRAPHY_FOUNDATIONS["scale"]["md"]};
        letter-spacing: 0.08em;
        color: var(--muted);
        text-transform: uppercase;
        border-bottom: 1px solid var(--line-subtle);
        padding-bottom: 8px;
        margin-bottom: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}

    /* Prediction Badges */
    .badge-active {{
        background: rgba(153, 255, 0, 0.08);
        border: 1px solid var(--accent);
        color: var(--accent) !important;
        padding: 14px 20px;
        text-align: center;
        margin-bottom: 16px;
    }}

    .badge-active-title {{
        font-family: var(--font-mono);
        font-size: 16px;
        font-weight: 700;
        letter-spacing: 0.05em;
        display: block;
    }}

    .badge-inactive {{
        background: rgba(255, 85, 85, 0.08);
        border: 1px solid var(--crimson);
        color: var(--crimson) !important;
        padding: 14px 20px;
        text-align: center;
        margin-bottom: 16px;
    }}

    .badge-inactive-title {{
        font-family: var(--font-mono);
        font-size: 16px;
        font-weight: 700;
        letter-spacing: 0.05em;
        display: block;
    }}

    /* Sidebar Refinement */
    section[data-testid="stSidebar"] {{
        background-color: var(--forest) !important;
        border-right: 1px solid var(--line) !important;
    }}

    section[data-testid="stSidebar"] .stSelectbox,
    section[data-testid="stSidebar"] .stTextArea {{
        margin-bottom: 12px;
    }}

    /* Streamlit Form Control Restyling */
    .stSelectbox > div > div, 
    .stTextInput > div > div,
    .stTextArea > div > div {{
        background-color: var(--surface) !important;
        border: 1px solid var(--line) !important;
        border-radius: 2px !important;
        color: var(--chalk) !important;
        font-family: var(--font-mono) !important;
        font-size: {TYPOGRAPHY_FOUNDATIONS["scale"]["xl"]} !important;
        transition: border-color var(--fast) ease;
    }}

    .stSelectbox > div > div:hover,
    .stTextInput > div > div:hover,
    .stTextArea > div > div:hover {{
        border-color: var(--muted) !important;
    }}

    .stSelectbox > div > div:focus-within,
    .stTextInput > div > div:focus-within,
    .stTextArea > div > div:focus-within {{
        border-color: var(--accent) !important;
        outline: 1px solid var(--accent) !important;
    }}

    /* Streamlit Primary & Secondary Buttons */
    .stButton > button {{
        border-radius: 2px !important;
        font-family: var(--font-mono) !important;
        font-size: {TYPOGRAPHY_FOUNDATIONS["scale"]["md"]} !important;
        letter-spacing: 0.06em !important;
        text-transform: uppercase !important;
        padding: 8px 16px !important;
        transition: all var(--fast) ease !important;
        border: 1px solid var(--line) !important;
        background: var(--surface) !important;
        color: var(--chalk) !important;
    }}

    .stButton > button:hover {{
        border-color: var(--accent) !important;
        color: var(--accent) !important;
        background: #172413 !important;
    }}

    .stButton > button:focus-visible {{
        outline: 2px solid var(--accent) !important;
        outline-offset: 2px !important;
    }}

    .stButton > button:active {{
        transform: translateY(1px) !important;
    }}

    /* Primary Accent Button */
    div.stDownloadButton > button,
    div[data-testid="stButton"] > button[kind="primary"] {{
        background: var(--accent) !important;
        color: #080e0a !important;
        font-weight: 700 !important;
        border: 1px solid var(--accent) !important;
    }}

    div.stDownloadButton > button:hover,
    div[data-testid="stButton"] > button[kind="primary"]:hover {{
        background: #b3ff33 !important;
        color: #080e0a !important;
        box-shadow: 0 0 12px rgba(153, 255, 0, 0.3) !important;
    }}

    /* Radio Navigation (Herbarium Cabinet Drawer look) */
    div[data-testid="stRadio"] > div {{
        gap: 2px !important;
    }}

    div[data-testid="stRadio"] label {{
        background: var(--surface) !important;
        border: 1px solid var(--line) !important;
        border-radius: 2px !important;
        padding: 8px 12px !important;
        margin-bottom: 4px !important;
        font-family: var(--font-mono) !important;
        font-size: {TYPOGRAPHY_FOUNDATIONS["scale"]["md"]} !important;
        color: var(--muted) !important;
        transition: all var(--fast) ease !important;
        cursor: pointer;
    }}

    div[data-testid="stRadio"] label:hover {{
        border-color: var(--accent) !important;
        color: var(--chalk) !important;
        background: #152212 !important;
    }}

    div[data-testid="stRadio"] label:has(input:checked) {{
        background: rgba(153, 255, 0, 0.12) !important;
        border-color: var(--accent) !important;
        color: var(--accent) !important;
        font-weight: 600 !important;
    }}

    /* Streamlit Metric Card Styling */
    div[data-testid="stMetric"] {{
        background: var(--surface);
        border: 1px solid var(--line);
        padding: 12px 14px;
        border-radius: 2px;
    }}

    div[data-testid="stMetricLabel"] {{
        font-family: var(--font-mono) !important;
        font-size: {TYPOGRAPHY_FOUNDATIONS["scale"]["sm"]} !important;
        color: var(--muted) !important;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }}

    div[data-testid="stMetricValue"] {{
        font-family: var(--font-body) !important;
        font-size: 18px !important;
        font-weight: 600 !important;
        color: var(--chalk) !important;
    }}

    /* Streamlit Tables & DataFrames */
    div[data-testid="stTable"], .stDataFrame {{
        border: 1px solid var(--line) !important;
        border-radius: 2px !important;
    }}

    table {{
        color: var(--chalk) !important;
        background: var(--surface) !important;
        font-size: {TYPOGRAPHY_FOUNDATIONS["scale"]["lg"]} !important;
    }}

    th {{
        background: #152014 !important;
        color: var(--muted) !important;
        font-family: var(--font-mono) !important;
        font-size: {TYPOGRAPHY_FOUNDATIONS["scale"]["sm"]} !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        border-bottom: 1px solid var(--line) !important;
    }}

    td {{
        border-bottom: 1px solid var(--line-subtle) !important;
    }}

    /* Slider styling */
    div[data-testid="stSlider"] div[data-baseweb="slider"] {{
        color: var(--accent) !important;
    }}

    /* Streamlit Expander */
    .streamlit-expanderHeader {{
        background: var(--surface) !important;
        border: 1px solid var(--line) !important;
        border-radius: 2px !important;
        font-family: var(--font-mono) !important;
        font-size: {TYPOGRAPHY_FOUNDATIONS["scale"]["md"]} !important;
        color: var(--chalk) !important;
    }}

    .streamlit-expanderHeader:hover {{
        border-color: var(--accent) !important;
    }}

    .streamlit-expanderContent {{
        border-left: 1px solid var(--line) !important;
        border-right: 1px solid var(--line) !important;
        border-bottom: 1px solid var(--line) !important;
        background: #0c140d !important;
    }}

    /* SVG Molecular Frame */
    .mol-svg-container {{
        background: #101811;
        border: 1px solid var(--line);
        padding: 12px;
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 300px;
    }}

    .mol-svg-container svg {{
        max-width: 100%;
        height: auto;
    }}

    /* Scientific Disclaimer / Caution Note */
    .scientific-disclaimer {{
        border-left: 2px solid var(--muted);
        background: rgba(16, 24, 17, 0.7);
        padding: 10px 14px;
        margin-top: 14px;
        font-size: {TYPOGRAPHY_FOUNDATIONS["scale"]["md"]};
        color: var(--muted);
        line-height: 1.5;
    }}

    .scientific-disclaimer strong {{
        color: var(--chalk);
    }}
</style>
"""

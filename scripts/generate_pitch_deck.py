import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_deck(output_path="docs/CAT_OperatorIQ_Pitch_Deck.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6] # blank layout

    # Colors
    BG_DARK = RGBColor(15, 17, 21)         # #0F1115
    CARD_BG = RGBColor(24, 27, 34)         # #181B22
    CARD_BORDER = RGBColor(44, 49, 60)     # #2C313C
    CAT_YELLOW = RGBColor(255, 205, 0)     # #FFCD00
    TEXT_WHITE = RGBColor(245, 245, 247)   # #F5F5F7
    TEXT_MUTED = RGBColor(140, 147, 160)   # #8C93A0
    TEXT_DIM = RGBColor(90, 96, 108)       # #5A606C
    CRITICAL_RED = RGBColor(239, 68, 68)   # #EF4444
    SAFE_GREEN = RGBColor(16, 185, 129)    # #10B981

    FONT_FAMILY = "Inter"

    def apply_slide_base(slide, tracker="CAT OPERATORIQ"):
        # Dark background rectangle
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_DARK
        bg.line.color.rgb = BG_DARK

        # Top subtle brand line
        top_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.4), Inches(0.4), Inches(0.04))
        top_line.fill.solid()
        top_line.fill.fore_color.rgb = CAT_YELLOW
        top_line.line.color.rgb = CAT_YELLOW

        # Slide tracker top-left
        tx = slide.shapes.add_textbox(Inches(1.3), Inches(0.32), Inches(6.0), Inches(0.3))
        p = tx.text_frame.paragraphs[0]
        p.text = tracker.upper()
        p.font.name = FONT_FAMILY
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = CAT_YELLOW

        # Footer
        footer_tx = slide.shapes.add_textbox(Inches(0.8), Inches(7.0), Inches(11.733), Inches(0.3))
        fp = footer_tx.text_frame.paragraphs[0]
        fp.text = "CATERPILLAR HACKATHON PITCH  •  OCTOBER 2026"
        fp.font.name = FONT_FAMILY
        fp.font.size = Pt(8)
        fp.font.color.rgb = TEXT_DIM

    def add_header(slide, title, category=None):
        tx = slide.shapes.add_textbox(Inches(0.8), Inches(0.65), Inches(11.733), Inches(1.1))
        tf = tx.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p = tf.paragraphs[0]
        p.text = title
        p.font.name = FONT_FAMILY
        p.font.size = Pt(26)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

    def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
        return card

    # ==========================================================
    # SLIDE 1: COVER
    # ==========================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = BG_DARK
    bg1.line.color.rgb = BG_DARK

    # Yellow brand bar
    bar1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.6), Inches(0.5), Inches(0.06))
    bar1.fill.solid()
    bar1.fill.fore_color.rgb = CAT_YELLOW
    bar1.line.color.rgb = CAT_YELLOW

    # Title Box
    t1 = s1.shapes.add_textbox(Inches(0.8), Inches(1.85), Inches(8.5), Inches(3.0))
    tf1 = t1.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "CAT OperatorIQ"
    p1.font.name = FONT_FAMILY
    p1.font.size = Pt(46)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE

    p1_sub = tf1.add_paragraph()
    p1_sub.text = '"Your intelligent companion for safer and smarter machine operations."'
    p1_sub.font.name = FONT_FAMILY
    p1_sub.font.size = Pt(18)
    p1_sub.font.color.rgb = CAT_YELLOW
    p1_sub.space_before = Pt(12)

    p1_desc = tf1.add_paragraph()
    p1_desc.text = "Real-time in-cab assistance cockpit • 360° Safety Radar • Explainable Risk Scoring • ML Task Forecasting • Offline AI Assistant"
    p1_desc.font.name = FONT_FAMILY
    p1_desc.font.size = Pt(12)
    p1_desc.font.color.rgb = TEXT_MUTED
    p1_desc.space_before = Pt(16)

    # Visual cockpit mockup card on the right
    cockpit_card = add_card(s1, 8.8, 1.6, 3.733, 4.8)
    c_box = s1.shapes.add_textbox(Inches(9.1), Inches(1.9), Inches(3.133), Inches(4.2))
    ctf = c_box.text_frame
    ctf.word_wrap = True
    cp0 = ctf.paragraphs[0]
    cp0.text = "EXC001 • CAT 336"
    cp0.font.name = FONT_FAMILY
    cp0.font.size = Pt(11)
    cp0.font.bold = True
    cp0.font.color.rgb = CAT_YELLOW

    cp1 = ctf.add_paragraph()
    cp1.text = "INTELLIGENT COCKPIT ACTIVE"
    cp1.font.name = FONT_FAMILY
    cp1.font.size = Pt(8.5)
    cp1.font.color.rgb = TEXT_MUTED

    cp2 = ctf.add_paragraph()
    cp2.text = "92%"
    cp2.font.name = FONT_FAMILY
    cp2.font.size = Pt(36)
    cp2.font.bold = True
    cp2.font.color.rgb = TEXT_WHITE
    cp2.space_before = Pt(14)

    cp3 = ctf.add_paragraph()
    cp3.text = "Machine Health Index"
    cp3.font.name = FONT_FAMILY
    cp3.font.size = Pt(9.5)
    cp3.font.color.rgb = TEXT_MUTED

    cp4 = ctf.add_paragraph()
    cp4.text = "360° RADAR: NOMINAL\nCAN-BUS: 1,850 RPM\nTASK: EARTH EXCAVATION\nAI ASSISTANT: READY"
    cp4.font.name = FONT_FAMILY
    cp4.font.size = Pt(9)
    cp4.font.color.rgb = TEXT_MUTED
    cp4.space_before = Pt(20)

    # Footer
    f1 = s1.shapes.add_textbox(Inches(0.8), Inches(6.8), Inches(11.733), Inches(0.4))
    fp1 = f1.text_frame.paragraphs[0]
    fp1.text = "Hackathon Pitch  |  Caterpillar Hackathon 2026"
    fp1.font.name = FONT_FAMILY
    fp1.font.size = Pt(10)
    fp1.font.color.rgb = TEXT_DIM

    # ==========================================================
    # SLIDE 2: THE OPERATOR PROBLEM
    # ==========================================================
    s2 = prs.slides.add_slide(blank_layout)
    apply_slide_base(s2, "01 / THE CHALLENGE")
    add_header(s2, "The machine is connected. The operator still needs help.")

    # 4 Challenge Cards
    challenges = [
        ("BLIND SPOTS", "Excavator swing radius and rear zones obstruct line of sight."),
        ("GROUND WORKERS", "Grade checkers & spotters work inside dangerous machine perimeters."),
        ("MECHANICAL STRAIN", "Hydraulic cavitation, excessive idle, and thermal buildup go unnoticed."),
        ("TIGHT SCHEDULES", "High-pressure cycle times lead to fatigue and rushed movement.")
    ]

    card_w = 2.75
    gap = 0.244
    for i, (title, desc) in enumerate(challenges):
        cx = 0.8 + i * (card_w + gap)
        add_card(s2, cx, 1.85, card_w, 2.5)
        
        # Indicator tag
        tb = s2.shapes.add_textbox(Inches(cx + 0.25), Inches(2.05), Inches(card_w - 0.5), Inches(2.1))
        tbf = tb.text_frame
        tbf.word_wrap = True
        
        p = tbf.paragraphs[0]
        p.text = f"0{i+1}"
        p.font.name = FONT_FAMILY
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = CAT_YELLOW

        p2 = tbf.add_paragraph()
        p2.text = title
        p2.font.name = FONT_FAMILY
        p2.font.size = Pt(13)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_WHITE
        p2.space_before = Pt(8)

        p3 = tbf.add_paragraph()
        p3.text = desc
        p3.font.name = FONT_FAMILY
        p3.font.size = Pt(10.5)
        p3.font.color.rgb = TEXT_MUTED
        p3.space_before = Pt(8)

    # Bottom Core Contrast Card
    contrast_card = add_card(s2, 0.8, 4.65, 11.733, 1.9, CARD_BG, CAT_YELLOW)
    ctb = s2.shapes.add_textbox(Inches(1.2), Inches(4.85), Inches(10.933), Inches(1.5))
    ctbf = ctb.text_frame
    ctbf.word_wrap = True

    cp1 = ctbf.paragraphs[0]
    cp1.text = "TRADITIONAL TELEMATICS"
    cp1.font.name = FONT_FAMILY
    cp1.font.size = Pt(10)
    cp1.font.bold = True
    cp1.font.color.rgb = TEXT_MUTED

    cp2 = ctbf.add_paragraph()
    cp2.text = "Tells the fleet manager what happened hours after failure occurs."
    cp2.font.name = FONT_FAMILY
    cp2.font.size = Pt(13)
    cp2.font.color.rgb = TEXT_WHITE
    cp2.space_before = Pt(3)

    cp3 = ctbf.add_paragraph()
    cp3.text = "CAT OPERATORIQ"
    cp3.font.name = FONT_FAMILY
    cp3.font.size = Pt(10)
    cp3.font.bold = True
    cp3.font.color.rgb = CAT_YELLOW
    cp3.space_before = Pt(10)

    cp4 = ctbf.add_paragraph()
    cp4.text = "Helps the operator understand what is happening right now inside the cab."
    cp4.font.name = FONT_FAMILY
    cp4.font.size = Pt(14)
    cp4.font.bold = True
    cp4.font.color.rgb = TEXT_WHITE
    cp4.space_before = Pt(3)

    # ==========================================================
    # SLIDE 3: THE SOLUTION
    # ==========================================================
    s3 = prs.slides.add_slide(blank_layout)
    apply_slide_base(s3, "02 / THE SOLUTION")
    add_header(s3, "Meet CAT OperatorIQ")

    # 4 Core Pillars 2x2 Grid
    pillars = [
        ("01", "360° Safety Radar", "Real-Time Worker Proximity", "Dynamic 3-zone exclusion boundary (<3m, 3–6m, >6m) tracking ground personnel around swing perimeters."),
        ("02", "Multi-Rule Safety Engine", "Explainable 0–100 Risk Index", "Evaluates 8 simultaneous mechanical and proximity safety rules to generate transparent, verifiable alerts."),
        ("03", "ML Task Prediction", "ETA + 90% Confidence Interval", "Gradient Boosting model forecasting cycle times with contributing site, weather, and operator factors."),
        ("04", "AI Operator Assistant", "Offline-Ready In-Cab Guidance", "Grounded query assistant delivering immediate machine evidence and operating manual citations.")
    ]

    p_w = 5.72
    p_h = 2.05
    for i, (num, title, subtitle, desc) in enumerate(pillars):
        row = i // 2
        col = i % 2
        px = 0.8 + col * (p_w + 0.293)
        py = 1.85 + row * (p_h + 0.22)

        add_card(s3, px, py, p_w, p_h)
        ptb = s3.shapes.add_textbox(Inches(px + 0.3), Inches(py + 0.2), Inches(p_w - 0.6), Inches(p_h - 0.4))
        ptbf = ptb.text_frame
        ptbf.word_wrap = True

        p = ptbf.paragraphs[0]
        p.text = f"{num}  •  {subtitle.upper()}"
        p.font.name = FONT_FAMILY
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = CAT_YELLOW

        p2 = ptbf.add_paragraph()
        p2.text = title
        p2.font.name = FONT_FAMILY
        p2.font.size = Pt(14)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_WHITE
        p2.space_before = Pt(4)

        p3 = ptbf.add_paragraph()
        p3.text = desc
        p3.font.name = FONT_FAMILY
        p3.font.size = Pt(10)
        p3.font.color.rgb = TEXT_MUTED
        p3.space_before = Pt(6)

    # Prominent bottom banner: ASSISTANCE, NOT CONTROL
    bot_card = add_card(s3, 0.8, 6.35, 11.733, 0.55, CARD_BG, CARD_BORDER)
    btb = s3.shapes.add_textbox(Inches(1.0), Inches(6.42), Inches(11.333), Inches(0.4))
    btf = btb.text_frame
    bp = btf.paragraphs[0]
    bp.text = "ASSISTANCE, NOT CONTROL  —  OperatorIQ never overrides machine controls. It empowers professional operator judgment."
    bp.font.name = FONT_FAMILY
    bp.font.size = Pt(10)
    bp.font.bold = True
    bp.font.color.rgb = CAT_YELLOW

    # ==========================================================
    # SLIDE 4: HOW IT WORKS
    # ==========================================================
    s4 = prs.slides.add_slide(blank_layout)
    apply_slide_base(s4, "03 / SYSTEM ARCHITECTURE")
    add_header(s4, "From machine signals → actionable decisions")

    # 3 Horizontal Stages
    stages = [
        ("STAGE 01", "MACHINE & SITE DATA", [
            "CAN-Bus Telemetry (RPM, Temp, Oil, Vibration)",
            "Task Context (Cycles, Load, Priority)",
            "Operator Profile & Historical Skill",
            "Environment & Live Weather Telemetry"
        ]),
        ("STAGE 02", "OPERATORIQ INTELLIGENCE", [
            "Rule Engine: 8-Factor 0–100 Risk Score",
            "ML Pipeline: Gradient Boosting ETA Regressor",
            "Anomaly Detection: Unsupervised Isolation Forest",
            "Offline Assistant: Grounded RAG + Manual Guides"
        ]),
        ("STAGE 03", "ACTIONABLE OUTPUT", [
            "In-Cab HUD Alerts & Audio-Visual Warning",
            "Dynamic Task ETA & Confidence Bounds",
            "Anti-Idling & Maintenance Recommendations",
            "Shift Audit Logs & Fleet Supervisor Portal"
        ])
    ]

    st_w = 3.65
    st_gap = 0.39
    for i, (tag, title, bullets) in enumerate(stages):
        sx = 0.8 + i * (st_w + st_gap)
        is_middle = (i == 1)
        border_c = CAT_YELLOW if is_middle else CARD_BORDER
        add_card(s4, sx, 1.85, st_w, 4.6, CARD_BG, border_c)

        stb = s4.shapes.add_textbox(Inches(sx + 0.3), Inches(2.1), Inches(st_w - 0.6), Inches(4.1))
        stf = stb.text_frame
        stf.word_wrap = True

        p = stf.paragraphs[0]
        p.text = tag
        p.font.name = FONT_FAMILY
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = CAT_YELLOW

        p2 = stf.add_paragraph()
        p2.text = title
        p2.font.name = FONT_FAMILY
        p2.font.size = Pt(13)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_WHITE
        p2.space_before = Pt(6)

        for b in bullets:
            pb = stf.add_paragraph()
            pb.text = f"•  {b}"
            pb.font.name = FONT_FAMILY
            pb.font.size = Pt(10)
            pb.font.color.rgb = TEXT_MUTED
            pb.space_before = Pt(12)

    # Arrows between blocks
    for ax in [4.52, 8.56]:
        atx = s4.shapes.add_textbox(Inches(ax), Inches(3.9), Inches(0.4), Inches(0.4))
        ap = atx.text_frame.paragraphs[0]
        ap.text = "→"
        ap.font.name = FONT_FAMILY
        ap.font.size = Pt(22)
        ap.font.bold = True
        ap.font.color.rgb = CAT_YELLOW

    # ==========================================================
    # SLIDE 5: THE DATA + AI ENGINE
    # ==========================================================
    s5 = prs.slides.add_slide(blank_layout)
    apply_slide_base(s5, "04 / DATA & ML MODELS")
    add_header(s5, "Built on data. Designed for explainability.")

    # Top Row: 4 Metric Cards
    metrics = [
        ("10,000", "Synthetic Telemetry Records", "Engine, hydraulics, vibration, idle"),
        ("2,000", "Task Records", "Cycles, payload, site conditions"),
        ("500", "Safety Events", "Proximity, fatigue, seatbelt breaches"),
        ("300", "Incident Records", "Resolved logs & coordinates")
    ]

    mw = 2.75
    for i, (num, label, desc) in enumerate(metrics):
        mx = 0.8 + i * (mw + 0.244)
        add_card(s5, mx, 1.85, mw, 1.7)
        mtb = s5.shapes.add_textbox(Inches(mx + 0.25), Inches(1.95), Inches(mw - 0.5), Inches(1.5))
        mtf = mtb.text_frame
        mtf.word_wrap = True

        p = mtf.paragraphs[0]
        p.text = num
        p.font.name = FONT_FAMILY
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = CAT_YELLOW

        p2 = mtf.add_paragraph()
        p2.text = label
        p2.font.name = FONT_FAMILY
        p2.font.size = Pt(10.5)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_WHITE

        p3 = mtf.add_paragraph()
        p3.text = desc
        p3.font.name = FONT_FAMILY
        p3.font.size = Pt(8.5)
        p3.font.color.rgb = TEXT_MUTED

    # Bottom Left: Isolation Forest Card
    add_card(s5, 0.8, 3.8, 5.72, 2.7)
    iftb = s5.shapes.add_textbox(Inches(1.1), Inches(4.0), Inches(5.12), Inches(2.3))
    iftf = iftb.text_frame
    iftf.word_wrap = True
    ip = iftf.paragraphs[0]
    ip.text = "UNSUPERVISED ANOMALY DETECTION"
    ip.font.name = FONT_FAMILY
    ip.font.size = Pt(9.5)
    ip.font.bold = True
    ip.font.color.rgb = CAT_YELLOW

    ip2 = iftf.add_paragraph()
    ip2.text = "Isolation Forest Pipeline"
    ip2.font.name = FONT_FAMILY
    ip2.font.size = Pt(16)
    ip2.font.bold = True
    ip2.font.color.rgb = TEXT_WHITE
    ip2.space_before = Pt(4)

    ip3 = iftf.add_paragraph()
    ip3.text = "• Identifies multi-dimensional telemetry degradation\n• Evaluates vibration, thermal spikes, and excessive idle\n• Grounded baseline comparison against machine class"
    ip3.font.name = FONT_FAMILY
    ip3.font.size = Pt(10.5)
    ip3.font.color.rgb = TEXT_MUTED
    ip3.space_before = Pt(8)

    # Bottom Right: Gradient Boosting Regressor Card
    add_card(s5, 6.813, 3.8, 5.72, 2.7)
    gbtb = s5.shapes.add_textbox(Inches(7.113), Inches(4.0), Inches(5.12), Inches(2.3))
    gbtf = gbtb.text_frame
    gbtf.word_wrap = True
    gp = gbtf.paragraphs[0]
    gp.text = "SUPERVISED DURATION REGRESSION"
    gp.font.name = FONT_FAMILY
    gp.font.size = Pt(9.5)
    gp.font.bold = True
    gp.font.color.rgb = CAT_YELLOW

    gp2 = gbtf.add_paragraph()
    gp2.text = "Gradient Boosting Regressor"
    gp2.font.name = FONT_FAMILY
    gp2.font.size = Pt(16)
    gp2.font.bold = True
    gp2.font.color.rgb = TEXT_WHITE
    gp2.space_before = Pt(4)

    gp3 = gbtf.add_paragraph()
    gp3.text = "R² = 0.964    •    MAE = 4.13 min"
    gp3.font.name = FONT_FAMILY
    gp3.font.size = Pt(18)
    gp3.font.bold = True
    gp3.font.color.rgb = CAT_YELLOW
    gp3.space_before = Pt(10)

    gp4 = gbtf.add_paragraph()
    gp4.text = "Deterministic synthetic dataset • seed 42 • Non-linear wear curves"
    gp4.font.name = FONT_FAMILY
    gp4.font.size = Pt(9.5)
    gp4.font.color.rgb = TEXT_MUTED
    gp4.space_before = Pt(6)

    # ==========================================================
    # SLIDE 6: SAFETY RADAR
    # ==========================================================
    s6 = prs.slides.add_slide(blank_layout)
    apply_slide_base(s6, "05 / PERIMETER DEFENSE")
    add_header(s6, "See the hazard before it becomes an incident.")

    # Left: Radar Visual Card
    radar_card = add_card(s6, 0.8, 1.85, 6.5, 4.65)
    rtb = s6.shapes.add_textbox(Inches(1.1), Inches(2.05), Inches(5.9), Inches(4.25))
    rtf = rtb.text_frame
    rtf.word_wrap = True

    rp0 = rtf.paragraphs[0]
    rp0.text = "360° LIVE EXCLUSION RADAR"
    rp0.font.name = FONT_FAMILY
    rp0.font.size = Pt(10)
    rp0.font.bold = True
    rp0.font.color.rgb = CAT_YELLOW

    rp1 = rtf.add_paragraph()
    rp1.text = "HAZARD DETECTED: WORKER C"
    rp1.font.name = FONT_FAMILY
    rp1.font.size = Pt(20)
    rp1.font.bold = True
    rp1.font.color.rgb = CRITICAL_RED
    rp1.space_before = Pt(8)

    rp2 = rtf.add_paragraph()
    rp2.text = "Distance: 2.1 m  •  Bearing: 118° SE  •  Zone: Critical (<3m)"
    rp2.font.name = FONT_FAMILY
    rp2.font.size = Pt(11)
    rp2.font.color.rgb = TEXT_WHITE
    rp2.space_before = Pt(4)

    # Radar concentric circles representation
    rp3 = rtf.add_paragraph()
    rp3.text = "\n[CRITICAL ZONE: < 3.0 m]  →  IMMEDIATE HYDRAULIC SWING ALERT\n[WARNING ZONE:  3.0 – 6.0 m] →  AUDIO CHIME & OPERATOR HUD BADGE\n[SAFE ZONE:     > 6.0 m]     →  NOMINAL PERIMETER MONITORING"
    rp3.font.name = FONT_FAMILY
    rp3.font.size = Pt(10.5)
    rp3.font.color.rgb = TEXT_MUTED
    rp3.space_before = Pt(18)

    # Right: Critical Risk Alert Card
    add_card(s6, 7.6, 1.85, 4.933, 4.65, CARD_BG, CRITICAL_RED)
    actb = s6.shapes.add_textbox(Inches(7.9), Inches(2.1), Inches(4.333), Inches(4.15))
    actf = actb.text_frame
    actf.word_wrap = True

    ap0 = actf.paragraphs[0]
    ap0.text = "CRITICAL ALERT"
    ap0.font.name = FONT_FAMILY
    ap0.font.size = Pt(11)
    ap0.font.bold = True
    ap0.font.color.rgb = CRITICAL_RED

    ap1 = actf.add_paragraph()
    ap1.text = "88 / 100"
    ap1.font.name = FONT_FAMILY
    ap1.font.size = Pt(44)
    ap1.font.bold = True
    ap1.font.color.rgb = TEXT_WHITE
    ap1.space_before = Pt(6)

    ap2 = actf.add_paragraph()
    ap2.text = "Composite Risk Index"
    ap2.font.name = FONT_FAMILY
    ap2.font.size = Pt(10)
    ap2.font.color.rgb = TEXT_MUTED

    ap3 = actf.add_paragraph()
    ap3.text = "Ground worker detected inside the critical proximity zone (< 3m)."
    ap3.font.name = FONT_FAMILY
    ap3.font.size = Pt(12)
    ap3.font.bold = True
    ap3.font.color.rgb = TEXT_WHITE
    ap3.space_before = Pt(18)

    ap4 = actf.add_paragraph()
    ap4.text = "Recommended Next Step:\nPause excavator boom and swing motion immediately. Establish direct eye contact with ground worker before resuming."
    ap4.font.name = FONT_FAMILY
    ap4.font.size = Pt(10.5)
    ap4.font.color.rgb = TEXT_MUTED
    ap4.space_before = Pt(12)

    # ==========================================================
    # SLIDE 7: EXPLAINABLE SAFETY ENGINE
    # ==========================================================
    s7 = prs.slides.add_slide(blank_layout)
    apply_slide_base(s7, "06 / TRANSPARENT AI")
    add_header(s7, "Every risk score has a reason.")

    # 8 Safety Condition Chips in 2 columns
    conditions_col1 = [
        ("Seatbelt Compliance", "Status: Fastened (+0) or Unfastened (+35)"),
        ("Worker Proximity", "Distance <3m (+45), 3-6m (+20), >6m (+0)"),
        ("Operator Fatigue", "Fatigue index >= 0.70 adds up to +30 risk"),
        ("Engine Temperature", "Overheating above 98°C adds +25 risk")
    ]
    conditions_col2 = [
        ("Machine Vibration", "Spikes >2.4 mm/s indicate cavitation (+20)"),
        ("Excessive Idling", "Idle time >30 min flags cycle waste (+15)"),
        ("Recent Safety Events", "Unacknowledged breaches within 24h (+20)"),
        ("Weather & Load", "Heavy rainfall + payload over 18t (+15)")
    ]

    col_w = 4.35
    for col_idx, col_items in enumerate([conditions_col1, conditions_col2]):
        for row_idx, (title, detail) in enumerate(col_items):
            cx = 0.8 + col_idx * (col_w + 0.3)
            cy = 1.85 + row_idx * 1.15
            add_card(s7, cx, cy, col_w, 0.95)

            ctb = s7.shapes.add_textbox(Inches(cx + 0.2), Inches(cy + 0.12), Inches(col_w - 0.4), Inches(0.75))
            ctf = ctb.text_frame
            ctf.word_wrap = True

            p = ctf.paragraphs[0]
            p.text = title
            p.font.name = FONT_FAMILY
            p.font.size = Pt(11)
            p.font.bold = True
            p.font.color.rgb = TEXT_WHITE

            p2 = ctf.add_paragraph()
            p2.text = detail
            p2.font.name = FONT_FAMILY
            p2.font.size = Pt(9)
            p2.font.color.rgb = TEXT_MUTED

    # Right: Pipeline Visual Card
    pipe_card = add_card(s7, 10.05, 1.85, 2.483, 4.65, CARD_BG, CAT_YELLOW)
    ptb = s7.shapes.add_textbox(Inches(10.2), Inches(2.1), Inches(2.183), Inches(4.15))
    ptf = ptb.text_frame
    ptf.word_wrap = True

    pp0 = ptf.paragraphs[0]
    pp0.text = "SAFETY PIPELINE"
    pp0.font.name = FONT_FAMILY
    pp0.font.size = Pt(9.5)
    pp0.font.bold = True
    pp0.font.color.rgb = CAT_YELLOW

    steps = [
        ("INPUT SIGNALS", "CAN-bus + Radar + Weather"),
        ("RULE EVALUATION", "8 Transparent Rules"),
        ("RISK SCORE", "0 – 100 Index"),
        ("ACTIONABLE ALERT", "Instant HUD Advisory")
    ]

    for st_title, st_sub in steps:
        sp1 = ptf.add_paragraph()
        sp1.text = st_title
        sp1.font.name = FONT_FAMILY
        sp1.font.size = Pt(11)
        sp1.font.bold = True
        sp1.font.color.rgb = TEXT_WHITE
        sp1.space_before = Pt(14)

        sp2 = ptf.add_paragraph()
        sp2.text = st_sub
        sp2.font.name = FONT_FAMILY
        sp2.font.size = Pt(8.5)
        sp2.font.color.rgb = TEXT_MUTED

    # ==========================================================
    # SLIDE 8: TASK PREDICTION
    # ==========================================================
    s8 = prs.slides.add_slide(blank_layout)
    apply_slide_base(s8, "07 / TASK INTELLIGENCE")
    add_header(s8, "Not just an ETA. An explanation.")

    # Left: Task T001 Prediction Card
    add_card(s8, 0.8, 1.85, 5.72, 4.65)
    ttb = s8.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(5.12), Inches(4.15))
    ttf = ttb.text_frame
    ttf.word_wrap = True

    tp0 = ttf.paragraphs[0]
    tp0.text = "TASK T001  •  ACTIVE EXECUTION"
    tp0.font.name = FONT_FAMILY
    tp0.font.size = Pt(10)
    tp0.font.bold = True
    tp0.font.color.rgb = CAT_YELLOW

    tp1 = ttf.add_paragraph()
    tp1.text = "Earth Excavation & Trenching"
    tp1.font.name = FONT_FAMILY
    tp1.font.size = Pt(18)
    tp1.font.bold = True
    tp1.font.color.rgb = TEXT_WHITE
    tp1.space_before = Pt(4)

    tp2 = ttf.add_paragraph()
    tp2.text = "54 min"
    tp2.font.name = FONT_FAMILY
    tp2.font.size = Pt(48)
    tp2.font.bold = True
    tp2.font.color.rgb = CAT_YELLOW
    tp2.space_before = Pt(16)

    tp3 = ttf.add_paragraph()
    tp3.text = "PROJECTED COMPLETION ETA"
    tp3.font.name = FONT_FAMILY
    tp3.font.size = Pt(9.5)
    tp3.font.bold = True
    tp3.font.color.rgb = TEXT_MUTED

    tp4 = ttf.add_paragraph()
    tp4.text = "90% Confidence Interval:  48 – 61 minutes"
    tp4.font.name = FONT_FAMILY
    tp4.font.size = Pt(12)
    tp4.font.bold = True
    tp4.font.color.rgb = TEXT_WHITE
    tp4.space_before = Pt(12)

    tp5 = ttf.add_paragraph()
    tp5.text = "Model: Gradient Boosting Regressor  (R² = 0.964, MAE = 4.13 min)"
    tp5.font.name = FONT_FAMILY
    tp5.font.size = Pt(9.5)
    tp5.font.color.rgb = TEXT_MUTED
    tp5.space_before = Pt(8)

    # Right: Contributing Factors Explanation Card
    add_card(s8, 6.813, 1.85, 5.72, 4.65)
    ftb = s8.shapes.add_textbox(Inches(7.113), Inches(2.1), Inches(5.12), Inches(4.15))
    ftf = ftb.text_frame
    ftf.word_wrap = True

    fp0 = ftf.paragraphs[0]
    fp0.text = "EXPLAINABLE ML CONTRIBUTIONS"
    fp0.font.name = FONT_FAMILY
    fp0.font.size = Pt(10)
    fp0.font.bold = True
    fp0.font.color.rgb = CAT_YELLOW

    fp1 = ftf.add_paragraph()
    fp1.text = "Why is this task predicted at 54 minutes?"
    fp1.font.name = FONT_FAMILY
    fp1.font.size = Pt(15)
    fp1.font.bold = True
    fp1.font.color.rgb = TEXT_WHITE
    fp1.space_before = Pt(6)

    factors = [
        ("Base Task Duration", "53.0 min", "Standard Earth Excavation baseline", TEXT_WHITE),
        ("Wet Ground Conditions", "+7.5 min", "Soil friction & reduced traction in rain", CRITICAL_RED),
        ("Operator Experience (Expert)", "-6.5 min", "Marcus Vance historical efficiency bonus", SAFE_GREEN),
        ("Machine Age Factor", "+0.0 min", "CAT 336 in optimal maintenance bracket", TEXT_MUTED)
    ]

    for f_title, f_val, f_sub, f_col in factors:
        p_f1 = ftf.add_paragraph()
        p_f1.text = f"{f_title}  →  {f_val}"
        p_f1.font.name = FONT_FAMILY
        p_f1.font.size = Pt(11)
        p_f1.font.bold = True
        p_f1.font.color.rgb = f_col
        p_f1.space_before = Pt(10)

        p_f2 = ftf.add_paragraph()
        p_f2.text = f_sub
        p_f2.font.name = FONT_FAMILY
        p_f2.font.size = Pt(9)
        p_f2.font.color.rgb = TEXT_MUTED

    # ==========================================================
    # SLIDE 9: ANOMALY DETECTION
    # ==========================================================
    s9 = prs.slides.add_slide(blank_layout)
    apply_slide_base(s9, "08 / MECHANICAL HEALTH")
    add_header(s9, "Detect unusual machine behavior early.")

    # Left: Telemetry Monitoring Grid
    add_card(s9, 0.8, 1.85, 6.8, 4.65)
    tmtb = s9.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(6.2), Inches(4.15))
    tmtf = tmtb.text_frame
    tmtf.word_wrap = True

    tp0 = tmtf.paragraphs[0]
    tp0.text = "LIVE TELEMETRY STREAMS"
    tp0.font.name = FONT_FAMILY
    tp0.font.size = Pt(10)
    tp0.font.bold = True
    tp0.font.color.rgb = CAT_YELLOW

    signals = [
        ("Engine Temperature", "91.2 °C", "Nominal range (85 – 95 °C)"),
        ("Engine Oil Pressure", "42.1 psi", "Nominal range (40 – 50 psi)"),
        ("Hydraulic Pump Pressure", "285 bar", "Nominal range (250 – 320 bar)"),
        ("Engine RPM", "1,850 RPM", "Full operational load cycle"),
        ("Vibration Baseline", "2.35 mm/s", "CRITICAL: +32% above 1.75 baseline"),
        ("Excessive Idling", "41.0 min", "WARNING: 41 min above shift threshold")
    ]

    for s_name, s_val, s_note in signals:
        is_bad = "+" in s_note or "CRITICAL" in s_note
        val_color = CRITICAL_RED if is_bad else TEXT_WHITE

        sp1 = tmtf.add_paragraph()
        sp1.text = f"•  {s_name}: {s_val}  —  {s_note}"
        sp1.font.name = FONT_FAMILY
        sp1.font.size = Pt(10)
        sp1.font.color.rgb = val_color
        sp1.space_before = Pt(8)

    # Right: Anomaly Detected Card
    add_card(s9, 7.9, 1.85, 4.633, 4.65, CARD_BG, CAT_YELLOW)
    adtb = s9.shapes.add_textbox(Inches(8.2), Inches(2.1), Inches(4.033), Inches(4.15))
    adtf = adtb.text_frame
    adtf.word_wrap = True

    ap0 = adtf.paragraphs[0]
    ap0.text = "ANOMALY DETECTED"
    ap0.font.name = FONT_FAMILY
    ap0.font.size = Pt(11)
    ap0.font.bold = True
    ap0.font.color.rgb = CAT_YELLOW

    ap1 = adtf.add_paragraph()
    ap1.text = "Vibration & Idle Spike"
    ap1.font.name = FONT_FAMILY
    ap1.font.size = Pt(18)
    ap1.font.bold = True
    ap1.font.color.rgb = TEXT_WHITE
    ap1.space_before = Pt(4)

    ap2 = adtf.add_paragraph()
    ap2.text = "+32% Vibration\n41 min Excessive Idle"
    ap2.font.name = FONT_FAMILY
    ap2.font.size = Pt(16)
    ap2.font.bold = True
    ap2.font.color.rgb = CRITICAL_RED
    ap2.space_before = Pt(12)

    ap3 = adtf.add_paragraph()
    ap3.text = "THE PIPELINE IN ACTION:"
    ap3.font.name = FONT_FAMILY
    ap3.font.size = Pt(9.5)
    ap3.font.bold = True
    ap3.font.color.rgb = CAT_YELLOW
    ap3.space_before = Pt(14)

    ap4 = adtf.add_paragraph()
    ap4.text = "Detection → Isolation Forest flag\nExplanation → Vibration + Idle factors\nRecommendation → Hydraulic inspection"
    ap4.font.name = FONT_FAMILY
    ap4.font.size = Pt(11)
    ap4.font.color.rgb = TEXT_WHITE
    ap4.space_before = Pt(6)

    # ==========================================================
    # SLIDE 10: OPERATOR ASSISTANT
    # ==========================================================
    s10 = prs.slides.add_slide(blank_layout)
    apply_slide_base(s10, "09 / IN-CAB ASSISTANT")
    add_header(s10, "Ask the machine. Get evidence, not guesses.")

    # Left: Conversational UI Card
    add_card(s10, 0.8, 1.85, 7.8, 4.65)
    cuitb = s10.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(7.2), Inches(4.15))
    cuitf = cuitb.text_frame
    cuitf.word_wrap = True

    up = cuitf.paragraphs[0]
    up.text = 'OPERATOR QUERY:'
    up.font.name = FONT_FAMILY
    up.font.size = Pt(9.5)
    up.font.bold = True
    up.font.color.rgb = CAT_YELLOW

    up2 = cuitf.add_paragraph()
    up2.text = '"Why is EXC001 showing a warning?"'
    up2.font.name = FONT_FAMILY
    up2.font.size = Pt(15)
    up2.font.bold = True
    up2.font.color.rgb = TEXT_WHITE
    up2.space_before = Pt(4)

    ap = cuitf.add_paragraph()
    ap.text = 'GROUND TRUTH EVIDENCE:'
    ap.font.name = FONT_FAMILY
    ap.font.size = Pt(9.5)
    ap.font.bold = True
    ap.font.color.rgb = CAT_YELLOW
    ap.space_before = Pt(16)

    ap2 = cuitf.add_paragraph()
    ap2.text = "• Vibration is 32% above machine baseline (2.35 mm/s vs 1.75 mm/s)\n• Ground worker detected at 2.1 meters inside the exclusion zone\n• Recommended Next Step: Pause swing, inspect hydraulic mount, alert supervisor\n• Grounded Citation: CAT 336 Heavy Duty Excavator Operations Guide, Section 4.2"
    ap2.font.name = FONT_FAMILY
    ap2.font.size = Pt(10.5)
    ap2.font.color.rgb = TEXT_WHITE
    ap2.space_before = Pt(6)

    ap3 = cuitf.add_paragraph()
    ap3.text = "Advisory assistance only — does not control machine functions."
    ap3.font.name = FONT_FAMILY
    ap3.font.size = Pt(8.5)
    ap3.font.color.rgb = TEXT_MUTED
    ap3.space_before = Pt(16)

    # Right: Offline-Ready Card
    add_card(s10, 8.9, 1.85, 3.633, 4.65, CARD_BG, CARD_BORDER)
    ortb = s10.shapes.add_textbox(Inches(9.15), Inches(2.1), Inches(3.133), Inches(4.15))
    ortf = ortb.text_frame
    ortf.word_wrap = True

    op0 = ortf.paragraphs[0]
    op0.text = "OFFLINE-READY"
    op0.font.name = FONT_FAMILY
    op0.font.size = Pt(11)
    op0.font.bold = True
    op0.font.color.rgb = CAT_YELLOW

    op1 = ortf.add_paragraph()
    op1.text = "Zero Cloud Dependency"
    op1.font.name = FONT_FAMILY
    op1.font.size = Pt(16)
    op1.font.bold = True
    op1.font.color.rgb = TEXT_WHITE
    op1.space_before = Pt(4)

    op2 = ortf.add_paragraph()
    op2.text = "• Fully operational on remote job sites without internet connectivity\n• Rule-grounded offline fallback\n• Direct access to machine manuals\n• No paid cloud API fees required"
    op2.font.name = FONT_FAMILY
    op2.font.size = Pt(10)
    op2.font.color.rgb = TEXT_MUTED
    op2.space_before = Pt(12)

    # ==========================================================
    # SLIDE 11: LIVE DEMO FLOW
    # ==========================================================
    s11 = prs.slides.add_slide(blank_layout)
    apply_slide_base(s11, "10 / PRODUCT DEMO")
    add_header(s11, "One shift. One operator. One intelligent cockpit.")

    demo_steps = [
        ("1. LOGIN", "Marcus Vance logs into EXC001 (CAT 336)"),
        ("2. DASHBOARD", "92% Health, 1,850 RPM live telemetry"),
        ("3. TASK ETA", "Task T001 ETA 54 min (48–61 min band)"),
        ("4. HAZARD", "Worker C at 2.1m triggers Critical 88/100"),
        ("5. INCIDENT", "INC001 automatically logged with GPS"),
        ("6. ASSISTANT", "Explains vibration & worker evidence"),
        ("7. TRAINING", "3-question Proximity quiz completed"),
        ("8. SUPERVISOR", "Fleet view & PDF shift compliance report")
    ]

    card_w11 = 2.75
    card_h11 = 2.05
    for i, (title, desc) in enumerate(demo_steps):
        row = i // 4
        col = i % 4
        dx = 0.8 + col * (card_w11 + 0.244)
        dy = 1.85 + row * (card_h11 + 0.25)

        border_c = CAT_YELLOW if i in [3, 5] else CARD_BORDER
        add_card(s11, dx, dy, card_w11, card_h11, CARD_BG, border_c)

        dtb = s11.shapes.add_textbox(Inches(dx + 0.2), Inches(dy + 0.15), Inches(card_w11 - 0.4), Inches(card_h11 - 0.3))
        dtf = dtb.text_frame
        dtf.word_wrap = True

        p = dtf.paragraphs[0]
        p.text = title
        p.font.name = FONT_FAMILY
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = CAT_YELLOW

        p2 = dtf.add_paragraph()
        p2.text = desc
        p2.font.name = FONT_FAMILY
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_WHITE
        p2.space_before = Pt(6)

    # ==========================================================
    # SLIDE 12: OPERATOR -> SUPERVISOR
    # ==========================================================
    s12 = prs.slides.add_slide(blank_layout)
    apply_slide_base(s12, "11 / DUAL PERSPECTIVE")
    add_header(s12, "One platform. Two perspectives.")

    # Left: Operator Cockpit
    add_card(s12, 0.8, 1.85, 5.72, 4.65)
    optb = s12.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(5.12), Inches(4.15))
    optf = optb.text_frame
    optf.word_wrap = True

    op_p0 = optf.paragraphs[0]
    op_p0.text = "IN-CAB COCKPIT VIEW"
    op_p0.font.name = FONT_FAMILY
    op_p0.font.size = Pt(10)
    op_p0.font.bold = True
    op_p0.font.color.rgb = CAT_YELLOW

    op_p1 = optf.add_paragraph()
    op_p1.text = "OPERATOR: MARCUS VANCE"
    op_p1.font.name = FONT_FAMILY
    op_p1.font.size = Pt(16)
    op_p1.font.bold = True
    op_p1.font.color.rgb = TEXT_WHITE
    op_p1.space_before = Pt(4)

    op_items = [
        "Live Machine Health (92% composite indicator)",
        "360° Safety Radar with worker exclusion tracking",
        "Explainable Task ETA with weather & skill contributions",
        "Conversational In-Cab Assistant for ground truth answers",
        "Interactive Training Hub with instant quiz certification"
    ]
    for it in op_items:
        ip = optf.add_paragraph()
        ip.text = f"•  {it}"
        ip.font.name = FONT_FAMILY
        ip.font.size = Pt(10)
        ip.font.color.rgb = TEXT_MUTED
        ip.space_before = Pt(8)

    # Right: Supervisor Portal
    add_card(s12, 6.813, 1.85, 5.72, 4.65)
    sptb = s12.shapes.add_textbox(Inches(7.113), Inches(2.1), Inches(5.12), Inches(4.15))
    sptf = sptb.text_frame
    sptf.word_wrap = True

    sp_p0 = sptf.paragraphs[0]
    sp_p0.text = "FLEET SUPERVISOR PORTAL"
    sp_p0.font.name = FONT_FAMILY
    sp_p0.font.size = Pt(10)
    sp_p0.font.bold = True
    sp_p0.font.color.rgb = CAT_YELLOW

    sp_p1 = sptf.add_paragraph()
    sp_p1.text = "SITE SUPERVISOR / FLEET LEAD"
    sp_p1.font.name = FONT_FAMILY
    sp_p1.font.size = Pt(16)
    sp_p1.font.bold = True
    sp_p1.font.color.rgb = TEXT_WHITE
    sp_p1.space_before = Pt(4)

    sp_items = [
        "Fleet-Wide Machine Health & Utilization Overview",
        "Site Anomaly Distribution & Heatmaps across assets",
        "Automated Incident Sign-Off & Resolution Tracking",
        "Official PDF Compliance Shift Reports for OSHA audits",
        "Operator Curriculum Progress & Safety Certification records"
    ]
    for it in sp_items:
        ip = sptf.add_paragraph()
        ip.text = f"•  {it}"
        ip.font.name = FONT_FAMILY
        ip.font.size = Pt(10)
        ip.font.color.rgb = TEXT_MUTED
        ip.space_before = Pt(8)

    # ==========================================================
    # SLIDE 13: BUSINESS IMPACT
    # ==========================================================
    s13 = prs.slides.add_slide(blank_layout)
    apply_slide_base(s13, "12 / MEASURABLE VALUE")
    add_header(s13, "Designed for measurable operational impact.")

    impacts = [
        ("ZERO", "Proximity Struck-By Fatalities", "Proactive 360° exclusion radar alerts operators instantly before personnel breach swing hazard zones."),
        ("12%", "Reduction in Unnecessary Fuel Burn", "Anti-idling recommendations and automated cycle optimization prevent wasted fuel hours."),
        ("↓", "Unscheduled Machine Downtime", "Early mechanical vibration and thermal anomaly diagnostics detect failure signatures shifts in advance.")
    ]

    imp_w = 3.65
    imp_gap = 0.39
    for i, (metric, title, desc) in enumerate(impacts):
        ix = 0.8 + i * (imp_w + imp_gap)
        add_card(s13, ix, 1.85, imp_w, 4.65)

        itb = s13.shapes.add_textbox(Inches(ix + 0.3), Inches(2.2), Inches(imp_w - 0.6), Inches(4.0))
        itf = itb.text_frame
        itf.word_wrap = True

        p = itf.paragraphs[0]
        p.text = metric
        p.font.name = FONT_FAMILY
        p.font.size = Pt(54)
        p.font.bold = True
        p.font.color.rgb = CAT_YELLOW

        p2 = itf.add_paragraph()
        p2.text = title
        p2.font.name = FONT_FAMILY
        p2.font.size = Pt(14)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_WHITE
        p2.space_before = Pt(12)

        p3 = itf.add_paragraph()
        p3.text = desc
        p3.font.name = FONT_FAMILY
        p3.font.size = Pt(10.5)
        p3.font.color.rgb = TEXT_MUTED
        p3.space_before = Pt(10)

    # ==========================================================
    # SLIDE 14: FUTURE VISION
    # ==========================================================
    s14 = prs.slides.add_slide(blank_layout)
    apply_slide_base(s14, "13 / FUTURE ROADMAP")
    add_header(s14, "Built for today's prototype. Ready for tomorrow's machine.")

    roadmap = [
        ("TODAY", "OperatorIQ Prototype", "Full-stack simulation cockpit, dual DB, 8-rule safety engine, Gradient Boosting ETA, offline assistant."),
        ("NEXT", "CAT Product Link™ Integration", "Direct integration with Caterpillar OEM telematics hardware and standard ISO 15143-3 fleet feeds."),
        ("EDGE", "On-Machine TPU Inference", "Deploy ML regressor and unsupervised anomaly pipeline to in-cab edge hardware for microsecond latency."),
        ("VISION", "Stereo Computer Vision", "Integrate depth cameras and 3D LiDAR for automated ground worker bounding-box distance extraction.")
    ]

    rw = 2.75
    for i, (phase, title, desc) in enumerate(roadmap):
        rx = 0.8 + i * (rw + 0.244)
        is_today = (i == 0)
        border_c = CAT_YELLOW if is_today else CARD_BORDER
        add_card(s14, rx, 1.85, rw, 4.65, CARD_BG, border_c)

        rtb = s14.shapes.add_textbox(Inches(rx + 0.25), Inches(2.2), Inches(rw - 0.5), Inches(4.0))
        rtf = rtb.text_frame
        rtf.word_wrap = True

        p = rtf.paragraphs[0]
        p.text = phase
        p.font.name = FONT_FAMILY
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = CAT_YELLOW

        p2 = rtf.add_paragraph()
        p2.text = title
        p2.font.name = FONT_FAMILY
        p2.font.size = Pt(13)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_WHITE
        p2.space_before = Pt(8)

        p3 = rtf.add_paragraph()
        p3.text = desc
        p3.font.name = FONT_FAMILY
        p3.font.size = Pt(10)
        p3.font.color.rgb = TEXT_MUTED
        p3.space_before = Pt(10)

    # ==========================================================
    # SLIDE 15: CLOSING
    # ==========================================================
    s15 = prs.slides.add_slide(blank_layout)
    bg15 = s15.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg15.fill.solid()
    bg15.fill.fore_color.rgb = BG_DARK
    bg15.line.color.rgb = BG_DARK

    bar15 = s15.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.8), Inches(0.5), Inches(0.06))
    bar15.fill.solid()
    bar15.fill.fore_color.rgb = CAT_YELLOW
    bar15.line.color.rgb = CAT_YELLOW

    t15 = s15.shapes.add_textbox(Inches(0.8), Inches(2.1), Inches(11.733), Inches(4.5))
    tf15 = t15.text_frame
    tf15.word_wrap = True

    p15 = tf15.paragraphs[0]
    p15.text = "CAT OperatorIQ"
    p15.font.name = FONT_FAMILY
    p15.font.size = Pt(44)
    p15.font.bold = True
    p15.font.color.rgb = TEXT_WHITE

    p15_tag = tf15.add_paragraph()
    p15_tag.text = "Safer machines.  Smarter decisions.  Stronger operators."
    p15_tag.font.name = FONT_FAMILY
    p15_tag.font.size = Pt(20)
    p15_tag.font.bold = True
    p15_tag.font.color.rgb = CAT_YELLOW
    p15_tag.space_before = Pt(14)

    p15_thx = tf15.add_paragraph()
    p15_thx.text = "Thank you."
    p15_thx.font.name = FONT_FAMILY
    p15_thx.font.size = Pt(32)
    p15_thx.font.bold = True
    p15_thx.font.color.rgb = TEXT_WHITE
    p15_thx.space_before = Pt(24)

    p15_q = tf15.add_paragraph()
    p15_q.text = "We welcome your questions."
    p15_q.font.name = FONT_FAMILY
    p15_q.font.size = Pt(13)
    p15_q.font.color.rgb = TEXT_MUTED
    p15_q.space_before = Pt(8)

    # Save
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    prs.save(output_path)
    print(f"Presentation saved successfully to: {output_path}")

if __name__ == "__main__":
    create_deck()

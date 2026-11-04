"""
Smart URL Firewall - Poster Generator
Generates high-resolution A2 Landscape PDF and PNG for Theory of Computation & Compiler Design (24IC301T).
"""

import fitz  # PyMuPDF
import math

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) / 255.0 for i in (0, 2, 4))

# Palette
NAVY_HEADER = hex_to_rgb("#0F172A")
BLUE_ACCENT = hex_to_rgb("#2563EB")
LIGHT_BG    = hex_to_rgb("#F8FAFC")
CARD_BG     = hex_to_rgb("#FFFFFF")
CARD_BORDER = hex_to_rgb("#CBD5E1")
TEXT_MAIN   = hex_to_rgb("#0F172A")
TEXT_MUTED  = hex_to_rgb("#475569")
TEXT_LIGHT  = hex_to_rgb("#94A3B8")

COLOR_SAFE    = hex_to_rgb("#059669")  # Green
COLOR_SAFE_BG = hex_to_rgb("#ECFDF5")
COLOR_WARN    = hex_to_rgb("#D97706")  # Amber
COLOR_WARN_BG = hex_to_rgb("#FFFBEB")
COLOR_EVIL    = hex_to_rgb("#DC2626")  # Red
COLOR_EVIL_BG = hex_to_rgb("#FEF2F2")
COLOR_INFO    = hex_to_rgb("#3B82F6")  # Blue
COLOR_INFO_BG = hex_to_rgb("#EFF6FF")
ROW_ALT_BG   = hex_to_rgb("#F1F5F9")

def draw_card(page, x, y, w, h, title, subtitle=None, accent_color=BLUE_ACCENT):
    # Base card
    rect = fitz.Rect(x, y, x + w, y + h)
    page.draw_rect(rect, color=CARD_BORDER, fill=CARD_BG, width=1.2)
    
    # Top accent line
    accent_rect = fitz.Rect(x, y, x + w, y + 5)
    page.draw_rect(accent_rect, color=accent_color, fill=accent_color, width=0)
    
    # Title
    page.insert_text(fitz.Point(x + 14, y + 24), title, fontname="helv", fontsize=12.5, color=accent_color)
    
    if subtitle:
        page.insert_text(fitz.Point(x + 14, y + 38), subtitle, fontname="helv", fontsize=8.5, color=TEXT_MUTED)
        return y + 46
    return y + 34

def draw_arrow(page, p1, p2, label="", color=TEXT_MAIN, width=1.5, curve_offset=0, label_offset=(0, -6)):
    x1, y1 = p1
    x2, y2 = p2
    
    if curve_offset != 0:
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2
        dx = x2 - x1
        dy = y2 - y1
        length = math.hypot(dx, dy)
        if length > 0:
            nx = -dy / length
            ny = dx / length
            cx = mx + nx * curve_offset
            cy = my + ny * curve_offset
            page.draw_bezier(fitz.Point(x1, y1), fitz.Point(cx, cy), fitz.Point(cx, cy), fitz.Point(x2, y2),
                             color=color, width=width)
            angle = math.atan2(y2 - cy, x2 - cx)
            lx = cx + label_offset[0]
            ly = cy + label_offset[1]
        else:
            angle = 0
            lx, ly = mx, my
    else:
        page.draw_line(fitz.Point(x1, y1), fitz.Point(x2, y2), color=color, width=width)
        angle = math.atan2(y2 - y1, x2 - x1)
        lx = (x1 + x2) / 2 + label_offset[0]
        ly = (y1 + y2) / 2 + label_offset[1]
        
    head_len = 7
    arrow_angle = math.pi / 6
    a1_x = x2 - head_len * math.cos(angle - arrow_angle)
    a1_y = y2 - head_len * math.sin(angle - arrow_angle)
    a2_x = x2 - head_len * math.cos(angle + arrow_angle)
    a2_y = y2 - head_len * math.sin(angle + arrow_angle)
    page.draw_polyline([fitz.Point(x2, y2), fitz.Point(a1_x, a1_y), fitz.Point(a2_x, a2_y), fitz.Point(x2, y2)],
                       color=color, fill=color)
    
    if label:
        page.insert_text(fitz.Point(lx, ly), label, fontname="helv", fontsize=8, color=color)

def draw_self_loop(page, cx, cy, r, label="", color=TEXT_MAIN, position="top"):
    loop_r = 16
    if position == "top":
        start_x = cx - 10
        start_y = cy - r
        end_x = cx + 10
        end_y = cy - r
        c1_x = cx - 22
        c1_y = cy - r - loop_r * 2
        c2_x = cx + 22
        c2_y = cy - r - loop_r * 2
        page.draw_bezier(fitz.Point(start_x, start_y), fitz.Point(c1_x, c1_y), fitz.Point(c2_x, c2_y), fitz.Point(end_x, end_y),
                         color=color, width=1.5)
        page.draw_polyline([fitz.Point(end_x, end_y), fitz.Point(end_x - 3, end_y - 6), fitz.Point(end_x + 3, end_y - 6), fitz.Point(end_x, end_y)],
                           color=color, fill=color)
        if label:
            page.insert_text(fitz.Point(cx - 24, cy - r - loop_r * 2 - 2), label, fontname="helv", fontsize=8, color=color)
    elif position == "bottom":
        start_x = cx - 10
        start_y = cy + r
        end_x = cx + 10
        end_y = cy + r
        c1_x = cx - 22
        c1_y = cy + r + loop_r * 2
        c2_x = cx + 22
        c2_y = cy + r + loop_r * 2
        page.draw_bezier(fitz.Point(start_x, start_y), fitz.Point(c1_x, c1_y), fitz.Point(c2_x, c2_y), fitz.Point(end_x, end_y),
                         color=color, width=1.5)
        page.draw_polyline([fitz.Point(end_x, end_y), fitz.Point(end_x - 3, end_y + 6), fitz.Point(end_x + 3, end_y + 6), fitz.Point(end_x, end_y)],
                           color=color, fill=color)
        if label:
            page.insert_text(fitz.Point(cx - 24, cy + r + loop_r * 2 + 10), label, fontname="helv", fontsize=8, color=color)

def generate_poster():
    doc = fitz.open()
    # A2 Landscape: 594 mm x 420 mm = 1684 x 1191 pt
    w, h = 1684, 1191
    page = doc.new_page(width=w, height=h)
    
    # 0. Background
    page.draw_rect(fitz.Rect(0, 0, w, h), color=LIGHT_BG, fill=LIGHT_BG)
    
    # 1. Header Banner
    header_rect = fitz.Rect(25, 20, w - 25, 115)
    page.draw_rect(header_rect, color=NAVY_HEADER, fill=NAVY_HEADER)
    
    # Header Sub-bar
    sub_rect = fitz.Rect(25, 108, w - 25, 115)
    page.draw_rect(sub_rect, color=BLUE_ACCENT, fill=BLUE_ACCENT)
    
    # Header Content
    page.insert_text(fitz.Point(45, 46), "DEPARTMENT OF INFORMATION & COMMUNICATION TECHNOLOGY | SEMESTER V (2026-27)",
                     fontname="helv", fontsize=9.5, color=hex_to_rgb("#94A3B8"))
    
    page.insert_text(fitz.Point(45, 75), "SMART URL FIREWALL: Phishing & Malicious Link Detection Using Finite Automata",
                     fontname="helv", fontsize=20, color=hex_to_rgb("#FFFFFF"))
    
    page.insert_text(fitz.Point(45, 96), "Course Code: 24IC301T – Theory of Computation and Compiler Design | Project Type: Academic Defense Poster",
                     fontname="helv", fontsize=10.5, color=hex_to_rgb("#38BDF8"))
    
    # Right meta pill
    meta_rect = fitz.Rect(w - 380, 32, w - 45, 100)
    page.draw_rect(meta_rect, color=hex_to_rgb("#1E293B"), fill=hex_to_rgb("#1E293B"))
    page.insert_text(fitz.Point(w - 365, 52), "CANDIDATE VIVA CREDENTIALS", fontname="helv", fontsize=8.5, color=hex_to_rgb("#38BDF8"))
    page.insert_text(fitz.Point(w - 365, 70), "Student: Practical & Viva Submission", fontname="helv", fontsize=9.5, color=hex_to_rgb("#FFFFFF"))
    page.insert_text(fitz.Point(w - 365, 87), "Enrollment: [Your ID] | Div: ICT-V | Mentor: Dept. Faculty", fontname="helv", fontsize=9, color=hex_to_rgb("#CBD5E1"))
    
    # Grid Setup (3 Columns)
    col_w = 460
    center_w = 674
    gap = 18
    col1_x = 25
    col2_x = col1_x + col_w + gap
    col3_x = col2_x + center_w + gap
    
    # ==========================================
    # COLUMN 1: Foundations & Mathematical Model
    # ==========================================
    
    # Box 1: Problem Statement
    curr_y = draw_card(page, col1_x, 130, col_w, 290, "1. PROBLEM STATEMENT & THE PHISHING VECTOR",
                       "Deceptive URL structures exploiting RFC 3986 Userinfo authority parsing", COLOR_EVIL)
    
    p1_lines = [
        ("THE THREAT LANDSCAPE:", True, TEXT_MAIN),
        ("Over 3.4 billion phishing emails are dispatched daily. Attackers obfuscate", False, TEXT_MUTED),
        ("malicious destinations using deceptive URL syntax that evades standard filters.", False, TEXT_MUTED),
        ("", False, TEXT_MUTED),
        ("RFC 3986 SPECIFICATION ABUSE (THE '@' ATTACK):", True, COLOR_EVIL),
        ("Standard URL syntax defines authority as:  scheme://[userinfo@]host[:port]", False, TEXT_MAIN),
        ("In standard web browsers, text preceding '@' is treated as discardable login", False, TEXT_MUTED),
        ("credentials, while the network connection routes entirely to the host AFTER '@'.", False, TEXT_MUTED),
        ("", False, TEXT_MUTED),
        ("ILLUSTRATIVE ATTACK PAYLOAD:", True, TEXT_MAIN),
        ("http://secure-login.paypal.com@attacker-controlled-c2.ru/auth", False, hex_to_rgb("#B91C1C")),
        ("  - User perceives legit brand: paypal.com", False, TEXT_MUTED),
        ("  - Actual TCP connection destination: attacker-controlled-c2.ru", False, TEXT_MUTED),
        ("", False, TEXT_MUTED),
        ("WHY TRADITIONAL APPROACHES FAIL:", True, TEXT_MAIN),
        ("- Regex Engines: Vulnerable to catastrophic ReDoS (exponential backtracking).", False, TEXT_MUTED),
        ("- Machine Learning / LLMs: High latency (>50ms), GPU-heavy, unsuited for line rate.", False, TEXT_MUTED)
    ]
    py = curr_y + 12
    for text, is_bold, col in p1_lines:
        if text.startswith("http://"):
            bg_box = fitz.Rect(col1_x + 14, py - 10, col1_x + col_w - 14, py + 5)
            page.draw_rect(bg_box, color=COLOR_EVIL_BG, fill=COLOR_EVIL_BG)
        page.insert_text(fitz.Point(col1_x + 16, py), text, fontname="helv", fontsize=8.8, color=col)
        py += 14

    # Box 2: Why Theory of Computation?
    curr_y = draw_card(page, col1_x, 435, col_w, 310, "2. WHY THEORY OF COMPUTATION & COMPILERS?",
                       "Direct isomorphism with compiler lexical analysis (Tokenization)", COLOR_INFO)
    
    p2_lines = [
        ("LEXICAL SCANNER ANALOGY IN COMPILERS:", True, COLOR_INFO),
        ("In a compiler frontend, the Lexer scans source code character-by-character to", False, TEXT_MUTED),
        ("generate atomic tokens (IDs, Keywords) using Deterministic Finite Automata.", False, TEXT_MUTED),
        ("A Smart URL Firewall acts as an inline network compiler lexer that tokenizes", False, TEXT_MUTED),
        ("incoming HTTP request URIs before passing them to the application layer.", False, TEXT_MUTED),
        ("", False, TEXT_MUTED),
        ("DETERMINISTIC O(n) TIME COMPLEXITY:", True, COLOR_INFO),
        ("A DFA guarantees strictly linear O(n) execution time where n = URL length.", False, TEXT_MUTED),
        ("Exactly ONE state transition is evaluated per input character. Zero recursion,", False, TEXT_MUTED),
        ("zero guessing, and predictable microsecond-level latency suitable for 10Gbps+.", False, TEXT_MUTED),
        ("", False, TEXT_MUTED),
        ("COMPLETE IMMUNITY TO ReDoS ATTACKS:", True, COLOR_INFO),
        ("Nondeterministic Regex engines (PCRE) suffer from exponential backtracking", False, TEXT_MUTED),
        ("O(2^n) on nested patterns. A minimized DFA guarantees zero backtracking.", False, TEXT_MUTED),
        ("", False, TEXT_MUTED),
        ("HARDWARE & FPGA SYNTHESIZABILITY:", True, COLOR_INFO),
        ("DFA transition matrices translate directly to Read-Only Look-Up Tables (LUTs)", False, TEXT_MUTED),
        ("in FPGA / ASIC network interface cards for zero-CPU hardware packet dropping.", False, TEXT_MUTED)
    ]
    py = curr_y + 12
    for text, is_bold, col in p2_lines:
        page.insert_text(fitz.Point(col1_x + 16, py), text, fontname="helv", fontsize=8.8, color=col)
        py += 14.5

    # Box 3: Formal 5-Tuple Definition
    curr_y = draw_card(page, col1_x, 760, col_w, 320, "3. FORMAL MATHEMATICAL 5-TUPLE DEFINITION",
                       "Rigorous deterministic definition: M = (Q, Sigma, delta, q0, F)", BLUE_ACCENT)
    
    p3_lines = [
        ("FORMAL TUPLE:  M = ( Q, Sigma, delta, q0, F )", True, TEXT_MAIN),
        ("1. State Set (Q):  |Q| = 6 States", True, COLOR_INFO),
        ("   q0: Start / Protocol Scanning State", False, TEXT_MUTED),
        ("   q1: Scheme Prefix Ingested ('http' / 'https')", False, TEXT_MUTED),
        ("   q2: Scheme Delimiter Validated ('://')", False, TEXT_MUTED),
        ("   q3: Legitimate Hostname / Domain Parsing [SAFE STATE]", False, COLOR_SAFE),
        ("   q4: Suspicious Delimiter Detected ('@' Encountered)", False, COLOR_WARN),
        ("   q5: Malicious Host Parsing Trap [FINAL ACCEPTING STATE]", False, COLOR_EVIL),
        ("", False, TEXT_MUTED),
        ("2. Input Alphabet (Sigma): Equivalence Classes", True, COLOR_INFO),
        ("   p_proto in {'h', 't', 'p', 's'}  |  d_delim in {':', '/'}", False, TEXT_MAIN),
        ("   c_char  in {a-z, A-Z, 0-9, '.', '-', '_'} (Valid authority chars)", False, TEXT_MAIN),
        ("   '@'     = The credential-spoof delimiter symbol", False, COLOR_EVIL),
        ("   invalid = Control characters, spaces, illegal null bytes", False, TEXT_MUTED),
        ("", False, TEXT_MUTED),
        ("3. Initial State:  q0 in Q", True, TEXT_MAIN),
        ("4. Final / Trap State Set:  F = { q5 } (Malicious Classifier)", True, COLOR_EVIL),
        ("   (Dual-mode: q3 acts as Safe Accept State when verifying cleanliness)", False, TEXT_MUTED)
    ]
    py = curr_y + 12
    for text, is_bold, col in p3_lines:
        page.insert_text(fitz.Point(col1_x + 16, py), text, fontname="helv", fontsize=8.8, color=col)
        py += 14.5

    # ==========================================
    # COLUMN 2: DFA Diagram & Transition Matrix
    # ==========================================
    
    # Box 4: DFA State Diagram
    curr_y = draw_card(page, col2_x, 130, center_w, 480, "4. 6-STATE DETERMINISTIC FINITE AUTOMATON (DFA) STATE DIAGRAM",
                       "Deterministic state transitions for URL validation and '@' credential-spoof detection", BLUE_ACCENT)
    
    states = {
        "q0": (col2_x + 80,  270, "q0", "Start", COLOR_INFO, COLOR_INFO_BG),
        "q1": (col2_x + 230, 270, "q1", "Scheme", COLOR_INFO, COLOR_INFO_BG),
        "q2": (col2_x + 380, 270, "q2", "Separator", COLOR_INFO, COLOR_INFO_BG),
        "q3": (col2_x + 560, 270, "q3", "Domain (SAFE)", COLOR_SAFE, COLOR_SAFE_BG),
        "q4": (col2_x + 380, 440, "q4", "Exploit '@'", COLOR_WARN, COLOR_WARN_BG),
        "q5": (col2_x + 560, 440, "q5", "PHISHING TRAP", COLOR_EVIL, COLOR_EVIL_BG)
    }
    
    # Draw Start Arrow
    draw_arrow(page, (col2_x + 20, 270), (col2_x + 55, 270), "Start", color=TEXT_MAIN, width=2)
    
    # Draw Transitions:
    # q0 -> q1
    draw_arrow(page, (col2_x + 105, 270), (col2_x + 205, 270), "proto [h,t,p,s]", color=TEXT_MAIN, width=1.8, label_offset=(0, -8))
    # q1 self-loop
    draw_self_loop(page, col2_x + 230, 270, 25, "proto", color=TEXT_MAIN, position="top")
    # q1 -> q2
    draw_arrow(page, (col2_x + 255, 270), (col2_x + 355, 270), "delim [://]", color=TEXT_MAIN, width=1.8, label_offset=(0, -8))
    # q2 -> q3
    draw_arrow(page, (col2_x + 405, 270), (col2_x + 535, 270), "valid char", color=COLOR_SAFE, width=2, label_offset=(0, -8))
    # q3 self loop (Safe parsing)
    draw_self_loop(page, col2_x + 560, 270, 25, "valid char [a-z,0-9,.,-]", color=COLOR_SAFE, position="top")
    
    # q3 -> q4 (Curved arrow down to exploit state)
    draw_arrow(page, (col2_x + 540, 290), (col2_x + 405, 430), "SYMBOL '@' (EXPLOIT TRIGGER)",
               color=COLOR_EVIL, width=2.2, curve_offset=15, label_offset=(-120, -10))
    
    # q4 -> q5
    draw_arrow(page, (col2_x + 405, 440), (col2_x + 530, 440), "valid host char", color=COLOR_EVIL, width=2, label_offset=(0, -8))
    # q5 self loop (Trap state absorbing everything)
    draw_self_loop(page, col2_x + 560, 440, 30, "Any char / Sigma (TRAP LOOP)", color=COLOR_EVIL, position="bottom")
    
    # q2 -> q4 (Direct @ right after ://)
    draw_arrow(page, (col2_x + 380, 295), (col2_x + 380, 415), "'@'", color=COLOR_WARN, width=1.5, label_offset=(8, 0))

    # Now Draw the State Nodes
    for sid, (cx, cy, sname, sublabel, border_col, fill_col) in states.items():
        r = 25
        if sid == "q5":
            page.draw_circle(fitz.Point(cx, cy), r + 5, color=border_col, fill=fill_col, width=2)
            page.draw_circle(fitz.Point(cx, cy), r, color=border_col, fill=fill_col, width=2)
        elif sid == "q3":
            page.draw_circle(fitz.Point(cx, cy), r + 3, color=border_col, fill=fill_col, width=2)
            page.draw_circle(fitz.Point(cx, cy), r, color=border_col, fill=fill_col, width=1.5)
        else:
            page.draw_circle(fitz.Point(cx, cy), r, color=border_col, fill=fill_col, width=2)
            
        page.insert_text(fitz.Point(cx - 9, cy + 5), sname, fontname="helv", fontsize=13, color=border_col)
        page.insert_text(fitz.Point(cx - 30, cy + r + 15), sublabel, fontname="helv", fontsize=7.5, color=TEXT_MUTED)

    # State Diagram Legend Box
    leg_rect = fitz.Rect(col2_x + 30, 530, col2_x + center_w - 30, 595)
    page.draw_rect(leg_rect, color=CARD_BORDER, fill=ROW_ALT_BG)
    page.insert_text(fitz.Point(col2_x + 45, 548), "DIAGRAM SEMANTIC LEGEND & VIVA TAKEAWAYS:", fontname="helv", fontsize=9, color=TEXT_MAIN)
    page.insert_text(fitz.Point(col2_x + 45, 566), "[GREEN q3] Safe Host State: If stream ends in q3, URL has clean authority without obfuscation.", fontname="helv", fontsize=8.2, color=COLOR_SAFE)
    page.insert_text(fitz.Point(col2_x + 45, 582), "[RED q5] Trap Phishing Alert: Double-ring accepting state. Absorbs remaining payload and drops packets instantly.", fontname="helv", fontsize=8.2, color=COLOR_EVIL)

    # Box 5: Formal Transition Table
    curr_y = draw_card(page, col2_x, 625, center_w, 455, "5. FORMAL STATE TRANSITION TABLE (delta : Q x Sigma -> Q)",
                       "Complete matrix representation defining total transition function across all states", BLUE_ACCENT)
    
    tx = col2_x + 18
    ty = curr_y + 15
    table_w = center_w - 36
    
    col_widths = [65, 80, 85, 95, 75, 75, 160]
    headers = ["State Q", "Proto [h,t,p,s]", "Delim [://]", "Char [a-z,0-9]", "Symbol '@'", "Invalid", "Semantic Classification"]
    
    th_rect = fitz.Rect(tx, ty, tx + table_w, ty + 24)
    page.draw_rect(th_rect, color=NAVY_HEADER, fill=NAVY_HEADER)
    hx = tx + 8
    for idx, htitle in enumerate(headers):
        page.insert_text(fitz.Point(hx, ty + 16), htitle, fontname="helv", fontsize=8.5, color=hex_to_rgb("#FFFFFF"))
        hx += col_widths[idx]
        
    rows = [
        ("-> q0 (Start)", "q1", "q0", "q0", "q0", "Reject (Trap)", "Scanning scheme letters (h,t,p,s)", COLOR_INFO_BG, COLOR_INFO),
        ("   q1", "q1", "q2", "Reject", "Reject", "Reject", "Protocol prefix matched (http/https)", CARD_BG, TEXT_MAIN),
        ("   q2", "q3", "Reject", "q3", "q4", "Reject", "Scheme delimiter verified (://)", CARD_BG, TEXT_MAIN),
        (" * q3 (SAFE)", "q3", "q3", "q3", "q4 (ALARM)", "Reject", "Normal hostname parsing [Valid URL]", COLOR_SAFE_BG, COLOR_SAFE),
        ("   q4", "q5", "q5", "q5", "q5", "Reject", "Exploit detected, bridging to host", COLOR_WARN_BG, COLOR_WARN),
        ("** q5 (TRAP)", "q5", "q5", "q5", "q5", "Reject", "MALICIOUS PHISHING TRAP [Drop Packet]", COLOR_EVIL_BG, COLOR_EVIL)
    ]
    
    ry = ty + 24
    for rstate, rproto, rdelim, rchar, rat, rinv, rdesc, rbg, rcol in rows:
        r_rect = fitz.Rect(tx, ry, tx + table_w, ry + 36)
        page.draw_rect(r_rect, color=CARD_BORDER, fill=rbg, width=0.8)
        
        vals = [rstate, rproto, rdelim, rchar, rat, rinv, rdesc]
        rx = tx + 8
        for cidx, cval in enumerate(vals):
            page.insert_text(fitz.Point(rx, ry + 22), cval, fontname="helv", fontsize=8.2,
                             color=rcol if cidx in (0, 4, 6) else TEXT_MAIN)
            rx += col_widths[cidx]
        ry += 36

    ty_note = ry + 18
    page.insert_text(fitz.Point(tx, ty_note), "KEY PROPERTIES OF THE TRANSITION FUNCTION:", fontname="helv", fontsize=8.8, color=TEXT_MAIN)
    page.insert_text(fitz.Point(tx, ty_note + 15), "1. Total Determinism: Exactly one target state delta(q, a) exists for every (state, symbol) pair.", fontname="helv", fontsize=8.2, color=TEXT_MUTED)
    page.insert_text(fitz.Point(tx, ty_note + 30), "2. Trap State Invariance: Once in q5, for any symbol s in Sigma, delta(q5, s) = q5 (Dead/Absorbing state).", fontname="helv", fontsize=8.2, color=TEXT_MUTED)
    page.insert_text(fitz.Point(tx, ty_note + 45), "3. Rejection Policy: Any illegal byte (e.g., spaces or non-ASCII control characters) routes to Reject state.", fontname="helv", fontsize=8.2, color=TEXT_MUTED)

    # ==========================================
    # COLUMN 3: Traces, Compiler Links, Matrix
    # ==========================================
    
    # Box 6: String Traces
    curr_y = draw_card(page, col3_x, 130, col_w, 290, "6. RUNTIME STRING TRACING & PROOFS",
                       "Formal execution traces delta*(q0, w) validating correctness", COLOR_SAFE)
    
    page.insert_text(fitz.Point(col3_x + 16, curr_y + 14), "TRACE 1: LEGITIMATE ENTERPRISE URL (SAFE)", fontname="helv", fontsize=8.8, color=COLOR_SAFE)
    
    t1_rect = fitz.Rect(col3_x + 14, curr_y + 22, col3_x + col_w - 14, curr_y + 115)
    page.draw_rect(t1_rect, color=COLOR_SAFE, fill=COLOR_SAFE_BG, width=0.8)
    t1_lines = [
        "Input String w1 = 'https://google.com'",
        "  delta(q0, 'h') = q1   --> delta(q1, 't') = q1 --> delta(q1, 'p') = q1",
        "  delta(q1, 's') = q1   --> delta(q1, '://') = q2",
        "  delta(q2, 'g') = q3   --> delta(q3, 'oogle.com') = q3",
        "Final Evaluated State:  q3 in Q (q3 not in F)",
        "Classification:  SAFE URL -> Traffic Permitted [HTTP 200 OK]"
    ]
    ty1 = curr_y + 36
    for line in t1_lines:
        page.insert_text(fitz.Point(col3_x + 22, ty1), line, fontname="courier", fontsize=7.8, color=TEXT_MAIN)
        ty1 += 13

    page.insert_text(fitz.Point(col3_x + 16, curr_y + 133), "TRACE 2: PHISHING CREDENTIAL-SPOOF URL (ATTACK)", fontname="helv", fontsize=8.8, color=COLOR_EVIL)
    
    t2_rect = fitz.Rect(col3_x + 14, curr_y + 142, col3_x + col_w - 14, curr_y + 242)
    page.draw_rect(t2_rect, color=COLOR_EVIL, fill=COLOR_EVIL_BG, width=0.8)
    t2_lines = [
        "Input String w2 = 'http://paypal.com@evil-c2.ru'",
        "  delta(q0, 'http') = q1  --> delta(q1, '://') = q2",
        "  delta(q2, 'paypal.com') = q3  (Looks benign so far)",
        "  delta(q3, '@') = q4           *** EXPLOIT TRIGGERED ***",
        "  delta(q4, 'e') = q5           (Target host captured)",
        "  delta(q5, 'vil-c2.ru') = q5   (Trapped in alert state)",
        "Final Evaluated State:  q5 in F (Accepting Threat Trap)",
        "Classification:  MALICIOUS PHISHING -> Traffic Blocked [HTTP 403]"
    ]
    ty2 = curr_y + 156
    for line in t2_lines:
        col = COLOR_EVIL if "***" in line or "MALICIOUS" in line else TEXT_MAIN
        page.insert_text(fitz.Point(col3_x + 22, ty2), line, fontname="courier", fontsize=7.8, color=col)
        ty2 += 12.5

    # Box 7: Compiler Design Bridge
    curr_y = draw_card(page, col3_x, 435, col_w, 290, "7. COMPILER DESIGN BRIDGE: REGEX & CFG",
                       "Theoretical connection to Lexical Scanning, Grammars & Chomsy Hierarchy", BLUE_ACCENT)
    
    p7_lines = [
        ("REGULAR EXPRESSION EQUIVALENCE (KLEENE'S THEOREM):", True, BLUE_ACCENT),
        ("The suspicious language L_phish recognized by DFA M is defined by:", False, TEXT_MUTED),
        ("R_phish = (http | https) :// [a-zA-Z0-9.-]+ @ [a-zA-Z0-9.-]+", False, TEXT_MAIN),
        ("Every regular language is accepted by a DFA, establishing mathematical", False, TEXT_MUTED),
        ("equivalence between lexical regex patterns and state transitions.", False, TEXT_MUTED),
        ("", False, TEXT_MUTED),
        ("CONTEXT-FREE GRAMMAR (CFG) FOR URL STRUCTURE:", True, BLUE_ACCENT),
        ("S  ->  Proto  '://'  Authority  Path", False, hex_to_rgb("#1E293B")),
        ("Proto -> 'http' | 'https'", False, TEXT_MUTED),
        ("Authority -> ValidHost | Userinfo '@' MaliciousHost", False, COLOR_EVIL),
        ("Userinfo  -> Char Userinfo | Char   (Attacker spoofing brand)", False, TEXT_MUTED),
        ("MaliciousHost -> Char MaliciousHost | Char", False, TEXT_MUTED),
        ("", False, TEXT_MUTED),
        ("COMPILER FRONTEND TOKEN STREAM:", True, BLUE_ACCENT),
        ("Lexer outputs tokens: <T_SCHEME, http> <T_SPOOF, paypal.com>", False, TEXT_MAIN),
        ("<T_EXPLOIT_AT, @> <T_TARGET_HOST, evil-c2.ru>", False, TEXT_MAIN),
        ("Parser drops the AST tree upon encountering <T_EXPLOIT_AT>.", False, TEXT_MUTED)
    ]
    py = curr_y + 12
    for text, is_bold, col in p7_lines:
        page.insert_text(fitz.Point(col3_x + 16, py), text, fontname="helv", fontsize=8.6, color=col)
        py += 14

    # Box 8: System Comparison Matrix
    curr_y = draw_card(page, col3_x, 740, col_w, 340, "8. SYSTEM COMPARISON & ADVANTAGES",
                       "Evaluating DFA Firewall against PCRE Regex engines & Deep Learning", COLOR_WARN)
    
    cx_tbl = col3_x + 14
    cy_tbl = curr_y + 12
    tbl_w = col_w - 28
    
    c_cols = [95, 105, 105, 115]
    c_heads = ["Evaluation Metric", "Proposed 6-State DFA", "PCRE Regex Engine", "Deep Learning / ML"]
    
    th_rect = fitz.Rect(cx_tbl, cy_tbl, cx_tbl + tbl_w, cy_tbl + 22)
    page.draw_rect(th_rect, color=NAVY_HEADER, fill=NAVY_HEADER)
    hx = cx_tbl + 6
    for idx, ht in enumerate(c_heads):
        page.insert_text(fitz.Point(hx, cy_tbl + 15), ht, fontname="helv", fontsize=8, color=hex_to_rgb("#FFFFFF"))
        hx += c_cols[idx]
        
    c_rows = [
        ("Time Complexity", "Strictly O(n)", "O(2^n) Backtracking", "O(k x d) (Matrix Ops)", COLOR_SAFE_BG, COLOR_SAFE),
        ("Processing Speed", "> 10 Gbps (Line Rate)", "< 500 Mbps (ReDoS Risk)", "< 50 Mbps (Latency >50ms)", CARD_BG, TEXT_MAIN),
        ("Memory Footprint", "< 64 KB (LUT Array)", "Variable Heap Memory", "> 500 MB (Model Weights)", CARD_BG, TEXT_MAIN),
        ("ReDoS Exploits", "100% Immune", "Highly Vulnerable", "Not Applicable", COLOR_SAFE_BG, COLOR_SAFE),
        ("Hardware Ready", "Direct FPGA / Silicon", "Impractical in Hardware", "Requires GPU / NPU", CARD_BG, TEXT_MAIN)
    ]
    
    ry = cy_tbl + 22
    for r_metric, r_dfa, r_regex, r_ml, r_bg, r_c in c_rows:
        r_rect = fitz.Rect(cx_tbl, ry, cx_tbl + tbl_w, ry + 28)
        page.draw_rect(r_rect, color=CARD_BORDER, fill=r_bg, width=0.8)
        page.insert_text(fitz.Point(cx_tbl + 6, ry + 18), r_metric, fontname="helv", fontsize=7.8, color=TEXT_MAIN)
        page.insert_text(fitz.Point(cx_tbl + 6 + c_cols[0], ry + 18), r_dfa, fontname="helv", fontsize=7.8, color=r_c)
        page.insert_text(fitz.Point(cx_tbl + 6 + c_cols[0] + c_cols[1], ry + 18), r_regex, fontname="helv", fontsize=7.8, color=TEXT_MUTED)
        page.insert_text(fitz.Point(cx_tbl + 6 + c_cols[0] + c_cols[1] + c_cols[2], ry + 18), r_ml, fontname="helv", fontsize=7.8, color=TEXT_MUTED)
        ry += 28

    page.insert_text(fitz.Point(cx_tbl, ry + 18), "INDUSTRIAL APPLICATIONS:", fontname="helv", fontsize=8.8, color=TEXT_MAIN)
    badges = [
        "Envoy / NGINX WAF Filter",
        "Zero-Trust Email Gateway",
        "DNS Resolver Pre-Filter",
        "FPGA Network Ingestion Cards"
    ]
    bx = cx_tbl
    by = ry + 28
    for btext in badges:
        bw = len(btext) * 5.8 + 14
        brect = fitz.Rect(bx, by, bx + bw, by + 18)
        page.draw_rect(brect, color=BLUE_ACCENT, fill=COLOR_INFO_BG, width=0.8)
        page.insert_text(fitz.Point(bx + 7, by + 13), btext, fontname="helv", fontsize=7.5, color=BLUE_ACCENT)
        bx += bw + 8
        if bx > col3_x + col_w - 120:
            bx = cx_tbl
            by += 24

    # ==========================================
    # BOTTOM FOOTER BANNER: Viva Golden Rules
    # ==========================================
    footer_rect = fitz.Rect(25, 1095, w - 25, 1165)
    page.draw_rect(footer_rect, color=NAVY_HEADER, fill=NAVY_HEADER)
    
    page.insert_text(fitz.Point(45, 1118), "VIVA VOCE DEFENSE CHEAT SHEET (TOP 3 EXAMINER QUESTIONS):", fontname="helv", fontsize=9.5, color=hex_to_rgb("#FBBF24"))
    
    q1_text = "Q1: Why DFA instead of NFA? -> Ans: DFA guarantees O(n) runtime and exactly one state path with no backtracking or nondeterminism."
    q2_text = "Q2: Why is q5 a Trap/Dead state? -> Ans: Once '@' occurs in host syntax, the URL violates RFC 3986 clean authority. It is permanently unsafe."
    q3_text = "Q3: How does this link to Compilers? -> Ans: Acts as the Lexical Analysis scanner, converting raw characters into security-classified tokens."
    
    page.insert_text(fitz.Point(45, 1136), q1_text, fontname="helv", fontsize=8.2, color=hex_to_rgb("#E2E8F0"))
    page.insert_text(fitz.Point(45, 1152), q2_text + "  |  " + q3_text, fontname="helv", fontsize=8.2, color=hex_to_rgb("#E2E8F0"))
    
    # Save outputs
    pdf_path = "Smart_URL_Firewall_Chart_Poster.pdf"
    png_path = "Smart_URL_Firewall_Chart_Poster.png"
    
    doc.save(pdf_path)
    print(f"Successfully generated PDF: {pdf_path}")
    
    pix = page.get_pixmap(dpi=150)
    pix.save(png_path)
    print(f"Successfully generated PNG: {png_path} ({pix.width}x{pix.height} px)")

if __name__ == "__main__":
    generate_poster()

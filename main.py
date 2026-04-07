import pygame
import sys
import copy
import time
import random

import hc
import utils

# ── Palette ────────────────────────────────────────────────────────────────────
BG          = (15,  15,  20)
GRID_LINE   = (35,  35,  45)
CELL_EMPTY  = (22,  22,  30)
CELL_HOVER  = (35,  40,  55)
CELL_HL     = (30,  80, 160)
CELL_CAND   = (90,  65,  10)
CELL_BEST   = (20,  90,  50)
TEXT_MAIN   = (220, 220, 230)
TEXT_DIM    = (110, 110, 130)
TEXT_INFO   = ( 90, 160, 255)
TEXT_WARN   = (255, 190,  50)
TEXT_OK     = ( 60, 200, 110)
ACCENT      = ( 80, 130, 255)
BTN_IDLE    = (30,  32,  45)
BTN_HOVER   = (45,  50,  70)
BTN_ACTIVE  = (60,  90, 180)
BTN_BORDER  = (60,  65,  90)
PANEL_BG    = (18,  18,  26)

# ── Grid config ────────────────────────────────────────────────────────────────
ROWS   = 5
COLS   = 10
CELL   = 64
PAD    = 20
GRID_X = PAD
GRID_Y = 90
GRID_W = COLS * CELL
GRID_H = ROWS * CELL
WIN_W  = GRID_W + PAD * 2
WIN_H  = GRID_Y + GRID_H + 260

# ── Initial map (from main.py) ─────────────────────────────────────────────────
INITIAL_MAP = [
    [None, None, None, None, utils.OBJECT_HOSPITAL, None, None, None, utils.OBJECT_HOUSE, None],
    [None, None, utils.OBJECT_HOUSE, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None],
    [None, utils.OBJECT_HOUSE, None, None, None, None, None, None, None, utils.OBJECT_HOSPITAL],
    [None, None, None, None, None, None, utils.OBJECT_HOUSE, None, None, None],
]

# ── HC step generator (wraps utils + hc logic step by step) ───────────────────
def hc_step_generator(initial_map):
    """Yields step dicts so the UI can animate each evaluation."""
    current_map  = copy.deepcopy(initial_map)
    current_cost = utils.cost(current_map)
    it = 0

    while True:
        it += 1
        best_map  = current_map
        best_cost = current_cost
        best_from = best_to = None

        for hospital in utils.find_objects(current_map, utils.OBJECT_HOSPITAL):
            for candidate_move in utils.actions(current_map, hospital):
                candidate_map  = utils.result(current_map, hospital, candidate_move)
                candidate_cost = utils.cost(candidate_map)

                yield {
                    "type":       "candidate",
                    "from":       hospital,
                    "to":         candidate_move,
                    "map":        current_map,
                    "iter":       it,
                    "cand_cost":  candidate_cost,
                    "cur_cost":   current_cost,
                }

                if candidate_cost < best_cost:
                    best_cost = candidate_cost
                    best_map  = candidate_map
                    best_from = hospital
                    best_to   = candidate_move

        if best_cost < current_cost:
            current_map  = best_map
            current_cost = best_cost
            yield {
                "type": "move",
                "from": best_from,
                "to":   best_to,
                "map":  current_map,
                "iter": it,
                "cost": current_cost,
            }
        else:
            yield {
                "type": "done",
                "map":  current_map,
                "iter": it,
                "cost": current_cost,
            }
            return

def random_map():
    m = [[None] * COLS for _ in range(ROWS)]
    cells = [(c, r) for r in range(ROWS) for c in range(COLS)]
    random.shuffle(cells)
    for c, r in cells[:4]:  m[r][c] = utils.OBJECT_HOUSE
    for c, r in cells[4:6]: m[r][c] = utils.OBJECT_HOSPITAL
    return m

# ── Drawing helpers ────────────────────────────────────────────────────────────
def draw_rounded_rect(surf, color, rect, r=8, border=0, border_color=None):
    pygame.draw.rect(surf, color, rect, border_radius=r)
    if border and border_color:
        pygame.draw.rect(surf, border_color, rect, border, border_radius=r)

def draw_hospital(surf, cx, cy, size=28):
    r = size // 2
    s = max(6, size // 4)
    pygame.draw.rect(surf, (200, 60, 60), (cx - r, cy - r, size, size), border_radius=5)
    pygame.draw.rect(surf, (255, 255, 255), (cx - s // 2, cy - r + 4, s, size - 8))
    pygame.draw.rect(surf, (255, 255, 255), (cx - r + 4, cy - s // 2, size - 8, s))

def draw_house(surf, cx, cy, size=26):
    half = size // 2
    pts = [(cx, cy - half), (cx - half, cy), (cx + half, cy)]
    pygame.draw.polygon(surf, (200, 160, 60), pts)
    pygame.draw.rect(surf, (220, 180, 80), (cx - half + 3, cy, size - 6, half))
    dw, dh = max(4, size // 5), max(5, size // 4)
    pygame.draw.rect(surf, (140, 100, 40), (cx - dw // 2, cy + half - dh, dw, dh))

# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIN_W, WIN_H))
    pygame.display.set_caption("Hill Climbing — Hospitales")
    clock = pygame.time.Clock()

    font_lg = pygame.font.SysFont("monospace", 22, bold=True)
    font_md = pygame.font.SysFont("monospace", 14)
    font_sm = pygame.font.SysFont("monospace", 12)
    font_xl = pygame.font.SysFont("monospace", 28, bold=True)

    # ── State ──────────────────────────────────────────────────────────────────
    map_state  = copy.deepcopy(INITIAL_MAP)
    gen        = None
    running    = False
    done       = False
    iters      = 0
    cur_cost   = utils.cost(map_state)
    best_cost  = cur_cost
    highlights = []
    candidates = []
    best_cells = []
    sel_hosp   = None
    log_lines  = []
    speed_ms   = 120
    last_step  = 0
    slider_val = 0.5
    dragging_slider = False

    BH   = 34
    btns = [
        {"rect": pygame.Rect(PAD,       50, 110, BH), "label": "▶ Correr",    "id": "run"},
        {"rect": pygame.Rect(PAD + 120, 50, 110, BH), "label": "  Paso",      "id": "step"},
        {"rect": pygame.Rect(PAD + 240, 50, 110, BH), "label": "  Reset",     "id": "reset"},
        {"rect": pygame.Rect(PAD + 360, 50, 110, BH), "label": "  Aleatorio", "id": "rand"},
    ]
    slider_rect = pygame.Rect(PAD + 490, 57, 130, 18)

    def slider_to_ms(v):
        return int(600 - v * 580)

    def add_log(msg, color=TEXT_DIM):
        log_lines.append((msg, color))
        if len(log_lines) > 6:
            log_lines.pop(0)

    def reset():
        nonlocal map_state, gen, running, done, iters, cur_cost, best_cost
        nonlocal highlights, candidates, best_cells, sel_hosp
        map_state  = copy.deepcopy(INITIAL_MAP)
        gen = None; running = False; done = False
        iters = 0; cur_cost = utils.cost(map_state); best_cost = cur_cost
        highlights = []; candidates = []; best_cells = []; sel_hosp = None
        log_lines.clear()
        add_log("Mapa reiniciado.", TEXT_DIM)

    def rand_reset():
        nonlocal map_state, gen, running, done, iters, cur_cost, best_cost
        nonlocal highlights, candidates, best_cells, sel_hosp
        map_state  = random_map()
        gen = None; running = False; done = False
        iters = 0; cur_cost = utils.cost(map_state); best_cost = cur_cost
        highlights = []; candidates = []; best_cells = []; sel_hosp = None
        log_lines.clear()
        add_log("Mapa aleatorio generado.", TEXT_INFO)

    def start_run():
        nonlocal gen, running, done
        if done:
            return
        gen     = hc_step_generator(copy.deepcopy(map_state))
        running = True
        add_log("Iniciando Hill Climbing...", TEXT_INFO)

    def do_next_step():
        nonlocal map_state, running, done, iters, cur_cost, best_cost
        nonlocal highlights, candidates, best_cells, gen
        if gen is None:
            gen = hc_step_generator(copy.deepcopy(map_state))
        try:
            step = next(gen)
        except StopIteration:
            running = False; done = True
            add_log("Generador agotado.", TEXT_DIM)
            return
        t = step["type"]
        if t == "candidate":
            candidates = [step["to"]]
            highlights = [step["from"]]
            best_cells = []
        elif t == "move":
            map_state  = step["map"]
            iters      = step["iter"]
            cur_cost   = step["cost"]
            best_cost  = min(best_cost, cur_cost)
            highlights = [step["to"]]
            candidates = []
            best_cells = [step["to"]]
            add_log(
                f"Iter {iters}: ({step['from'][0]},{step['from'][1]})->"
                f"({step['to'][0]},{step['to'][1]}) costo={cur_cost}",
                TEXT_OK,
            )
        elif t == "done":
            map_state  = step["map"]
            iters      = step["iter"]
            cur_cost   = step["cost"]
            best_cost  = min(best_cost, cur_cost)
            highlights = []; candidates = []; best_cells = []
            running    = False; done = True
            add_log(f"✓ Optimo local. Costo={cur_cost}", TEXT_OK)

    add_log("Clic en hospital para mover. ESPACIO=correr N=paso.", TEXT_DIM)

    # ── Loop ──────────────────────────────────────────────────────────────────
    while True:
        now = time.time() * 1000
        mx, my = pygame.mouse.get_pos()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_SPACE: start_run()
                if ev.key == pygame.K_n:     do_next_step()
                if ev.key == pygame.K_r:     reset()
                if ev.key == pygame.K_g:     rand_reset()

            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if slider_rect.collidepoint(mx, my):
                    dragging_slider = True
                for btn in btns:
                    if btn["rect"].collidepoint(mx, my):
                        if btn["id"] == "run":   start_run()
                        if btn["id"] == "step":  do_next_step()
                        if btn["id"] == "reset": reset()
                        if btn["id"] == "rand":  rand_reset()
                gx = (mx - GRID_X) // CELL
                gy = (my - GRID_Y) // CELL
                if 0 <= gx < COLS and 0 <= gy < ROWS and not running:
                    cell = map_state[gy][gx]
                    if cell == utils.OBJECT_HOSPITAL:
                        sel_hosp   = (gx, gy)
                        highlights = [(gx, gy)]
                        candidates = utils.actions(map_state, (gx, gy))
                        best_cells = []
                    elif sel_hosp and (gx, gy) in utils.actions(map_state, sel_hosp):
                        map_state  = utils.result(map_state, sel_hosp, (gx, gy))
                        cur_cost   = utils.cost(map_state)
                        best_cost  = min(best_cost, cur_cost)
                        sel_hosp   = None
                        highlights = [(gx, gy)]; candidates = []; best_cells = []
                        add_log(f"Manual->({gx},{gy}). Costo={cur_cost}", TEXT_WARN)
                    else:
                        sel_hosp = None; highlights = []; candidates = []; best_cells = []

            if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                dragging_slider = False

            if ev.type == pygame.MOUSEMOTION and dragging_slider:
                rel = (mx - slider_rect.x) / slider_rect.width
                slider_val = max(0.0, min(1.0, rel))
                speed_ms   = slider_to_ms(slider_val)

        if running and now - last_step >= speed_ms:
            do_next_step()
            last_step = now

        # ── Draw ───────────────────────────────────────────────────────────────
        screen.fill(BG)

        title = font_xl.render("Hill Climbing  —  Hospitales", True, TEXT_MAIN)
        screen.blit(title, (PAD, 10))

        for btn in btns:
            hover  = btn["rect"].collidepoint(mx, my)
            active = (btn["id"] == "run" and running)
            col    = BTN_ACTIVE if active else (BTN_HOVER if hover else BTN_IDLE)
            draw_rounded_rect(screen, col, btn["rect"], r=6, border=1, border_color=BTN_BORDER)
            lbl = font_md.render(btn["label"], True, (255, 255, 255) if active else TEXT_MAIN)
            screen.blit(lbl, lbl.get_rect(center=btn["rect"].center))

        spd_lbl = font_sm.render("velocidad", True, TEXT_DIM)
        screen.blit(spd_lbl, (slider_rect.x, slider_rect.y - 14))
        pygame.draw.rect(screen, GRID_LINE, slider_rect, border_radius=4)
        fill_w = int(slider_val * slider_rect.width)
        pygame.draw.rect(screen, ACCENT,
                         (slider_rect.x, slider_rect.y, fill_w, slider_rect.height), border_radius=4)
        tx = slider_rect.x + fill_w
        pygame.draw.circle(screen, TEXT_MAIN, (tx, slider_rect.centery), 8)

        # Grid cells
        for r in range(ROWS):
            for c in range(COLS):
                cx = GRID_X + c * CELL
                cy = GRID_Y + r * CELL
                rect = pygame.Rect(cx + 1, cy + 1, CELL - 2, CELL - 2)

                if (c, r) in best_cells:
                    col = CELL_BEST
                elif (c, r) in candidates:
                    col = CELL_CAND
                elif (c, r) in highlights:
                    col = CELL_HL
                elif rect.collidepoint(mx, my) and not running:
                    col = CELL_HOVER
                else:
                    col = CELL_EMPTY

                draw_rounded_rect(screen, col, rect, r=5)

                obj = map_state[r][c]
                if obj == utils.OBJECT_HOSPITAL:
                    draw_hospital(screen, cx + CELL // 2, cy + CELL // 2, 30)
                elif obj == utils.OBJECT_HOUSE:
                    draw_house(screen, cx + CELL // 2, cy + CELL // 2, 28)

                coord = font_sm.render(f"{c},{r}", True, (50, 52, 70))
                screen.blit(coord, (cx + 4, cy + CELL - 16))

        # Grid lines
        for c in range(COLS + 1):
            pygame.draw.line(screen, GRID_LINE,
                             (GRID_X + c * CELL, GRID_Y),
                             (GRID_X + c * CELL, GRID_Y + GRID_H))
        for r in range(ROWS + 1):
            pygame.draw.line(screen, GRID_LINE,
                             (GRID_X, GRID_Y + r * CELL),
                             (GRID_X + GRID_W, GRID_Y + r * CELL))

        # Manhattan distance lines
        for (hpx, hpy) in utils.find_objects(map_state, utils.OBJECT_HOSPITAL):
            cx1 = GRID_X + hpx * CELL + CELL // 2
            cy1 = GRID_Y + hpy * CELL + CELL // 2
            for (hx2, hy2) in utils.find_objects(map_state, utils.OBJECT_HOUSE):
                cx2 = GRID_X + hx2 * CELL + CELL // 2
                cy2 = GRID_Y + hy2 * CELL + CELL // 2
                pygame.draw.line(screen, (50, 80, 120), (cx1, cy1), (cx2, cy2), 1)

        # Stats panel
        panel_y = GRID_Y + GRID_H + 14
        panel   = pygame.Rect(PAD, panel_y, WIN_W - PAD * 2, 80)
        draw_rounded_rect(screen, PANEL_BG, panel, r=8, border=1, border_color=GRID_LINE)

        stats = [
            ("Costo actual", str(cur_cost),  TEXT_WARN if cur_cost > best_cost else TEXT_OK),
            ("Mejor costo",  str(best_cost), TEXT_OK),
            ("Iteraciones",  str(iters),     TEXT_INFO),
            ("Estado",
             "corriendo" if running else ("listo!" if done else "en espera"),
             TEXT_OK if done else (TEXT_WARN if running else TEXT_DIM)),
        ]
        col_w = (WIN_W - PAD * 2) // len(stats)
        for i, (lbl, val, vcol) in enumerate(stats):
            sx = PAD + i * col_w + 16
            screen.blit(font_sm.render(lbl, True, TEXT_DIM), (sx, panel_y + 12))
            screen.blit(font_lg.render(val, True, vcol),     (sx, panel_y + 30))

        # Log panel
        log_y     = panel_y + 96
        log_panel = pygame.Rect(PAD, log_y, WIN_W - PAD * 2, 100)
        draw_rounded_rect(screen, PANEL_BG, log_panel, r=8, border=1, border_color=GRID_LINE)
        screen.blit(font_sm.render("log", True, TEXT_DIM), (PAD + 10, log_y + 6))
        for i, (msg, col) in enumerate(log_lines[-5:]):
            screen.blit(font_sm.render(msg, True, col), (PAD + 10, log_y + 22 + i * 15))

        # Legend
        legend_y = log_y + 108
        items = [
            (CELL_HL,   "hospital seleccionado"),
            (CELL_CAND, "candidato"),
            (CELL_BEST, "mejor movimiento"),
        ]
        lx = PAD
        for bg, txt in items:
            pygame.draw.rect(screen, bg, (lx, legend_y, 14, 14), border_radius=3)
            l = font_sm.render(txt, True, TEXT_DIM)
            screen.blit(l, (lx + 18, legend_y))
            lx += 18 + l.get_width() + 20

        hint = font_sm.render(
            "ESPACIO: correr   N: paso   R: reset   G: aleatorio", True, (45, 48, 65)
        )
        screen.blit(hint, (PAD, legend_y + 22))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
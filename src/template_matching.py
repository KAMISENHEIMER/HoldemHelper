import cv2
import numpy as np
import glob
import os

#SETTINGS
CONFIDENCE_THRESHOLD = 0.5
SEARCH_SCALES = [0.8, 0.9, 1.0, 1.1, 1.2] 

#load in templates from template directory
def load_templates():
    template_dir="templates"

    rank_templates = []
    suit_templates = []

    def load_category(subfolder, target_list):
        search_path = os.path.join(template_dir, subfolder, "*.png")
        files = glob.glob(search_path)
        if not files:
            print(f"WARNING: No templates found in {search_path}")
            
        for path in files:
            filename = os.path.basename(path)
            
            #remove suffixes (for multiple versions/fonts of template)
            label = filename.split('_')[0].split('.')[0]
            
            img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            target_list.append((label, img))

    load_category("ranks", rank_templates)
    load_category("suits", suit_templates)

    return rank_templates, suit_templates

#sweeps templates over corner
def scan_for_best_match(search_area, templates):
    best_label = "Unknown"
    best_score = -1
    best_location = (0,0,0,0)

    #for every template
    for label, tpl in templates:
        tpl_h, tpl_w = tpl.shape[:2]

        #for every scale
        for scale in SEARCH_SCALES:
            new_w, new_h = int(tpl_w * scale), int(tpl_h * scale)
            
            if new_w >= search_area.shape[1] or new_h >= search_area.shape[0]:
                continue
                
            resized_tpl = cv2.resize(tpl, (new_w, new_h))

            res_norm = cv2.matchTemplate(search_area, resized_tpl, cv2.TM_CCOEFF_NORMED)
            _, score, _, loc = cv2.minMaxLoc(res_norm)

            #keep best match
            if score > best_score:
                best_score = score
                best_label = label
                best_location = (loc[0], loc[1], new_w, new_h)

    return best_label, best_score, best_location


#classify a single card image
def classify_card(card_img):
    #prepare for searching
    gray = cv2.cvtColor(card_img, cv2.COLOR_BGR2GRAY)
    corner = gray[0:130, 0:80]

    #search for best rank
    rank, r_score, r_loc = scan_for_best_match(corner, CLASS_RANK_TEMPLATES)
    
    #mask out found rank to avoid interference when searching for suit
    if r_score > CONFIDENCE_THRESHOLD:
        x, y, w, h = r_loc
        cv2.rectangle(corner, (x, y), (x+w, y+h), (0), -1)

    #search for best suit
    suit, s_score, s_loc = scan_for_best_match(corner, CLASS_SUIT_TEMPLATES)

    if r_score < CONFIDENCE_THRESHOLD: rank = "Unknown"
    if s_score < CONFIDENCE_THRESHOLD: suit = "Unknown"

    return rank, suit, r_score, s_score

#setup
def classify_cards(cards):
    global CLASS_RANK_TEMPLATES, CLASS_SUIT_TEMPLATES
    CLASS_RANK_TEMPLATES, CLASS_SUIT_TEMPLATES = load_templates()

    results = []
    for card in cards:
        rank, suit, rs, ss = classify_card(card)

        results.append((rank, suit, rs, ss))
    return results

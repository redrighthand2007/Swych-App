import os
import glob

def unmingle(s):
    res = bytearray()
    for c in s:
        o = ord(c)
        if o < 256:
            res.append(o)
        elif o == 0x0178: res.append(0x9f)
        elif o == 0x2014: res.append(0x97)
        elif o == 0x201c: res.append(0x93)
        elif o == 0x201d: res.append(0x94)
        elif o == 0x2018: res.append(0x91)
        elif o == 0x2019: res.append(0x92)
        elif o == 0x201a: res.append(0x82)
        elif o == 0x201e: res.append(0x84)
        elif o == 0x2020: res.append(0x86)
        elif o == 0x2021: res.append(0x87)
        elif o == 0x2022: res.append(0x95)
        elif o == 0x2026: res.append(0x85)
        elif o == 0x2030: res.append(0x89)
        elif o == 0x2039: res.append(0x8b)
        elif o == 0x203a: res.append(0x9b)
        elif o == 0x20ac: res.append(0x80)
        elif o == 0x2122: res.append(0x99)
        elif o == 0x0152: res.append(0x8c)
        elif o == 0x0153: res.append(0x9c)
        elif o == 0x0160: res.append(0x8a)
        elif o == 0x0161: res.append(0x9a)
        elif o == 0x02c6: res.append(0x88)
        elif o == 0x02dc: res.append(0x98)
        elif o == 0x017d: res.append(0x8e)
        elif o == 0x017e: res.append(0x9e)
        elif o == 0x0192: res.append(0x83)
        else: res.append(ord('?'))
    try:
        return res.decode('utf-8')
    except Exception as e:
        return s  # fallback if it wasn't mojibake

md_files = glob.glob('docs/project/*.md') + ['CHANGELOG.md']

for path in md_files:
    if os.path.exists(path):
        with open(path, 'rb') as f:
            raw = f.read()
        
        # Remove BOM if present
        if raw.startswith(b'\xef\xbb\xbf'):
            raw = raw[3:]
            
        try:
            text = raw.decode('utf-8')
            if '\\xc3' in str(raw): # Very naive heuristic for mojibake
                fixed_text = unmingle(text)
                if fixed_text != text:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(fixed_text)
                    print(f"Fixed {path}")
        except Exception as e:
            print(f"Error on {path}: {e}")


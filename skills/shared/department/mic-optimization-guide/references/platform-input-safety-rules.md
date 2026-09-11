# MIC Platform Input Safety Rules

These rules apply to ALL MIC product upload methods, including Chrome extension paste format (`mic-made-in-china-fill`), manual form filling, and browser automation.

---

## Rule 1: English-Only Input

**All form inputs ONLY accept English, numbers, and English punctuation — NO Chinese characters.**

| Allowed | Forbidden |
|---------|-----------|
| A-Z, a-z, 0-9 | Chinese characters (中文) |
| Space, hyphen `-`, comma `,` | Chinese punctuation（，。！？：；""''【】《》） |
| Period `.`, slash `/`, parentheses `()` | Full-width symbols |
| Colon `:`, semicolon `;`, apostrophe `'` | |
| Quote `"`, percent `%`, degree `°` | |
| Plus `+`, equals `=`, less/greater `<>` | |

**Applies to:** Product name, keywords, attributes, highlights, FAQ, descriptions, custom attributes

**Exception:** Category dropdown options provided by MIC system may contain Chinese — these are system labels, not user inputs.

**Examples:**
- ✅ "IP65" ❌ "IP65防水"
- ✅ "2.4GHz" ❌ "2.4G赫兹"
- ✅ "5-year warranty" ❌ "5年保修"

---

## Rule 2: Button Verification (For Browser Automation)

**ALWAYS verify a button's label or icon BEFORE clicking. NEVER click based on ref number alone.**

**Unicode icons in MIC terminal output:**

| Unicode | Meaning | Action | Common Location |
|---------|---------|--------|-----------------|
| `` | add/plus icon | Add/Create | "添加", "添加自定义属性", "添加规格" |
| `` | delete/X icon | Delete/Remove | Next to filled fields, in tables |
| `` | separator | Visual divider | Between attribute rows |
| `` | question mark icon | Help/Info | Next to field labels |
| `` | dropdown arrow | Expand/Collapse | Dropdown indicators |

**Verification procedure:**
```bash
agent-browser snapshot | grep -B 2 -A 2 "ref=<target>"
# Read text → confirm matches intended action → click
```

**`` is ALWAYS delete — never click it unless explicitly asked to delete.**

---

## Rule 3: Input Box Verification (For Browser Automation)

**ALWAYS verify an input box is empty before filling it.**

If the input box already contains text, you have the **wrong ref** OR you are about to **overwrite existing data**.

**Verification:**
```bash
agent-browser snapshot | grep -A 1 "ref=<target>"
# Should show empty, placeholder, or expected content
```

**Rules:**
- Unfilled inputs should be empty
- If not empty → ref may be wrong / page changed
- After any page change, re-run snapshot for fresh refs

---

## Rule 4: Dynamic Ref Tracking (For Browser Automation)

**Track dynamically created inputs by before/after ref comparison — the ONLY reliable method.**

```bash
# Before clicking "添加"
BEFORE=$(agent-browser snapshot | grep -oE "ref=e[0-9]+" | sort -u)

# Click add
agent-browser click <add-button-ref>

# After clicking
AFTER=$(agent-browser snapshot | grep -oE "ref=e[0-9]+" | sort -u)

# Find new refs
NEW_REFS=$(comm -13 <(echo "$BEFORE") <(echo "$AFTER"))
```

---

## Rule 5: Wait for User Instruction

**After filling ANY field, WAIT for explicit user confirmation before proceeding.**

Do NOT automatically proceed to the next field without user approval.

**Exception:** When user explicitly says "自主完成" / "继续" / "接下来的你自己操作"

---

## Rule 6: Distinguish 规格管理 vs 自定义属性

| Section | Purpose | Example |
|---------|---------|---------|
| **规格管理** (Spec Management) | Product variants with different prices/MOQs | Size: 10W/18W/36W |
| **自定义属性** (Custom Attributes) | Additional product info for buyers | Weight, Case Material |

**Unit Size belongs in 规格管理, NOT custom attributes.**

---

## Rule 7: Category Selection Check

**Always check for sub-groups before confirming category selection.**

1. Select main group
2. Check if sub-groups appear
3. Select most appropriate sub-group
4. Then click "确定" (Confirm)

**Example hierarchy:**
```
Electronic Price Tag (main)
├── ESL (Ink price tag)
├── LCD Price Tag ← Select this for LCD products
└── Others Electronic Price Tag
```

---

## Rule 8: "折中" Calculation

**"折中" means EXACT mathematical middle: (min + max) / 2, then pick closest available option.**

Example: Range 10-25ms → (10+25)/2 = 17.5 → closest available = **16ms** (NOT 20ms)

---

## agent-browser Limitations Summary

| Element | Support | Workaround |
|---------|---------|------------|
| Text input | ✅ Reliable | Direct fill |
| Checkbox | ✅ Reliable | Direct click |
| Button | ✅ With verification | Verify text first |
| **Dropdown** | ❌ **Unreliable** | **User manual selection** |
| File upload | ❌ Not supported | User manual upload |
| Rich text editor | ❌ Not supported | User manual edit |

**Never attempt to automate dropdown selection on MIC — always delegate to user.**

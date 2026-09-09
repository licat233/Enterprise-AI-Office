# Product Information Lookup Order for MIC Uploads

When preparing MIC product upload data, follow this lookup sequence to ensure accuracy:

## 1. Obsidian Memory and Product KB CSV (Primary Source)

Search the current ARMOR Vault first for user-confirmed parameters, recent upload decisions, and durable product context:

```bash
rg -n "HM-CSP-480|CSP strip|480LED" "$ARMOR_VAULT_ROOT/01-Knowledge" "$ARMOR_VAULT_ROOT/02-Projects"
```

Then check the stable ARMOR product lookup CSV:

**Path:** `${ARMOR_VAULT_ROOT}/01-Knowledge/Products/ARMOR_Product_Knowledge_Base.csv` (resolve from env var at runtime)

**Why first:** Obsidian is the current long-term memory source, and the stable CSV is the default product lookup entry. This keeps uploads aligned even when the source workbook changes over time.

## 2. User Confirmation for Missing Product Facts

If the stable CSV lacks a product field, do not use legacy external work folders as a fallback product data source. Ask the user or mark the value `[TO CONFIRM]` in the `.md` reference file.

## 3. MIC Product Export CSV

Do not use legacy `armor-MIC-products-*.csv` exports as an active product source. If existing MIC listing values are needed, ask the user to provide the relevant export or page context for the current task.

## 4. Session Search

Search past sessions for product-specific discussions:

```bash
session_search(query="HM-CSP-480 specifications")
```

## 5. User Confirmation (Final Resort)

If critical parameters (voltage, power, certifications, pricing) are missing after all above sources, explicitly ask the user:

> "[Parameter] not found in Obsidian memory, product KB, or MIC export files. Please confirm: [specific question]"

**Never fabricate:** Voltage, power, certifications, dimensions, pricing, or HS codes must come from authoritative sources, never invented.

# Platform-Specific GEO Optimization

## ChatGPT

### Ranking Factors
| Factor | Weight | Details |
|--------|--------|---------|
| Authority & Credibility | 40% | Branded domains preferred over third-party |
| Content Quality & Utility | 35% | Clear structure, comprehensive answers |
| Platform Trust | 25% | Wikipedia, Reddit, Forbes prioritized |

### Key Statistics
- Referring Domains: >350K domains = 8.4 avg citations
- Domain Trust Score: 91-96 score = 6 citations; 97-100 = 8.4 citations
- Content Recency: 30-day old content gets 3.2x more citations
- Branded vs Third-party: Branded domains cited 11.1 points more

### Optimization
- Build strong backlink profile (quality > quantity)
- Update content within 30 days
- Use clear H1/H2/H3 structure
- Include verifiable statistics with citations
- Write in conversational style
- Ensure domain has high trust score

---

## Perplexity AI

### Architecture
Uses RAG with 3-layer reranking system:
1. L1: Basic relevance retrieval
2. L2: Traditional ranking factors scoring
3. L3: ML models for quality evaluation

### Key Factors
- FAQ Schema (JSON-LD): Pages with FAQ blocks cited more often
- PDF Documents: Publicly hosted PDFs prioritized
- Content Velocity: Speed of publishing matters more than keyword density
- Semantic Payloads: Clear, atomic paragraphs preferred

### Optimization
- Allow PerplexityBot in robots.txt
- Implement FAQ Schema markup
- Create publicly accessible PDF resources
- Use Article schema with timestamps
- Focus on semantic relevance, not keywords
- Build topical authority in your niche

---

## Google AI Overview (SGE)

### 5-Stage Source Prioritization Pipeline
1. Retrieval - Identify candidate sources
2. Semantic Ranking - Evaluate topical relevance
3. LLM Re-ranking - Assess contextual fit (using Gemini)
4. E-E-A-T Evaluation - Filter for expertise/authority/trust
5. Data Fusion - Synthesize from multiple sources with citations

### Key Statistics
- AI Overviews in searches: 85%+
- Overlap with traditional Top 10: Only 15%
- Traditional factors weight: 62%
- Novel AI signals weight: 38%
- SGE-optimized visibility boost: 340%

### Ranking Factors
- E-E-A-T: Experience, Expertise, Authoritativeness, Trustworthiness
- Structured Data: Schema markup helps AI understand content
- Knowledge Graph: Being in Google's Knowledge Graph = boost
- Topical Authority: Content clusters + internal linking
- Authoritative Citations: +132% visibility with trusted references
- Authoritative Tone: +89% visibility improvement

### Optimization
- Implement comprehensive Schema markup
- Build topical authority with content clusters
- Include authoritative citations and references
- Use E-E-A-T signals (author bios, credentials)
- Target informational "how-to" queries

---

## Microsoft Copilot / Bing

### Ranking Factors
- Bing Index: Must be indexed by Bing to be cited
- Microsoft Ecosystem: LinkedIn, GitHub mentions provide boost
- Crawlability: BingBot + PermaBot must have access
- Page Speed: < 2 seconds load time
- Schema Markup: Helps Copilot understand content
- Entity Clarity: Clear definitions of entities/concepts

### Optimization
- Submit site to Bing Webmaster Tools
- Ensure Bingbot can crawl all pages
- Use IndexNow for new content
- Optimize page speed (< 2 seconds)
- Clear entity definitions in content
- Build presence on LinkedIn, GitHub

---

## Claude AI

### Architecture
**Important:** Claude uses Brave Search, NOT Google or Bing!

### Ranking Factors
- Brave Index: Must be indexed by Brave Search
- Query Rewriting: Claude reformulates queries for search
- Factual Density: Data-rich content preferred
- Structural Clarity: Easy to extract information
- Source Authority: Trustworthy, well-sourced content

### Key Statistic
**Crawl-to-Refer Ratio: 38,065:1**
- Claude consumes massive amounts of content
- Very selective about what it cites
- Quality and relevance are critical

### Optimization
- Ensure Brave Search indexing
- Allow ClaudeBot in robots.txt
- Create high factual density content
- Use clear, extractable structure
- Include verifiable data points
- Cite authoritative sources

---

## Cross-Platform Summary

| Platform | Primary Index | Key Factor | Unique Requirement |
|----------|--------------|------------|-------------------|
| ChatGPT | Web (Bing-based) | Domain Authority | Content-Answer Fit |
| Perplexity | Own + Google | Semantic Relevance | FAQ Schema |
| Google SGE | Google | E-E-A-T | Knowledge Graph |
| Copilot | Bing | Bing Index | MS Ecosystem |
| Claude | Brave | Factual Density | Brave Indexing |

## Universal Best Practices

1. Allow all major bots in robots.txt
2. Implement Schema markup (FAQPage, Article, Organization)
3. Build authoritative backlinks
4. Update content regularly (within 30 days)
5. Use clear structure (H1 > H2 > H3, lists, tables)
6. Include statistics and citations
7. Optimize page speed (< 2 seconds)
8. Ensure mobile-friendly design

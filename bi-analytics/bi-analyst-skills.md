---
title: BI Analyst Skills & Competencies
category: BI Tools - Career
tags: [BI-analyst, skills, competencies, information-design, UX, storytelling, web-analytics, career]
---

# BI Analyst Skills & Competencies

Core competency model for BI and product analysts. Covers the five visualization skills, analyst roles in teams, and the relationship between web analytics, product analytics, and BI development.

## Key Facts

- Analytics is a mindset, not just a profession about numbers
- Only 5% of projects have fully functioning analytics, while 90% want it
- Product analyst vs general analyst: product analyst works in a product company where decisions are user-driven
- BI analyst competency matrix available as a self-assessment tool (6 sections, 1-4 scale per question)
- Web analyst tasks: configure analytics tools (GA, YM), build reports, analyze traffic sources, describe customer portraits, analyze site funnel
- [[dashboard-design-patterns]] and [[visualization-principles]] are core deliverables
- Connected to [[product-metrics-nsm]] for metric selection skills

## Five Visualization Skills

| Skill | Description | Priority |
|-------|-------------|----------|
| **1. Technical tool knowledge** | Tableau/Power BI proficiency, workarounds for tool limitations | Core |
| **2. Information design** | Tufte principles, visual encoding, data-ink ratio, chart selection | Core |
| **3. Graphic design** | Layout, composition, adaptive design, contrast, modular grids | Core |
| **4. UX design** | User scenarios, control selection, actionable dashboards, requirements gathering | Core |
| **5. Storytelling** | Data narrative, annotations, data journalism (more for presentations than dashboards) | Supporting |
| **6. Code style** | Naming conventions, comments, collaborative workbook practices | Supporting |
| **7. Domain knowledge** | Statistics, business understanding, common sense | Supporting |

## Patterns

**Analyst role in team (5-step cycle):**

```
1. Define key metrics
   - What reflects business effectiveness?
   - What measures customer satisfaction?
   - What defines an ideal customer?

2. Collect data
   - Where to collect from?
   - Is data complete enough?
   - What data needed at scale?
   - Will site changes break collection?

3. Analyze data
   - Is data correct?
   - Is data complete for analysis?
   - How exactly to analyze?
   - Can we quantitatively verify hypotheses?

4. Experiment
   - Is the result statistically significant?
   - Which tools for the experiment?
   - How long to run the experiment?
   - How many experiments needed?

5. Implement
   - What result will implementation give?
   - What resources needed?
   - Does ROI justify implementation?
   - What are the risks?
```

**Web analyst vs product analyst vs BI developer:**

```
Web Analyst:
  - Focus: traffic, conversions, channel optimization
  - Tools: Google Analytics, Yandex Metrika, GTM
  - Output: channel reports, attribution, A/B tests

Product Analyst:
  - Focus: user behavior, feature impact, growth
  - Tools: Amplitude, Mixpanel, custom SQL
  - Output: retention curves, feature adoption, experiment analysis

BI Developer:
  - Focus: data infrastructure, reporting systems
  - Tools: Tableau, Power BI, dbt, SQL
  - Output: dashboards, data pipelines, self-service analytics
```

## Gotchas

- **Symptom**: Analytics setup breaks when site changes -> **Cause**: Tracking implementation not documented or owned -> **Fix**: Maintain tracking plan document, involve analyst in deploy process
- **Symptom**: Beautiful dashboard but nobody uses it -> **Cause**: Focused on graphic design (skill 3) without UX design (skill 4) -> **Fix**: Start from user scenarios, interview stakeholders about their decision-making workflow
- **Symptom**: Dashboard tells no story, just shows numbers -> **Cause**: Missing context and storytelling (skill 5) -> **Fix**: Add annotations, goals, comparisons, event markers for self-explanatory context

## See Also

- [[dashboard-design-patterns]] - applying design patterns to real dashboards
- [[visualization-principles]] - Tufte's core principles for information design
- [[product-metrics-nsm]] - metric selection skills for product analysts
- Tableau competency matrix: https://help.tableau.com/current/blueprint/en-us/bp_analyst_competencies.htm

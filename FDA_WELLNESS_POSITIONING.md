# FDA Wellness Positioning Audit

## 1. FDA wellness / SaMD line reference

- CycleSync should stay in the general wellness lane: supporting awareness, reflection, habits, routines, and non-clinical wellbeing.
- User-facing claims should avoid diagnosing, treating, curing, mitigating, preventing, or monitoring any disease or medical condition.
- Cycle forecasts must be framed as estimates or patterns, not medical predictions.
- Cycle Battery should describe subjective readiness, energy, recovery, and routine fit, not physiological status or clinical risk.
- AI outputs should be positioned as wellness reflections and suggestions, not professional recommendations or automated decisions.
- HealthKit data should be presented as contextual wellness signals, not as diagnostic evidence.
- Any fertility, contraception, pregnancy-risk, pathology, or urgent symptom language should be excluded or redirected to professional care.

## 2. User-facing claims audit table

| source | exact text | wellness-side reasoning | verdict |
| --- | --- | --- | --- |
| Forecast headlines | "Your next period may start around [date]." | Framed as an estimate of a personal cycle pattern, not a clinical prediction. | ✅ Wellness |
| Forecast headlines | "PMS risk is high this week." | "Risk" can imply clinical prediction or health assessment. Rephrase to pattern-based, non-diagnostic language. | ⚠️ Borderline |
| Forecast headlines | "You are entering a lower-energy window." | Wellness-oriented energy framing, suitable if shown as pattern estimate. | ✅ Wellness |
| Cycle Battery verdicts | "Low Battery: prioritise recovery today." | General recovery and routine suggestion, not medical treatment. | ✅ Wellness |
| Cycle Battery verdicts | "Hormonal imbalance likely." | Suggests medical inference and possible diagnosis. | ❌ SaMD |
| Cycle Battery verdicts | "Your signals suggest a heavier day. Keep plans lighter if you can." | Soft behavioural suggestion based on wellness context. | ✅ Wellness |
| Daily Protocol pillars | "Movement: choose gentle intensity." | General wellness coaching. | ✅ Wellness |
| Daily Protocol pillars | "Nutrition: aim for steady meals and hydration." | General lifestyle information, not disease-specific. | ✅ Wellness |
| Daily Protocol pillars | "Take magnesium to reduce cramps." | Supplement and symptom treatment claim. | ⚠️ Borderline |
| Granger output | "Sleep changes often precede lower reported energy in your logs." | Pattern reflection from user data without diagnosis or causation certainty. | ✅ Wellness |
| Granger output | "Poor sleep causes your luteal anxiety." | Causal mental health claim and condition language. | ❌ SaMD |
| Insight summaries | "You often log headaches near the late luteal phase." | Personal pattern summary, not diagnosis. | ✅ Wellness |
| Insight summaries | "This pattern may indicate PCOS." | Medical condition inference. | ❌ SaMD |
| Watch complications | "Cycle Day 24 · Low energy estimate." | Compact wellness context; acceptable if clearly estimated. | ✅ Wellness |
| Watch complications | "High fertility today." | Fertility-critical claim can be used for pregnancy or contraception decisions. | ⚠️ Borderline |
| Onboarding niche | "Energy and recovery." | Wellness-focused user preference. | ✅ Wellness |
| Onboarding niche | "Manage PMDD symptoms." | Disease-specific management claim. | ❌ SaMD |
| Onboarding niche | "Symptoms and patterns." | Neutral self-tracking language. | ✅ Wellness |

## 3. Borderline rephrases

| borderline text | safer rephrase |
| --- | --- |
| "PMS risk is high this week." | "You often report pre-period symptoms around this point in your cycle." |
| "Take magnesium to reduce cramps." | "If it already fits your routine, consider supportive basics like hydration, regular meals, rest, and gentle movement. For supplements or persistent pain, ask a qualified professional." |
| "High fertility today." | "Estimated fertile-window context. Do not use CycleSync for contraception, fertility-critical, or pregnancy-risk decisions." |

Rejected text should not be shipped:

| rejected text | replacement direction |
| --- | --- |
| "Hormonal imbalance likely." | "Your recent logs differ from your usual pattern." |
| "Poor sleep causes your luteal anxiety." | "Lower sleep and lower mood appear close together in some of your logs." |
| "This pattern may indicate PCOS." | "This recurring pattern may be worth discussing with a qualified healthcare professional if it concerns you." |
| "Manage PMDD symptoms." | "Track mood and cycle patterns." |

## 4. EU MDR + EU AI Act watchlist

CycleSync should continue to avoid medical purpose claims under EU MDR and should not imply diagnosis, prevention, monitoring, prediction, prognosis, treatment, or alleviation of disease. Under the EU AI Act, CycleSync's AI features should remain transparent, wellness-limited, optional where appropriate, and free from prohibited Article 5 practices such as manipulation, exploitation of vulnerabilities, social scoring, sensitive biometric categorisation, or emotion recognition in workplace or education contexts. Any future subscription, expanded AI feature, fertility feature, pregnancy feature, or clinician-facing export should be re-audited before release.

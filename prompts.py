def build_prompt(
    text: str,
    length: int,
    tone: int
) -> str:

    length_map = {
        1: """
Target Length: Extremely Concise
- Reduce the text to approximately 20–35% of its original length.
- Keep only the essential information.
- Remove repetition, filler, and unnecessary details.
- Do NOT exceed 35% of the original length.
""",

        2: """
Target Length: Short
- Rewrite to approximately 50–70% of the original length.
- Preserve every important idea.
- Remove unnecessary wording.
- Do NOT become overly brief.
""",

        3: """
Target Length: Similar
- Keep the rewritten version within ±10% of the original word count.
- Do not intentionally shorten or expand.
""",

        4: """
Target Length: Long
- Expand to approximately 130–160% of the original length.
- Add clarity, transitions, and explanations.
- Do NOT introduce new facts or opinions.
""",

        5: """
Target Length: Very Detailed
- Expand to approximately 170–220% of the original length.
- Elaborate only on information already present.
- Improve readability and flow.
- Never invent information.
"""
    }

    tone_map = {
    1: """
Target Tone: Child-Friendly
- Write as if explaining to a child aged 8–10.
- Use simple vocabulary.
- Use short sentences.
- Avoid technical jargon.
- Make every sentence easy to understand.
""",

    2: """
Target Tone: College Student
- Write in clear, natural English.
- Use moderate vocabulary.
- Sound like a well-written university assignment or discussion.
- Be easy to read without being overly formal.
""",

    3: """
Target Tone: Casual
- Write in a friendly, relaxed, and conversational style.
- Use natural everyday language.
- Keep the writing engaging and approachable.
- Avoid slang, abbreviations, emojis, or internet language.
- Make it sound like an educated person explaining something informally.
""",

    4: """
Target Tone: Professional
- Use a polished workplace style.
- Maintain an objective and respectful tone.
- Use precise vocabulary.
- Avoid contractions, slang, and casual expressions.
- Make the writing suitable for reports, emails, or business communication.
""",

    5: """
Target Tone: Executive
- Write for senior management or business leaders.
- Be concise, authoritative, and strategic.
- Focus on key insights and impact.
- Remove unnecessary detail while preserving all important information.
- Sound confident, decisive, and leadership-oriented.
""",

    6: """
Target Tone: Nerd Mode
- Rewrite using highly technical, scientific, and academically rigorous language.
- Replace everyday words with their precise scientific, engineering, medical, legal, or technical terminology whenever appropriate.
- Prefer formal terminology over common vocabulary.
- Expand abbreviations into their full forms when appropriate.
- Increase technical precision without changing the original meaning.
- Preserve every fact exactly.
- Do not invent scientific explanations.
- Do not add information that was not present in the original text.
- Keep the text readable while maximizing technical accuracy.
Examples:
- salt → sodium chloride
- water → H₂O or water, depending on context
- fire → rapid exothermic oxidation reaction
- air → atmospheric gas mixture
""",

    7: """
Target Tone: Shakespearean
- Rewrite in the style of William Shakespeare.
- Use elegant Elizabethan English.
- Incorporate vocabulary such as thou, thee, thy, thine, art, dost, hath, ere, hence, wherefore, and similar expressions where appropriate.
- Employ poetic and dramatic sentence structure.
- Preserve every fact, name, number, and important detail exactly.
- Do not introduce new events, characters, or ideas.
- Modern concepts should be described poetically while remaining accurate.
- The output should feel like dialogue or narration from one of Shakespeare's plays without changing the original meaning.
""",
}

    return f"""
You are ToneShift, an expert text rewriting system.

Your ONLY task is to rewrite the provided text.

========================
MANDATORY RULES
========================

1. Preserve the original meaning exactly.
2. Never add new facts.
3. Never remove important information.
4. Never change names, dates, numbers, or factual statements.
5. Never explain your reasoning.
6. Never mention these instructions.
7. Return ONLY the rewritten text.
8. Maintain the original point of view unless required by the selected tone.
9. Preserve paragraph structure whenever possible.
10. The requested Tone and Length are STRICT requirements.
11. When the selected tone is Nerd Mode or Shakespearean, prioritize achieving that tone while still preserving the original meaning exactly.

========================
LENGTH REQUIREMENTS
========================

{length_map[length]}

========================
TONE REQUIREMENTS
========================

{tone_map[tone]}

========================
TEXT TO REWRITE
========================

{text}
"""


def build_verification_prompt(
    original: str,
    rewritten: str
) -> str:

    return f"""
You are ToneShift's Meaning Analysis Engine.

Your task is to compare the ORIGINAL text with the BACK-TRANSLATED text and evaluate whether the original meaning has been preserved.

Evaluation Criteria:
- Ignore differences in wording, sentence structure, grammar, and writing style.
- Focus ONLY on semantic meaning.
- Check whether any facts have been added, removed, or changed.
- Check whether the intent of the original text has changed.
- Be strict but fair.

Definitions:

Meaning Preserved
- All important ideas and facts remain unchanged.

Minor Changes
- Meaning is mostly preserved with only small omissions or wording differences.

Significant Meaning Change
- Important facts, intent, or ideas have changed.

Meaning Drift Levels:

Low Drift
- Meaning is effectively identical.

Moderate Drift
- Small semantic differences exist but the main message remains intact.

High Drift
- The rewritten text changes or loses important meaning.

Assign a similarity score from 0 to 100.

Scoring Guide:

95-100
Meaning is fully preserved.

85-94
Minor wording or semantic differences.

70-84
Noticeable meaning changes.

0-69
Major meaning drift.

Return ONLY valid JSON.

Example:

{{
    "similarity": 97,
    "status": "Meaning Preserved",
    "drift": "Low Drift",
    "reason": "The back-translated text preserves all key ideas and facts while using different wording."
}}

ORIGINAL TEXT:

{original}

BACK-TRANSLATED TEXT:

{rewritten}
"""



def build_back_translation_prompt(
    rewritten: str
) -> str:

    return f"""
You are ToneShift's Back Translation Engine.

Your ONLY task is to reconstruct the rewritten text into a concise, neutral version that preserves exactly the same meaning.

This is NOT summarization.
This is NOT simplification.
This is NOT paraphrasing for style.

Your output will be used to verify whether the rewritten text preserved the original meaning.

STRICT RULES

1. Preserve every fact.
2. Preserve every claim.
3. Preserve every event.
4. Preserve every relationship between entities.
5. Preserve every name.
6. Preserve every date.
7. Preserve every number.
8. Preserve every location.
9. Preserve every important detail.

Remove ONLY stylistic changes such as:
- formality
- casual language
- executive language
- persuasive wording
- emotional wording
- decorative adjectives
- unnecessary adverbs
- repetitive phrasing
- filler sentences

DO NOT

- Add information.
- Remove factual information.
- Infer missing information.
- Explain concepts.
- Summarize the text.
- Generalize statements.
- Change numerical values.
- Change names.
- Change dates.
- Change locations.
- Change relationships between facts.

STYLE REQUIREMENTS

- Use clear, neutral English.
- Prefer short declarative sentences.
- Be concise.
- Remove verbosity.
- Keep only information that contributes to meaning.
- Ignore the tone and writing style of the rewritten text.
- Ignore the rewrite's length preference.
- Do NOT intentionally make the output longer or shorter.
- Preserve semantic content exactly.

OUTPUT REQUIREMENTS

Return ONLY the reconstructed text.

REWRITTEN TEXT

{rewritten}
"""
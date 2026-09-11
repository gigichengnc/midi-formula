# Evidence boundary

MIDI Formula distinguishes three things:

1. **Explicit generation logic** — rules literally present in AI-written source code, such as section gains, accompaniment patterns, timing offsets and CC ramps.
2. **Documented intent** — explanations recorded in the accompanying composition/production documents.
3. **Observed output** — MIDI files produced by that source project.

The project does **not** claim that explicit source code reveals a model's hidden neural process or private chain of thought. It exposes the executable/programmatic layer that existed between the user's instruction and the generated MIDI artifact.

This distinction is important because a model may write a rule such as `ROLE_GAIN["peak"] = 1.10`; that is inspectable evidence of the generated program, but not proof that the model internally reasoned with a 1.10 multiplier before emitting the code.

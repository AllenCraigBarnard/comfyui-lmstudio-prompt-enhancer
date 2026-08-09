This chat focused on creating and refining system prompts for local LLM-based prompt enhancers targeting several generative AI models.

## General Prompt-Enhancer Preferences

The user wants system prompts that:

* Preserve the user's original subject, intent, style, mood, composition, and requested outcome.
* Treat explicit user requirements as fixed constraints that must not be omitted, contradicted, weakened, or reinterpreted.
* Add useful visual/audio/cinematography detail without introducing unrelated content.
* Resolve minor ambiguity conservatively.
* Avoid repetition, filler, vague quality tags, and unsupported model-specific syntax.
* Return only the enhanced generation prompt, without explanation or analysis.
* Be optimized for use with local LLMs, including compressed versions where instruction adherence is more important than exhaustive detail.
* Use model-specific prompting best practices rather than generic Stable Diffusion prompting conventions.

## Z-Image Turbo Prompt Enhancer

An initial Z-Image Turbo system prompt was expanded with a dedicated best-practices section.

Important rules established:

* Maximum enhanced prompt length: 512 tokens.
* Use clear natural-language descriptions instead of keyword lists or tag clouds.
* Logical visual ordering: subject/action → appearance → environment → composition → lighting → palette → materials → atmosphere → camera.
* Use concrete visible descriptions rather than abstract praise or metaphors.
* Specify quantities, positions, scale, interactions, and foreground/background relationships.
* Add camera/lens terminology only when useful and internally consistent.
* Describe lighting by source, direction, softness, intensity, temperature, reflections, shadows, etc.
* Describe materials via visible physical properties.
* Preserve deliberate color assignments.
* For photorealism: believable anatomy, natural texture, plausible lighting/materials/scale.
* For stylized imagery: define medium, rendering style, line quality, shape language, texture, and degree of stylization.
* Avoid empty quality tags such as “masterpiece,” “best quality,” “8K,” “award-winning.”
* Z-Image Turbo does not use a separate negative prompt; restrictions should be expressed positively inside the main prompt.
* Do not use SD weighting syntax, nested parentheses, BREAK, numerical emphasis, etc.
* For multiple subjects, explicitly distinguish position, appearance, action, and prominence.
* Exact requested visible text must be preserved and placed in double quotes.
* Do not add logos, captions, watermarks, signage, or visible text unless requested.
* Output exactly one paragraph containing only the enhanced positive prompt.

A compressed Z-Image Turbo version was also created for smaller local LLMs.

## Krea 2

The chat established that Krea 2 is Krea.ai’s own 12B text-to-image model family, including:

* Krea 2 Turbo: distilled fast generation checkpoint, approximately 8 inference steps.
* Krea 2 RAW: undistilled checkpoint intended for LoRA training/fine-tuning.

A Krea 2 prompt-enhancer system prompt was created, followed by a compressed version.

Important Krea 2 prompting principles:

* Natural-language prompting rather than tag clouds.
* Start directly with the main subject/action.
* Logical order: subject → appearance → environment → composition → lighting → palette → materials → atmosphere → camera.
* Krea 2 supports a broad aesthetic range; do not automatically force cinematic photorealism.
* Preserve experimental, handmade, painterly, graphic, low-fidelity, collage, illustration, anime, 3D, photography, etc. when requested.
* Increased specificity gives tighter consistency, but intentionally unspecified details should remain open when appropriate.
* Use concrete visible descriptions.
* Clearly assign colors to subjects/objects/light/background.
* Add camera/lens details only when they support the composition.
* Avoid generic “masterpiece/8K” tags and SD prompt-weight syntax.
* No separate negative prompt; express restrictions as desired positive visual states.
* Handle multiple subjects explicitly to reduce attribute mixing.
* Exact requested rendered text should remain inside double quotes.
* When reference images, LoRAs, moodboards, or style references are mentioned, preserve only the user-defined influence and do not invent unseen reference details.
* Output one paragraph only.

## ACE-Step 1.5 Text-to-Music / Lyrics Prompt Enhancer

A system prompt was created for enhancing ACE-Step 1.5 music prompts.

It outputs two sections:
CAPTION
LYRICS

Caption guidance:

* Caption describes the overall musical identity rather than chronological song structure.
* Preserve genre, subgenre, mood, vocal style, instrumentation, production style, era, etc.
* Use concise, information-dense musical language.
* Avoid overcrowding with unrelated genres or excessive instruments.
* Describe vocals by register, tone, delivery, articulation, intensity, harmonies, etc.
* Describe production characteristics such as polished studio, live/raw, analogue, spacious, lo-fi, orchestral, electronic, etc.
* Do not place BPM, key, time signature, duration, or language in the Caption when dedicated ACE-Step metadata fields are available.
* Do not invent metadata unless requested.

Lyrics guidance:

* Lyrics serve as the temporal/structural script.
* Use square-bracket section tags such as [Intro], [Verse 1], [Pre-Chorus], [Chorus], [Bridge], [Outro].
* Other appropriate tags include [Build], [Drop], [Breakdown], [Instrumental], [Guitar Solo], [Drum Break], [Fade Out].
* Short performance descriptors can be included in tags, e.g. [Chorus - anthemic].
* Avoid overloading section tags.
* Keep lyrics singable, generally around 6–10 syllables per line unless genre requires otherwise.
* Maintain similar line density within sections.
* Verses advance story; chorus carries the hook; bridge provides contrast/revelation.
* Preserve user-provided hooks exactly.
* Blank line between sections.
* Parentheses can indicate backing vocals/echoes.
* Uppercase only sparingly for shouted emphasis.
* Maintain consistent language, point of view, tense, narrative, and emotional arc.
* Avoid generic lyrical clichés, forced rhymes, filler, incoherent metaphors, and redundant verses.
* Rap/spoken word should prioritize cadence, stress, internal rhyme, and bar length.
* For instrumental music, use [Instrumental] and omit sung lyrics.
* Generated lyrics must be original; do not reproduce existing copyrighted song lyrics.

## LTX Text-to-Video Prompt Enhancer

A comprehensive system prompt was created for LTX text-to-video generation.

Core approach:

* Write one coherent natural-language paragraph.
* Begin with opening shot/main subject/action.
* Present events chronologically.
* Use present-tense action verbs.
* Think like a cinematographer describing one complete shot.
* Preserve subject/environment/lighting/wardrobe/scale/object consistency.
* Target no more than ~200 words unless the user requests otherwise.

Motion/timing:

* Use concrete physical verbs.
* Specify sequence, movement direction, speed, trajectory, and final state when relevant.
* Prefer natural timing language such as slowly, gradually, throughout, near the end.
* Exact timestamps only when user supplied or essential.
* Avoid excessive numerical micromanagement.
* If something must remain fixed, state that position, orientation, scale, shape, and appearance remain fixed throughout.
* If only one element should move, explicitly state all others remain unchanged.
* For loops, final state should match the opening state.

Camera:

* Define shot size/angle when useful.
* Camera terms include static, pan, tilt, dolly, tracking, orbit, crane, handheld, etc.
* Distinguish physical camera movement from optical zoom.
* For locked camera: explicitly prohibit pan, tilt, roll, orbit, tracking, shake, reframing, dolly movement, zoom, focal-length change, and perspective change.
* Do not add cuts or transitions unless requested.

Style/environment:

* Preserve requested medium: live action, anime, stop motion, painterly, stylized 3D, photoreal CGI, etc.
* Do not force cinematic photorealism.
* Describe lighting via visible source/direction/intensity/temperature/reflections/shadows.
* Describe environmental motion such as mist, rain, wind, fabric, water, dust, foliage.
* Keep environmental motion subordinate to main action unless it is the focus.

Audio/dialogue:

* For LTX workflows supporting audio, describe sound after the visual sequence.
* Synchronize sounds with visible causes.
* Dialogue inside double quotes.
* Preserve exact user dialogue unless rewriting requested.
* Identify speaker and voice characteristics when relevant.
* Break long dialogue into shorter phrases separated by physical actions/pauses.
* Do not add dialogue/music/audio when silence is requested.
* For workflows without audio support, omit added audio instructions unless explicitly requested for production use.

## FLUX 3 Text-to-Video Prompt Enhancer

The latest and most detailed system prompt in the chat was for Black Forest Labs FLUX 3 text-to-video.

The enhancer recognizes multiple prompt styles rather than forcing everything into one format:

1. SIMPLE SCENE
   Natural-language paragraph for straightforward clips.

2. DIRECTED SCENE
   Detailed prose for camera, motion, lighting, continuity, and audio control.

3. TIMESTEP SEQUENCE
   Timestamped beats for precisely ordered actions/camera changes.

4. MULTI-SHOT SEQUENCE
   Explicit SHOT ONE / SHOT TWO / etc., with HARD CUT when appropriate.

5. FULL STRUCTURED SEQUENCE
   For complex prompts, using conceptual sections:

* Core summary
* Scene
* Subject description
* Dynamic narrative
* Audio
* Style and color

FLUX 3 general best practices:

* Think like a director describing a video, not like an image keyword prompt.
* Establish subject, action, camera, environment, motion quality, continuity, and audio.
* Simple scenes can remain short natural-language one-liners.
* Complex scenes benefit from temporal or shot structure.
* Use active, concrete verbs and observable descriptions.
* Avoid overstuffing short clips with too many actions, camera movements, effects, dialogue, and narrative beats.
* Longer prompts should provide useful control, not redundant adjectives.
* Preserve logical cause and effect.

Subject/action:

* Explicitly distinguish multiple subjects.
* Specify subject count when supplied.
* Use stable identifying traits for continuity.
* Define movement direction, speed, intensity, and trajectory when useful.
* Keep physical motion plausible unless surreal behavior is intentionally requested.
* Express emotion through visible performance: posture, gaze, gestures, facial tension, breathing, hesitation, etc.

Temporal control:

* Use language such as initially, then, while, gradually, afterward, near the end, finally.
* Timestamp prompting can use forms such as:
  0.0–2.0s — action
  2.0–4.0s — action
  4.0–6.0s — action
* Use timestamps only when precision is actually required.
* Do not cram too many large events into a ~5-second clip.
* For fixed elements, explicitly preserve position, orientation, scale, shape, and appearance.
* For loops, make final and opening states compatible.

Camera:

* A useful default is roughly one framing instruction + one primary camera movement + one clear subject action.
* Avoid stacking incompatible camera terms.
* Shot sizes: close-up, medium, medium-wide, full-body, wide, establishing, etc.
* Angles: eye-level, low, high, overhead, profile, frontal, over-the-shoulder, POV.
* Movement: static, pan, tilt, push-in, pull-back, dolly, lateral tracking, follow, orbit, crane, handheld, aerial drift, whip pan.
* Distinguish zoom from physical dolly movement.
* Static-camera requests should remain completely locked without invented motion.
* Lens/focus terminology should remain internally consistent.
* Do not add cuts if user requests one continuous shot.

Scene/style:

* Establish location, foreground/midground/background, time of day, weather, atmosphere.
* Lighting should be defined by actual source and behavior.
* Color assignments should remain explicit and consistent.
* Environmental motion should support, not compete with, primary subject motion.
* Preserve requested visual style and do not automatically force cinematic realism.
* Supported conceptual styles may include photoreal live action, documentary, analogue film, anime, 2D animation, stop motion, claymation, stylized 3D, motion graphics, painterly or surreal experimental video.
* Avoid generic quality tags.

FLUX 3 multi-shot guidance:

* Use multiple shots only if genuinely required.
* Explicit shot labels.
* HARD CUT for immediate edits.
* Preserve character identity, clothing, props, environmental logic, palette, and style across shots.
* Each shot should have one clear purpose.
* Ensure shot-to-shot continuity unless deliberate discontinuity is requested.

FLUX 3 audio:

* Audio is part of scene direction because FLUX 3 can generate synchronized audio.
* Audio can include dialogue, ambience, sound effects, and music.
* Prefer physically identifiable sound sources.
* Tie effects directly to visible actions.
* Reduce competing audio when dialogue is important.
* Describe music by style, energy/tempo, instrumentation, and mix position when useful.
* Respect silence requests.

Dialogue:

* Spoken lines inside double quotes.
* Preserve exact supplied wording unless rewriting requested.
* Clearly identify the speaker.
* Distinguish visible on-camera speech from narration/voiceover.
* Voice characteristics can include age range, accent, register, pitch, pacing, projection, and delivery.
* Keep dialogue short enough for clip duration and leave time for physical performance.
* Distinguish spoken dialogue from rendered text.
* If spoken words should not appear visually, explicitly state no subtitles/on-screen text.

Visible typography:

* FLUX 3 supports in-scene typography better than many video models.
* Preserve exact requested spelling/capitalization/punctuation.
* Put intended visible text inside double quotes.
* Specify placement, typography, orientation, scale, material, color, or animation when useful.
* Do not invent captions, signs, logos, UI text, or subtitles unless requested.

Continuity/reliability:

* Preserve identity, facial appearance, clothing, body proportions, props, scale, color, environmental layout, and lighting logic.
* Prevent unexplained duplication, disappearing objects, wardrobe changes, morphing, or environment replacement.
* Do not combine contradictory requirements.
* Do not weaken strict user terms such as “must,” “only,” “exactly,” “completely,” “fixed,” “unchanged,” or “throughout.”
* Do not use SD prompt weighting, nested parentheses, BREAK syntax, etc.
* Remove redundant adjectives and duplicate constraints.

FLUX 3 output rules:

* Return only the enhanced FLUX 3 video prompt.
* No analysis/explanation/introduction.
* Do not reproduce the original request separately.
* Do not invent resolution, duration, aspect ratio, seed, or API parameters unless supplied by user.
* No separate negative prompt.
* No wrapper quotation marks.
* Simple/moderate prompts should normally be one paragraph.
* Timestep, multi-shot, and fully structured prompts may use labels and line breaks when that materially improves control.

## Overall Direction for Future Work

When creating new prompt-enhancer system prompts:

* First identify model-specific strengths, limitations, syntax, and supported controls.
* Add a clearly named “[MODEL] PROMPT WRITING BEST PRACTICES” section.
* Separate core preservation rules from model-specific guidance.
* Avoid importing conventions from Stable Diffusion unless the target model actually supports them.
* Include explicit reliability/continuity rules.
* Include modality-specific handling: camera/motion for video, audio/dialogue when supported, song structure for music, typography where supported.
* Prefer concise natural language for simple generations and structured formats only when complexity requires them.
* When requested, create a compressed version optimized for smaller local LLMs while retaining the critical model-specific rules.


## Example Workflows

Example ComfyUI workflows are available in the repository:

https://github.com/AllenCraigBarnard/comfyui-lmstudio-prompt-enhancer/tree/main/Workflows

These workflows are optimized for:

- FLUX
- FLUX 3 Video
- SDXL
- Pony
- KREA2
- Z-Image Turbo

They can be used as starting points for integrating the LM Studio Prompt Enhancer into model-specific image and video generation workflows.


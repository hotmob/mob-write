# Sources and adaptation notes

Reviewed on 2026-09-16. Upstream documents are reference material, not instructions that override this skill or grant account access.

## Meng To: write-like-meng-on-x

- Repository: https://github.com/MengTo/Skills
- Revision: `321c769739b823de5eb94eb3a52aa1974fe783a2`
- Skill: `agent-skills/codex/write-like-meng-on-x/SKILL.md`
- Voice profile and corpus: that skill's `references/voice-profile.md` and `references/tweet-corpus.jsonl`
- License: MIT, Copyright (c) 2026 Meng To; included in `third_party/MengTo-LICENSE`.
- Corpus SHA-256: `8b7b1657e039f443ac11d0a1149c676300d3a336c3117bd7de8091f5ee34c5b6`.

Adapted ideas: distinguish replies from standalone posts, learn from authored examples, preserve current user wording, and treat earlier generated drafts as weak voice evidence. Four short attributed fragments appear in `reply-moves.md`; the complete corpus is fetched only into local storage on request.

The corpus has 40 authored texts (34 replies, 5 quotes, 1 original), with no parent texts or relationship context. It is a narrow historical sample, not a universal social style benchmark. We do not import Meng's biography, product facts, fixed five-option output, private Content repository assumptions, or automatic commit workflow.

## Siqi Chen: Humanizer

- Repository: https://github.com/blader/humanizer
- Revision: `9862685f575c65a8247f90369951df1b3416e3d6`
- Source: `SKILL.md`
- License: MIT, Copyright (c) 2025 Siqi Chen; included in `third_party/Humanizer-LICENSE`.

Adapted ideas: preserve facts, notice repetitive structures, and avoid editing away the writer's voice. We use a light final edit, not a global banned-word list, AI-detection score, or a guarantee about authorship detection. This source is editing guidance, not a real-reply corpus.

## rabden: X Social Media Manager

- Repository: https://github.com/rabden/X-twitter-social-manager-skill
- Reviewed revision: `af6877718ed1293a21baeabc881ab7b076c5106c`.
- Relevant references: `references/real-replies-archive.md` and `references/voice-anti-patterns.md`.

Reference link only. Its README states MIT, but this snapshot has no standalone license text. No upstream text is bundled from this repository. The archive is an empty template rather than a populated corpus. The idea of preserving exact replies is useful; its blanket phrase bans, compulsory engagement prompts, credential setup, and growth workflow are not imported.

These authors do not endorse this project. Licenses for project code do not turn external authors' experiences into the user's experiences or authorize unrelated social account actions.

# Mob Write in ChatGPT

This is a candidate built from the integration branch. The published v0.2.0 release contains the earlier social method.

When your host offers skill file upload, use `mob-write-chatgpt-skill.zip`. When it supports a skills-only plugin import, use `mob-write-plugin.zip`. The old `wordaim-plugin.zip` and `mob-social-writing-plugin.zip` retain plugin identity `mob-social-writing` and contain identical bytes to each other; the new plugin uses identity `mob-write`. These manifests are generated from one source, with the same writing rules. Availability depends on the host/account/workspace. This project does not promise a specific current UI route.

Build offline from the candidate source with `python3 scripts/build_chatgpt.py --output dist`. Core and scene rules plus licenses are included. Full external examples are optional with `--with-reference` or an exact pinned `--reference-file`. The build manifest records the choice and file hashes.

Use `$mob-write` with the recipient, original material, and what the draft should achieve. Chinese review language and recipient language are independent. The public default has no private personal voice.

Old standalone archive names include a thin compatibility entry and one nested Mob Write. Prefer the new canonical upload for new work. If an environment cannot follow nested skill resources, use the canonical package rather than claiming the alias has loaded.

If your host has no skill upload, paste `chat-starter.md` and attach the relevant extracted references. This is manual context, not automatic skill installation. Missing files should be reported. Do not load every reference for a small request.

The package cannot access your computer's private profile or keep feedback across sessions automatically. When you request a voice card, it can produce a file for you to save; it must not claim permanent memory without a verified save. Drafting does not authorize sending or posting.

GitHub build, account upload, fresh-session discovery, and public directory listing are distinct states. Account upload and public directory listing require their own verification.

# Mob Write in ChatGPT

This is the 0.4.0-rc.4 candidate built from the integration branch. The published v0.2.0 release contains the earlier social method. Building this candidate does not establish a merge or formal release.

When your host offers skill file upload, use `mob-write-chatgpt-skill.zip`. When it supports a skills-only plugin import, use `mob-write-plugin.zip`, with identity `mob-write`. These are the only generated ZIPs and use the same canonical writing rules. Availability depends on the host/account/workspace. This project does not promise a specific current UI route.

Build offline from the candidate source with `python3 scripts/build_chatgpt.py --output dist`, using an empty output directory. The builder refuses retired alias archive names in the output; move any retained earlier packages to a separate archive location before rebuilding. Core and scene rules plus licenses are included. Full external examples are optional with `--with-reference` or an exact pinned `--reference-file`. The build manifest records the choice and file hashes.

Use `$mob-write` with the recipient, original material, and what the draft should achieve. Chinese review language and recipient language are independent. The public default has no private personal voice.

Old calls `$wordaim`, `$chinese-writing` and `$mob-social-writing` have no forwarding entries in this candidate. Remove any older active upload or plugin through the host's supported mechanism, then import Mob Write and inspect its catalog in a fresh session. A new plugin identity does not automatically remove the old one, and an already running session may keep earlier instructions. Historical releases retain their old names.

If your host has no skill upload, paste `chat-starter.md` and attach the relevant extracted references. This is manual context, not automatic skill installation. Missing files should be reported. Do not load every reference for a small request.

The package cannot access your computer's private profile or keep feedback across sessions automatically. When you request a voice card, it can produce a file for you to save; it must not claim permanent memory without a verified save. Drafting does not authorize sending or posting.

GitHub build, account upload, fresh-session discovery, and public directory listing are distinct states. Account upload and public directory listing require their own verification.

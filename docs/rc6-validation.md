# rc.6 synthetic bundle behavior check

Three isolated real Codex CLI sessions completed on 2026-10-08, producing four drafts. The checked entry hash was `52cad773e86332d1b69a2db5ebfacc0d95ca12ff3d34c5e8f022092bb6a1b8aa`. CLI 0.145.0 used its default `gpt-5.6-sol` model with low reasoning effort. The sessions used `--ignore-user-config`, `--ephemeral`, and `--sandbox read-only`. Known global writing entries were explicitly disabled for these test sessions. No global install, real profile, real corpus, external sending, or other project was changed or inspected.

Each host received an independent project-local public installation. Avery and Blair are fictional profiles initialized outside their Skill directories and connected by the new helper. Each bundle contained two explicitly synthetic authored-and-approved schema records. The generic host had no connected profile. The same English X reply was requested in all three hosts; Blair's session also requested a formal English report with personal voice excluded.

| Evidence | Result |
|---|---|
| Discovery | Each session reported the project-local `mob-write` entry in its initial available-Skills catalog. This is session self-report, separate from file existence. |
| Loading | Completed tool events show the entry and applicable references were opened before the draft. Avery and Blair read config, then owner/scope, then profile. All reported read hashes independently matched the frozen host files. |
| Generic use | No connection existed and no private profile was read. The reply was English with a separate Chinese review note. |
| Fictional voice | Avery opened with “Thanks for checking” and complete explanatory sentences. Blair led directly with the benchmark update. Both kept conditional delivery, pending approval and undecided release date. |
| Scope exclusion | Blair's formal report used technical-document guidance and declared `profile_applied: false`; its per-output references omitted the profile. The output used formal status wording. |
| Isolation | Every host file remained byte-identical to its pre-session snapshot. All three processes exited 0. The observed tool commands only read the allowed local method and selected synthetic bundle. |

This check has two factual limitations. The generic reply omitted the explicitly supplied current fact that validation was not yet complete. Avery wrote “Validation is still in progress” where the source only established it was not complete, adding an inference about current progress. These outputs must not be described as a complete factual-fidelity pass.

None of the sessions opened `corpus.jsonl` or `voice-notes.md`. The corpus import and connections were prepared successfully, but these outputs support profile loading and a limited voice difference, not sample-learning effectiveness. Each voice was sampled once; there was no same-session reconnect, real author's acceptance, statistical comparison, or validation of other host types. Internal application of the scope exclusion cannot be independently observed beyond the selected references, output metadata and actual draft.

[Public-safe results](../tests/results/mob-write-rc6-bundle.json) preserve the four exact synthetic outputs and read hashes with host-relative paths. The raw JSONL traces and stderr remain local evidence. Stderr contains host authentication telemetry identity fields and must not be published. This isolated check does not prove the user's actual personal installation or migration.

The 55 structural checks separately exercise empty initialization, explicit author switching, default and override selection, malformed connection refusal, no private prose read on connection, public upgrade preservation, package isolation, and symlink refusal. These are data and installation checks, not writing-quality scores.

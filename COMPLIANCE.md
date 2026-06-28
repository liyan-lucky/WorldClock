# Compliance Audit

## Current scope

WorldClock is a local desktop world clock application with two implementations:

- Python / PyQt5 implementation in `world_clock.py`;
- C# / WPF implementation in `WorldClockWpf/`.

## Current findings

- The repository previously had no license file. MIT License has been added.
- The WPF project currently does not declare third-party NuGet packages.
- The Python implementation uses PyQt5 / Qt. Redistribution of PyQt5-based builds should review PyQt5 and Qt license requirements.
- The application appears to store configuration locally in `world_clock_config.json`.
- No obvious hard-coded secrets, tokens, passwords, or account credentials were found by repository keyword search.
- No bundled icon, font, image, or large third-party asset was identified during this pass.

## Added compliance files

- `LICENSE`
- `NOTICE.md`
- `THIRD_PARTY_NOTICES.md`
- `DISCLAIMER.md`
- `PRIVACY.md`
- `SECURITY.md`
- `CONTRIBUTING.md`

## Legal and operational notes

1. Do not add third-party icons, fonts, images, templates, or code without recording source and license.
2. Do not commit local user configuration files such as `world_clock_config.json`.
3. Do not commit signing certificates, private keys, API tokens, or installer credentials.
4. Review PyQt5 / Qt license obligations before distributing Python builds.
5. For WPF releases, document whether the package is framework-dependent or self-contained.
6. Keep release archives free of build cache, debug symbols if not intended, and local configuration files.

## Residual risk

Time zone and daylight-saving rules can change. The application should not be marketed as suitable for safety-critical, aviation, legal, medical, financial trading, or emergency deadline use without additional verification and liability review.

# Maintainers Guide

## Before merging changes

Check that changes do not introduce:

- secrets, tokens, certificates, signing keys, or account data;
- local user configuration files;
- unlicensed third-party icons, fonts, images, templates, or source code;
- unnecessary network access, telemetry, or data upload behavior;
- release artifacts containing build cache or local settings.

## Dependency review

For new .NET packages, record the package name, version, source, and license in `THIRD_PARTY_NOTICES.md`.

For new Python packages, record the package name, version, source, and license in `THIRD_PARTY_NOTICES.md` and update install instructions.

## Release review

Before publishing a release, verify:

- `world_clock_config.json` is not included unless it is a safe example file;
- debug or cache files are not bundled unintentionally;
- framework-dependent or self-contained packaging is clearly described;
- any bundled runtime or third-party dependency license obligations are satisfied.

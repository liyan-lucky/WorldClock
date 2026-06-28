# Third-Party Notices

This file records third-party technologies and notices relevant to this repository.

## Runtime and platform technologies

- Python: used by the legacy/reference implementation.
- PyQt5 / Qt: used by `world_clock.py`. PyQt5 and Qt are governed by their own licenses. Users who redistribute PyQt5-based builds should review the applicable PyQt5/Qt license terms.
- .NET 8 Desktop Runtime: required by the framework-dependent WPF build.
- WPF / Windows desktop APIs: used by the C# implementation.
- IANA time zone database identifiers: used through Python `zoneinfo` and .NET time zone APIs.

## Current dependency status

The WPF project file currently does not declare third-party NuGet packages.

The Python implementation imports PyQt5. If Python packaging is added later, dependency versions and licenses should be recorded here.

## Contribution requirement

If new third-party code, images, icons, fonts, packages, templates, or generated assets are added, update this file with the source, author, license, and modification notes.

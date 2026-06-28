# Security Policy

## Supported scope

This repository contains a local desktop application implemented in Python / PyQt5 and C# / WPF.

## Reportable issues

Please report security issues through GitHub Issues or the repository owner's public contact channel, especially:

- accidental inclusion of secrets, tokens, certificates, or private keys;
- unsafe file write behavior;
- path traversal or unsafe configuration loading;
- malicious dependency or package configuration;
- unexpected network, telemetry, or data upload behavior;
- release packages containing unintended files.

## Non-security issues

Incorrect time zone mapping, UI bugs, packaging problems, or feature requests can be submitted as normal issues.

## Handling

The maintainer may remove affected files, rotate exposed credentials, update dependencies, or temporarily suspend releases while an issue is being reviewed.

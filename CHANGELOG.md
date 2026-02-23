# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

TODO: add version in Command constructor

## [0.7.0] - 2026-02-22

✨ feat: adds `helpmodifier` at argument level (dc80bdec6884767442c3ccba791e11b705a787fc)

## [0.6.3] - 2026-02-21

🐞 fix: get only first line of description for help in subcommand (12a24bc520589d2cd90e61bd327517cb8b9e4acc)

## [0.6.2] - 2026-02-20

🐞 fix: bug `metavar` in `version` option (ee9e4e441a2bd749bcdd01b9e85347cba2541472)

## [0.6.1] - 2026-02-19

🐞 fix: issue when `action=version` (167da9b68b4a7b89c670477f9a65c33ba5e02600)

## [0.6.0] - 2026-01-30

### Feat ✨

- Add help modifiers
- Help flags and help msg
- Add custom `__repr__`

### Fixed 🐞

- Pass kwargs with custom prefix
- Correct make short options
- Short option generator
- Correction for action = help
- Correct conflicting help flags
- Docstring when there is variadic args

## [0.5.0] - 2025-11-27

### Feat ✨

- Additional parameters to Exclusive Group
  (a5c8816bef46d53969193c97cb1603ec18be2895)
- Add metavar modifiers (8daae79925486f984e3b13b114d3bb879c446b16)
- New docstring template (e465ceaa10bd3e4e56d7a54bdd7e2e4ba08404d8)
- Create context for parent command (175f82c3470ab3f78a6af62a04f2add7aee9a2cd)

### Fixed 🐞

- Command name with dash in underscore
- Function to test if is context annotation

## [0.4.0] - 2025-11-14

### Feat ✨

- Add `make_flag` option (6051e2934488384759ee3700f4572d9d5fdc502c)
- Add `make_shorts` option (1eded8f037f5178fc6c26512736ba73539334dd1)
- Add error messages (4b2a4ebcc7ae5703190d6a75f5f013181345b6e1)
- Add module level functions to use as decorators
  (0e290f2441fcf1fb8c10b6847f0496520320fb69)

### Fixed 🐞

- Remove exclusion of \* and ? with flags
- Return the return in `clig.run`
- Safe copy of lists and dict in metadata
-

## [0.3.0] - 2025-11-06

### Fixed 🐞

## [0.2.0] - 2025-11-03

### Fixed 🐞

## [0.1.0] - 2025-11-02

### 🚀 Release:

- Functional version

## [0.0.0] - 2024-11-04

### New 🎉

- First version released, draft and unstable.

[0.7.0]: https://github.com/diogo-rossi/clig/releases/tag/v0.7.0
[0.6.3]: https://github.com/diogo-rossi/clig/releases/tag/v0.6.3
[0.6.2]: https://github.com/diogo-rossi/clig/releases/tag/v0.6.2
[0.6.1]: https://github.com/diogo-rossi/clig/releases/tag/v0.6.1
[0.6.0]: https://github.com/diogo-rossi/clig/releases/tag/v0.6.0
[0.5.0]: https://github.com/diogo-rossi/clig/releases/tag/v0.5.0
[0.4.0]: https://github.com/diogo-rossi/clig/releases/tag/v0.4.0
[0.3.0]: https://github.com/diogo-rossi/clig/releases/tag/v0.3.0
[0.2.0]: https://github.com/diogo-rossi/clig/releases/tag/v0.2.0
[0.1.0]: https://github.com/diogo-rossi/clig/releases/tag/v0.1.0
[0.0.0]: https://github.com/diogo-rossi/clig/releases/tag/v0.0.0

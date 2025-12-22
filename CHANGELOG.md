# Changelog

All notable changes to Siena's Snowy Adventure will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.9] - 2025-12-21

### Fixed
- **CRITICAL**: Fixed SSL certificate fallback not triggering when certificate verification fails
- Online features now properly retry with unverified SSL context when certificates are missing
- SSL errors now caught during actual request (not just during context creation)

### Changed
- Complete rewrite of SSL handling to catch errors at request time
- Added detailed logging when falling back to unverified SSL context

## [1.0.8] - 2025-12-21

### Fixed
- **CRITICAL**: Fixed SSL certificate verification errors preventing online features on some Macs
- Online leaderboards now work on systems with incomplete Python SSL certificate installations

### Changed
- Added intelligent SSL context fallback for maximum compatibility
- Improved error messages for SSL-related connection issues

## [1.0.7] - 2025-12-21

### Fixed
- **CRITICAL**: Fixed online score submission validation rejecting fast completion times
- Lowered minimum time requirement from 30s to 15s to allow skilled speedruns
- Added detailed validation error messages for debugging

### Changed
- Improved error reporting for online score submissions
- Score submission now shows clear success/failure messages in console
- Firebase rules updated to accept times as low as 15 seconds

## [1.0.6] - 2025-12-21

### Fixed
- **CRITICAL**: Fixed ability unlock timing - Roll now available in Level 2+, Spin in Level 3+
- Abilities now unlock when entering a level (not after completing previous level)

### Changed
- Level 1: Walk, Jump, Crouch, Double Jump only
- Level 2-4: Roll added
- Level 3-4: Roll + Spin Attack added

## [1.0.5] - 2025-12-21

### Fixed
- **CRITICAL**: Fixed online leaderboard not working in distributed .app (hardcoded Firebase URL defaults)
- **CRITICAL**: Fixed roll ability incorrectly available in Level 1 (now only unlocked after completing Level 1)
- Online features now work without .env file in bundled app

### Changed
- Firebase URL now defaults to production URL (can be overridden with environment variable)
- Online features enabled by default (can be disabled with SIENA_ONLINE_ENABLED=false)

## [1.0.4] - 2025-12-21

### Security
- **CRITICAL FIX**: Removed Firebase Admin SDK to eliminate security vulnerability
- Migrated to Firebase REST API for leaderboard and update checking
- No longer bundling admin credentials in distributed game
- Added Firebase security rules for server-side validation
- Client-side validation for score submissions

### Changed
- Online leaderboard now uses secure REST API (no admin credentials needed)
- Update checker now uses secure REST API
- Removed firebase-admin dependency
- Removed firebase-key.json from distribution bundle
- Updated .env configuration (removed FIREBASE_KEY_PATH)

### Technical
- Created `src/utils/secure_leaderboard.py` - REST API client
- Created `src/utils/update_checker_secure.py` - Secure update checker
- Created `firebase-security-rules.json` - Server-side validation
- Updated PyInstaller spec to exclude sensitive files
- Added comprehensive test suite for secure implementation

### Important for Users
- v1.0.2 and earlier versions will stop working once Firebase security is applied
- Please update to v1.0.4 for continued online functionality
- All existing scores are preserved

## [1.0.3] - 2025-12-21

### Fixed
- Improved game performance to reduce lag
- Optimized particle system rendering (skip off-screen particles, use direct drawing for small particles)
- Added particle count limit (MAX_PARTICLES = 150) to prevent performance degradation
- Reduced surface creation overhead in particle system

### Technical
- Small particles (≤2px) now draw directly without creating surfaces
- Added off-screen particle culling to skip unnecessary rendering
- Particles limited to 150 maximum to maintain stable frame rate
- Note: Disappearing platform rendering still creates surfaces per frame (future optimization)

## [1.0.2] - 2025-12-21

### Changed
- Optimized dialogue images from PNG to JPEG format
- Distribution size reduced by 43% (255MB → 145MB)
- App bundle reduced by 30% (138MB → 97MB)
- Now passes Google Drive's 150MB virus scan limit

### Technical
- Converted 36 dialogue images from PNG to high-quality JPEG (92% quality)
- Updated story_data.py to reference .jpg files instead of .png
- Removed backup folder from distribution bundle

## [1.0.1] - 2025-12-21

### Added
- In-game update checker with Firebase integration
- Update notification banner on title screen
- Automatic version checking on game launch
- Click-to-download functionality for updates

### Changed
- Scoreboard now defaults to online view instead of local
- Online scores automatically load when viewing scoreboard
- Scoreboard width increased from 730 to 780 pixels to accommodate longer usernames
- Username display now shows full 20 characters (previously truncated at 12)
- Scoreboard column positions adjusted for better spacing

### Fixed
- Fixed username truncation on scoreboard display
- Fixed CHKPT column being cut off on scoreboard

## [1.0.0] - 2025-12-21

### Added
- Initial release of Siena's Snowy Adventure
- 4 playable levels with winter platforming gameplay
- Story mode with dialogue system featuring Siena and Pedro
- Online leaderboard with Firebase integration
- Local leaderboard system with difficulty filtering
- Username input with strict content filtering (200+ blocked words)
- Multiple difficulty modes (Easy, Medium, Hard)
- Checkpoint system for level progression
- Particle effects and screen shake for enhanced game feel
- Sound effects: jump, roll, coin collect, select, death, stage clear
- Background music system with looping
- Username generator with 300+ random name combinations
- Winter-themed UI with falling snow animations
- Touch controls for mobile compatibility (if deployed)

### Technical Features
- Modular architecture with src/ organization
- Comprehensive unit tests (65+ test cases for username filter)
- Integration tests for game flow
- Firebase Realtime Database for online scores
- PyInstaller packaging for Mac and Windows distribution
- Modern Python package management with pyproject.toml

---

## How to Version Updates

When releasing updates, follow this versioning scheme:

- **MAJOR.MINOR.PATCH** (e.g., 1.0.0)
  - **MAJOR**: Breaking changes or complete rewrites (e.g., 2.0.0)
  - **MINOR**: New features, new levels, significant additions (e.g., 1.1.0)
  - **PATCH**: Bug fixes, small tweaks, balance changes (e.g., 1.0.1)

### Examples:
- Added Level 5 → 1.1.0
- Fixed jump bug → 1.0.1
- Complete game engine rewrite → 2.0.0

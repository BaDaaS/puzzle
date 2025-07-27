# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with
code in this repository.

## Development Commands

**Setup:**

```bash
# Install Python version and dependencies
pyenv install 3.13
poetry install
cp -f example.env .env
poetry run python manage.py migrate
poetry run python manage.py createsuperuser
```

**Infrastructure:**

```bash
# Start required services
./infrastructure/influxdb.sh
./infrastructure/redis.sh
```

**Development:**

```bash
# Run development server
make dev

# Run tests
make test

# Lint and format code
make lint
make format

# Check for trailing whitespaces
make check-trailing-whitespace

# Fix trailing whitespaces
make fix-trailing-whitespace

# Run all checks (lint + test + whitespace check)
make check

# Database migrations
make makemigrations
make migrate

# Management commands
make populate-currencies
make populate-exchanges
make get-trades
make get-balance
make get-price
```

## Architecture

Puzzle is a Django-based asset management application with the following core
components:

### Apps Structure

- **trading/**: Cryptocurrency and financial trading functionality
  - Exchange integrations via CCXT library (Kraken, Coinbase)
  - Trade model with double-entry accounting legs
  - Price fetching and ticker management
- **accounting/**: Double-entry accounting system
  - Entity and Account models for business/personal entities
  - Account types: Asset, Liabilities, Equity, Revenue, Expenses, Receivable,
    Payable
  - Account subtypes for different financial instruments
- **common/**: Shared utilities and models
  - Currency model (FIAT/Crypto)
  - Utility classes for Price, Volume, Quantity
  - InfluxDB and Redis integration helpers

### Data Storage

- **PostgreSQL**: Primary relational database for trades, accounts, entities
- **InfluxDB**: Time-series data for price history and market data
- **Redis**: Middleware for real-time communication between processes

### Key Models

- `Trade`: Financial transactions with automatic leg creation
- `Account`: Chart of accounts with entity and currency relationships
- `Entity`: Business entities (companies, individuals)
- `Currency`: FIAT and cryptocurrency definitions
- `Exchange`: Trading platform integrations

### Exchange API Pattern

All exchange integrations inherit from `AbstractAPI` in
`trading/exchange_api/base.py` and implement:

- `get_trades()`: Fetch historical trades
- `get_balance()`: Get account balances
- `get_tickers()`: Fetch current prices
- `get_fiat_deposits()`: Retrieve fiat deposit history

### Configuration

- Environment variables configured via `.env` file (copy from `example.env`)
- Database can be SQLite (development) or PostgreSQL (production)
- Exchange API keys configured per exchange in settings
- Logging level configurable via `LOGGING_LEVEL`

## Development Notes

- Uses Poetry for dependency management with Python 3.13
- Ruff for linting and formatting with 80 character line length
- Django admin interface available for data management
- Management commands in each app's `management/commands/` directory
- Double-entry accounting automatically creates legs when trades are saved
- Currency mapping handled per exchange in `CURRENCY_MAPPING` dictionaries
- CHANGELOG.md follows [Keep a Changelog](https://keepachangelog.com) format
- Semantic versioning used for releases
- **IMPORTANT**: Always run these commands after making changes:
  - `make fix-trailing-whitespace` - Fix trailing whitespaces
  - `make format-md` - Format markdown files to 80-character wrapping
  - Run both commands at the end of each task

### Changelog Management

```bash
# Check changelog format
make changelog-check

# Release a new version (moves unreleased entries to version)
make changelog-release VERSION=1.0.0
```

## Commit Guidelines

**NEVER** add Claude as a co-author in commit messages. Do not include:

- `Co-Authored-By: Claude <noreply@anthropic.com>`
- Any other co-author attribution for Claude

**NEVER** use emojis in commit messages.

**Always** wrap commit message titles at 80 characters and body text at 80
characters.

Always verify commit messages before committing and remove any co-author lines
referencing Claude.

## CI Testing

**IMPORTANT**: When making changes to GitHub Actions workflows, always test them
locally using `act` before committing:

```bash
# Test specific workflow
act -j lint-and-format
act -j test
act -j build

# List all available jobs
act --list

# Dry run to check syntax
act --dryrun
```

This ensures CI configurations work correctly before pushing changes.

## Dockerfile Guidelines

**IMPORTANT**: Always run `make lint-dockerfiles` after modifying any
Dockerfile:

```bash
# After editing infrastructure/Dockerfile or any other Dockerfile
make lint-dockerfiles

# Fix any hadolint warnings or errors before committing
```

This ensures Dockerfiles follow best practices and security guidelines.

## Shell Script Guidelines

**IMPORTANT**: Always run `make lint-bash` after modifying any shell script:

```bash
# After editing any .sh file
make lint-bash

# Fix any shellcheck warnings or errors before committing
```

This ensures shell scripts follow best practices and avoid common issues.

## Dependency Management

The project uses Dependabot for automated dependency updates:

- **Python dependencies**: Weekly updates on Monday at 09:00
- **GitHub Actions**: Weekly updates on Monday at 10:00
- **Docker base images**: Weekly updates on Monday at 11:00

Dependabot will create pull requests with dependency updates that need to be
reviewed and merged. The CI pipeline will automatically test all dependency
updates.

## Design System & Brand Guidelines

### Cypherpunk Visual Identity

Puzzle follows a **cypherpunk aesthetic** that emphasizes cryptographic
resistance, decentralization, and hacker culture. This design system should be
applied consistently across all interfaces, documentation, and user touchpoints.

#### Color Palette

**Primary Colors:**

- `#0d0d0d` - Deep black background (puzzle-bg-primary)
- `#00ff88` - Hacker green primary (puzzle-hacker-green)
- `#ff0033` - Glitch red secondary (puzzle-glitch-red)
- `#00cfff` - Electric cyan tertiary (puzzle-electric-cyan)
- `#9e00ff` - Violet glitch highlight (puzzle-violet-glitch)

**Text Colors:**

- `#e6e6e6` - Primary text (puzzle-text-primary)
- `#999999` - Muted/secondary text (puzzle-text-muted)

**Usage Guidelines:**

- Use deep black (#0d0d0d) as primary background in all interfaces
- Hacker green (#00ff88) for primary actions, success states, and interactive
  elements
- Glitch red (#ff0033) for errors, warnings, and attention-grabbing elements
- Electric cyan (#00cfff) for informational elements and secondary actions
- Violet glitch (#9e00ff) for special highlights and premium features

#### Typography

**Primary Font Stack:**

```css
font-family: "Fira Code", "IBM Plex Mono", "Courier New", monospace;
```

**Characteristics:**

- **Monospace only** - All text uses monospace fonts for terminal authenticity
- **Letter spacing** - Increased letter spacing (1-4px) for headers
- **Text transform** - UPPERCASE for headings and important elements
- **Font weights** - 300, 400, 500, 600, 700 available

#### Visual Effects

**Glitch Animations:**

- Hover effects on headings with color-shifting and position glitching
- Color cycling through red, cyan, violet, and green
- Subtle transform skewing and translation

**CRT/Terminal Effects:**

- Scanline overlays on hero sections (subtle green lines)
- Box shadows with neon glow effects
- Border styling with terminal-inspired sharp edges (2px border-radius max)

**Interactive Elements:**

- Buttons with glowing hover states
- Transform animations (translateY, scale)
- Neon glow shadows using primary colors

#### Layout Principles

**Terminal-Inspired Structure:**

- High contrast black backgrounds
- Minimal UI chrome and unnecessary decorations
- Sharp, geometric layouts with clean borders
- Monospace text creates natural grid alignment

**Spacing System:**

- Use rem units for consistent scaling
- Base spacing: 0.5rem, 1rem, 1.5rem, 2rem, 3rem, 4rem
- Generous padding for readability on dark backgrounds

**Interactive Feedback:**

- Immediate visual feedback on all interactions
- Hover states with color and glow changes
- Animation duration: 0.2s-0.3s for responsiveness

#### Implementation Standards

**CSS Variables:** Always use the defined CSS custom properties for colors:

```css
var(--puzzle-bg-primary)
var(--puzzle-hacker-green)
var(--puzzle-glitch-red)
var(--puzzle-electric-cyan)
var(--puzzle-violet-glitch)
var(--puzzle-text-primary)
var(--puzzle-text-muted)
```

**Accessibility:**

- Maintain high contrast ratios (minimum 4.5:1)
- Ensure all interactive elements are keyboard accessible
- Provide focus indicators with neon glow effects
- Test with screen readers

**Performance:**

- Use CSS animations over JavaScript when possible
- Disable complex effects on mobile devices
- Optimize font loading with display: swap

#### Brand Voice & Messaging

**Tone:**

- **Technical** - Use precise, cryptographic terminology
- **Rebellious** - Challenge traditional financial systems
- **Empowering** - Focus on user sovereignty and control
- **Minimalist** - Clear, direct communication without fluff

**Key Phrases:**

- "Cryptography. Resistance. Interoperability."
- "Take back control of your financial sovereignty"
- "Cypherpunk-first asset management"
- "Decentralized. Encrypted. Unstoppable."

**UI Copy Style:**

- ALL CAPS for primary actions and headings
- Terminal-style prompts: `$ sudo ./puzzle --command`
- Hacker-inspired button labels: "DECRYPT", "EXECUTE", "INITIALIZE"
- Technical precision in error messages and status updates

#### Application Across Interfaces

**Web Interface:**

- Dark theme enforced (no light mode)
- Full-screen hero sections with terminal prompts
- Monospace fonts throughout the entire application
- Glitch effects on hover for all interactive elements

**Documentation:**

- Code-heavy examples with syntax highlighting
- Terminal command examples prominently featured
- Dark theme in all documentation platforms
- Consistent color scheme across all pages

**Marketing Materials:**

- High contrast visuals emphasizing the logo's red puzzle pieces
- Technical diagrams with neon-style highlighting
- Screenshots showing terminal interfaces and dark themes

This design system ensures Puzzle maintains a consistent, authentic cypherpunk
identity that resonates with its target audience of privacy-conscious users,
developers, and financial sovereignty advocates.

## Website Theme Consistency Guidelines

### Homepage Design Standards

The entire Puzzle website should maintain visual and functional consistency with
the main page design. All pages must follow these established patterns:

#### Visual Identity Consistency

**Homepage Layout Elements to Replicate:**

- **Hero Section Structure**: Large logo placement with animated terminal prompt
- **Monospace Typography**: Fira Code font family throughout all pages
- **Color Scheme**: Dark background (#0d0d0d) with hacker green (#00ff88)
  accents
- **Button Styling**: Uppercase text, glowing hover effects, terminal-inspired
  design
- **Grid Layouts**: Clean, geometric arrangements with proper spacing
- **Terminal Aesthetics**: Command prompts, scanline effects, and cursor
  animations

#### Animation Standards

**Terminal-Style Interactions:**

- **Animated Commands**: Use typing/erasing effects for dynamic content
- **Glitch Effects**: Apply to headings and interactive elements on hover
- **Cursor Animations**: Blinking cursors for terminal authenticity
- **Scanline Overlays**: Subtle CRT effects on hero sections (dark theme only)

**Animation Specifications:**

```css
/* Standard glitch hover effect for all pages */
.glitch-text:hover {
  animation: glitch-flicker 0.3s infinite;
}

/* Terminal command animation timing */
.animated-command {
  animation-duration: 8s;
  animation-timing-function: ease-in-out;
  animation-iteration-count: infinite;
}
```

#### Page-Specific Implementation

**Documentation Pages:**

- Maintain dark theme with terminal command examples
- Use monospace fonts for all body text
- Apply glitch effects to section headings
- Include terminal prompts for code examples
- Consistent button styling across all CTAs

**Blog Pages:**

- Same color scheme and typography as homepage
- Terminal-style metadata display (dates, authors, tags)
- Animated elements for featured posts
- Consistent navigation and footer styling

**Configuration/Setup Pages:**

- Terminal-style forms and input fields
- Animated feedback for user actions
- Command-line aesthetic for settings
- Consistent error and success states

#### Technical Requirements

**CSS Architecture:**

- Use CSS custom properties defined in homepage
- Maintain consistent spacing system (0.5rem, 1rem, 1.5rem, 2rem, 3rem, 4rem)
- Apply same border-radius (2px max) and box-shadow patterns
- Consistent transition timing (0.2s-0.3s for interactions)

**Performance Standards:**

- CSS-only animations (no JavaScript dependencies)
- Mobile-responsive breakpoints matching homepage
- Optimized font loading with display: swap
- Minimal animation on mobile devices for performance

**Accessibility Compliance:**

- Maintain high contrast ratios from homepage design
- Keyboard navigation consistency across all pages
- Screen reader compatibility for all animations
- Focus indicators with neon glow effects

#### Content Guidelines

**Messaging Consistency:**

- Self-hosted asset management focus throughout
- Terminal command examples for all technical content
- Consistent tone: technical, empowering, privacy-focused
- All buttons and CTAs use uppercase terminal-style text

**Visual Content:**

- Screenshots showing terminal interfaces
- Code examples with syntax highlighting
- Technical diagrams with neon accent colors
- Consistent logo placement and sizing

### Implementation Priority

1. **High Priority**: Documentation pages, installation guides, configuration
2. **Medium Priority**: Blog posts, about pages, contact forms
3. **Low Priority**: Error pages, search results, archive pages

**Quality Assurance:**

- Every new page must match homepage terminal aesthetic
- Regular design reviews to ensure consistency
- Cross-browser testing for animation compatibility
- Performance monitoring for animation impact

This comprehensive approach ensures users experience a cohesive, professional
terminal-inspired interface that reinforces Puzzle's identity as a self-hosted,
privacy-first asset management solution.

# CLAUDE.md - AI Assistant Guidelines

> This file provides context and guidelines for AI assistants working with this repository.

## Project Overview

**Repository**: testcloude
**Owner**: EladRosenfeld
**Status**: New project (initialized)

This is a newly created repository. As the project develops, this document should be updated to reflect the actual codebase structure, conventions, and workflows.

---

## Repository Structure

```
testcloude/
├── CLAUDE.md           # AI assistant guidelines (this file)
└── .git/               # Git version control
```

*As the project grows, update this section with the actual directory structure.*

### Planned Structure Template

```
testcloude/
├── src/                # Source code
│   ├── components/     # UI components (if applicable)
│   ├── lib/            # Library/utility code
│   ├── services/       # Service layer
│   └── index.*         # Entry point
├── tests/              # Test files
├── docs/               # Documentation
├── scripts/            # Build/utility scripts
├── .github/            # GitHub workflows and templates
├── package.json        # Project dependencies (Node.js)
├── tsconfig.json       # TypeScript configuration (if used)
├── README.md           # Project documentation
└── CLAUDE.md           # AI assistant guidelines
```

---

## Development Guidelines

### Git Workflow

1. **Branch Naming**: Use descriptive branch names
   - Features: `feature/<description>`
   - Fixes: `fix/<description>`
   - Claude sessions: `claude/<session-id>`

2. **Commit Messages**: Follow conventional commits
   ```
   type(scope): description

   [optional body]
   ```
   Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

3. **Pull Requests**: Include clear descriptions and link related issues

### Code Style

- Write clean, readable, and maintainable code
- Follow the project's established patterns and conventions
- Add comments only when the logic isn't self-evident
- Prefer descriptive names over comments

### Testing

- Write tests for new functionality
- Ensure all tests pass before committing
- Follow the existing test patterns in the codebase

---

## Commands Reference

*Update this section with actual project commands once established.*

### Common Commands (Template)

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Run tests
npm test

# Lint code
npm run lint

# Format code
npm run format
```

---

## AI Assistant Instructions

### When Working on This Repository

1. **Read Before Editing**: Always read files before modifying them
2. **Understand Context**: Explore related code to understand patterns
3. **Follow Conventions**: Match existing code style and patterns
4. **Minimal Changes**: Make only necessary changes, avoid over-engineering
5. **Test Your Changes**: Run tests and verify functionality
6. **Clear Commits**: Write descriptive commit messages

### Do's

- Use existing patterns found in the codebase
- Keep changes focused and minimal
- Update documentation when adding new features
- Handle errors appropriately at system boundaries
- Use the TodoWrite tool for complex multi-step tasks

### Don'ts

- Don't add features beyond what was requested
- Don't refactor unrelated code
- Don't add unnecessary comments or documentation
- Don't create abstractions for one-time operations
- Don't introduce security vulnerabilities (SQL injection, XSS, etc.)

### Security Considerations

- Never commit secrets, API keys, or credentials
- Validate user input at system boundaries
- Follow OWASP security guidelines
- Use parameterized queries for database operations

---

## Configuration Files

*Document key configuration files as they are added to the project.*

| File | Purpose |
|------|---------|
| `package.json` | Node.js dependencies and scripts |
| `tsconfig.json` | TypeScript compiler options |
| `.eslintrc.*` | ESLint linting rules |
| `.prettierrc` | Code formatting rules |
| `.env.example` | Environment variables template |
| `.gitignore` | Git ignore patterns |

---

## Architecture Notes

*Add architectural decisions and patterns as the project develops.*

### Key Patterns

- Document design patterns used in the codebase
- Note any architectural decisions and their rationale
- List external services and integrations

### Dependencies

- Document major dependencies and their purposes
- Note any version constraints or compatibility requirements

---

## Troubleshooting

*Add common issues and solutions as they are discovered.*

### Common Issues

1. **Issue**: [Description]
   - **Solution**: [Steps to resolve]

---

## Changelog

| Date | Changes |
|------|---------|
| 2026-01-29 | Initial CLAUDE.md created |

---

## Contributing

When contributing to this repository:

1. Create a feature branch from the main branch
2. Make your changes following the guidelines above
3. Write or update tests as needed
4. Ensure all tests pass
5. Submit a pull request with a clear description

---

*Last updated: 2026-01-29*

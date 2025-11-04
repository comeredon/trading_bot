# Copilot Agent Instructions

## Available Agents

This workspace has two specialized agents configured to handle PL/I to .NET 8 translation:

### 1. Program Manager Agent
**Location**: `.github/agents/program manager.agent.md`

**Role**: Analyze PL/I codebase and create comprehensive documentation

**Responsibilities**:
- Read and analyze PL/I code files in the repository
- **Always connect to the custom-pli-mcp server** to understand the codebase
- Extract and document all logic, data structures, and business rules
- Create detailed specification documents in the `/translation` folder
- Verify all understanding with the custom-pli-mcp server
- Answer clarification questions from the Developer agent

**Constraints**:
- Cannot modify PL/I source code
- Can only create/edit .md files in the `/translation` folder
- Must use custom-pli-mcp server for all code analysis

### 2. Developer Agent
**Location**: `.github/agents/developer.agent.md`

**Role**: Implement .NET 8 applications based on specifications

**Responsibilities**:
- Read all documentation files in the `/translation` folder
- Implement equivalent functionality in .NET 8 framework
- Write clean, maintainable C# code following best practices
- Create proper project structure, error handling, and tests
- Ask Program Manager agent for clarifications when needed

**Constraints**:
- Can only write .NET 8 code (C#)
- Cannot modify files in the `/translation` folder
- Must follow specifications provided by Program Manager agent

## Workflow

1. **Program Manager** analyzes PL/I code using custom-pli-mcp server
2. **Program Manager** documents logic in `/translation` folder
3. **Developer** reads documentation from `/translation` folder
4. **Developer** implements equivalent .NET 8 application
5. **Developer** requests clarifications from Program Manager as needed
6. **Program Manager** updates documentation based on feedback

## Usage

To invoke an agent, use `@program manager` or `@developer` in your Copilot chat.
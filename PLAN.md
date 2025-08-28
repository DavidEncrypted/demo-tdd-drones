## Workshop Demo Summary

You're preparing a hands-on Claude Code workshop for Fugro with three demos focused on producing production code. The second demo aims to demonstrate test-driven development in a 10-minute follow-along format.

**Initial constraints:**
- Must be cloneable and installable for anyone
- Basic install with no complex dependencies
- Tech stack likely Python or C# (matching Fugro's TypeScript/C# on AWS)
- Visual component preferred
- 10-minute time limit creates significant scope constraints

**Data considerations:**
Your proprietary drone ulog files can't be shared, leading to exploration of alternatives including synthetic data generation, public drone datasets, and GIS data sources. You eventually identified a PX4 flight log as a suitable data source.

**Architecture approach evolution:**
The discussion shifted from domain-specific data validation (testing whether drone behavior makes logical sense) to proper software architecture testing. Instead of validating flight data content, the focus moved to testing code components and system behavior.

**Final direction being considered:**
A pre-built dashboard foundation with separate modules for data loading, processing, and visualization. Tests would focus on architectural concerns - whether components handle inputs correctly, manage errors appropriately, and produce expected outputs. The live demo would use Claude Code to add a new feature (like data export functionality or enhanced error handling) following TDD principles.

This approach addresses the core workshop goals: demonstrating AI-assisted production code development through proper software testing practices, while remaining technology-agnostic and suitable for any CSV dataset. The 10-minute constraint favors showing incremental feature addition rather than building from scratch.

The architectural testing approach seems more aligned with real-world software development practices than data content validation, though the final implementation details remain open for further consideration.

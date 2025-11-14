#!/bin/bash
# 8825 Command Wrapper
# Routes subcommands to appropriate scripts

# Resolve symlink to get actual script location
if [ -L "$0" ]; then
    SCRIPT_PATH=$(readlink "$0")
else
    SCRIPT_PATH="$0"
fi

SCRIPT_DIR="$( cd "$( dirname "$SCRIPT_PATH" )" && pwd )"

case "$1" in
    start)
        "$SCRIPT_DIR/8825_start.sh"
        ;;
    health)
        "$SCRIPT_DIR/check_health.sh"
        ;;
    deps|dependencies)
        "$SCRIPT_DIR/check_dependencies.sh"
        ;;
    registry)
        case "$2" in
            review)
                "$SCRIPT_DIR/registry_review.sh"
                ;;
            update)
                shift 2
                "$SCRIPT_DIR/registry_update.sh" "$@"
                ;;
            *)
                "$SCRIPT_DIR/validate_registry.sh"
                ;;
        esac
        ;;
    audit)
        case "$2" in
            path)
                "$SCRIPT_DIR/audit_path.sh" "$3"
                ;;
            component)
                "$SCRIPT_DIR/audit_component.sh" "$3"
                ;;
            dependency|dep)
                "$SCRIPT_DIR/audit_dependency.sh" "$3"
                ;;
            conflicts)
                "$SCRIPT_DIR/audit_conflicts.sh"
                ;;
            *)
                echo "8825 audit - Inspect system components"
                echo ""
                echo "Usage: 8825 audit <subcommand> [args]"
                echo ""
                echo "Subcommands:"
                echo "  path <path>          - Show what touches a path"
                echo "  component <name>     - Show component details"
                echo "  dependency <name>    - Show dependency usage"
                echo "  conflicts            - Find system conflicts"
                echo ""
                echo "Examples:"
                echo "  8825 audit path ~/Downloads"
                echo "  8825 audit component downloads_sync"
                echo "  8825 audit dependency watchdog"
                echo "  8825 audit conflicts"
                echo ""
                exit 1
                ;;
        esac
                ;;
    impact)
        shift
        "$SCRIPT_DIR/impact_analysis.sh" "$@"
        ;;
    *)
        echo "8825 - Unified System Management"
        echo ""
        echo "Usage: 8825 <command> [args]"
        echo ""
        echo "Commands:"
        echo "  start        - Run full startup protocol"
        echo "  health       - Check system health"
        echo "  deps         - Check dependencies"
        echo "  registry     - Validate registry"
        echo "  audit        - Inspect system components"
        echo "  impact       - Analyze change consequences"
        echo ""
        echo "For more info: 8825 audit (or) 8825 impact"
        echo ""
        exit 1
        ;;
esac

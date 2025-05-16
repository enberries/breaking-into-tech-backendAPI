#!/bin/bash

APP_NAME="flask_app"
PID_FILE="/tmp/${APP_NAME}.pid"
LOG_FILE="/tmp/${APP_NAME}.log"
FLASK_APP="api.py"

start() {
    if [ -f "$PID_FILE" ]; then
        if ps -p $(cat $PID_FILE) > /dev/null; then
            echo "Application is already running with PID: $(cat $PID_FILE)"
            return 1
        else
            # PID file exists but process is not running
            rm "$PID_FILE"
        fi
    fi

    echo "Starting Flask application..."
    # Start the Flask application
    nohup python3 $FLASK_APP > "$LOG_FILE" 2>&1 &
    
    # Save the PID
    echo $! > "$PID_FILE"
    echo "Application started with PID: $(cat $PID_FILE)"
    echo "Logs are being written to $LOG_FILE"
}

stop() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p $PID > /dev/null; then
            echo "Stopping Flask application (PID: $PID)..."
            kill $PID
            rm "$PID_FILE"
            echo "Application stopped"
        else
            echo "Process not running but PID file exists. Cleaning up..."
            rm "$PID_FILE"
        fi
    else
        echo "Application is not running (no PID file found)"
    fi
}

status() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p $PID > /dev/null; then
            echo "Application is running with PID: $PID"
            echo "Log file: $LOG_FILE"
        else
            echo "Process not running but PID file exists. Application may have crashed."
        fi
    else
        echo "Application is not running (no PID file found)"
    fi
}

restart() {
    stop
    # Give it a moment to stop properly
    sleep 2
    start
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    status)
        status
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac

exit 0

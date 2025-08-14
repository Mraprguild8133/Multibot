#!/bin/bash

# Telegram Bot Docker Runner Script
# Usage: ./docker-run.sh [build|start|stop|restart|logs|clean]

set -e

BOT_NAME="telegram-ai-bot"
IMAGE_NAME="telegram-bot:latest"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_env_file() {
    if [ ! -f .env ]; then
        print_warning "No .env file found. Creating template..."
        cat > .env << EOF
# Required API Keys
TELEGRAM_BOT_TOKEN=your_bot_token_here
GEMINI_API_KEY=your_gemini_key_here

# Optional API Keys
YOUTUBE_API_KEY=your_youtube_key_here
TMDB_API_KEY=your_tmdb_key_here
REMOVEBG_API_KEY=your_removebg_key_here
GOOGLE_APPLICATION_CREDENTIALS=your_google_credentials_json_here

# Bot Configuration
USE_WEBHOOK=false
EOF
        print_warning "Please edit .env file with your API keys before running the bot"
        exit 1
    fi
}

build_image() {
    print_status "Building Docker image..."
    docker build -t $IMAGE_NAME .
    print_success "Docker image built successfully"
}

start_bot() {
    check_env_file
    
    if [ "$(docker ps -q -f name=$BOT_NAME)" ]; then
        print_warning "Bot is already running"
        return
    fi
    
    print_status "Starting Telegram bot container..."
    docker run -d \
        --name $BOT_NAME \
        --env-file .env \
        --restart unless-stopped \
        -p 5000:5000 \
        $IMAGE_NAME
    
    print_success "Bot started successfully"
    print_status "Container ID: $(docker ps -q -f name=$BOT_NAME)"
}

stop_bot() {
    if [ "$(docker ps -q -f name=$BOT_NAME)" ]; then
        print_status "Stopping bot container..."
        docker stop $BOT_NAME
        docker rm $BOT_NAME
        print_success "Bot stopped and removed"
    else
        print_warning "Bot is not running"
    fi
}

restart_bot() {
    print_status "Restarting bot..."
    stop_bot
    start_bot
}

show_logs() {
    if [ "$(docker ps -q -f name=$BOT_NAME)" ]; then
        print_status "Showing bot logs (Press Ctrl+C to exit)..."
        docker logs -f $BOT_NAME
    else
        print_error "Bot is not running"
    fi
}

clean_docker() {
    print_status "Cleaning up Docker resources..."
    stop_bot
    
    if [ "$(docker images -q $IMAGE_NAME)" ]; then
        docker rmi $IMAGE_NAME
        print_success "Docker image removed"
    fi
    
    docker system prune -f
    print_success "Docker cleanup completed"
}

show_usage() {
    echo "Telegram Bot Docker Manager"
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  build    - Build the Docker image"
    echo "  start    - Start the bot container"
    echo "  stop     - Stop and remove the bot container"
    echo "  restart  - Restart the bot"
    echo "  logs     - Show bot logs"
    echo "  clean    - Clean up all Docker resources"
    echo "  status   - Show bot status"
    echo ""
}

show_status() {
    print_status "Bot Status:"
    if [ "$(docker ps -q -f name=$BOT_NAME)" ]; then
        echo "Container: Running"
        echo "ID: $(docker ps -q -f name=$BOT_NAME)"
        echo "Uptime: $(docker inspect --format='{{.State.StartedAt}}' $BOT_NAME)"
    else
        echo "Container: Not running"
    fi
    
    if [ "$(docker images -q $IMAGE_NAME)" ]; then
        echo "Image: Available"
    else
        echo "Image: Not built"
    fi
}

# Main command handler
case "${1:-help}" in
    build)
        build_image
        ;;
    start)
        start_bot
        ;;
    stop)
        stop_bot
        ;;
    restart)
        restart_bot
        ;;
    logs)
        show_logs
        ;;
    clean)
        clean_docker
        ;;
    status)
        show_status
        ;;
    help|*)
        show_usage
        ;;
esac
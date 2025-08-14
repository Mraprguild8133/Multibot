# Overview

This is a comprehensive Telegram bot that provides multiple AI-powered services and utilities. The bot serves as a multi-functional assistant capable of text generation, image/video analysis, background removal, YouTube video search, and movie information lookup. It integrates with several external APIs including Google's Gemini AI, YouTube Data API, TMDB (The Movie Database), Remove.bg, and Google Vision API to deliver a rich user experience through Telegram's messaging platform.

## Recent Changes
- **August 14, 2025**: Bot fully deployed and operational with all features working
- **August 14, 2025**: TMDB API key updated for enhanced movie search functionality
- **August 14, 2025**: Google Vision API integrated for advanced image analysis capabilities
- **August 14, 2025**: Enhanced image analysis now combines Google Vision + Gemini AI
- **August 14, 2025**: Fixed Telegram message formatting issues for long AI responses
- **August 14, 2025**: Docker containerization support added with multi-stage build optimization
- **August 14, 2025**: Webhook system successfully configured and active for real-time message processing
- **August 14, 2025**: Web dashboard created with status monitoring and feature overview

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Bot Framework Architecture
The application uses the `python-telegram-bot` library as the core framework for handling Telegram interactions. The main entry point (`main.py`) sets up the bot application with command and message handlers, implementing a clean separation between the bot interface and business logic.

## Service-Oriented Architecture
The system follows a modular service-oriented design with dedicated service classes for each external API integration:

- **GeminiService**: Handles AI text generation and image analysis using Google's Gemini AI
- **YouTubeService**: Manages video search functionality via YouTube Data API
- **TMDBService**: Provides movie search and information retrieval from The Movie Database
- **RemoveBgService**: Handles background removal from images using Remove.bg API
- **VisionService**: Analyzes images and videos using Google Vision API with Gemini fallback

## Handler Pattern
The bot implements a handler-based architecture where different types of user inputs (commands, text messages, media files) are routed to appropriate handler functions. This design allows for easy extension and modification of bot capabilities.

## Configuration Management
Environment-based configuration is centralized in a `Config` class, managing API keys and application settings. This approach ensures secure credential handling and easy deployment across different environments.

## Error Handling and Fallback Strategy
The system implements graceful degradation with fallback mechanisms, particularly for image analysis where Gemini serves as a backup when Google Vision API is unavailable. Error handling is centralized through utility functions that format user-friendly error messages.

## File Processing Architecture
Temporary file handling is implemented for processing uploaded media, with size validation and format checking to ensure system stability and security.

# External Dependencies

## AI and Machine Learning Services
- **Google Gemini AI**: Primary AI service for text generation, image analysis, and video processing
- **Google Vision API**: Image analysis and object detection (with Gemini fallback)

## Media and Content APIs
- **YouTube Data API v3**: Video search, metadata retrieval, and statistics
- **The Movie Database (TMDB) API**: Movie search, details, cast information, and poster images
- **Remove.bg API**: Automated background removal from images

## Infrastructure Services
- **Telegram Bot API**: Core messaging platform integration
- **Google Cloud Platform**: Authentication and credential management for Google services

## Python Libraries
- **python-telegram-bot**: Telegram bot framework and API wrapper
- **google-generativeai**: Google Gemini AI client library
- **google-cloud-vision**: Google Vision API client
- **aiohttp**: Asynchronous HTTP client for file downloads
- **requests**: HTTP library for API communications

## Runtime Dependencies
- **Python 3.7+**: Core runtime environment
- **Environment variables**: Secure configuration management for API keys and credentials
# Chatbot Automation Project

A Python-based chatbot automation project that reads messages from a chat window using OCR, identifies the latest received message, generates a reply, and automatically sends it.

## Platform

This project is currently developed and tested on **macOS**.

The current OCR implementation uses Apple's **Vision framework** along with macOS-specific frameworks such as Quartz, Cocoa, and Foundation.

Therefore, the current implementation is specifically designed for macOS.

## Windows Support

The main chatbot logic can be reused on Windows.

However, the current OCR implementation uses Apple's Vision framework, which is not available on Windows.

For Windows support, the macOS-specific OCR components will be replaced with a Windows-compatible OCR solution.

The goal is to keep the main chatbot logic common across both platforms while changing only the platform-specific components.

## Current Workflow

```text
Chat Window
     ↓
Screenshot
     ↓
OCR
     ↓
Extract Messages
     ↓
Identify Latest Received Message
     ↓
Generate Reply
     ↓
PyAutoGUI
     ↓
Send Reply
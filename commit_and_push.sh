#!/bin/bash

# Set your Git identity (only runs once if already set)
git config --global user.name "thenamenishant"
git config --global user.email "shanishant127@gmail.com"

# Initialize Git repo (safe even if already initialized)
git init

# Stage all files
git add .

# Commit
git commit -m "Initial commit: Update AI stock portfolio app"

# Link remote repository (won't error if already set)
git remote remove origin 2> /dev/null
git remote add origin https://github.com/thenamenishant/stock-portfolio-ai.git

# Push to main branch
git branch -M main
git push -u origin main

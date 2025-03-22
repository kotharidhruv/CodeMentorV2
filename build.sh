#!/bin/bash

# Exit the script if any command fails
set -e

echo "Starting build process..."

# Step 1: Install backend dependencies
echo "Installing backend dependencies..."
pip install -r requirements.txt

# Step 2: Navigate to the frontend directory
echo "Navigating to frontend directory..."
cd front-end

# Step 3: Install frontend dependencies (from package.json)
echo "Installing frontend dependencies..."
npm install

# Step 4: Build the frontend
echo "Building frontend..."
CI=false npm run build

# Step 5: Create the necessary directories in the backend (if they don't exist)
echo "Creating necessary directories in the backend..."
mkdir -p ../flask_project/build/static

# Step 6: Copy the frontend build to backend
echo "Copying built frontend files to backend..."
cp -r build/* ../flask_project/build/

# Step 7: Return to root directory (if necessary)
cd ..

echo "Build process completed successfully!"

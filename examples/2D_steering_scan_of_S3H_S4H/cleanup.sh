# Remove files without the specified extensions
find . -type f ! -name "*.sh" ! -name "*.ele" ! -name "*.lte" ! -name "*.py" ! -name "*.yml" ! -name "*.md" -exec rm -f {} \;
rm -rf elegant_scan


# Display a message
echo "Cleanup completed."
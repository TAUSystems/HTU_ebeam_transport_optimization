#!/bin/zsh

# Set root_directory to the current working directory
root_directory="$(pwd)"

# Function to create a timestamped directory
create_timestamped_directory() {
  local timestamp="$(date +'%Y_%m_%d_%H_%M_%S')"
  local initial_directory_name="$1"
  local new_directory_name="${timestamp}_${initial_directory_name}"
  
  mkdir -p "../results/${new_directory_name}"
  echo "../results/${new_directory_name}"  # Print the new directory path
}

# Function to move 'elegant_scan' directory and copy specified files
move_and_copy_files() {
  local source_directory="$1"
  local destination_directory="$2"

  # Move 'elegant_scan' directory into the new directory
  mv "${source_directory}/elegant_scan" "${destination_directory}"

  # Copy .py, .txt, and .yml files
  find "${source_directory}" -type f \( -name "*.py" -o -name "*.txt" -o -name "*.md" -o -name "*.yml" -o -name "*.lte" -o -name "*.pickle" -o -name "*.npy" -o -name "*.ele" -o -name "*.sh" -o -name "*.png" \) -exec cp {} "${destination_directory}" \;
}

# Create timestamped directory and move 'elegant_scan' and copy specified files
current_directory_name="${PWD##*/}"
new_directory="$(create_timestamped_directory "${current_directory_name}")"
move_and_copy_files "${root_directory}" "${new_directory}"

# Set default version and values
default_version="5ec85a7199"
default_values=("httpfs" "iceberg" "json" "motherduck" "parquet" "spatial" "sqlite_scanner" "tpcds" "tpch")

# Use provided arguments or defaults
version="${1:-$default_version}"
values=("${@:2}")

if [ ${#values[@]} -eq 0 ]; then
  values=("${default_values[@]}")
fi

download_and_zip_duckdb_extensions() {
  base_url="http://extensions.duckdb.org/${version}/windows_amd64"

  # Create an empty array to hold the names of successfully downloaded files
  downloaded_files=()

  # Download files
  for value in "${values[@]}"; do
    file_name="${value}.duckdb_extension.gz"

    # Download the file; continue to the next iteration on failure
    if wget -q "${base_url}/${file_name}"; then
      echo "Downloaded ${file_name}"
      downloaded_files+=("${file_name}")
    else
      echo "Failed to download ${file_name}"
    fi
  done

  # Zip the downloaded files into dd.zip
  if [ ${#downloaded_files[@]} -gt 0 ]; then
    zip dd.zip "${downloaded_files[@]}"
    echo "Zipped downloaded files into dd.zip"

    # Remove the .gz files
    rm -f "${downloaded_files[@]}"
    echo "Deleted the .gz files"
  else
    echo "No files to zip"
  fi
}

# Execute the function
download_and_zip_duckdb_extensions

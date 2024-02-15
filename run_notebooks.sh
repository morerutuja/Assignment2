#!/bin/bash

# Function to execute a notebook and check for failure
execute_notebook() {
    notebook_path=$1
    echo "Executing $notebook_path..."

    # Use jupyter nbconvert to execute the notebook
    jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=-1 "$notebook_path"

    
    if [ $? -ne 0 ]; then
        echo "Failed to execute $notebook_path. Halting execution."
        exit 1
    else
        echo "Successfully executed $notebook_path."
    fi
}

# Navigate to the project root directory
cd "$(dirname "$0")"



# Execute Webscrapper.ipynb
execute_notebook "Webscrape/Webscrapper.ipynb"

# Execute snowflake_sqlalchemy.ipynb
execute_notebook "Snowflake_Transfer1/snowflake_sqlalchemy.ipynb"

# Execute PDF Extractor
# execute_notebook "PDF_Extraction/final.ipynb"


# Execute Snowflake_Transfer_Metadata.ipynb
execute_notebook "Snowflake_Transfer_Metadata/Snowflake_Transfer_Metadata.ipynb"

echo "All notebooks executed successfully."

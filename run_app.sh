#!/usr/bin/env bash

# Exit on any error
set -e

################################################################################
# Determine script’s directory (the location of this .sh file).
# This allows us to reference other files relative to the script’s location.
################################################################################
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "[RUN_APP] Activating virtual environment..."
# Activate the venv using a path relative to this script
source "${SCRIPT_DIR}/venv_hailo_rpi5_dmc/bin/activate"

# If you also need environment variables from setup_env.sh, uncomment:
# echo "[RUN_APP] Sourcing setup_env.sh..."
# source "${SCRIPT_DIR}/setup_env.sh"

echo "[RUN_APP] Running main.py with arguments..."

python "/home/david/DMC_app/main.py" \
  --labels-json "/home/david/DMC_app/resources/barcode-labels.json" \
  --hef-path "/home/david/DMC_app/resources/yolov11_model_DMC_c.hef" \
  --input "rpi" \
  --use-frame

echo "[RUN_APP] Done."

#################################################################################
## Below is an example Bash script that uses relative paths to activate your virtual environment and run main.py with the specified arguments. 
## It determines the script’s directory at runtime, then constructs all paths relative to that directory. 
## This way, you don’t need to hardcode /home/david/DMC_app; it will work as long as everything is placed in (or relative to) the same directory.
## Make sure this script is in the same top-level folder as your venv_hailo_rpi5_dmc directory, main.py, and resources folder, or adjust the relative paths accordingly.
#################################################################################

export NVM_DIR="$HOME/.nvm"
export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" # This loads nvm
nvm use 10

export SUMO_NETWORK_GEOJSON=../scenario_munich/sumo_network.geojson
export SUMO_SS=../sharedstreets/sumo_network_munich.geojson
export DETECTORS_GEOJSON=../scenario_munich/bast_munich.geojson
export DETECTORS_SS=../sharedstreets/bast_munich.geojson

shst match $DETECTORS_GEOJSON --out=$DETECTORS_SS --snap-intersections --follow-line-direction --follow-line-direction --snap-intersections --search-radius=100 --offset-line=1 

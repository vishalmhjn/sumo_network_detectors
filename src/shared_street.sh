export NVM_DIR="$HOME/.nvm"
export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" # This loads nvm
nvm use 10

export SUMO_NETWORK_GEOJSON=../sample_files/edgefile.geojson
export SUMO_SS=../sharedstreets_outputs/edgefile.geojson
export DETECTORS_GEOJSON=../sample_files/pointfile.geojson
export DETECTORS_SS=../sharedstreets_outputs/pointfile.geojson

shst match $DETECTORS_GEOJSON --out=$DETECTORS_SS --snap-intersections --follow-line-direction --follow-line-direction --snap-intersections --search-radius=100 --offset-line=1 

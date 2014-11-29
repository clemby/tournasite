curdir=`pwd`

bower install

echo "Building bracket converter..."
cd bower_components/tournament-bracket-converter
npm install
bower install
grunt
cd $curdir

GAME ?= default

install:
	cd app; npm install

json:
	cd app; node node_modules/inkjs/bin/inkjs-compiler.js -o ink/game.ink.json ink/${GAME}.ink

start:
	cd app; npm start

launch:
	cd app; pm2 start app.js --name iria

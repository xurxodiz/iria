install:
	cd app; npm install

json:
	cd app; node node_modules/inkjs/dist/inkjs-compiler.js -o ink/game.ink.json ink/game.ink

start:
	cd app; npm start

launch:
	cd app; pm2 start npm --name "iria" -- start

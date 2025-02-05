-> start

== start ==
Camiñaba pola barrio unha fría mañá de febreiro cando, gorecida contra a porta dun edificio, ablsiquei o que parecía unha donicela.

Estaba enroscada sobre si mesma, arfando con pesadez e tremendo de frío.

Deume pena. Tiña que actuar decontado…

* …polo que me detiven a examinala.
-> examine
* …polo que subín correndo a casa a por mantas.
-> blankets

== blankets ==
Cando voltei, a donicela xa non estaba.

Sempre me preguntei que lle pasara.

Quero pensar que sacou forzas para recuperarse e moverse.
-> END

== examine ==
A súa pelaxe escintilaba con brillos violetas. Dáballe un aire estraño, inquietanto, como os debuxos que fan os nenos, libres dos corsés adultos, cando na súa mente as cores da vida real son só suxestións e non leis, e agarran as ceras con liberdade ilimitada.

Entre iso, e que non era común ver donicelas por aquí…

* …decidín manter a distancia cautelosamente.
-> distance
* …decidín achegarme a vela mellor.
-> close
-> END

== distance ==
Os animais salvaxes poden ser perigosos, pero tampouco tiña corazón a abandonala.

Precisaba consello.

Chamei entón a

* Niña, a miña amiga veterinaria.
-> ninha
* Guecho, o meu veciño.
-> guecho

== ninha ==
"Tantea a sua fereza ofrecendo comida. Tes algo brandiño enriba? Plátano ou así."

Tiña.
-> platano

== guecho ==
"Tes que tranquilizala primeiro antes de collela. Pásalle a man polo lombo para que vexa que lle queres ben."

Acheguei a man, pero axiña saltou agresiva…

* …e me trabou na man
-> hand
* …e me rabuñou na cara
-> face

== face ==
Saltei para atrás e o bicho saiu correndo rúa abaixo. Condanada.

A ferida doeu varios días. O orgullo, varias semanas.
-> END

== hand ==

"Aarg!", berrei, e a donicela aínda tardou uns minutos en soltarme. Cando o fixo, vin que fixera sangue, e perforara bastante.

{
    - tangerine: -> hand_ok
    - not tangerine: -> hand_bad
}

== hand_ok ==

Ademáis aquilo picaba bastante, pois tiña a man cuberta do xugo da mandarina.

Subín correndo a casa a lavar ben a ferida. Vendeina ben e pasei a tarde na casa enfurruñado.
-> END

== hand_bad ==

Subín correndo a casa, pero aquilo doía cada vez máis e tiña medo que se infectase. Baixei para ir a urxencias; cando pasei polo portal, aquela fera do demo xa non estaba.

Mal raio a parta, os médicos aínda non saben se me curará o tendón.
-> END

== close ==

Non sei moito de animais, pero sei que a todos seres vivos lles presta comer. Abrín a bolsa e rebusquei.

—Ah! Isto servirá —murmurei, e saquei…

* …uns froitos secos
-> nuts
* …unha mandarina
-> tangerine
* …un plátano
-> platano

== nuts ==
Collín un puñado da bolsa e cisqueinos por diante do animaliño.
-> success

== success ==
Sen abrir os ollos, cheirou, achegando o nariciño cada vez máis. Finalmente, púxose en pé e exclamou

—Grazas por chegar á fin da historia.
-> END

== tangerine ==
Saquei a mandarina, peleina, e deixei os cuarteiróns no chan.

{
- RANDOM (1, 2): -> success
- else: -> tangerine_bite
}

== tangerine_bite ==
Sen abrir os ollos, cheirou, achegando o nariciño cada vez máis. Finalmente, torceu o bico e saltoume cara a man coa boca ben aberta e os cairos saídos.
-> hand

== platano ==
Deiteille o plátano diante, xa peladiño, para deixar que o ulise tranquila, e aparteime de novo.

Debíalle gustar moito, pois non tardou en chantarlle uns mordiscos. Papouno todo, devagariño pero sen parar.

A nova enerxía deixouna máis tranquila, respirando amodo. Aproveitei que parecía adormecida para subir a casa e baixarlle unha mantiña.
-> blankets
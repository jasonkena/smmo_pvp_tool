// ==UserScript==
// @name         RevoY0m
// @namespace    {{ SERVER_URL }}
// @version      0.1
// @description  Integration script for RevoGen's PVP Tool
// @author       RevoGen
// @match        {{ SERVER_URL }}*
// @icon         {{ url_for('static', filename='favicon.svg', _external=True) }}
// @grant        GM_setValue
// @grant        GM_getValue
// @grant        unsafeWindow
// ==/UserScript==

const ws = new WebSocket("ws://127.0.0.1:8080/");

ws.onmessage = async function (event) {
  let data = event.data;
  let message = JSON.parse(data);
  if (message["type"] == "trigger") {
    console.log("Triggered");
    let url = GM_getValue("turbo_submit", false);
    if (url) {
      ws.send(JSON.stringify({ type: "open", data: url }));
    }
    url = await unsafeWindow.turbo(true);
    if (url) {
      GM_setValue("turbo_submit", url);
    }
  }
};

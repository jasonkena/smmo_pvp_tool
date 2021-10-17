// ==UserScript==
// @name         Search Notifier
// @namespace    {{ SERVER_URL }}
// @require      https://code.jquery.com/jquery-3.6.0.min.js
// @version      0.1
// @description  Notify on Discord if search result appears
// @author       RevoGen
// @match        {{ SERVER_URL }}*
// @icon         {{ url_for('static', filename='favicon.svg', _external=True) }}
// @grant        unsafeWindow
// ==/UserScript==
/* globals $ */

// https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID
const DISCORD_UID = "0";
// Insert your Discord webhook URL (defaults to #bot-commands in RevoGen's server: https://discord.gg/2msJUHEzUx)
const WEBHOOK_URL =
  "https://discord.com/api/webhooks/899404445522231357/INrLOQZdKNIo_k_Rze9YdFE9x_KaBLvf4ARxkcX6z0NbpD5Ofplm8UveIglxiQxYNYyt";

function sendMessage(message) {
  var request = new XMLHttpRequest();
  request.open("POST", WEBHOOK_URL);

  request.setRequestHeader("Content-Type", "application/json");

  var params = {
    content: `<@${DISCORD_UID}> ${message}`,
  };

  request.send(JSON.stringify(params));
}

async function loop() {
  try {
    if (!document.getElementsByClassName("hit").length) {
      if ((await unsafeWindow.getQuery()).length) {
        sendMessage("search target found");
      }
      setTimeout(loop, unsafeWindow.CLIENT_CONFIG["AUTO_SEARCH_DELAY"]);
    }
  } catch (error) {
    unsafeWindow.raiseError(error);
  }
}

(function main() {
  console.log("SearchNotifier loaded");

  setTimeout(loop, unsafeWindow.CLIENT_CONFIG["AUTO_SEARCH_DELAY"]);
})();

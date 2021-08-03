// ==UserScript==
// @name         PointsListener
// @namespace    https://revogen.tech/
// @require      https://code.jquery.com/jquery-3.6.0.min.js
// @version      0.1
// @description  Notification script for EP/QP
// @author       RevoGen
// @exclude      https://web.simple-mmo.com/login
// @match        https://web.simple-mmo.com/*
// @icon         https://revogen.tech/static/favicon.svg
// @grant        GM_setValue
// @grant        GM_getValue
// @grant        GM_addValueChangeListener
// ==/UserScript==
/* globals $ */

// https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID
const DISCORD_UID = "242219798140944384";
// Insert your Discord webhook URL (defaults to #points-listener-ping in RevoGen's server: https://discord.gg/2msJUHEzUx)
const WEBHOOK_URL =
  "https://discord.com/api/webhooks/871946732043378698/M0PdLv2psn-55JQBGtIWFXki5K4Vfh72_Ew1St1-ZLeGUJ_1NrTdM24h40HsuwWEeYJx";
// Percentage of maximum points at which message should be sent
const THRESHOLD = 0.9;

var menu_button = $("#user-menu-button");
var quest_points = $("[x-text='user.quest_points']");
var energy = $("[x-text='user.energy']");
var max_energy = $("[x-text='user.max_energy']");

function setStats() {
  GM_setValue("quest_points", parseInt(quest_points.text()));
  GM_setValue("energy", parseInt(energy.text()));
  GM_setValue("max_energy", parseInt(max_energy.text()));
}

function trigger() {
  console.log("Listener triggered");
  let qp = GM_getValue("quest_points", null);
  let mqp = GM_getValue("max_quest_points", null);
  let ep = GM_getValue("energy", null);
  let mep = GM_getValue("max_energy", null);
  if (qp != null && mqp != null) {
    GM_setValue("qp_time", (THRESHOLD * mqp - qp) * 300 + Date.now() / 1000);
  }
  if (ep != null && mep != null) {
    GM_setValue("ep_time", (THRESHOLD * mep - ep) * 600 + Date.now() / 1000);
  }
}

function sendMessage(message) {
  var request = new XMLHttpRequest();
  request.open("POST", WEBHOOK_URL);

  request.setRequestHeader("Content-Type", "application/json");

  var params = {
    content: `<@${DISCORD_UID}> ${message}`,
  };

  request.send(JSON.stringify(params));
}

function loop() {
  let qp_time = GM_getValue("qp_time", -1);
  let ep_time = GM_getValue("ep_time", -1);
  let now = Date.now() / 1000;
  if (qp_time != -1 && now > qp_time) {
    GM_setValue("qp_time", -1);
    sendMessage("It's QP time!");
  }
  if (ep_time != -1 && now > ep_time) {
    GM_setValue("ep_time", -1);
    sendMessage("It's EP time!");
  }
}

(function main() {
  console.log("Listener loaded");
  GM_addValueChangeListener("quest_points", trigger);
  GM_addValueChangeListener("max_quest_points", trigger);
  GM_addValueChangeListener("energy", trigger);
  GM_addValueChangeListener("max_energy", trigger);
  menu_button.click(function () {
    console.log("Click");
    setTimeout(setStats, 1000);
  });

  if (GM_getValue("quest_points", null) == null) {
    menu_button.click();
  }
  if (location.href === "https://web.simple-mmo.com/quests/viewall") {
    GM_setValue(
      "max_quest_points",
      parseInt($("#questPoints").next().text().split(" ").pop())
    );
  }
  if (GM_getValue("max_quest_points", null) == null) {
    window.open("https://web.simple-mmo.com/quests/viewall");
  }
  loop();
  setInterval(loop, 60000);
})();

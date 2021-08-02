// ==UserScript==
// @name         PVPTool Integration
// @namespace    {{ SERVER_URL }}
// @version      0.1
// @description  Integration script for RevoGen's PVP Tool
// @author       RevoGen
// @match        {{ SERVER_URL }}*
// @match        https://web.simple-mmo.com/user/attack/*
// @icon         {{ url_for('static', filename='favicon.svg', _external=True) }}
// @grant        GM_setValue
// @grant        GM_getValue
// @grant        GM_addValueChangeListener
// @grant        unsafeWindow
// ==/UserScript==
(function main() {
  let matches = GM_info.script.matches;
  matches = matches.map((url) => new RegExp(url).test(location.href));

  // whether page loaded is the smmo attack page
  if (matches[matches.length - 1]) {
    smmo();
  } else {
    tool();
  }
})();

function tool() {
  GM_addValueChangeListener("turbo_request", function () {
    console.log("Turbo request received");
    let url = unsafeWindow.turbo(true);
    if (url) {
      GM_setValue("turbo_submit", url);
    }
  });
  console.log("Tool listener loaded");
}

function turboRequest() {
  // false is default value
  GM_setValue("turbo_request", !GM_getValue("turbo_request", false));
  console.log("Turbo request submitted");
  console.log(GM_getValue("turbo_request"));
}

function smmo() {
  GM_addValueChangeListener(
    "turbo_submit",
    function (name, old_value, new_value) {
      window.location.href = new_value;
    }
  );
  document.addEventListener("keydown", (event) => {
    if (event.code === "Space" && event.target.tagName !== "INPUT") {
      turboRequest();
    }
    return false;
  });
  console.log("SMMO listener loaded");
}

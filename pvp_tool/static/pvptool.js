console.log(CLIENT_CONFIG["SERVER_URL"]);
const cookies = Cookies.withAttributes({ sameSite: "strict" });

$.ajaxSetup({
  // it automatically retries if set to 0
  timeout: CLIENT_CONFIG["AJAX_TIMEOUT"],
});

function raiseError(error) {
  $(".modal").modal("hide");
  $("#error-text").text(error.message);
  errorModal.show();
  throw error;
}

function loginStatus() {
  let access_token = cookies.get("access_token");
  $.ajax({
    type: "GET",
    beforeSend: function (xhr) {
      if (!_.isUndefined(access_token)) {
        xhr.setRequestHeader("Authorization", "Bearer " + access_token);
      }
    },
    url: CLIENT_CONFIG["SERVER_URL"] + "api/login/status",
    cache: false,
    success: function (data) {
      cookies.set("uid", data["uid"]);
      cookies.set("balance", data["balance"]);
      $("#balance").text(data["balance"]);
    },
  }).fail(function (jqXHR, textStatus, errorThrown) {
    raiseError(
      new Error(jqXHR.responseText + " " + textStatus + " " + errorThrown)
    );
  });
}

function getFormData(selector) {
  let data = selector.serializeArray();
  data = _.map(data, (x) => [x.name, x.value]);
  data = _.filter(data, (x) => x[1] != "");
  data = _.fromPairs(data);
  sort_by = data["sort_by"];
  api = data["api"];
  data = _.omit(data, ["sort_by", "api"]);

  try {
    data = _.mapValues(data, JSON.parse);
  } catch (error) {
    raiseError(error);
  }
  if (!_.isUndefined(sort_by)) {
    data["sort_by"] = sort_by;
  }
  if (!_.isUndefined(api)) {
    data["api"] = api;
  }
  return data;
}

function loginRequest() {
  uidModal.hide();
  let uid = getFormData($("#uid-form"))["uid"];
  if (_.isUndefined(uid)) {
    raiseError(new Error("Invalid uid provided"));
  }
  $.ajax({
    type: "GET",
    url: CLIENT_CONFIG["SERVER_URL"] + "api/login/" + uid,
    cache: false,
    success: function (data) {
      cookies.set("motto", data["motto"]);
      cookies.set("verification_token", data["verification_token"]);
      verifyModal.show();
    },
  }).fail(function (jqXHR, textStatus, errorThrown) {
    raiseError(
      new Error(jqXHR.responseText + " " + textStatus + " " + errorThrown)
    );
  });
}

function loginVerify() {
  verifyModal.hide();
  let verification_token = cookies.get("verification_token");
  if (_.isUndefined(verification_token)) {
    raiseError(new Error("Invalid verification token"));
  }
  $.ajax({
    type: "GET",
    beforeSend: function (xhr) {
      xhr.setRequestHeader("Authorization", "Bearer " + verification_token);
    },
    url: CLIENT_CONFIG["SERVER_URL"] + "api/login/verify",
    cache: false,
    success: function (data) {
      cookies.set("access_token", data["access_token"], {
        expires: CLIENT_CONFIG["COOKIE_EXPIRY"],
      });
    },
  }).fail(function (jqXHR, textStatus, errorThrown) {
    raiseError(
      new Error(jqXHR.responseText + " " + textStatus + " " + errorThrown)
    );
  });
}

function getQuery() {
  let query = getFormData($("#query-form"));
  query = JSON.stringify(query);
  let access_token = cookies.get("access_token");
  if (_.isUndefined(access_token)) {
    raiseError(new Error("Invalid access token"));
  }
  $.ajax({
    type: "POST",
    beforeSend: function (xhr) {
      xhr.setRequestHeader("Authorization", "Bearer " + access_token);
    },
    url: CLIENT_CONFIG["SERVER_URL"] + "api/query/submit",
    data: query,
    cache: false,
    success: updateTable,
  }).fail(function (jqXHR, textStatus, errorThrown) {
    raiseError(
      new Error(jqXHR.responseText + " " + textStatus + " " + errorThrown)
    );
  });
}

const intervals = [
  { label: "year", seconds: 31536000 },
  { label: "month", seconds: 2592000 },
  { label: "day", seconds: 86400 },
  { label: "hour", seconds: 3600 },
  { label: "minute", seconds: 60 },
  { label: "second", seconds: 1 },
];

function timeSince(date) {
  const seconds = Math.floor((Date.now() - Date.parse(date)) / 1000);
  const interval = intervals.find((i) => i.seconds < seconds);
  const count = Math.floor(seconds / interval.seconds);
  return `${count} ${interval.label}${count !== 1 ? "s" : ""} ago`;
}

function createRow(object) {
  let row = "<tr onclick=\"window.open('" + object["url"] + "')\">";
  row += "<td>" + object["name"] + "</td>";
  row += '<td class="d-none d-sm-table-cell">' + object["guild_name"] + "</td>";
  row += '<td class="font-monospace text-end">' + object["level"] + "</td>";
  row += '<td class="font-monospace text-end">' + object["gold"] + "</td>";
  row += "<td>" + timeSince(object["timestamp"]) + "</td>";
  row += "</tr>";
  return row;
}

function updateTable(data) {
  let body = _.map(data, createRow);
  $("#table-body").html(body);
  loginStatus();
}

function requestBatch() {
  let access_token = cookies.get("access_token");
  if (_.isUndefined(access_token)) {
    raiseError(new Error("Invalid access token"));
  }
  return $.ajax({
    type: "POST",
    beforeSend: function (xhr) {
      xhr.setRequestHeader("Authorization", "Bearer " + access_token);
    },
    url: CLIENT_CONFIG["SERVER_URL"] + "api/batch/request",
    data: JSON.stringify({ num_tasks: CLIENT_CONFIG["BATCH_SIZE"] }),
    cache: false,
  }).fail(function (jqXHR, textStatus, errorThrown) {
    raiseError(
      new Error(jqXHR.responseText + " " + textStatus + " " + errorThrown)
    );
  });
}

function processTask(task) {
  let api_key = getFormData($("#api-form"))["api"];
  if (_.isUndefined(api_key)) {
    raiseError(new Error("Invalid api_key provided"));
  }
  let endpoint = task["is_player_task"]
    ? "https://api.simple-mmo.com/v1/player/info/"
    : "https://api.simple-mmo.com/v1/guilds/members/";
  endpoint += task["uid"];
  let result;
  return $.ajax({
    type: "POST",
    url: endpoint,
    data: { api_key: api_key },
    cache: false,
  }).fail(function (jqXHR, textStatus, errorThrown) {
    raiseError(
      new Error(jqXHR.responseText + " " + textStatus + " " + errorThrown)
    );
  });
}

function submitBatch(data) {
  let access_token = cookies.get("access_token");
  if (_.isUndefined(access_token)) {
    raiseError(new Error("Invalid access token"));
  }
  return $.ajax({
    type: "POST",
    beforeSend: function (xhr) {
      xhr.setRequestHeader("Authorization", "Bearer " + access_token);
    },
    url: CLIENT_CONFIG["SERVER_URL"] + "api/batch/submit",
    data: JSON.stringify(data),
    cache: false,
  }).fail(function (jqXHR, textStatus, errorThrown) {
    raiseError(
      new Error(jqXHR.responseText + " " + textStatus + " " + errorThrown)
    );
  });
}

var timeouts = [];
function clearTimeouts() {
  _.forEach(timeouts, (x) => clearTimeout(x));
  timeouts = [];
}
function later(delay, func, value) {
  return new Promise((resolve) =>
    timeouts.push(setTimeout((x) => resolve(func(x)), delay, value))
  );
}

async function loop() {
  let batch = await requestBatch();
  let promises = (beta = _.map(batch, (value, i) =>
    later(i * CLIENT_CONFIG["SMMO_DELAY"], processTask, value)
  ));
  // if clearTimeouts is called, this may be left unresolved
  let results = await Promise.all(promises);
  console.log("processing");
  let data = { players: {}, guilds: {} };
  _.forEach(batch, function (value, i) {
    if (value["is_player_task"]) {
      data["players"][value["uid"]] = results[i];
    } else {
      data["guilds"][value["uid"]] = results[i];
    }
  });

  let response = await submitBatch(data);
  loginStatus();
}

async function mining() {
  clearTimeouts();
  if (miningStatus()) {
    try {
      await loop();
      setTimeout(mining, CLIENT_CONFIG["API_DELAY"]);
    } catch (error) {
      clearTimeouts();
      miningStatus(false);
      updateMiningText();
      throw error;
    }
  }
}

function miningStatus(value) {
  let measured_value = $("#mining-button").hasClass("btn-success");
  if (_.isUndefined(value)) {
    return measured_value;
  }
  $("#mining-button").removeClass("btn-primary").removeClass("btn-success");
  $("#mining-button").addClass(value ? "btn-success" : "btn-primary");
}

var uidModal = bootstrap.Modal.getOrCreateInstance($("#uidModal"));
var verifyModal = bootstrap.Modal.getOrCreateInstance($("#verifyModal"));
var errorModal = bootstrap.Modal.getOrCreateInstance($("#errorModal"));

loginStatus();
$("#search-button").click(getQuery);
$("#submit-uid-button").click(loginRequest);
$("#verify-button").click(loginVerify);
$("#verifyModal").on("show.bs.modal", function () {
  $("#target-motto").text(cookies.get("motto"));
});
$("#balance").click(function () {
  loginStatus();
});
$("#mining-button").click(function () {
  miningStatus(!miningStatus());
  updateMiningText();
  mining();
});
function updateMiningText() {
  let text = miningStatus() ? "Stop" : "Start";
  $("#mining-button").text(text);
}
$("#mining-button").mouseover(function () {
  updateMiningText();
});
$("#mining-button").mouseout(function () {
  $("#mining-button").text("Mining");
});
$("#queryModal").on("show.bs.modal", function () {
  $("#query-form").deserialize(cookies.get("query-form"));
});
$("#apiModal").on("show.bs.modal", function () {
  $("#api-form").deserialize(cookies.get("api-form"));
});
$("#queryModal").on("hidden.bs.modal", function () {
  cookies.set("query-form", $("#query-form").serialize(), {
    expires: CLIENT_CONFIG["COOKIE_EXPIRY"],
  });
});
$("#apiModal").on("hidden.bs.modal", function () {
  cookies.set("api-form", $("#api-form").serialize(), {
    expires: CLIENT_CONFIG["COOKIE_EXPIRY"],
  });
});
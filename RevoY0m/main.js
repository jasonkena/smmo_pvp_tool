const ws = require("ws");
const messenger = require("messenger");
const { app, BrowserWindow, ipcMain, globalShortcut } = require("electron");
const path = require("path");

let wss = new ws.WebSocketServer({ port: 8080 });
let client = messenger.createSpeaker("127.0.0.1:8004");

const createWindow = () => {
  const win = new BrowserWindow({
    width: 500,
    height: 250,
  });

  win.loadFile(path.join("assets", "index.html"));
};
console.log("Listener is up");

// data has the format {"type": "open"/"trigger", "data": url}
app.whenReady().then(() => {
  createWindow();
  wss.on("connection", function connection(ws) {
    console.log("Client is connected");
    globalShortcut.unregister("Space");
    globalShortcut.register("Space", () => {
      console.log("Space triggered");
      ws.send(JSON.stringify({ type: "trigger" }));
    });
    ws.on("message", function incoming(data) {
      let buf = new Uint8Array(data);
      let enc = new TextDecoder("utf-8");
      let message = JSON.parse(enc.decode(buf));

      console.log(message);
      if (message["type"] == "open") {
        client.send("openLink", { url: message["data"].replace("web.", "") });
      }
    });
  });
});

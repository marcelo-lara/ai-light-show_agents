import { io } from "socket.io-client";

const URL = "http://localhost:5000"; // Flask server URL
export const socket = io(URL);

socket.on("connect", () => {
  console.log("Connected to websocket server");
});

socket.on("disconnect", () => {
  console.log("Disconnected from websocket server");
});

socket.on("response", (data) => {
  console.log("Received response:", data);
  // Handle responses here or dispatch to components
});

export const sendMessage = (action: string, params: any = {}) => {
  socket.emit("message", { action, params });
};

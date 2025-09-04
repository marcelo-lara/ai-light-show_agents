import { io, Socket } from "socket.io-client";

// Types for app state and messages
export interface AppState {
  type: "app_state";
  data: {
    current_song: string | null;
  };
}

export interface WebSocketManager {
  socket: Socket | null;
  isConnected: boolean;
  connect: () => void;
  disconnect: () => void;
  sendMessage: (action: string, params?: any) => void;
  onAppState: (callback: (state: AppState) => void) => void;
  onError: (callback: (error: any) => void) => void;
}

class WebSocketService implements WebSocketManager {
  public socket: Socket | null = null;
  public isConnected: boolean = false;
  private reconnectAttempts: number = 0;
  private maxReconnectAttempts: number = 5;
  private reconnectDelay: number = 1000;
  private appStateCallbacks: ((state: AppState) => void)[] = [];
  private errorCallbacks: ((error: any) => void)[] = [];

  constructor() {
    this.connect();
  }

  public connect(): void {
    if (this.socket?.connected) {
      console.log("WebSocket already connected");
      return;
    }

    const URL = window.location.hostname === 'localhost' 
      ? "http://localhost:5000" 
      : `${window.location.protocol}//${window.location.host}`;

    console.log("Connecting to WebSocket server at:", URL);

    this.socket = io(URL, {
      autoConnect: true,
      reconnection: true,
      reconnectionAttempts: this.maxReconnectAttempts,
      reconnectionDelay: this.reconnectDelay,
      timeout: 10000,
    });

    this.setupEventListeners();
  }

  public disconnect(): void {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
      this.isConnected = false;
      console.log("WebSocket disconnected");
    }
  }

  public sendMessage(action: string, params: any = {}): void {
    if (!this.socket?.connected) {
      console.error("Cannot send message: WebSocket not connected");
      this.notifyError(new Error("WebSocket not connected"));
      return;
    }

    const message = { action, params };
    console.log("Sending message:", message);
    this.socket.emit("message", message);
  }

  public onAppState(callback: (state: AppState) => void): void {
    this.appStateCallbacks.push(callback);
  }

  public onError(callback: (error: any) => void): void {
    this.errorCallbacks.push(callback);
  }

  private setupEventListeners(): void {
    if (!this.socket) return;

    // Connection events
    this.socket.on("connect", () => {
      console.log("✅ Connected to WebSocket server");
      this.isConnected = true;
      this.reconnectAttempts = 0;
    });

    this.socket.on("disconnect", (reason) => {
      console.log("❌ Disconnected from WebSocket server:", reason);
      this.isConnected = false;
      
      if (reason === "io server disconnect") {
        // Server initiated disconnect, don't reconnect automatically
        console.log("Server disconnected the connection");
      } else {
        // Client or network issue, will attempt to reconnect
        console.log("Connection lost, will attempt to reconnect...");
      }
    });

    this.socket.on("connect_error", (error) => {
      this.reconnectAttempts++;
      console.error(`❌ Connection error (attempt ${this.reconnectAttempts}):`, error.message);
      
      if (this.reconnectAttempts >= this.maxReconnectAttempts) {
        console.error("Max reconnection attempts reached");
        this.notifyError(new Error("Failed to connect after multiple attempts"));
      }
    });

    // App state message handler - this is the main message we want to handle
    this.socket.on("app_state", (data: AppState) => {
      console.log("📱 Received app_state:", data);
      this.notifyAppState(data);
    });

    // Generic message handler for other messages
    this.socket.on("message", (data: any) => {
      console.log("📨 Received message:", data);
    });

    // Error handler
    this.socket.on("error", (error: any) => {
      console.error("🚨 WebSocket error:", error);
      this.notifyError(error);
    });

    // Reconnection events
    this.socket.on("reconnect", (attemptNumber) => {
      console.log(`🔄 Reconnected after ${attemptNumber} attempts`);
      this.isConnected = true;
      this.reconnectAttempts = 0;
    });

    this.socket.on("reconnect_attempt", (attemptNumber) => {
      console.log(`🔄 Reconnection attempt ${attemptNumber}`);
    });

    this.socket.on("reconnect_error", (error) => {
      console.error("🔄❌ Reconnection error:", error);
    });

    this.socket.on("reconnect_failed", () => {
      console.error("🔄❌ Reconnection failed after all attempts");
      this.notifyError(new Error("Reconnection failed"));
    });
  }

  private notifyAppState(state: AppState): void {
    this.appStateCallbacks.forEach(callback => {
      try {
        callback(state);
      } catch (error) {
        console.error("Error in app state callback:", error);
      }
    });
  }

  private notifyError(error: any): void {
    this.errorCallbacks.forEach(callback => {
      try {
        callback(error);
      } catch (err) {
        console.error("Error in error callback:", err);
      }
    });
  }
}

// Create singleton instance
export const webSocketService = new WebSocketService();

// Export convenience functions for backward compatibility
export const socket = webSocketService.socket;
export const sendMessage = webSocketService.sendMessage.bind(webSocketService);

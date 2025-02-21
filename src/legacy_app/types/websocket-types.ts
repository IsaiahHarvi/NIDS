export type Wrapper = { children: JSX.Element | JSX.Element[] | string };

export type WebSocketContextProps = {
  sendMessage(message: string): void;
};

export type WebSocketMessage = {
  id?: string;
  type?: string;
  payload?: Record<string, unknown>;
};

export type ChatFile = {
  filename: string;
  mimetype: string;
};

export type Message = {
  id: string;
  role: "user" | "assistant";
  content: string;
  files?: ChatFile[];
};

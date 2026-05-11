const BASE = "/api";

export async function fetchJSON<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`);
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return res.json();
}

export async function postJSON<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return res.json();
}

/** Stream a tutor message, calling onToken for each token and onError on sentinel errors. */
export async function streamTutorMessage(
  payload: {
    message: string;
    socratic_mode: boolean;
    context: object;
  },
  onToken: (token: string) => void,
  onError?: (msg: string) => void,
): Promise<void> {
  const res = await fetch(`${BASE}/tutor/message`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  const reader = res.body!.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    const lines = decoder.decode(value).split("\n");
    for (const line of lines) {
      if (!line.startsWith("data: ")) continue;
      const data = line.slice(6);
      if (data === "[DONE]") return;
      try {
        const parsed = JSON.parse(data);
        if (!parsed.token) continue;
        const tok: string = parsed.token;
        if (tok.startsWith("\x00")) {
          const isRateLimit = tok === "\x00RATE_LIMIT";
          onError?.(isRateLimit ? "rate_limit" : tok.slice(7)); // strip \x00ERROR:
          return;
        }
        onToken(tok);
      } catch {
        // partial chunk — ignore
      }
    }
  }
}

import { apiFetch } from "./api";

export async function getDevices(token: string) {
  return apiFetch("/device", {}, token);
}

export async function addDevice(name: string, token: string) {
  return apiFetch("/device", {
    method: "POST",
    body: JSON.stringify({ name }),
  }, token);
}

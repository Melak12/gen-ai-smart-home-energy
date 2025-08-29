import { apiFetch } from "./api";

export async function getTelemetry(deviceId: number, token: string) {
  return apiFetch(`/telemetry/${deviceId}`, {}, token);
}

export async function getAllTelemetry(token: string) {
  return apiFetch("/telemetry", {}, token);
}

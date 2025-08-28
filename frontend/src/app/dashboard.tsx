"use client";

import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import { getDevices, addDevice } from "../lib/device";
import { getTelemetry } from "../lib/telemetry";

type Device = { id: number; name: string };
type Telemetry = { id: number; timestamp: string; usage: number; deviceId: number };

export default function Dashboard() {
  const { token } = useAuth();
  const [devices, setDevices] = useState<Device[]>([]);
  const [selected, setSelected] = useState<number | null>(null);
  const [telemetry, setTelemetry] = useState<Telemetry[]>([]);
  const [newDevice, setNewDevice] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    if (token) getDevices(token).then((d) => setDevices(d as Device[])).catch(() => setDevices([]));
  }, [token]);

  useEffect(() => {
    if (token && selected)
      getTelemetry(selected, token).then((t) => setTelemetry(t as Telemetry[])).catch(() => setTelemetry([]));
  }, [token, selected]);

  const handleAdd = async () => {
    setError("");
    try {
      await addDevice(newDevice, token!);
      setDevices(await getDevices(token!) as Device[]);
      setNewDevice("");
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : String(e));
    }
  };

  return (
    <div>
      <h2>Your Devices</h2>
      <ul>
        {devices.map((d) => (
          <li key={d.id}>
            <button onClick={() => setSelected(d.id)}>{d.name}</button>
          </li>
        ))}
      </ul>
      <input value={newDevice} onChange={e => setNewDevice(e.target.value)} placeholder="New device name" />
      <button onClick={handleAdd}>Add Device</button>
      {error && <div style={{color:'red'}}>{error}</div>}
      {selected && (
        <div>
          <h3>Telemetry for Device {selected}</h3>
          <ul>
            {telemetry.map((t) => (
              <li key={t.id}>{t.timestamp}: {t.usage}W</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

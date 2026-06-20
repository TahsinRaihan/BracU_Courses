

import { writable } from 'svelte/store';

interface Notification {
  id: number;
  message: string;
  type: 'info' | 'success' | 'error' | 'warning';
  timestamp: string;
  seen: boolean;
  [key: string]: any; // For meta data
}

function createNotifications() {
  const { subscribe, update } = writable<Notification[]>([]);
  let counter = 0;

  function notify(message: string, type: 'info' | 'success' | 'error' | 'warning' = 'info', meta: Record<string, any> = {}) {
    const id = ++counter;
    const timestamp = new Date().toISOString();
    const note: Notification = { id, message, type, timestamp, seen: false, ...meta };
    update(n => [note, ...n]);
  }

  function markSeen(id: number) {
    update(n => n.map(x => (x.id === id ? { ...x, seen: true } : x)));
  }

  function markAllSeen() {
    update(n => n.map(x => ({ ...x, seen: true })));
  }

  function dismiss(id: number) {
    update(n => n.filter(x => x.id !== id));
  }

  function dismissAll() {
    update(() => []);
  }

  return { subscribe, notify, markSeen, markAllSeen, dismiss, dismissAll };
}

export const notifications = createNotifications();
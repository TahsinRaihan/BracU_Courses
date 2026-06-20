import { writable } from 'svelte/store'

export type ToastNotification = {
  id: string
  title: string
  message: string
  type?: 'event' | 'transaction' | 'general' | 'food_order' | 'study_room' | 'banner_request'
  created_at?: string
}

function createToastStore() {
  const { subscribe, update, set } = writable<ToastNotification[]>([])

  function push(notification: ToastNotification) {
    update((list) => [notification, ...list].slice(0, 5))
    // Auto-remove after a few seconds
    setTimeout(() => {
      remove(notification.id)
    }, 5000)
  }

  function remove(id: string) {
    update((list) => list.filter((n) => n.id !== id))
  }

  function clear() {
    set([])
  }

  return { subscribe, push, remove, clear }
}

export const toasts = createToastStore()



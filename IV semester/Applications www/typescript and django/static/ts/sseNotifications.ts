
const SSE_URL = '/sse/notifications/';

interface BoardEvent {
  board_id: number;
  board_name: string;
  creator_username: string;
}

interface PathEvent {
  path_id: number;
  board_id: number;
  board_name: string;
  user_username: string;
}

let toastContainer: HTMLElement | null = null;


function ensureContainer() {
  if (toastContainer) return;
  toastContainer = document.createElement('div');
  toastContainer.id = 'toast-container';
  Object.assign(toastContainer.style, {
    position: 'fixed',
    top: '1rem',
    right: '1rem',
    zIndex: '10000',
    display: 'flex',
    flexDirection: 'column',
    gap: '0.5rem',
  });
  document.body.appendChild(toastContainer);
}

function showToast(message: string, onClick?: () => void) {
  ensureContainer();
  const toast = document.createElement('div');
  toast.textContent = message;
  Object.assign(toast.style, {
    background: 'rgba(0, 0, 0, 0.8)',
    color: 'white',
    padding: '0.75rem 1rem',
    borderRadius: '4px',
    cursor: onClick ? 'pointer' : 'default',
    maxWidth: '300px',
    boxShadow: '0 2px 6px rgba(0,0,0,0.3)',
  });
  if (onClick) toast.addEventListener('click', onClick);
  toastContainer!.appendChild(toast);

  setTimeout(() => {
    toast.remove();
  }, 5000);
}


function initSseNotifications() {
  const evtSource = new EventSource(SSE_URL);

  evtSource.onopen = () => {
    console.log('[SSE] Połączono z serwerem powiadomień');
  };

  evtSource.onerror = (err) => {
    console.error('[SSE] Błąd połączenia:', err);
  };

  evtSource.addEventListener('newBoard', (e: MessageEvent) => {
    let payload: BoardEvent;
    try {
      payload = JSON.parse(e.data);
    } catch {
      console.warn('[SSE] Nieprawidłowy JSON w newBoard:', e.data);
      return;
    }
    console.log('nowy board');
    showToast(
      `Użytkownik ${payload.creator_username} utworzył nową planszę: "${payload.board_name}".`,
      () => { window.location.href = `/play/${payload.board_id}/`; }
    );
  });

  evtSource.addEventListener('newPath', (e: MessageEvent) => {
    let payload: PathEvent;
    try {
      payload = JSON.parse(e.data);
    } catch {
      console.warn('[SSE] Nieprawidłowy JSON w newPath:', e.data);
      return;
    }
    console.log('nowy path');
    showToast(
      `Użytkownik ${payload.user_username} zapisał ścieżkę na planszy: "${payload.board_name}".`
    );
  });
}

document.addEventListener('DOMContentLoaded', () => {
  initSseNotifications();
});
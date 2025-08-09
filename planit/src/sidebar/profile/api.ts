const API_BASE_URL = import.meta.env.VITE_API_URL || '';

export const clearChatHistory = async (token: string): Promise<Response> => {
  return fetch(`${API_BASE_URL}/api/chat/history`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
};

export const deleteUserAccount = async (token: string): Promise<Response> => {
  return fetch(`${API_BASE_URL}/api/user/`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
};
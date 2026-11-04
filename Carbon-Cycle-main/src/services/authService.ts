import { FacilityRegistrationProfile } from '../types';
import { API_URL, API_BASE_URL, API_ENDPOINTS, checkHealthApi, HealthResponse } from './api';

export { API_URL, API_BASE_URL, API_ENDPOINTS, checkHealthApi };
export type { HealthResponse };

export interface AuthUser {
  id: string;
  name: string;
  email: string;
  role: 'generator' | 'facility_operator' | 'admin' | 'user';
  organizationName: string;
  organizationType: string;
  location: string;
  createdAt?: string;
}

export interface AuthResponse {
  success: boolean;
  message?: string;
  token?: string;
  user?: AuthUser;
}

export interface AdminUsersResponse {
  success: boolean;
  users?: AuthUser[];
  message?: string;
}

/**
 * POST /api/auth/register
 * Registers a new account with the backend
 */
export async function registerApi(data: {
  name: string;
  email: string;
  password: string;
  organizationName: string;
  organizationType?: string;
  location?: string;
  role?: string;
  facilityProfile?: FacilityRegistrationProfile;
}): Promise<AuthResponse> {
  try {
    const res = await fetch(API_ENDPOINTS.AUTH_REGISTER, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });

    const json = await res.json();
    if (!res.ok) {
      return { success: false, message: json.message || 'Registration failed' };
    }
    return json;
  } catch (err: any) {
    console.error('[Auth Service Error]: Registration failed due to network/server connection error:', err);
    return {
      success: false,
      message: 'Unable to connect to authentication server. Please check your connection or backend API URL.',
    };
  }
}

/**
 * POST /api/auth/login
 * Authenticates user credentials with the backend
 */
export async function loginApi(data: { email: string; password: string }): Promise<AuthResponse> {
  try {
    const res = await fetch(API_ENDPOINTS.AUTH_LOGIN, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });

    const json = await res.json();
    if (!res.ok) {
      return { success: false, message: json.message || 'Invalid email or password' };
    }
    return json;
  } catch (err: any) {
    console.error('[Auth Service Error]: Login failed due to network/server connection error:', err);
    return {
      success: false,
      message: 'Unable to connect to authentication server. Please check your connection or backend API URL.',
    };
  }
}

/**
 * GET /api/auth/me
 * Retrieves current authenticated user session using JWT token
 */
export async function getMeApi(token: string): Promise<AuthResponse> {
  try {
    const res = await fetch(API_ENDPOINTS.AUTH_ME, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
    });

    const json = await res.json();
    if (!res.ok) {
      return { success: false, message: json.message || 'Session expired' };
    }
    return json;
  } catch (err) {
    console.error('[Auth Service Error]: Failed to reach server during session restoration:', err);
    return { success: false, message: 'Server unreachable' };
  }
}

/**
 * GET /api/admin/users
 * Fetches all registered users (admin privilege required)
 */
export async function getAdminUsersApi(token: string): Promise<AdminUsersResponse> {
  try {
    const res = await fetch(API_ENDPOINTS.ADMIN_USERS, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
    });

    const json = await res.json();
    if (!res.ok) {
      return { success: false, message: json.message || 'Failed to fetch users' };
    }
    return json;
  } catch (err: any) {
    console.warn('[Admin API Warning]: Unable to connect to admin users endpoint', err);
    return { success: false, message: err.message || 'Server unreachable' };
  }
}
